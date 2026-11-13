import gsap from "../animations/gsap-timelines.js";
import { openAbout } from "../ui/about-panel.js";
import { openProject } from "../ui/project-panel.js";
import { openContact } from "../ui/contact-panel.js";
import { portfolioData } from "../data/data.js";
import { CHAR_LAYERS } from "../character/character-state.js";

// shelf slot order matches tools/gen_props.py PROJECT_MODELS keys
const SLOT_KEYS = ["store", "phone", "robot", "tower", "dashboard", "apps"];

function makeInteractive(obj, { cursor = "pointer" } = {}) {
  obj.eventMode = "static";
  obj.cursor = cursor;
  return obj;
}

function hoverPulse(obj, { lift = 6, scale = 1.06 } = {}) {
  const base = { y: obj.y, scaleX: obj.scale.x, scaleY: obj.scale.y };
  let tween;
  obj.on("pointerover", () => {
    tween?.kill();
    tween = gsap.to(obj, {
      y: base.y - lift,
      pixi: { scaleX: base.scaleX * scale, scaleY: base.scaleY * scale },
      duration: 0.28,
      ease: "back.out(2)",
    });
    obj.alpha = 1;
  });
  obj.on("pointerout", () => {
    tween?.kill();
    tween = gsap.to(obj, {
      y: base.y,
      pixi: { scaleX: base.scaleX, scaleY: base.scaleY },
      duration: 0.32,
      ease: "power2.out",
    });
  });
}

export function wireHotspots({ app, scene, character }) {
  const { layers } = scene;

  // ---- A. Character — About Me -------------------------------------------
  // Wired on EVERY character layer (idle/typing/look/sit/walk/coffee), not
  // just the seated ones — the character periodically gets up to make
  // coffee, and he must stay clickable wherever he currently is, or the
  // hotspot silently "stops working" for seconds at a time.
  for (const name of CHAR_LAYERS) {
    const sp = layers.get(name);
    if (!sp) continue;
    makeInteractive(sp);
    sp.on("pointerover", () => {
      sp.tint = 0xcfe9ff;
      character.lookAround?.(); // no-op (ignored) unless currently seated
    });
    sp.on("pointerout", () => (sp.tint = 0xffffff));
    sp.on("pointertap", () => openAbout());
  }

  // Fallback: the empty chair itself (when he's stepped away) still opens
  // About — it's still "his seat".
  for (const name of ["chair-back", "chair-front"]) {
    const sp = layers.get(name);
    if (!sp) continue;
    makeInteractive(sp);
    sp.on("pointertap", () => openAbout());
  }

  // ---- B. Project shelf — Projects ---------------------------------------
  SLOT_KEYS.forEach((key, i) => {
    const sp = layers.get(`proj-${key}`);
    if (!sp) return;
    makeInteractive(sp);
    hoverPulse(sp, { lift: 7, scale: 1.12 });
    sp.on("pointertap", () => {
      const project = portfolioData.projects.find((p) => p.shelfSlot === i);
      if (project) openProject(project);
    });
  });

  // ---- C. Laptop — Contact & Résumé --------------------------------------
  const laptop = layers.get("laptop");
  if (laptop) {
    makeInteractive(laptop);
    laptop.on("pointerover", () => {
      laptop.tint = 0xdfffff;
      gsap.to(laptop, { pixi: { scaleX: 1.04, scaleY: 1.04 }, duration: 0.25 });
    });
    laptop.on("pointerout", () => {
      laptop.tint = 0xffffff;
      gsap.to(laptop, { pixi: { scaleX: 1, scaleY: 1 }, duration: 0.3 });
    });
    laptop.on("pointertap", () => openContact());
  }

  // Keyboard accessibility: Tab to each hotspot via invisible DOM buttons
  // already present in index.html's quick-nav; canvas hotspots are a
  // progressive-enhancement layer on top of that baseline.
}
