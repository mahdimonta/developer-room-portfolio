---
name: developer-room-portfolio
description: Design and engineering rulebook for THE DEVELOPER'S ROOM — an isometric pixel-art PixiJS portfolio. Load this before editing anything under public/assets, src/engine, src/character, src/cat, src/interactions, src/animations, src/ui, tools/, or src/data/data.js.
---

# THE DEVELOPER'S ROOM — project skill

Permanent design and development rules for this repository. `CLAUDE.md` at
the project root is the short version; this file is the detailed rulebook.

## 1. Visual direction

- **Isometric 2D / 2.5D**, pixel-art-inspired, 2:1 projection
  (`tools/isolib.py`: `TW=64, TH=32, ZH=32`). Never mix a different
  projection or tile ratio into the same scene.
- **One light direction**: upper-left. Every `box_mat`/`box` call shades top
  lightest, left face mid, right face darkest, matching that direction.
  Don't add a prop with reversed shading.
- **One palette** (`tools/isolib.py: P`). Add new colours there, don't
  inline hex values in generator functions — keeps the whole room coherent.
- **Cozy cyberpunk**: deep navy/purple base, cyan/electric-blue/magenta RGB
  accents, small amber/orange practicals (lamps, coffee machine display).
  RGB ambient lighting is baked glow sprites (`radial_glow` in
  `tools/isolib.py`), never a runtime filter — keeps render cost flat.
- **Character is anonymous**: rear or rear-three-quarter view only, no face.
  See `tools/gen_character.py: _head()` — it draws hair/headphones/nape,
  never eyes or a mouth. Do not add a front-facing frame.

## 2. PixiJS v8 architecture

- `src/engine/pixi-app.js` — boots `Application`, loads assets, wires
  everything. `preference: "webgl"`, `antialias: false` (pixel-art must stay
  crisp — never enable antialiasing).
- `src/engine/room-scene.js` — builds the scene graph from
  `public/assets/room/room-layout.json` (produced by `tools/build_assets.py`
  — never hand-edit this JSON). Every sprite/anim becomes its own
  `Sprite`/`AnimatedSprite`, named via `.label`, stored in `scene.layers`
  (a `Map`) for lookup by other modules. Character and cat frames are
  grouped into `char-group`/`cat-group` Containers so the whole figure can
  be translated as one unit (for real walking, not just an animation swap).
- Depth/z-order comes from each asset's `sort` value in `room-layout.json`
  (set by the Python generator, e.g. `emit(..., sort=24)`), applied via
  `zIndex` on a `sortableChildren = true` world container. When adding a
  prop, pick a `sort` that matches its isometric depth relative to
  neighbours — don't guess, compare against existing values for nearby
  objects.
- Screens (monitor/laptop) are **not** pixel art — see §5.

## 3. Vanilla JavaScript only

No React/Vue/Svelte, no Tailwind, no CSS-in-JS, no bundler beyond Vite.
ES modules (`type="module"`), one responsibility per file, no global state
beyond what's exposed on `window.__room` for debugging.

## 4. GSAP conventions

- Import `gsap` from `src/animations/gsap-timelines.js` (not the bare
  `"gsap"` package) anywhere you need the `pixi:` plugin syntax
  (`gsap.to(sprite, { pixi: { scaleX: 1.1 } })`) — that file registers
  `PixiPlugin` once, centrally.
- Panel open/close: `src/ui/navigation.js`. Hover/click micro-animation on
  hotspots: `src/interactions/hotspots.js`. Ambient loops (lamp breathing,
  character/cat scheduling): `src/animations/room-animations.js`.
- Always provide an `ease`; prefer `power2`/`sine`/`back.out` families for
  the cozy, slightly bouncy feel already established.

## 5. Monitor/laptop "code" is real HTML

`src/engine/monitor-screens.js` overlays `<pre>` elements on top of the
canvas, CSS-transformed (`matrix(...)`) to match each screen's baked
isometric quad from `room-layout.json`'s `quads` section. **Never** bake
code text into a pixel-art PNG — it must stay real, selectable text per the
project brief. If you change a monitor's position/size in
`tools/gen_props.py`, the quad updates automatically on rebuild; no manual
CSS math needed on your end beyond re-running `npm run assets:build`.

## 6. Sprite sheets & the asset pipeline

- `tools/isolib.py` — drawing primitives (isometric boxes, tiles, glows,
  outlines, dithering) and the shared palette.
- `tools/stage.py` — shared staging canvas + `emit()`/`emit_anim()`/
  `emit_quad()` helpers that crop each sprite to content and register its
  world position/sort/hotspot in `room-layout.json`.
- `tools/gen_room.py`, `gen_props.py`, `gen_character.py`, `gen_cat.py`,
  `gen_effects.py` — one generator module per area. `tools/build_assets.py`
  runs all of them in order and writes the final `room-layout.json`.
- Run `npm run assets:build` (or `python tools/build_assets.py` directly)
  after any generator change, then `python tools/preview.py` to render a
  flat composite to `docs/_preview_room.png` for a quick visual sanity
  check before touching any engine code.
- Animated sprites are packed as horizontal strips with a known frame
  count/size (`emit_anim`); `src/engine/asset-loader.js: sliceFrames()`
  turns a strip texture into the `Texture[]` an `AnimatedSprite` needs.

## 7. Layer management & depth sorting

- Never flatten interactive objects into the base room illustration. Each
  project model on the shelf, the laptop, and every character/cat layer is
  its own sprite with its own hotspot.
- Chair is split into `chair-back` (sort 28, behind the character) and
  `chair-front` (sort 31, in front) specifically so the seated character
  (sort 30) reads as sitting *inside* the chair, not floating beside it.
  Keep this split if you ever redraw the chair.

## 8. Mouse / touch interactions

- `src/interactions/hotspots.js` sets `eventMode = "static"` and `cursor =
  "pointer"` on each interactive sprite, with `pointerover`/`pointerout`
  hover feedback (GSAP lift/scale, tint) and `pointertap` to open a panel.
  `pointertap` fires for both mouse clicks and touch taps — don't add a
  separate touch handler.
- Keyboard users reach the same three actions via the always-visible
  `<nav class="quick-nav">` buttons in `index.html` (real `<button>`
  elements, Tab-reachable, `Escape` closes any open panel — see
  `src/ui/navigation.js`).

## 9. Responsive behaviour

- `src/engine/scene-manager.js: fitRoomToViewport()` scales+centers the
  fixed-size isometric room to fit the viewport (margin + scale cap, no
  stretching). Don't make the Pixi canvas itself responsive via CSS
  width/height percentages — that blurs pixel art; scale the Pixi
  `Container`, not the canvas element.
- CSS breakpoints at 900px (tablet) and 560px (mobile) in `src/style.css`
  adjust panel layout and nav position — don't just shrink desktop content;
  mobile gets its own stacked About layout and bottom-anchored nav.

## 10. Accessibility

- Respect `prefers-reduced-motion` (`utils/performance.js:
  watchReducedMotion`) — ambient lamp breathing and the cat's
  cursor-tracking glance are skipped/reduced; state-conveying animations
  (idle/typing/walk) still play since they're informational, not decorative.
- Every panel has `role`/`aria-hidden`/focus management
  (`src/ui/navigation.js`): focus moves to the close button on open, returns
  to the trigger on close, `Escape` closes.
- Decorative monitor "code" text is `aria-hidden="true"` (it's flavour, not
  content) — real content (About/Projects/Contact) is always plain
  accessible HTML, never canvas-only.

## 11. Performance

- `antialias: false`, `resolution` capped at 2, pixel-art `image-rendering:
  pixelated` on the canvas.
- Tab-hidden pause: `visibilitychange` must stop **both** `app.ticker` and
  `Ticker.shared` — `AnimatedSprite` defaults to the latter, which is a
  *different instance* from a private `app.ticker`. Forgetting `Ticker.shared`
  means the character/cat silently keep animating in a hidden tab. See
  `engine/pixi-app.js`.
- All baked glows (`radial_glow`) are pre-rendered PNGs, not runtime
  filters — don't add `BlurFilter`/`GlowFilter` for ambient lighting; bake
  it with the Python pipeline instead.

## 12. Asset licensing

All visual assets in this project are **generated by the Python pipeline in
`tools/`** — no third-party game-art packs are embedded. Fonts come from
Google Fonts (OFL) loaded via `@font-face`/`<link>`, no font files bundled.
See `ASSET_SOURCES.md` and `THIRD_PARTY_LICENSES.md`. If you ever do add a
downloaded asset, it must be CC0 or an equally permissive licence explicit
about commercial/public use, and must be logged in both of those files plus
`ASSET_MANIFEST.json` before use.

## 13. Data-driven project management

- `src/data/data.js` is the only file content edits should touch for
  profile/projects/skills/achievements/contact.
- Each project needs a `shelfSlot` (0–5) matching one of the six baked shelf
  models (`store`, `phone`, `robot`, `tower`, `dashboard`, `apps` — see
  `tools/gen_props.py: PROJECT_MODELS`). Empty `links.github`/`links.demo`
  must not render a broken button — `src/ui/project-panel.js` already
  guards this; keep that guard if you touch the panel.

## 14. Browser testing requirement

Before considering any room/engine change "done": start `npm run dev`,
open it in a real browser (or this environment's Browser pane / Playwright),
click all three hotspots, open and close every panel, check
`prefers-reduced-motion` and the tab-hidden pause, and check the console for
errors. Then run `npm run build` to confirm the production bundle works too
— dev-only testing is not sufficient.
