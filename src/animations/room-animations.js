import gsap from "./gsap-timelines.js";

const TYPING_MIN = 4000;
const TYPING_MAX = 11000;
const IDLE_MIN = 3000;
const IDLE_MAX = 6000;

/**
 * Drives the room's ambient life: the character's idle<->typing loop with
 * occasional coffee breaks, the cat's autonomous schedule, and small
 * cursor-reactive flourishes. All loops respect prefers-reduced-motion by
 * slowing or disabling the non-essential flourishes (ambient sprite
 * animations from room-scene.js keep running either way, since they convey
 * state, not just decoration).
 */
export function startRoomAnimations({ app, scene, character, cat, reducedMotion }) {
  let charTimer = null;
  let roamCooldown = 0;

  function rand(min, max) {
    return min + Math.random() * (max - min);
  }

  function scheduleCharacterBeat() {
    clearTimeout(charTimer);
    const delay = reducedMotion.reduced ? rand(IDLE_MIN, IDLE_MAX) * 1.5 : rand(IDLE_MIN, IDLE_MAX);
    charTimer = setTimeout(() => {
      if (character.state === "idle") {
        roamCooldown++;
        const r = Math.random();
        // Varied, attractive developer behavior:
        // Every 4th beat: stands up and visits the window, browses the bookshelf,
        // takes a stretch, or gets coffee — keeping the workspace lively!
        if (roamCooldown % 4 === 0 && !reducedMotion.reduced) {
          character.startRoam();
        } else if (r < 0.35 && !reducedMotion.reduced) {
          character.lookAround();
        } else {
          character.type(rand(TYPING_MIN, TYPING_MAX));
        }
      }
      scheduleCharacterBeat();
    }, delay);
  }
  scheduleCharacterBeat();

  cat.startAutonomy();

  // Subtle light-pool breathing on the desk lamp / wall lamp glows.
  const lamps = ["desk-lamp", "wall-lamp"]
    .map((n) => scene.layers.get(n))
    .filter(Boolean);
  if (!reducedMotion.reduced) {
    for (const lamp of lamps) {
      gsap.to(lamp, {
        alpha: 0.86,
        duration: 2.4 + Math.random(),
        yoyo: true,
        repeat: -1,
        ease: "sine.inOut",
      });
    }
  }

  // ---- Dynamic 5-Second Cycling RGB Room Lighting -------------------------
  // Switches smoothly between cyber red, electric cyan, neon violet, emerald, amber, magenta
  const RGB_PALETTE = [
    { num: 0xff1e44, hex: "#ff1e44" }, // Red
    { num: 0x00f0ff, hex: "#00f0ff" }, // Cyan
    { num: 0xa855f7, hex: "#a855f7" }, // Violet
    { num: 0x10b981, hex: "#10b981" }, // Emerald
    { num: 0xffb300, hex: "#ffb300" }, // Amber
    { num: 0xec4899, hex: "#ec4899" }, // Magenta
    { num: 0x3b82f6, hex: "#3b82f6" }, // Blue
  ];

  const ambientLayer = scene.layers.get("ambient-rgb");
  const rgbStrip = scene.layers.get("rgb-strip");
  const hudDot = document.querySelector(".hud-dot");
  let rgbIdx = 0;

  function cycleRgbLight() {
    rgbIdx = (rgbIdx + 1) % RGB_PALETTE.length;
    const current = RGB_PALETTE[rgbIdx];

    if (ambientLayer) {
      gsap.to(ambientLayer, {
        pixi: { tint: current.num },
        duration: 1.6,
        ease: "sine.inOut",
      });
    }

    if (rgbStrip) {
      gsap.to(rgbStrip, {
        pixi: { tint: current.num },
        duration: 1.6,
        ease: "sine.inOut",
      });
    }

    if (hudDot) {
      hudDot.style.background = current.hex;
      hudDot.style.boxShadow = `0 0 10px ${current.hex}, 0 0 2px #fff`;
    }
  }

  const rgbInterval = setInterval(cycleRgbLight, 5000);

  // Cursor-reactive cat glance: a light-weight, throttled listener
  let lastGlance = 0;
  app.canvas.addEventListener("pointermove", () => {
    if (reducedMotion.reduced) return;
    const now = performance.now();
    if (now - lastGlance < 6000) return;
    if (cat.state !== "idle" && cat.state !== "sit") return;
    if (Math.random() < 0.015) {
      lastGlance = now;
      cat.glanceAt();
    }
  });

  return {
    stop() {
      clearTimeout(charTimer);
      clearInterval(rgbInterval);
      cat.stopAutonomy();
    },
  };
}
