#!/usr/bin/env python3
"""
scripts/validate_effects.py
===========================

Validates every effects/<slug>/ against CONTRACT.md and the
meta.json schema. Used by CI (.github/workflows/validate.yml)
and by contributors before opening a PR.

Exit code 0 on full pass, 1 on any violation. Output is human-
readable by default and machine-readable with --json.

Stdlib only. No external deps.
"""
import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
EFFECTS = REPO / "effects"
SCHEMA = REPO / "schemas" / "meta.schema.json"

CATEGORIES = [
    "zoom", "pan", "rotate", "3d", "filter", "reveal", "fade",
    "shadow", "light", "border", "distortion", "overlay", "composite",
]

# Match real JS event handlers: `on` must be a standalone attribute
# (preceded by whitespace or `<`), not part of a longer word like
# `content`, `controls`, or `data-on`.
JS_RE = re.compile(r"<\s*script|(?<=[\s<])on[a-z]+\s*=|javascript:", re.I)
FOCUS_RE = re.compile(r":focus-visible", re.I)
SELECTOR_RE = re.compile(r"\.hover-effect\.([a-z0-9][a-z0-9-]*[a-z0-9])")


def load_schema() -> dict:
    if not SCHEMA.exists():
        sys.exit(f"error: schema not found at {SCHEMA}")
    return json.loads(SCHEMA.read_text())


def validate_meta(meta: dict, schema: dict) -> list[str]:
    errs = []
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
            errs.append(f"{k}: expected string")
        elif t == "array" and not isinstance(v, list):
            errs.append(f"{k}: expected array")
        elif t == "boolean" and not isinstance(v, bool):
            errs.append(f"{k}: expected boolean")
        if "enum" in spec and v not in spec["enum"]:
            errs.append(f"{k}: '{v}' not in enum {spec['enum']}")
        if "const" in spec and v != spec["const"]:
            errs.append(f"{k}: must be {spec['const']!r}, got {v!r}")
        if "maxLength" in spec and isinstance(v, str) and len(v) > spec["maxLength"]:
            errs.append(f"{k}: longer than {spec['maxLength']} chars")
        if "minLength" in spec and isinstance(v, str) and len(v) < spec["minLength"]:
            errs.append(f"{k}: shorter than {spec['minLength']} chars")
        if "pattern" in spec and isinstance(v, str) and not re.fullmatch(spec["pattern"], v):
            errs.append(f"{k}: '{v}' does not match pattern {spec['pattern']}")
    if meta.get("category") not in CATEGORIES:
        errs.append(f"category: '{meta.get('category')}' not in {CATEGORIES}")
    if schema.get("additionalProperties") is False:
        allowed = set(props.keys())
        for k in meta:
            if k not in allowed:
                errs.append(f"meta.json has unknown field: {k}")
    return errs


def check_effect(slug: str, schema: dict) -> list[str]:
    d = EFFECTS / slug
    errs = []
    css = d / "effect.css"
    meta_p = d / "meta.json"
    html = d / "index.html"
    for f in (css, meta_p, html):
        if not f.exists():
            errs.append(f"missing required file: {f.name}")
    if errs:
        return errs
    try:
        meta = json.loads(meta_p.read_text())
    except Exception as e:
        return [f"meta.json invalid JSON: {e}"]
    if meta.get("id") != slug or meta.get("slug") != slug:
        errs.append(f"meta.id/slug must match directory name ({slug})")
    errs.extend(validate_meta(meta, schema))
    if JS_RE.search(html.read_text()):
        errs.append("index.html contains JavaScript (CONTRACT.md §1)")
    if any(d.glob("*.js")):
        errs.append("effect directory contains .js files (CONTRACT.md §1)")
    css_text = css.read_text()
    if not SELECTOR_RE.search(css_text):
        errs.append("effect.css has no .hover-effect.<slug> selector (CONTRACT.md §2)")
    if not FOCUS_RE.search(css_text):
        errs.append("effect.css missing :focus-visible mirror (CONTRACT.md §5)")
    if JS_RE.search(css_text):
        errs.append("effect.css contains JavaScript (CONTRACT.md §1)")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--slug", help="validate a single effect")
    args = ap.parse_args()
    schema = load_schema()
    targets = [args.slug] if args.slug else [
        d.name for d in sorted(EFFECTS.iterdir())
        if d.is_dir() and not d.name.startswith("_") and (d / "meta.json").exists()
    ]
    results = {}
    failed = 0
    for slug in targets:
        errs = check_effect(slug, schema)
        results[slug] = errs
        if errs:
            failed += 1
    if args.json:
        print(json.dumps({"checked": len(targets), "failed": failed, "results": results}, indent=2))
    else:
        print(f"Checked: {len(targets)}  Failed: {failed}  Passed: {len(targets) - failed}")
        for slug, errs in results.items():
            status = "PASS" if not errs else "FAIL"
            print(f"  {slug:<32} {status}")
            for e in errs:
                print(f"      - {e}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
