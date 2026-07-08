
# Clip Reveal

A clipping mask gradually unveils the image from the center.

## Demo

Open the [dedicated page](index.html).

## CSS Code

````css
.clip-reveal {
  overflow: hidden;
  display: inline-block;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  transition: box-shadow 0.2s ease;
}
.clip-reveal__img {
  display: block;
  width: 100%;
  height: auto;
  clip-path: inset(0 50% 0 50%); /* center only visible */
  transition: clip-path 0.5s ease-out, transform 0.5s ease-out;
}
.clip-reveal:hover .clip-reveal__img {
  clip-path: inset(0 0 0 0); /* all visible */
  transform: scale(1.1);
}
````

## Browser Support

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| CSS `clip-path` | 28+ | 28+ | 9+ | 28+ |

Check the effect on the dedicated page.
