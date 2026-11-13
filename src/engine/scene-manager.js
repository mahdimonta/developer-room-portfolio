/**
 * Fits the fixed-size isometric room into whatever viewport is available,
 * keeping pixel-art crispness (integer-ish scale where possible) and
 * centering the composition. Re-runs on resize/orientation change.
 */
export function fitRoomToViewport(app, world, canvasSize) {
  const resize = () => {
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const margin = vw < 700 ? 0.98 : 0.96;
    const scale = Math.min(
      (vw * margin) / canvasSize.w,
      (vh * margin) / canvasSize.h,
      2.2
    );
    world.scale.set(scale);
    world.position.set(
      (vw - canvasSize.w * scale) / 2,
      (vh - canvasSize.h * scale) / 2
    );
  };
  resize();
  window.addEventListener("resize", resize);
  window.addEventListener("orientationchange", resize);
  return resize;
}
