import { openPanel } from "./navigation.js";

function el(tag, cls, text) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (text != null) e.textContent = text;
  return e;
}

function row(label, href, text, icon) {
  const a = el("a", "contact-row");
  a.href = href;
  if (href.startsWith("http")) {
    a.target = "_blank";
    a.rel = "noopener noreferrer";
  }
  const ic = el("span", "contact-icon", icon);
  const body = el("span", "contact-text");
  body.append(el("strong", null, label));
  body.append(el("span", "contact-value", text));
  a.append(ic, body);
  return a;
}

export function initContactPanel(data) {
  const { contact, profile } = data;
  const host = document.getElementById("contact-body");
  host.innerHTML = "";

  host.append(el("p", "contact-intro", `${profile.status}. Reach out any time.`));

  const list = el("div", "contact-list");
  if (contact.email) list.append(row("Email", `mailto:${contact.email}`, contact.email, "✉"));
  if (contact.github) list.append(row("GitHub", contact.github, contact.github.replace(/^https?:\/\//, ""), "⌨"));
  if (contact.linkedin) list.append(row("LinkedIn", contact.linkedin, contact.linkedin.replace(/^https?:\/\//, ""), "in"));
  if (contact.phone) list.append(row("Phone", `tel:${contact.phone}`, contact.phone, "☎"));
  host.append(list);

  if (contact.resume) {
    const dl = el("a", "btn btn-primary btn-resume", "Download Résumé (PDF)");
    dl.href = contact.resume;
    dl.setAttribute("download", "");
    host.append(dl);
  }
}

export function openContact() {
  openPanel("contact");
}
