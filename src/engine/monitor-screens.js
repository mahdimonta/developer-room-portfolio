/**
 * Renders LIVE HTML "code" onto the monitor/laptop screens.
 *
 * Per the project brief, on-screen text must stay real text (selectable,
 * accessible) rather than being baked into a pixel-art image. We overlay a
 * plain HTML <pre> on top of the canvas, warped with a CSS transform so its
 * quad lines up with the isometric screen surface baked into
 * room-layout.json, and keep it in sync with the room's pan/zoom.
 */

/**
 * Renders LIVE interactive animated HTML "code" onto the monitor/laptop screens.
 *
 * Simulates real active programming:
 * - Main monitor: Real-time code typing with blinking cursor, auto-scrolling, functions & shaders.
 * - Side monitor: Live streaming developer logs, build pipelines, and git commands.
 * - Laptop: System telemetry, git commit tracker, and hardware stats.
 */

const MAIN_SNIPPETS = [
  "// Robotics Autonomous Drive & AprilTag Tracking",
  "import { IMU, PIDController, Vision } from '@robotics/core';",
  "",
  "class RobotNavigator {",
  "  constructor() {",
  "    this.imu = new IMU({ calibration: 'auto' });",
  "    this.vision = new Vision({ targetTag: 7 });",
  "    this.pid = new PIDController(1.4, 0.05, 0.25);",
  "    this.speed = 0.85;",
  "  }",
  "",
  "  async update(telemetry) {",
  "    const heading = await this.imu.getHeading();",
  "    const tag = this.vision.findTag();",
  "    if (tag.detected) {",
  "      const correction = this.pid.calculate(tag.bearing);",
  "      this.drive(heading + correction, this.speed);",
  "      console.log(`[tag] locked: dist=${tag.distance.toFixed(2)}m`);",
  "    }",
  "    return telemetry.record(heading);",
  "  }",
  "}",
  "",
  "// WebGL & Isometric Shader Pipeline",
  "function compilePixelShaders(gl) {",
  "  const vbo = gl.createBuffer();",
  "  gl.bindBuffer(gl.ARRAY_BUFFER, vbo);",
  "  gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);",
  "  console.log('✓ WebGL2 Pipeline Online: 60 FPS');",
  "}",
];

const SIDE_LOGS = [
  "$ npx vite --port 5174",
  "  VITE v7.3.7  ready in 214 ms",
  "  ➜  Local: http://localhost:5174/",
  "  ✓ 749 modules transformed",
  "  [assets] loaded 33 sprites, 16 anims",
  "  [pixi] WebGL2 renderer initialized (autoDensity: true)",
  "  [fps] 60.0 locked, 0 dropped frames",
  "  $ git status",
  "  On branch main: working tree clean",
  "  $ pytest tests/test_robot.py",
  "  ✓ test_imu_drift PASSED [14ms]",
  "  ✓ test_apriltag_track PASSED [22ms]",
  "  ✓ test_motor_pwm PASSED [8ms]",
  "  [build] 3 passed in 0.04s",
  "  [deploy] git push origin main -> deployed ✓",
  "  [system] all services operational",
];

const LAPTOP_STATS = [
  "git branch: main*",
  "HEAD -> v2.1.0",
  "commit 7e2f1a0 (HEAD)",
  "Author: Mahdi Montazeri",
  "CPU: 18%  | RAM: 4.8 GB",
  "GPU: WebGL2 (discrete)",
  "Status: Open to internships",
  "Uptime: 99.98%",
];

function quadToCss(points, w, h) {
  const [p0, p1, p2, p3] = points;
  const ex = (p1[0] - p0[0]) / w;
  const fx = (p1[1] - p0[1]) / w;
  const ey = (p3[0] - p0[0]) / h;
  const fy = (p3[1] - p0[1]) / h;
  return `matrix(${ex}, ${fx}, ${ey}, ${fy}, ${p0[0]}, ${p0[1]})`;
}

export function mountMonitorScreens({ quads, world, canvasSize }) {
  const host = document.createElement("div");
  host.className = "screen-host";
  document.getElementById("app").appendChild(host);

  const nodes = [];
  let mainCodeEl = null;
  let sideCodeEl = null;
  let laptopCodeEl = null;

  for (const [name, q] of Object.entries(quads)) {
    if (q.kind !== "screen") continue;
    const w = Math.hypot(q.points[1][0] - q.points[0][0], q.points[1][1] - q.points[0][1]);
    const h = Math.hypot(q.points[3][0] - q.points[0][0], q.points[3][1] - q.points[0][1]);

    const el = document.createElement("pre");
    el.className = "screen-code";
    el.setAttribute("aria-hidden", "true");
    el.style.width = `${w}px`;
    el.style.height = `${h}px`;
    el.style.overflow = "hidden";
    host.appendChild(el);

    if (name === "monitor-main-screen") mainCodeEl = el;
    else if (name === "monitor-side-screen") sideCodeEl = el;
    else if (name === "laptop-screen") laptopCodeEl = el;

    nodes.push({ name, el, q, w, h });
  }

  // ---- 1. Main Monitor: Real-time Live Code Typing Simulation ----
  let lineIdx = 0;
  let charIdx = 0;
  let currentLines = [];
  let blinkState = true;

  function typeCodeStep() {
    if (!mainCodeEl) return;
    if (lineIdx >= MAIN_SNIPPETS.length) {
      lineIdx = 0;
      charIdx = 0;
      currentLines = [];
    }

    const currentLineTarget = MAIN_SNIPPETS[lineIdx];
    if (charIdx <= currentLineTarget.length) {
      const lineText = currentLineTarget.slice(0, charIdx);
      const displayLines = [...currentLines, lineText + (blinkState ? "▌" : " ")];
      mainCodeEl.textContent = displayLines.join("\n");
      mainCodeEl.scrollTop = mainCodeEl.scrollHeight;
      charIdx += 2; // type speed
      setTimeout(typeCodeStep, 65);
    } else {
      currentLines.push(currentLineTarget);
      if (currentLines.length > 12) currentLines.shift();
      lineIdx++;
      charIdx = 0;
      setTimeout(typeCodeStep, currentLineTarget === "" ? 120 : 380);
    }
  }
  typeCodeStep();

  // Cursor blink interval
  setInterval(() => {
    blinkState = !blinkState;
  }, 480);

  // ---- 2. Side Monitor: Continuous Scrolling Terminal Logs ----
  let sideIdx = 0;
  let displayedLogs = [];
  function streamSideLogs() {
    if (!sideCodeEl) return;
    displayedLogs.push(SIDE_LOGS[sideIdx % SIDE_LOGS.length]);
    if (displayedLogs.length > 9) displayedLogs.shift();
    sideCodeEl.textContent = displayedLogs.join("\n");
    sideCodeEl.scrollTop = sideCodeEl.scrollHeight;
    sideIdx++;
    setTimeout(streamSideLogs, 1600 + Math.random() * 800);
  }
  streamSideLogs();

  // ---- 3. Laptop Screen: Live Hardware & Git Metrics ----
  let laptopCycle = 0;
  function updateLaptopScreen() {
    if (!laptopCodeEl) return;
    const cpu = 15 + Math.floor(Math.sin(laptopCycle) * 12 + 10);
    const ram = (4.2 + Math.cos(laptopCycle) * 0.4).toFixed(1);
    const lines = [
      ...LAPTOP_STATS.slice(0, 4),
      `CPU: ${cpu}%  | RAM: ${ram} GB`,
      ...LAPTOP_STATS.slice(5)
    ];
    laptopCodeEl.textContent = lines.join("\n");
    laptopCycle += 0.3;
    setTimeout(updateLaptopScreen, 2200);
  }
  updateLaptopScreen();

  function sync() {
    const s = world.scale.x;
    const ox = world.position.x;
    const oy = world.position.y;
    host.style.transform = `translate(${ox}px, ${oy}px) scale(${s})`;
    for (const n of nodes) {
      n.el.style.transform = quadToCss(n.q.points, n.w, n.h);
    }
  }

  return { host, sync, nodes };
}
