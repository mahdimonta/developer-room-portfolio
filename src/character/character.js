import gsap from "../animations/gsap-timelines.js";
import { createStateMachine } from "../utils/performance.js";
import { CHAR_LAYERS, CHAR_STATES } from "./character-state.js";

/**
 * Owns the character's AnimatedSprite layers (grouped into one Container by
 * room-scene.js, so the whole group can be translated for real movement —
 * not just an animation swap in place) and exposes a small state-machine API
 * so room-animations.js and hotspots.js can request behaviour changes
 * without knowing about sprite internals.
 */
const WALK_LEG_MS = 1600;

// Varied destinations across the room:
// - window: walks over to gaze at the rainy city skyline
// - bookshelf: walks over to browse books & tech manuals
// - stretch: steps beside the desk for a stand-and-stretch break
// - coffee: walks to the cabinet coffee machine
const DESTINATIONS = [
  { name: "window", offset: { x: 205, y: -45 }, waitMs: 4200, layer: "char-look" },
  { name: "bookshelf", offset: { x: -135, y: -25 }, waitMs: 3800, layer: "char-look" },
  { name: "stretch", offset: { x: 28, y: 36 }, waitMs: 3200, layer: "char-idle" },
  { name: "coffee", offset: { x: 196, y: 34 }, waitMs: 3400, isCoffee: true },
];

export function createCharacterController(scene) {
  const group = scene.layers.get("char-group");
  const layers = {};
  for (const name of CHAR_LAYERS) {
    const sp = scene.layers.get(name);
    if (sp) {
      sp.visible = false;
      sp.loop = sp.label !== "char-sit" && sp.label !== "char-look" && sp.label !== "char-coffee";
      layers[name] = sp;
    }
  }

  let activeDest = DESTINATIONS[0];
  let destCounter = 0;

  function show(key, { reverse = false, onComplete } = {}) {
    for (const [name, sp] of Object.entries(layers)) {
      sp.visible = name === key;
    }
    const sp = layers[key];
    if (!sp) return;
    sp.loop = !onComplete;
    sp.onComplete = undefined;
    if (reverse) {
      sp.gotoAndPlay(sp.totalFrames - 1);
      sp.animationSpeed = -Math.abs(sp.animationSpeed);
    } else {
      sp.animationSpeed = Math.abs(sp.animationSpeed);
      sp.gotoAndPlay(0);
    }
    if (onComplete) sp.onComplete = onComplete;
  }

  function moveGroup(targetOffset, durationMs, onDone) {
    if (!group) return onDone?.();
    gsap.to(group, {
      x: targetOffset.x,
      y: targetOffset.y,
      duration: durationMs / 1000,
      ease: "sine.inOut",
      onComplete: onDone,
    });
  }

  const sm = createStateMachine(
    {
      idle: { ...CHAR_STATES.idle, onEnter: () => show("char-idle") },
      typing: { ...CHAR_STATES.typing, onEnter: () => show("char-typing") },
      look: {
        ...CHAR_STATES.look,
        onEnter: (unlock) =>
          show("char-look", {
            onComplete: () => {
              unlock();
              sm.go("idle", { force: true });
            },
          }),
      },
      standingUp: {
        ...CHAR_STATES.standingUp,
        onEnter: (unlock) =>
          show("char-sit", {
            reverse: true,
            onComplete: () => {
              unlock();
              sm.go("walk", { force: true });
              // Walk to chosen destination
              moveGroup(activeDest.offset, WALK_LEG_MS, () => {
                if (activeDest.isCoffee) {
                  sm.go("coffee", { force: true });
                } else {
                  sm.go("roamAction", { force: true });
                }
              });
            },
          }),
      },
      walk: { ...CHAR_STATES.walk, onEnter: () => show("char-walk") },
      roamAction: {
        ...CHAR_STATES.roamAction,
        onEnter: (unlock) => {
          show(activeDest.layer || "char-idle");
          setTimeout(() => {
            unlock();
            sm.go("walk", { force: true });
            // Walk back to desk
            moveGroup({ x: 0, y: 0 }, WALK_LEG_MS, () => sm.go("sittingDown", { force: true }));
          }, activeDest.waitMs || 3000);
        },
      },
      coffee: {
        ...CHAR_STATES.coffee,
        onEnter: (unlock) =>
          show("char-coffee", {
            onComplete: () => {
              unlock();
              sm.go("walk", { force: true });
              moveGroup({ x: 0, y: 0 }, WALK_LEG_MS, () => sm.go("sittingDown", { force: true }));
            },
          }),
      },
      sittingDown: {
        ...CHAR_STATES.sittingDown,
        onEnter: (unlock) =>
          show("char-sit", {
            onComplete: () => {
              unlock();
              sm.go("idle", { force: true });
            },
          }),
      },
    },
    "idle"
  );

  show("char-idle");

  return {
    layers,
    get state() {
      return sm.state;
    },
    lookAround() {
      sm.go("look");
    },
    type(durationMs = 2600) {
      if (sm.go("typing")) {
        setTimeout(() => sm.go("idle"), durationMs);
      }
    },
    /** Starts a dynamic roaming sequence to a varied spot (window, bookshelf, stretch, coffee). */
    startRoam(customDest) {
      if (sm.state !== "idle" && sm.state !== "typing") return false;
      if (customDest) {
        activeDest = customDest;
      } else {
        destCounter++;
        activeDest = DESTINATIONS[destCounter % DESTINATIONS.length];
      }
      return sm.go("standingUp");
    },
    goMakeCoffee() {
      return this.startRoam(DESTINATIONS[3]);
    },
    idle() {
      gsap.killTweensOf(group);
      if (group) group.position.set(0, 0);
      sm.go("idle", { force: true });
    },
    destroy() {
      gsap.killTweensOf(group);
    },
  };
}
