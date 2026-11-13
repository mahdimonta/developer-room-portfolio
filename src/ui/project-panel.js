import { openPanel } from "./navigation.js";

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

let dataRef = null;

// Generated gradient + glyph "cover" per category — stands in for a real
// screenshot (none were supplied) without faking one. Matches the shelf
// model's own accent so the panel feels connected to the object you clicked.
const COVERS = {
  "Web Platform": { glyph: "◈", from: "#46e4e0", to: "#4a7dff" },
  "Android App": { glyph: "▣", from: "#8fd18b", to: "#4a7dff" },
  "Android Apps": { glyph: "▣", from: "#8fd18b", to: "#4a7dff" },
  Robotics: { glyph: "⬡", from: "#ff7a3d", to: "#ff4d9d" },
  "Robotics / IoT": { glyph: "⬢", from: "#ffb347", to: "#ff7a3d" },
};

function buildCover(project) {
  const cover = el("div", "project-cover");
  const style = COVERS[project.category] || { glyph: "◆", from: "#46e4e0", to: "#9670ff" };
  cover.style.background = `linear-gradient(135deg, ${style.from}, ${style.to})`;
  cover.append(el("span", "project-cover-glyph", style.glyph));
  const label = el("span", "project-cover-label", project.title);
  cover.append(label);
  return cover;
}

function renderProject(project) {
  const host = document.getElementById("project-detail");
  if (!host) return;
  host.innerHTML = "";

  host.append(buildCover(project));

  const header = el("div", "project-header");
  header.append(el("h3", null, project.title));
  const meta = el("div", "project-meta");
  meta.append(el("span", "pill", project.category));
  meta.append(el("span", "pill pill-year", String(project.year)));
  meta.append(el("span", "pill pill-status", project.status));
  header.append(meta);
  host.append(header);

  host.append(el("p", "project-desc", project.description));

  if (project.technologies?.length) {
    const tags = el("div", "tag-row");
    for (const t of project.technologies) tags.append(el("span", "tag", t));
    host.append(tags);
  }

  const links = el("div", "project-links");
  if (project.links?.github) {
    const a = el("a", "btn btn-primary", "View on GitHub");
    a.href = project.links.github;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    links.append(a);
  }
  if (project.links?.demo) {
    const a = el("a", "btn btn-ghost", "Live demo");
    a.href = project.links.demo;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    links.append(a);
  }
  if (links.children.length === 0) {
    links.append(el("p", "project-no-link", "No public link yet — ask me about it."));
  }
  host.append(links);

  // Simple prev/next between shelf projects, so the shelf's pagination
  // requirement works even from inside the detail panel.
  if (dataRef?.projects?.length > 1) {
    const nav = el("div", "project-nav");
    const idx = dataRef.projects.findIndex((p) => p.id === project.id);
    const prev = dataRef.projects[(idx - 1 + dataRef.projects.length) % dataRef.projects.length];
    const next = dataRef.projects[(idx + 1) % dataRef.projects.length];
    const prevBtn = el("button", "btn btn-ghost", "← " + prev.title);
    prevBtn.type = "button";
    prevBtn.addEventListener("click", () => renderProject(prev));
    const nextBtn = el("button", "btn btn-ghost", next.title + " →");
    nextBtn.type = "button";
    nextBtn.addEventListener("click", () => renderProject(next));
    nav.append(prevBtn, nextBtn);
    host.append(nav);
  }
}

export function initProjectPanel(data) {
  dataRef = data;
  if (data?.projects?.length) {
    renderProject(data.projects[0]);
  }
}

export function openProject(project) {
  renderProject(project);
  openPanel("projects");
}
