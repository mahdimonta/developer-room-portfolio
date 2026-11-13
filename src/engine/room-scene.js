import { Container, Sprite, AnimatedSprite, Graphics } from "pixi.js";
import { sliceFrames } from "./asset-loader.js";

/**
 * Builds the layered room from room-layout.json. Every furniture/effect
 * piece stays an independent display object (named via `.label`) so
 * interactions.js and the animation modules can reach back into the scene.
 *
 * Returns { world, layers } where `layers` is a Map<name, Container|Sprite>
 * for quick lookup (monitors, laptop, project models, character anchor...).
 */
export function buildRoomScene({ layout, textures }) {
  const world = new Container();
  world.label = "room-world";
  const layers = new Map();

  const put = (name, obj, sort) => {
    obj.label = name;
    obj.zIndex = sort;
    layers.set(name, obj);
    world.addChild(obj);
  };

  // ---- static sprites (furniture, room shell pieces, decor) -------------
  for (const [name, s] of Object.entries(layout.sprites)) {
    const tex = textures[`sprite:${name}`];
    if (!tex) continue;
    const sp = new Sprite(tex);
    sp.position.set(s.x, s.y);
    if (s.hotspot) sp.cursor = "pointer";
    put(name, sp, s.sort);
  }

  // ---- animated layers (character, cat, effects) -------------------------
  // Character and cat frames are grouped into their own Containers so
  // character.js / cat.js can translate the WHOLE group (walking across the
  // room) while individual AnimatedSprite layers keep their baked relative
  // offsets — swapping which one is visible never jumps position.
  const charGroup = new Container();
  const catGroup = new Container();
  put("char-group", charGroup, 30);
  put("cat-group", catGroup, 35);

  for (const [name, a] of Object.entries(layout.anims)) {
    const sheet = textures[`anim:${name}`];
    if (!sheet) continue;
    const frames = sliceFrames(sheet, a.frames, a.fw, a.fh);
    const anim = new AnimatedSprite(frames);
    anim.position.set(a.x, a.y);
    anim.animationSpeed = a.fps / 60;
    anim.loop = a.loop;
    anim.play();
    anim.label = name;

    if (name.startsWith("char-")) {
      charGroup.addChild(anim);
      layers.set(name, anim);
    } else if (name.startsWith("cat-")) {
      catGroup.addChild(anim);
      layers.set(name, anim);
    } else {
      put(name, anim, a.sort);
    }
  }

  // ---- "screen" quads: rendered separately as live HTML/canvas content ---
  // Register their pixel bounds so monitor-screens.js can position overlays.
  const quads = layout.quads || {};

  // ---- room border mask so nothing bleeds outside the canvas -------------
  const mask = new Graphics()
    .rect(0, 0, layout.meta.canvas.w, layout.meta.canvas.h)
    .fill(0xffffff);
  world.mask = mask;
  world.addChild(mask);

  world.sortableChildren = true;

  return { world, layers, quads, canvasSize: layout.meta.canvas, tile: layout.meta.tile };
}
