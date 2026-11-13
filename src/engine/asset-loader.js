import { Assets, Texture, Rectangle } from "pixi.js";

/**
 * Loads room-layout.json (positions/sort/anim metadata baked by the Python
 * asset pipeline in /tools) plus every sprite + spritesheet it references.
 */
export async function loadRoomAssets(onProgress) {
  const base = import.meta.env.BASE_URL || "/";
  const layoutRes = await fetch(`${base}assets/room/room-layout.json`);
  if (!layoutRes.ok) {
    throw new Error(
      `room-layout.json missing (${layoutRes.status}) — run "npm run assets:build"`
    );
  }
  const layout = await layoutRes.json();

  const bundle = {};
  for (const [name, s] of Object.entries(layout.sprites)) {
    bundle[`sprite:${name}`] = `${base}${s.src}`;
  }
  for (const [name, a] of Object.entries(layout.anims)) {
    bundle[`anim:${name}`] = `${base}${a.src}`;
  }

  Assets.addBundle("room", bundle);
  const textures = await Assets.loadBundle("room", (progress) => {
    onProgress?.(10 + Math.round(progress * 80));
  });

  return { layout, textures, base };
}

/** Slice a loaded spritesheet texture into `frameCount` equal-width frames. */
export function sliceFrames(sheetTexture, frameCount, fw, fh) {
  const frames = [];
  for (let i = 0; i < frameCount; i++) {
    frames.push(
      new Texture({
        source: sheetTexture.source,
        frame: new Rectangle(i * fw, 0, fw, fh),
      })
    );
  }
  return frames;
}
