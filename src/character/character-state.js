/**
 * Character behaviour states. Only one of these AnimatedSprite layers is
 * visible at a time; room-layout.json positions them all at (roughly) the
 * same seat, so swapping visibility reads as one continuous character.
 *
 * Transition rules (per the brief: never let typing/walking/sitting/coffee
 * conflict):
 *   idle <-> typing <-> look        (all seated, interchangeable)
 *   idle/typing -> sit (reversed = stand) -> walk -> coffee -> walk -> sit (reversed)
 */
export const CHAR_LAYERS = [
  "char-idle",
  "char-typing",
  "char-look",
  "char-sit",
  "char-walk",
  "char-coffee",
];

export const CHAR_STATES = {
  idle: { allow: ["typing", "look", "standingUp"] },
  typing: { allow: ["idle", "look", "standingUp"] },
  look: { allow: ["idle", "typing", "standingUp"], exclusive: true },
  standingUp: { allow: ["walk"], exclusive: true }, // char-sit played reversed
  walk: { allow: ["coffee", "roamAction", "sittingDown"] },
  roamAction: { allow: ["walk"], exclusive: true },
  coffee: { allow: ["walk"], exclusive: true },
  sittingDown: { allow: ["idle"], exclusive: true }, // char-sit played forward
};
