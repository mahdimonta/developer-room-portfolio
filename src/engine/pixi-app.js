import { Application, Ticker } from "pixi.js";
import { loadRoomAssets } from "./asset-loader.js";
import { buildRoomScene } from "./room-scene.js";
import { fitRoomToViewport } from "./scene-manager.js";
import { mountMonitorScreens } from "./monitor-screens.js";
import { createCharacterController } from "../character/character.js";
import { createCatController } from "../cat/cat.js";
import { wireHotspots } from "../interactions/hotspots.js";
import { startRoomAnimations } from "../animations/room-animations.js";
import { watchReducedMotion } from "../utils/performance.js";

export async function boot(canvas, onProgress) {
  const app = new Application();
  await app.init({
    canvas,
    backgroundAlpha: 0,
    antialias: false, // keep pixel-art crisp; no smoothing between texels
    resolution: Math.min(window.devicePixelRatio || 1, 2),
    autoDensity: true,
    resizeTo: window,
    preference: "webgl",
  });
  onProgress?.(20);

  const { layout, textures } = await loadRoomAssets(onProgress);
  onProgress?.(70);

  const scene = buildRoomScene({ layout, textures });
  app.stage.addChild(scene.world);

  const character = createCharacterController(scene);
  const cat = createCatController(scene);
  onProgress?.(82);

  const screens = mountMonitorScreens(scene);
  const resync = fitRoomToViewport(app, scene.world, scene.canvasSize);
  screens.sync();
  window.addEventListener("resize", () => screens.sync());

  const reducedMotion = watchReducedMotion();
  wireHotspots({ app, scene, character });
  startRoomAnimations({ app, scene, character, cat, reducedMotion });
  onProgress?.(95);

  // Pause heavy work when the tab is hidden (perf + battery requirement).
  // AnimatedSprite (character/cat) drives playback from Ticker.shared by
  // default, a separate instance from app.ticker — both must be stopped,
  // or the character/cat would keep animating invisibly in a hidden tab.
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) {
      app.stop();
      Ticker.shared.stop();
    } else {
      app.start();
      Ticker.shared.start();
    }
  });

  return { app, scene, character, cat, resync };
}
