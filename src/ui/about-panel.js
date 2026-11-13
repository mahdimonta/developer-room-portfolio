import { openPanel } from "./navigation.js";

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

export function initAboutPanel(data) {
  const { profile, skills, achievements } = data;

  document.getElementById("about-title").textContent = profile.fullName;
  document.querySelector(".about-role").textContent = profile.roleLong;
  document.querySelector(".about-bio").textContent = profile.bio;

  const photo = document.getElementById("about-photo");
  photo.src = profile.photo;
  photo.alt = `Portrait of ${profile.fullName}`;
  photo.onerror = () => {
    photo.style.display = "none";
  };

  const facts = document.querySelector(".about-facts");
  facts.innerHTML = "";
  const addFact = (label, value) => {
    if (!value) return;
    const dt = el("dt", null, label);
    const dd = el("dd", null, value);
    facts.append(dt, dd);
  };
  addFact("Location", profile.location);
  addFact("Status", profile.status);
  addFact("Education", `${profile.education.degree} — GPA ${profile.education.gpa} (${profile.education.years})`);
  addFact("Languages", profile.languages.map((l) => `${l.name} — ${l.level}`).join(" · "));
  addFact("Interests", profile.interests.join(" · "));

  const skillsGrid = document.getElementById("skills-grid");
  skillsGrid.innerHTML = "";
  for (const s of skills) {
    const card = el("div", "skill-card");
    card.append(el("h4", null, s.title));
    card.append(el("p", null, s.description));
    const tags = el("div", "tag-row");
    for (const t of s.tools) tags.append(el("span", "tag", t));
    card.append(tags);
    skillsGrid.append(card);
  }

  const achList = document.getElementById("achievements-list");
  achList.innerHTML = "";
  const stat = el("div", "ach-stat");
  stat.append(el("span", "ach-stat-num", String(achievements.statNumber)));
  stat.append(el("span", "ach-stat-label", achievements.statLabel));
  achList.append(stat);

  const medalRow = el("div", "medal-row");
  for (const m of achievements.medals) {
    const card = el("div", "medal-card");
    card.append(el("h5", null, m.title));
    card.append(el("p", "medal-event", `${m.event} · ${m.year}`));
    card.append(el("p", "medal-desc", m.description));
    medalRow.append(card);
  }
  achList.append(medalRow);

  if (achievements.more?.length) {
    const more = el("ul", "ach-more");
    for (const m of achievements.more) more.append(el("li", null, m));
    achList.append(more);
  }
}

export function openAbout() {
  openPanel("about");
}
