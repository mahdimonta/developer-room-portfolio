import gsap from "../animations/gsap-timelines.js";
import { createStateMachine } from "../utils/performance.js";
import { CAT_LAYERS, CAT_STATES } from "./cat-state.js";

const AUTONOMOUS_SEQUENCE = [
  { state: "sleep", minMs: 14000, maxMs: 28000 },
  { state: "stretch", minMs: 2500, maxMs: 2500 },
  { state: "sit", minMs: 6000, maxMs: 12000 },
  { state: "idle", minMs: 4000, maxMs: 8000 },
  { state: "walk", minMs: 5000, maxMs: 8000 },
  { state: "sit", minMs: 6000, maxMs: 10000 },
  { state: "idle", minMs: 3500, maxMs: 6000 },
  { state: "sleep", minMs: 16000, maxMs: 32000 },
];

function rand(min, max) {
  return min + Math.random() * (max - min);
}

export function createCatController(scene) {
  const group = scene.layers.get("cat-group");
  const layers = {};
  for (const name of CAT_LAYERS) {
    const sp = scene.layers.get(name);
    if (sp) {
      sp.visible = false;
      layers[name] = sp;
    }
  }

  function show(key, { onComplete } = {}) {
    for (const [name, sp] of Object.entries(layers)) sp.visible = name === key;
    const sp = layers[key];
    if (!sp) return;
    sp.loop = !onComplete;
    sp.onComplete = onComplete || undefined;
    sp.animationSpeed = Math.abs(sp.animationSpeed);
    sp.gotoAndPlay(0);
  }

  // The cat mostly rests on its plush cushion or the rug.
  // The walk state moves it slowly and gracefully — a calm, natural stroll.
  function wander() {
    if (!group) return;
    gsap.killTweensOf(group);
    const legs = 1 + Math.round(Math.random());
    const tl = gsap.timeline();
    for (let i = 0; i < legs; i++) {
      const dx = rand(-90, 90);
      const dy = rand(-35, 35);
      const dist = Math.hypot(dx - group.x, dy - group.y);
      tl.to(group, {
        x: dx,
        y: dy,
        duration: Math.max(2.4, dist / 42),
        ease: "sine.inOut",
      });
    }
  }
  function goHome() {
    if (!group) return;
    gsap.killTweensOf(group);
    const dist = Math.hypot(group.x, group.y);
    gsap.to(group, { x: 0, y: 0, duration: Math.max(2.2, dist / 42), ease: "sine.inOut" });
  }

  const sm = createStateMachine(
    {
      idle: { ...CAT_STATES.idle, onEnter: () => { show("cat-idle"); goHome(); } },
      walk: { ...CAT_STATES.walk, onEnter: () => { show("cat-walk"); wander(); } },
      sit: { ...CAT_STATES.sit, onEnter: () => { show("cat-sit"); goHome(); } },
      sleep: { ...CAT_STATES.sleep, onEnter: () => { show("cat-sleep"); goHome(); } },
      stretch: {
        ...CAT_STATES.stretch,
        onEnter: (unlock) =>
          show("cat-stretch", {
            onComplete: () => {
              unlock();
              sm.go("sit", { force: true });
            },
          }),
      },
      look: {
        ...CAT_STATES.look,
        onEnter: (unlock) =>
          show("cat-look", {
            onComplete: () => {
              unlock();
              sm.go("idle", { force: true });
            },
          }),
      },
    },
    "idle"
  );

  show("cat-idle");

  let autoTimer = null;
  let seqIndex = 0;
  function scheduleNext() {
    clearTimeout(autoTimer);
    const step = AUTONOMOUS_SEQUENCE[seqIndex % AUTONOMOUS_SEQUENCE.length];
    seqIndex++;
    sm.go(step.state);
    autoTimer = setTimeout(scheduleNext, rand(step.minMs, step.maxMs));
  }

  return {
    layers,
    get state() {
      return sm.state;
    },
    startAutonomy() {
      scheduleNext();
    },
    stopAutonomy() {
      clearTimeout(autoTimer);
      gsap.killTweensOf(group);
    },
    /** Pointer-tracking glance, used by room-animations' mousemove handler. */
    glanceAt() {
      sm.go("look");
    },
  };
}
