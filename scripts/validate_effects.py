#!/usr/bin/env python3
"""
scripts/validate_effects.py
===========================

v2 contract validator. Enforces every clause of CONTRACT.md,
META_SCHEMA.md, ACCESSIBILITY.md, and BROWSER_SUPPORT.md for every
effects/<slug>/. Used by CI (.github/workflows/validate.yml) and
by contributors before opening a PR.

Architecture: each validation area is a separate function that appends
to a shared errs list. The orchestrator runs all checks and exits
non-zero on any violation.

Supports a `--check-fixtures` mode that runs the validator against
known-good (tests/fixtures/positive/) and known-bad
(tests/fixtures/negative/) fixtures, comparing results against
expected.txt files. This prevents the validator from silently
weakening over time.

Exit codes:
  0 — all effects pass (and fixtures pass, if --check-fixtures)
  1 — at least one effect or fixture failed

Stdlib only. No external deps.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EFFECTS = REPO / "effects"
SCHEMA = REPO / "schemas" / "meta.schema.json"
FIXTURES = REPO / "tests" / "fixtures"

CATEGORIES = [
    "zoom", "pan", "rotate", "3d", "filter", "reveal", "fade",
    "shadow", "light", "border", "distortion", "overlay", "composite",
]

# JS event handler detection (must be a standalone attribute, not part
# of a longer word like "content" or "controls").
JS_RE = re.compile(r"<\s*script|(?<=[\s<])on[a-z]+\s*=|javascript:", re.I)
FOCUS_RE = re.compile(r":focus-visible", re.I)
SELECTOR_RE = re.compile(r"\.hover-effect\.([a-z0-9][a-z0-9-]*[a-z0-9])")
IMPORT_RE = re.compile(r"@import\b", re.I)
ANIMATION_RE = re.compile(r"@keyframes\b|\banimation\s*:", re.I)
TRANSFORM_RE = re.compile(r"\btransform\s*:", re.I)
TRANSITION_RE = re.compile(r"\btransition\s*:", re.I)
CLIP_PATH_RE = re.compile(r"\bclip-path\s*:", re.I)
FILTER_RE = re.compile(r"(?<!-)\bfilter\s*:")  # not backdrop-filter
BACKDROP_RE = re.compile(r"\bbackdrop-filter\s*:")
PERSPECTIVE_RE = re.compile(
    r"\bperspective\s*:|\brotate[xyz]\(|\btranslatez\(|\brotate3d", re.I
)
BLEND_RE = re.compile(r"\bmix-blend-mode\s*:|\bbackground-blend-mode\s*:")
HAS_RE = re.compile(r":has\(", re.I)
PSEUDO_ELEMENT_RE = re.compile(r"::(before|after)\b")
BOX_SHADOW_RE = re.compile(r"\bbox-shadow\s*:")
REDUCED_MOTION_RE = re.compile(r"@media\s*\(\s*prefers-reduced-motion", re.I)
IMPORTANT_RE = re.compile(r"!important", re.I)
CROSS_EFFECT_REF_RE = re.compile(r"effects/([a-z0-9][a-z0-9-]*[a-z0-9])/")
JS_STATE_CLASS_RE = re.compile(r"\.(is-|has-|js-)[a-z][a-z0-9-]*", re.I)

# Gallery-only classes (from styles/catalog.css). An effect that
# references any of these is coupled to the catalog implementation.
GALLERY_CLASS_PREFIXES = (
    "card", "card__", "gallery", "gallery__", "filter", "filter__",
    "section", "section__", "hero", "hero__", "featured", "featured__",
    "site-footer", "page-header", "back-link",
)


# ----------------------------------------------------------------------
# CSS parser (tracks positions for accurate line numbers)
# ----------------------------------------------------------------------

def parse_css_rules(text: str) -> list[tuple[str, int]]:
    """Parse top-level CSS into (selector_text, start_line) pairs.

    Handles @media nesting (recurses). Skips @keyframes, @supports
    bodies. Returns the selector text and the line number where it
    starts. Does NOT include @rule selectors (those are handled
    separately by _at_rules_with_body).
    """
    rules: list[tuple[str, int]] = []
    i, n = 0, len(text)

    def skip_ws_and_comments() -> None:
        nonlocal i
        while i < n:
            ch = text[i]
            if ch in " \t\n\r":
                i += 1
            elif text[i:i+2] == "/*":
                end = text.find("*/", i + 2)
                i = n if end == -1 else end + 2
            else:
                break

    skip_ws_and_comments()
    while i < n:
        if text[i] == "@":
            brace = text.find("{", i)
            if brace == -1:
                break
            header = text[i:brace].strip().lower()
            depth, j = 1, brace + 1
            while j < n and depth > 0:
                if text[j] == "{": depth += 1
                elif text[j] == "}": depth -= 1
                j += 1
            body = text[brace + 1:j - 1]
            if header.startswith("@media") or header.startswith("@supports") \
                    or header.startswith("@container"):
                rules.extend(parse_css_rules(body))
            i = j
            skip_ws_and_comments()
            continue
        brace = text.find("{", i)
        if brace == -1:
            break
        selector = text[i:brace].strip()
        line = text[:i].count("\n") + 1
        depth, j = 1, brace + 1
        while j < n and depth > 0:
            if text[j] == "{": depth += 1
            elif text[j] == "}": depth -= 1
            j += 1
        rules.append((selector, line))
        i = j
        skip_ws_and_comments()
    return rules


def at_rules_with_body(text: str) -> list[tuple[str, str, int]]:
    """Return (header, body, line) for each top-level @media/@supports.
    Skips regular rules and comments between @rules."""
    out = []
    i, n = 0, len(text)
    while i < n:
        # Skip non-@ content: whitespace, regular rules, comments
        while i < n and text[i] != "@":
            if text[i:i+2] == "/*":
                end = text.find("*/", i + 2)
                i = n if end == -1 else end + 2
            elif text[i] == "}":
                i += 1
            elif text[i] == "{":
                # skip a regular rule's body
                depth, j = 1, i + 1
                while j < n and depth > 0:
                    if text[j] == "{": depth += 1
                    elif text[j] == "}": depth -= 1
                    j += 1
                i = j
            else:
                i += 1
        if i >= n:
            break
        # text[i] == "@"
        brace = text.find("{", i)
        if brace == -1:
            break
        header = text[i:brace].strip()
        depth, j = 1, brace + 1
        while j < n and depth > 0:
            if text[j] == "{": depth += 1
            elif text[j] == "}": depth -= 1
            j += 1
        body = text[brace + 1:j - 1]
        line = text[:i].count("\n") + 1
        out.append((header, body, line))
        i = j
    return out


# ----------------------------------------------------------------------
# Canonical markup checker
# ----------------------------------------------------------------------

class CanonicalHTMLChecker(HTMLParser):
    """Verify that index.html contains exactly one
    `.hover-effect <slug>` wrapper with exactly one `<img>` child."""

    VOID = {"area", "base", "br", "col", "embed", "hr", "img",
            "input", "link", "meta", "param", "source", "track", "wbr"}

    def __init__(self, slug: str):
        super().__init__(convert_charrefs=True)
        self.slug = slug
        self.errors: list[str] = []
        self.wrapper_depth = 0
        self.wrapper_count = 0
        self.imgs_in_current = 0
        self.non_void_in_current: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = dict(attrs)
        cls = (a.get("class") or "").strip()
        is_wrapper = tag == "div" and cls.split() == ["hover-effect", self.slug]
        if is_wrapper:
            self.wrapper_count += 1
            self.wrapper_depth = 1
            self.imgs_in_current = 0
            self.non_void_in_current = []
        elif self.wrapper_depth > 0:
            if tag == "img":
                self.imgs_in_current += 1
            elif tag not in self.VOID:
                self.non_void_in_current.append(tag)
            if tag not in self.VOID:
                self.wrapper_depth += 1

    def handle_endtag(self, tag: str) -> None:
        if self.wrapper_depth > 0:
            if tag not in self.VOID:
                self.wrapper_depth -= 1
            if self.wrapper_depth == 0:
                if self.imgs_in_current != 1:
                    self.errors.append(
                        f"canonical wrapper contains {self.imgs_in_current} "
                        f"<img> elements (expected exactly 1)"
                    )
                if self.non_void_in_current:
                    self.errors.append(
                        f"canonical wrapper contains non-img elements: "
                        f"{self.non_void_in_current} (only <img> allowed)"
                    )


# ----------------------------------------------------------------------
# Individual check functions
# ----------------------------------------------------------------------

def check_files_exist(slug: str, d: Path, errs: list[str]) -> None:
    for name in ("effect.css", "index.html", "meta.json"):
        if not (d / name).exists():
            errs.append(f"missing required file: {name}")


def check_meta_schema(slug: str, d: Path, schema: dict, errs: list[str]) -> dict | None:
    meta_p = d / "meta.json"
    try:
        meta = json.loads(meta_p.read_text())
    except Exception as e:
        errs.append(f"meta.json invalid JSON: {e}")
        return None
    if meta.get("id") != slug or meta.get("slug") != slug:
        errs.append(f"meta.id/slug must match directory name ({slug})")
    for req in schema.get("required", []):
        if req not in meta:
            errs.append(f"meta.json missing required field: {req}")
    props = schema.get("properties", {})
    for k, spec in props.items():
        if k not in meta:
            continue
        v = meta[k]
        t = spec.get("type")
        if t == "string" and not isinstance(v, str):
            errs.append(f"meta.{k}: expected string")
        elif t == "array" and not isinstance(v, list):
            errs.append(f"meta.{k}: expected array")
        elif t == "boolean" and not isinstance(v, bool):
            errs.append(f"meta.{k}: expected boolean")
        if "enum" in spec and v not in spec["enum"]:
            errs.append(f"meta.{k}: '{v}' not in enum {spec['enum']}")
        if "const" in spec and v != spec["const"]:
            errs.append(f"meta.{k}: must be {spec['const']!r}, got {v!r}")
        if "maxLength" in spec and isinstance(v, str) and len(v) > spec["maxLength"]:
            errs.append(f"meta.{k}: longer than {spec['maxLength']} chars")
        if "minLength" in spec and isinstance(v, str) and len(v) < spec["minLength"]:
            errs.append(f"meta.{k}: shorter than {spec['minLength']} chars")
        if "pattern" in spec and isinstance(v, str) and not re.fullmatch(spec["pattern"], v):
            errs.append(f"meta.{k}: '{v}' does not match pattern {spec['pattern']}")
    if meta.get("category") not in CATEGORIES:
        errs.append(f"meta.category: '{meta.get('category')}' not in {CATEGORIES}")
    if schema.get("additionalProperties") is False:
        allowed = set(props.keys())
        for k in meta:
            if k not in allowed:
                errs.append(f"meta.json has unknown field: {k}")
    return meta


def check_no_js(slug: str, d: Path, html_text: str, css_text: str, errs: list[str]) -> None:
    if JS_RE.search(html_text):
        errs.append("index.html contains JavaScript (CONTRACT.md §1)")
    if JS_RE.search(css_text):
        errs.append("effect.css contains JavaScript (CONTRACT.md §1)")
    for f in d.glob("*.js"):
        errs.append(f"effect directory contains {f.name} (CONTRACT.md §1)")


def check_focus_visible(slug: str, css_text: str, errs: list[str]) -> None:
    if not FOCUS_RE.search(css_text):
        errs.append("effect.css missing :focus-visible mirror (CONTRACT.md §5)")


def check_selector_present(slug: str, css_text: str, errs: list[str]) -> None:
    if not SELECTOR_RE.search(css_text):
        errs.append(
            f"effect.css has no .hover-effect.{slug} selector (CONTRACT.md §2)"
        )


def _selectors_for_slug(slug: str, css_text: str) -> list[tuple[str, int]]:
    """Return (selector, line) for every top-level rule whose selector
    references `.hover-effect.<slug>`. Works inside @media too."""
    out = []
    for selector, line in parse_css_rules(css_text):
        if re.search(r"\.hover-effect\." + re.escape(slug) + r"\b", selector):
            out.append((selector, line))
    return out


def check_no_descendant_selectors(slug: str, css_text: str, errs: list[str]) -> None:
    """Detect `.hover-effect.<slug>` followed by a descendant or child
    combinator (space or `>`) then a class selector that is NOT `img`
    and NOT a pseudo-element. These imply extra HTML markup inside
    the wrapper and violate CONTRACT.md §2.

    Allowed:
      .hover-effect.<slug>          (the wrapper itself)
      .hover-effect.<slug>:hover   (pseudo-class on wrapper)
      .hover-effect.<slug>:focus-visible
      .hover-effect.<slug>::before / ::after  (pseudo-elements)
      .hover-effect.<slug> > img   (the canonical img child)
      .hover-effect.<slug> img     (descendant img)

    Forbidden:
      .hover-effect.<slug> .<x>    (assumed child element)
      .hover-effect.<slug> > .<x>  (assumed child element)
    """
    cls = re.escape(slug)
    # Match `.hover-effect.<slug>` followed by whitespace or `>` then
    # a `.class` that is NOT `img`. Use negative lookahead to exclude img.
    pattern = re.compile(
        r"\.hover-effect\." + cls + r"\s*[ >]\s*\.(?!img\b)([a-z][a-z0-9-]*)",
        re.I,
    )
    for m in pattern.finditer(css_text):
        # Extract the full selector by walking back to {, , or start
        start = m.start()
        while start > 0 and css_text[start - 1] not in "{},\n":
            start -= 1
        # Walk forward to {, , or end
        end = m.end()
        while end < len(css_text) and css_text[end] not in "{},\n":
            end += 1
        selector = css_text[start:end].strip()
        line = css_text[:m.start()].count("\n") + 1
        # Skip if this is actually a pseudo-element (::before, ::after)
        # The regex already excludes these because `::` doesn't match `.`
        child_class = m.group(1)
        errs.append(
            f"effect.css:{line}: selector '{selector}' "
            f"targets assumed child element '.{child_class}' "
            f"(CONTRACT.md §2: wrapper must contain only <img>)"
        )


def check_canonical_markup(slug: str, html_text: str, errs: list[str]) -> None:
    checker = CanonicalHTMLChecker(slug)
    checker.feed(html_text)
    if checker.wrapper_count == 0:
        errs.append(
            f"index.html has no <div class=\"hover-effect {slug}\"> wrapper"
        )
    elif checker.wrapper_count > 1:
        errs.append(
            f"index.html has {checker.wrapper_count} "
            f"<div class=\"hover-effect {slug}\"> wrappers (expected 1)"
        )
    errs.extend(checker.errors)


def check_no_gallery_coupling(slug: str, css_text: str, errs: list[str]) -> None:
    for selector, line in _selectors_for_slug(slug, css_text):
        for prefix in GALLERY_CLASS_PREFIXES:
            if re.search(r"\." + re.escape(prefix) + r"(?![a-z-])", selector, re.I):
                errs.append(
                    f"effect.css:{line}: selector '{selector.strip()}' "
                    f"references gallery-only class '.{prefix}' "
                    f"(CONTRACT.md §7: gallery isolation)"
                )


def check_no_js_state_classes(slug: str, css_text: str, errs: list[str]) -> None:
    """Detect selectors referencing JS-generated state classes
    (.is-*, .has-*, .js-*). These imply the effect requires JavaScript
    to toggle a class, violating CONTRACT.md §1."""
    for selector, line in _selectors_for_slug(slug, css_text):
        for m in JS_STATE_CLASS_RE.finditer(selector):
            errs.append(
                f"effect.css:{line}: selector '{selector.strip()}' "
                f"references JS-generated state class '{m.group()}' "
                f"(CONTRACT.md §1: pure CSS, no JS-driven state)"
            )


def check_no_imports(slug: str, css_text: str, errs: list[str]) -> None:
    if IMPORT_RE.search(css_text):
        m = IMPORT_RE.search(css_text)
        line = css_text[:m.start()].count("\n") + 1
        errs.append(
            f"effect.css:{line}: @import found "
            f"(CONTRACT.md §6: effect must be self-contained)"
        )


def check_no_cross_effect_refs(slug: str, css_text: str, errs: list[str]) -> None:
    for m in CROSS_EFFECT_REF_RE.finditer(css_text):
        if m.group(1) != slug:
            line = css_text[:m.start()].count("\n") + 1
            errs.append(
                f"effect.css:{line}: references another effect "
                f"'effects/{m.group(1)}/' (CONTRACT.md §6)"
            )


def check_alt_attribute(slug: str, html_text: str, errs: list[str]) -> None:
    m = re.search(
        rf'<div\s+class="hover-effect\s+{re.escape(slug)}"[^>]*>(.*?)</div>',
        html_text, re.I | re.S
    )
    if not m:
        return
    inner = m.group(1)
    imgs = re.findall(r"<img\b[^>]*>", inner, re.I)
    if len(imgs) == 1 and "alt=" not in imgs[0]:
        errs.append(
            "canonical wrapper <img> has no alt attribute "
            "(ACCESSIBILITY.md)"
        )


def check_reduced_motion(slug: str, css_text: str, errs: list[str]) -> None:
    for header, body, line in at_rules_with_body(css_text):
        if not REDUCED_MOTION_RE.search(header):
            continue
        if IMPORTANT_RE.search(body):
            errs.append(
                f"effect.css:{line}: redefines "
                f"@media (prefers-reduced-motion) with !important "
                f"(CONTRACT.md §4: rely on global reset in styles/base.css)"
            )


def _detect_features(css_text: str) -> set[str]:
    """Detect which CSS features the effect's stylesheet actually uses."""
    used: set[str] = set()
    if TRANSFORM_RE.search(css_text): used.add("transform")
    if TRANSITION_RE.search(css_text): used.add("transition")
    if CLIP_PATH_RE.search(css_text): used.add("clip-path")
    if FILTER_RE.search(css_text): used.add("filter")
    if BACKDROP_RE.search(css_text): used.add("backdrop-filter")
    if PERSPECTIVE_RE.search(css_text): used.add("perspective")
    if BLEND_RE.search(css_text): used.add("blend-mode")
    if HAS_RE.search(css_text): used.add("has")
    if ANIMATION_RE.search(css_text): used.add("animation")
    if PSEUDO_ELEMENT_RE.search(css_text): used.add("pseudo-element")
    if BOX_SHADOW_RE.search(css_text): used.add("box-shadow")
    return used


def check_meta_accuracy(slug: str, css_text: str, meta: dict, errs: list[str]) -> None:
    """Every feature claimed in meta.css_features must be detectable
    in the CSS. Features used by the CSS but not listed in meta are
    allowed (meta is informative, not exhaustive)."""
    claimed = set(meta.get("css_features", []))
    used = _detect_features(css_text)
    for f in sorted(claimed - used):
        errs.append(
            f"meta.css_features claims '{f}' but effect.css does not use it"
        )




# ----------------------------------------------------------------------
# Repo-level checks (run once, not per effect)
# ----------------------------------------------------------------------

def check_base_css() -> list[str]:
    """Verify styles/base.css contains the a11y guards required by
    CONTRACT.md §3, §4, §5, §7 and ACCESSIBILITY.md."""
    errs: list[str] = []
    base = (REPO / "styles" / "base.css").read_text()
    if "@media (hover: none)" not in base:
        errs.append(
            "styles/base.css missing @media (hover: none) guard "
            "(CONTRACT.md §7, ACCESSIBILITY.md §07)"
        )
    if "@media (prefers-reduced-motion: reduce)" not in base:
        errs.append(
            "styles/base.css missing @media (prefers-reduced-motion: reduce) "
            "(CONTRACT.md §4)"
        )
    if "@media (prefers-contrast: more)" not in base:
        errs.append(
            "styles/base.css missing @media (prefers-contrast: more) "
            "(ACCESSIBILITY.md §09)"
        )
    if ".hover-effect:focus-visible" not in base:
        errs.append(
            "styles/base.css missing .hover-effect:focus-visible outline "
            "(CONTRACT.md §5)"
        )
    return errs


# ----------------------------------------------------------------------
# Orchestrator
# ----------------------------------------------------------------------

def check_effect(slug: str, schema: dict, base: Path = EFFECTS) -> list[str]:
    d = base / slug
    errs: list[str] = []
    check_files_exist(slug, d, errs)
    if errs:
        return errs
    css_text = (d / "effect.css").read_text()
    html_text = (d / "index.html").read_text()
    meta = check_meta_schema(slug, d, schema, errs)
    if meta is None:
        return errs
    check_no_js(slug, d, html_text, css_text, errs)
    check_focus_visible(slug, css_text, errs)
    check_selector_present(slug, css_text, errs)
    check_no_descendant_selectors(slug, css_text, errs)
    check_canonical_markup(slug, html_text, errs)
    check_no_gallery_coupling(slug, css_text, errs)
    check_no_js_state_classes(slug, css_text, errs)
    check_no_imports(slug, css_text, errs)
    check_no_cross_effect_refs(slug, css_text, errs)
    check_alt_attribute(slug, html_text, errs)
    check_reduced_motion(slug, css_text, errs)
    check_meta_accuracy(slug, css_text, meta, errs)
    return errs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--slug", help="validate a single effect")
    ap.add_argument("--check-fixtures", action="store_true",
                    help="run fixture tests and exit")
    args = ap.parse_args()

    if args.check_fixtures:
        sys.exit(run_fixtures())

    schema = json.loads(SCHEMA.read_text())
    base_errs = check_base_css() + check_catalog_featured_slugs()
    if base_errs:
        print("Repository-level a11y violations:")
        for e in base_errs:
            print(f"  - {e}")
        if not (args.json or args.check_fixtures):
            print()
    targets = [args.slug] if args.slug else [
        d.name for d in sorted(EFFECTS.iterdir())
        if d.is_dir() and not d.name.startswith("_") and (d / "meta.json").exists()
    ]
    results: dict[str, list[str]] = {}
    failed = 0
    for slug in targets:
        errs = check_effect(slug, schema)
        results[slug] = errs
        if errs:
            failed += 1
    if args.json:
        print(json.dumps({"checked": len(targets), "failed": failed,
                          "results": results}, indent=2))
    else:
        print(f"Checked: {len(targets)}  Failed: {failed}  "
              f"Passed: {len(targets) - failed}")
        for slug, errs in results.items():
            status = "PASS" if not errs else "FAIL"
            print(f"  {slug:<32} {status}")
            for e in errs:
                print(f"      - {e}")
    sys.exit(1 if failed or base_errs else 0)



def check_catalog_featured_slugs() -> list[str]:
    """Verify that every slug listed as FEATURED in
    scripts/build_catalog.py exists as a real effect directory and
    passes the per-effect checks."""
    errs: list[str] = []
    bc = REPO / "scripts" / "build_catalog.py"
    if not bc.exists():
        return errs
    src = bc.read_text()
    # Extract FEATURED_SLUGS = [ ... ]
    import re
    m = re.search(r"FEATURED_SLUGS\s*=\s*\[([^\]]+)\]", src)
    if not m:
        return errs
    slugs = re.findall(r'"([a-z0-9][a-z0-9-]*[a-z0-9])"', m.group(1))
    schema = json.loads(SCHEMA.read_text())
    for s in slugs:
        if not (EFFECTS / s).is_dir():
            errs.append(
                f"scripts/build_catalog.py references featured slug "
                f"'{s}' which has no effects/<slug>/ directory"
            )
            continue
        effect_errs = check_effect(s, schema)
        if effect_errs:
            errs.append(
                f"featured slug '{s}' fails validation: "
                f"{'; '.join(effect_errs)}"
            )
    return errs


# ----------------------------------------------------------------------
# Fixture runner
# ----------------------------------------------------------------------

def run_fixtures() -> int:
    """Run validator against tests/fixtures/{positive,negative}/*.
    Positive fixtures must pass; negative fixtures must fail with
    errors matching their expected.txt."""
    schema = json.loads(SCHEMA.read_text())
    failures = 0

    pos_dir = FIXTURES / "positive"
    if pos_dir.exists():
        for fx in sorted(pos_dir.iterdir()):
            if not fx.is_dir():
                continue
            errs = check_effect(fx.name, schema, base=pos_dir)
            if errs:
                failures += 1
                print(f"FAIL positive/{fx.name} (expected PASS):")
                for e in errs:
                    print(f"  - {e}")
            else:
                print(f"PASS positive/{fx.name}")
    else:
        print("(no tests/fixtures/positive directory)")

    neg_dir = FIXTURES / "negative"
    if neg_dir.exists():
        for fx in sorted(neg_dir.iterdir()):
            if not fx.is_dir():
                continue
            expected_path = fx / "expected.txt"
            errs = check_effect(fx.name, schema, base=neg_dir)
            if not errs:
                failures += 1
                print(f"FAIL negative/{fx.name} (expected at least one error)")
                continue
            actual = "\n".join(errs)
            if expected_path.exists():
                expected = expected_path.read_text().strip()
                missing = [
                    line for line in expected.splitlines()
                    if line.strip() and line.strip() not in actual
                ]
                if missing:
                    failures += 1
                    print(f"FAIL negative/{fx.name} (missing expected errors):")
                    for m in missing:
                        print(f"  expected: {m}")
                    print(f"  actual:")
                    for e in errs:
                        print(f"    - {e}")
                else:
                    print(f"PASS negative/{fx.name}")
            else:
                print(f"PASS negative/{fx.name} (failed as expected, "
                      f"{len(errs)} errors)")
    else:
        print("(no tests/fixtures/negative directory)")

    print()
    if failures:
        print(f"Fixtures: {failures} failure(s)")
    else:
        print("Fixtures: all pass")
    return 1 if failures else 0


if __name__ == "__main__":
    main()
