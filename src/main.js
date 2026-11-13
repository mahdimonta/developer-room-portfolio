import { boot } from "./engine/pixi-app.js";
import { initNav } from "./ui/navigation.js";
import { initAboutPanel } from "./ui/about-panel.js";
import { initProjectPanel } from "./ui/project-panel.js";
import { initContactPanel } from "./ui/contact-panel.js";
import { portfolioData } from "./data/data.js";

function setLoading(pct) {
  const fill = document.getElementById("loading-fill");
  if (fill) fill.style.width = `${pct}%`;
}

function hideLoading() {
  const el = document.getElementById("loading");
  if (!el) return;
  el.style.opacity = "0";
  el.addEventListener("transitionend", () => el.remove(), { once: true });
  setTimeout(() => el.remove(), 900);
}

function fillFooter() {
  const el = document.getElementById("footer-name");
  if (el) el.textContent = `© ${new Date().getFullYear()} ${portfolioData.profile.fullName}`;
}

async function main() {
  fillFooter();
  initNav();
  initAboutPanel(portfolioData);
  initProjectPanel(portfolioData);
  initContactPanel(portfolioData);

  setLoading(15);
  const canvas = document.getElementById("room-canvas");
  const { app, scene, character, cat } = await boot(canvas, (pct) => setLoading(pct));

  window.__room = { app, scene, character, cat }; // handy for manual QA in devtools

  setLoading(100);
  hideLoading();

  showOnboardingGuide();
}

/** First-load interactive guide: points at the three clickable zones. */
function showOnboardingGuide() {
  const guide = document.getElementById("guide");
  const dismissBtn = document.getElementById("guide-dismiss");
  if (!guide || !dismissBtn) return;

  const close = () => {
    guide.classList.remove("show");
    setTimeout(() => (guide.hidden = true), 500);
  };

  guide.hidden = false;
  requestAnimationFrame(() => guide.classList.add("show"));
  dismissBtn.addEventListener("click", close, { once: true });
  guide.addEventListener(
    "click",
    (e) => {
      if (e.target === guide) close();
    },
    { once: true }
  );
  document.addEventListener(
    "keydown",
    function onEsc(e) {
      if (e.key === "Escape") {
        close();
        document.removeEventListener("keydown", onEsc);
      }
    }
  );
}

main().catch((err) => {
  console.error("[room] fatal boot error", err);
  const el = document.getElementById("loading");
  if (el) {
    el.querySelector(".loading-text").textContent =
      "Something went wrong loading the room. Please refresh.";
  }
});
