import gsap from "gsap";
import { PixiPlugin } from "gsap/PixiPlugin";
import * as PIXI from "pixi.js";

// Registers GSAP's PixiPlugin once so `gsap.to(obj, { pixi: {...} })` works
// anywhere in the app. Import `gsap` from THIS file (not the bare "gsap"
// package) wherever a tween touches a PixiJS object's `pixi:` properties.
PixiPlugin.registerPIXI(PIXI);
gsap.registerPlugin(PixiPlugin);

export default gsap;
