/** Cat behaviour states — fully independent of the character's state machine. */
export const CAT_LAYERS = ["cat-idle", "cat-walk", "cat-sit", "cat-sleep", "cat-stretch", "cat-look"];

export const CAT_STATES = {
  idle: { allow: ["walk", "sit", "look"] },
  walk: { allow: ["idle", "sit"] },
  sit: { allow: ["idle", "sleep", "stretch", "look"] },
  sleep: { allow: ["stretch"] },
  stretch: { allow: ["sit"], exclusive: true },
  look: { allow: ["idle", "sit"], exclusive: true },
};
