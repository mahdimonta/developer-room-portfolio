# CLAUDE.md — THE DEVELOPER'S ROOM

Permanent project rules for Claude (or any agent) working in this repository.
See also `.claude/skills/developer-room-portfolio/SKILL.md` for the detailed
design/engineering rulebook.

## What this project is

An interactive isometric pixel-art portfolio ("THE DEVELOPER'S ROOM") for
Mahdi Montazeri. The room is the interface — there is no conventional hero
section. Visitors explore a PixiJS-rendered bedroom/workspace and click three
hotspots (character, project shelf, laptop) to open HTML panels.

## Hard constraints — do not change without being asked

- **Vanilla JS, HTML, CSS only.** No React, no Vue, no Tailwind, no backend,
  no database, no auth. Vite is the only build tool.
- **PixiJS v8** for the scene, **GSAP** for UI/panel animation and ambient
  tweens. Don't introduce Three.js or another renderer.
- **No conventional portfolio hero.** The room is the landing experience.
- **Character stays anonymous.** Never generate or add a front-facing face.
  Back / rear-three-quarter view only.
- **`src/data/data.js` is the single source of truth** for all personal
  content (profile, projects, skills, achievements, contact). Adding or
  removing a project must never require touching scene/animation code —
  only `data.js` plus, if the shelf should show a new 3D-ish model, a new
  `proj-*` generator function in `tools/gen_props.py`.
- **Never invent personal information.** Placeholders only, clearly marked,
  for anything not supplied by the user.

## Assets

- All room/character/cat/effect art is **generated, not downloaded** — see
  `tools/*.py` (Pillow-based isometric drawing library + per-area
  generators) and `npm run assets:build`. This keeps licensing unambiguous
  (100% original work) and keeps the whole room in one consistent palette,
  isometric angle (2:1), and light direction.
- If you add a new sprite, use `tools/isolib.py` / `tools/stage.py` helpers
  so it's automatically registered in `public/assets/room/room-layout.json`
  with correct world position and depth-sort key. Never hand-edit
  `room-layout.json` — it's build output.
- Fonts are system/Google Fonts loaded by CSS only (no bundled font files).
- See `ASSET_SOURCES.md` and `THIRD_PARTY_LICENSES.md` for the full
  licensing record.

## Engine conventions

- Every interactive/furniture piece is an **independent display object**
  (named via `.label`), never flattened into one image. `room-scene.js`
  builds the scene from `room-layout.json`; `src/engine/pixi-app.js` wires
  it all together.
- Character and cat frames live in their own `Container` groups
  (`char-group`, `cat-group`) so `character.js` / `cat.js` can translate the
  WHOLE group for real movement (e.g. walking to the coffee machine),
  instead of just swapping animation frames in place.
- Monitor/laptop "code" is **real HTML text** (`engine/monitor-screens.js`),
  not baked into pixel art, so it stays selectable/accessible and can be
  swapped without touching art.
- State machines (`utils/performance.js: createStateMachine`) drive both the
  character and the cat. Keep states mutually exclusive where the spec
  requires it (e.g. never let "typing" and "walking" show at once).

## Before calling a UI/animation change done

1. Run `npm run dev` and exercise it in a real browser (Playwright, or the
   Browser pane tool) — click all three hotspots, open/close each panel,
   check the console for errors.
2. Check `prefers-reduced-motion` is still respected
   (`utils/performance.js: watchReducedMotion`).
3. Check the tab-hidden pause still works — `visibilitychange` must stop
   **both** `app.ticker` and `Ticker.shared` (AnimatedSprite defaults to the
   latter; see `engine/pixi-app.js`).
4. Run `npm run build` — don't ship on `npm run dev` alone.
