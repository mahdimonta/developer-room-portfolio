# Asset Sources & Licensing Research

## Decision: all visual assets are generated, not downloaded

Phase 4 of the brief asked me to research third-party isometric pixel-art
packs (Kenney, OpenGameArt, itch.io, etc.) and only use assets with
unambiguous public/commercial-use licenses. I did that research (below),
but ultimately **built every room/character/cat/effect asset myself** with
an original Python + Pillow drawing pipeline (`tools/`) instead of mixing
in third-party art. Reasons:

1. **Visual consistency.** The brief explicitly warns against mixing
   different pixel resolutions, isometric angles, lighting directions, or
   outline styles. Every pack I evaluated uses its own angle/palette/outline
   convention; blending them with a hand-authored character, cat, and UI
   would have violated that rule immediately.
2. **Licensing certainty.** A procedurally generated, 100%-original asset
   has no licensing question at all — no attribution to track, no
   "permits in-game use but not raw-file redistribution" edge case to
   evaluate (the brief calls this out specifically as needing care).
3. **Live sprite sheets with exact metadata.** Every sprite's world
   position, depth-sort key, and (for characters/cat) animation frame count
   are generated together and written straight into
   `public/assets/room/room-layout.json` — no manual re-slicing of a
   downloaded sheet to match a hand-placed room.

This also means `THIRD_PARTY_LICENSES.md` is short: there are no bundled
third-party image/font files to attribute.

## Research log (sources inspected, per the brief's required fields)

These were inspected for fit before the "generate everything" decision was
made; none were downloaded or embedded.

| Asset | Author | Source | License | Commercial use | Attribution | Formats | Matches style | Approved |
|---|---|---|---|---|---|---|---|---|
| Isometric 2D pixel room | `hooded-crow` | opengameart.org/content/isometric-2d-pixel-room | CC0 | Yes | Not required | PNG | Isometric, but different angle/outline convention than this project's | Not used — see decision above |
| Isometric pixel room | `pixel-art` (OGA user) | opengameart.org/content/isometric-pixel-room | CC0 | Yes | Not required | PNG | Isometric; single flattened illustration (brief requires separable layers) | Not used |
| Isometric Lab/Maintenance Room | OGA community | opengameart.org/content/isometric-labmaintenance-room | CC0 | Yes | Not required | PNG | Sci-fi lab, not bedroom/cozy-cyberpunk | Not used |
| Isometric furniture | OGA community | opengameart.org/content/isometric-furniture | CC0 | Yes | Not required | PNG | Different outline weight than needed for a cohesive room | Not used |
| Kenney Pixel assets | Kenney | kenney.nl/assets | CC0 | Yes | Not required | PNG | Top-down/platformer style, not the isometric bedroom convention needed | Not used |
| riekahq — Isometric Interiors Lite | riekahq | itch.io (riekahq.itch.io/isometric-interiors-lite) | Per itch.io listing (verify before any future use) | Verify on page | Verify on page | PNG | Isometric interiors, closest stylistic fit of all candidates | Not downloaded — itch.io was unreachable from this environment (network returned no response); never embed an asset whose license page you could not actually load and read |
| thurraya — Isometric Bedroom Assets Pack | thurraya | itch.io | Per itch.io listing (verify before any future use) | Verify on page | Verify on page | PNG | Isometric bedroom, close fit | Not downloaded — same reachability issue as above |

**Rule applied:** an asset is only ever "approved" once its license page has
actually been loaded and read in this session. Two of the brief's named
itch.io sources returned no response from this sandboxed environment
(network egress to `itch.io` was blocked/unreachable), so — per the brief's
own instruction not to bypass access restrictions — they were left
unapproved rather than guessed at.

## Fonts

- **UI font**: system font stack (`Inter`/`system-ui`/`-apple-system`) —
  already licensed for use on the visitor's own device; no files bundled.
- **Pixel display font**: "Press Start 2P" via Google Fonts
  (`fonts.googleapis.com`), **SIL Open Font License 1.1** — free for
  commercial and personal use, no attribution file required but credited
  here for transparency. Loaded by `@font-face`/Google's CSS endpoint at
  runtime; no font binary is committed to the repo.
- **Monospace "code" font**: `VT323` family stack with system monospace
  fallback, loaded the same way.

## If you want to swap in real third-party art later

1. Read the license page yourself (don't trust a filename or a search
   snippet) and confirm it covers a **public website**, commercial or not,
   matching the brief's "Only approve assets whose licenses permit the
   intended public website use" rule.
2. Add a row to the table above with every field the brief requires (name,
   author, source URL, license, commercial-use permission, attribution
   requirement, formats, contents, download availability, style match,
   approval).
3. Log the downloaded file in `ASSET_MANIFEST.json` and, if attribution is
   required, add it to `THIRD_PARTY_LICENSES.md`.
4. Redraw it through `tools/isolib.py`'s palette/angle conventions (or
   accept the visual-consistency trade-off explicitly) before adding it to
   the room.
