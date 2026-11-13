import gsap from "../animations/gsap-timelines.js";

let activePanel = null;
let lastFocused = null;

function panelEl(name) {
  return document.getElementById(`panel-${name}`);
}

export function openPanel(name) {
  const el = panelEl(name);
  if (!el || el === activePanel) return;
  if (activePanel) closePanel();

  lastFocused = document.activeElement;
  el.setAttribute("aria-hidden", "false");
  el.classList.add("open");
  document.body.classList.add("panel-open");
  activePanel = el;

  const card = el.querySelector(".panel-card");
  gsap.fromTo(
    el,
    { autoAlpha: 0 },
    { autoAlpha: 1, duration: 0.25, ease: "power2.out" }
  );
  gsap.fromTo(
    card,
    { y: 24, autoAlpha: 0, scale: 0.98 },
    { y: 0, autoAlpha: 1, scale: 1, duration: 0.38, ease: "back.out(1.6)", delay: 0.03 }
  );

  const closeBtn = el.querySelector("[data-close]");
  closeBtn?.focus({ preventScroll: true });
}

export function closePanel() {
  if (!activePanel) return;
  const el = activePanel;
  const card = el.querySelector(".panel-card");
  gsap.to(card, { y: 16, autoAlpha: 0, scale: 0.98, duration: 0.22, ease: "power1.in" });
  gsap.to(el, {
    autoAlpha: 0,
    duration: 0.26,
    delay: 0.05,
    onComplete: () => {
      el.setAttribute("aria-hidden", "true");
      el.classList.remove("open");
    },
  });
  document.body.classList.remove("panel-open");
  activePanel = null;
  if (lastFocused && typeof lastFocused.focus === "function") {
    lastFocused.focus({ preventScroll: true });
  }
}

export function initNav() {
  document.querySelectorAll("[data-open]").forEach((btn) => {
    btn.addEventListener("click", () => openPanel(btn.dataset.open));
  });
  document.querySelectorAll("[data-close]").forEach((btn) => {
    btn.addEventListener("click", () => closePanel());
  });
  document.querySelectorAll(".panel").forEach((panel) => {
    panel.addEventListener("click", (e) => {
      if (e.target === panel) closePanel();
    });
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && activePanel) closePanel();
  });
}
