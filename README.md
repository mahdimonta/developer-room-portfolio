# 🎮 Mahdi Montazeri — Developer Room Portfolio

> An interactive isometric pixel-art workspace portfolio where the room itself is the user interface.

[![Vite](https://img.shields.io/badge/Vite-7.x-646CFF?style=flat&logo=vite&logoColor=white)](https://vitejs.dev/)
[![PixiJS](https://img.shields.io/badge/PixiJS-v8-E72264?style=flat&logo=pixijs&logoColor=white)](https://pixijs.com/)
[![GSAP](https://img.shields.io/badge/GSAP-3.x-88CE02?style=flat&logo=greensock&logoColor=white)](https://greensock.com/)
[![JavaScript](https://img.shields.io/badge/Vanilla_JS-ES_Modules-F7DF1E?style=flat&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## ✨ Highlights & Features

- **The Room is the UI**: No generic cookie-cutter hero section. Visitors explore an animated cyberpunk/lo-fi isometric bedroom and workspace.
- **Three Core Interactive Hotspots**:
  1. 👤 **The Character** — Click to open the **About Me** panel with bio, education, skills, and international robotics medals.
  2. 🏆 **The Project Shelf** — Click any shelf model to inspect project details, tech stacks, and live GitHub repositories.
  3. 💻 **The Laptop** — Click to open the **Contact & Résumé** panel with download links and contact details.
- **Dynamic 5-Second Cycling RGB Lighting**: The entire room, floor seam LED strips, and HUD indicator smoothly transition every 5 seconds through a vibrant cyber color spectrum (Cyber Red, Electric Cyan, Neon Violet, Emerald Matrix, Warm Amber, Cyberpunk Magenta).
- **Live Programming Monitors**:
  - **Main Monitor**: Real-time code typing simulation with character-by-character typing, blinking cursor, and automatic vertical scrolling.
  - **Side Monitor**: Streaming terminal logs with live build status and command outputs.
  - **Laptop Screen**: Real-time CPU, RAM, and Git repository telemetry.
- **Lively Ambient Life**:
  - The developer types, ponders, stands up to browse the bookshelf, gazes out the rainy city window, stretches, or grabs a coffee.
  - The resident cat stretches, takes calm strolls across the rug, and curls up for cozy naps on its floor cushion.
- **100% Procedurally Generated Art**: All sprites and tiles are generated via custom Python Pillow isometric tools (`tools/`) ensuring crisp 2:1 isometric projection, zero third-party licensing issues, and optimized lightweight assets (~136 KB total!).

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- [Node.js](https://nodejs.org/) (v18 or higher recommended)
- [Python 3.10+](https://www.python.org/) with `Pillow` (only if you wish to rebuild or customize the pixel art)

### Installation & Run

```bash
# 1. Install dependencies
npm install

# 2. Start the local development server (with HMR)
npm run dev

# Open your browser at http://localhost:5173
```

### Production Build

```bash
# Compile and bundle optimized assets to dist/
npm run build

# Preview the production build locally
npm run preview
```

---

## 🎨 Content Customization

You do not need to touch any rendering, physics, or scene code to change portfolio content!

All personal content is centralized in **`src/data/data.js`**:
- **Profile**: Name, role, location, bio, education, languages.
- **Projects**: Title, category, year, description, technologies, GitHub / demo links, shelf slot mapping.
- **Skills & Medals**: Skill categories, tool tags, international competition awards.
- **Contact & Résumé**: Email, phone, GitHub, LinkedIn, and PDF resume path.

---

## 🌐 Free Hosting & Deployment Guides

You can deploy this static project for **100% free** on any modern hosting platform with global CDN acceleration and free automated SSL.

### 1. Cloudflare Pages (Recommended ⚡)

Cloudflare Pages provides instant edge caching, unlimited bandwidth, and automated continuous deployments.

#### Method A: Via Cloudflare Dashboard (Automatic Git Deploys)
1. Push your repository to **GitHub** or **GitLab**.
2. Log in to the [Cloudflare Dashboard](https://dash.cloudflare.com/) and navigate to **Workers & Pages** > **Create application** > **Pages** > **Connect to Git**.
3. Select your repository.
4. Configure the build settings:
   - **Framework preset**: `Vite`
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
5. Click **Save and Deploy**. Your site will be live on a `*.pages.dev` domain in seconds!

#### Method B: Direct Upload via Wrangler CLI
```bash
# Install Wrangler globally
npm install -g wrangler

# Build the project
npm run build

# Deploy dist folder directly
npx wrangler pages deploy dist --project-name=mahdi-portfolio
```

---

### 2. GitHub Pages (Free via GitHub Actions)

Deploy directly from your GitHub repository using GitHub Actions.

1. In your GitHub repository, go to **Settings** > **Pages**.
2. Under **Build and deployment** > **Source**, choose **GitHub Actions**.
3. Create `.github/workflows/deploy.yml` with the following workflow:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: 'pages'
  cancel-in-progress: true

jobs:
  build-and-deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build project
        run: npm run build

      - name: Setup Pages
        uses: actions/configure-pages@v4

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: './dist'

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

> **Note for GitHub Pages**: If deploying to a repository subpath (e.g. `username.github.io/repo/`), ensure `base: "./"` is set in `vite.config.js` (already configured by default in this repo).

---

### 3. Vercel

1. Push your code to GitHub.
2. Sign in to [Vercel](https://vercel.com/) and click **Add New...** > **Project**.
3. Import your repository. Vercel automatically detects Vite:
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
4. Click **Deploy**.

---

### 4. Netlify

1. Sign in to [Netlify](https://www.netlify.com/).
2. Click **Add new site** > **Import an existing project** (or drag and drop the `dist/` folder into the Netlify Drop zone).
3. Set build settings:
   - **Build command**: `npm run build`
   - **Publish directory**: `dist`
4. Click **Deploy site**.

---

## 🛠️ Procedural Asset Pipeline

If you want to modify room geometry, furniture, or animations:

```bash
# Rebuild all isometric sprites and generate room-layout.json
npm run assets:build

# Generate flat QA preview image to docs/_preview_room.png
python tools/preview.py
```

### Asset Tool Modules
- `tools/isolib.py` — Isometric 2:1 projection math, color palette, primitive drawers.
- `tools/gen_room.py` — Generates floor tiles, walls, and ambient base.
- `tools/gen_props.py` — Furniture, desk, dual monitors, project shelf, electronics.
- `tools/gen_character.py` — Seated, typing, walking, stretching, and coffee animations.
- `tools/gen_cat.py` — Sleeping, stretching, sitting, looking, and walking cat cycles.
- `tools/stage.py` — Automatic bounding-box cropping, depth-sorting, and layout exporter.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
All pixel art and generated assets are 100% original works generated by code.
