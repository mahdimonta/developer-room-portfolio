/** Shared perf/accessibility helpers used across the engine. */

export function watchReducedMotion() {
  const mq = window.matchMedia("(prefers-reduced-motion: reduce)");
  const state = { reduced: mq.matches };
  mq.addEventListener("change", (e) => (state.reduced = e.matches));
  return state;
}

/** Simple finite-state machine: one active state, guarded transitions. */
export function createStateMachine(states, initial) {
  let current = initial;
  let locked = false;
  const listeners = new Set();

  function can(to) {
    const def = states[current];
    return !locked && def && (!def.allow || def.allow.includes(to));
  }

  function go(to, opts = {}) {
    if (to === current && !opts.force) return false;
    if (!opts.force && !can(to)) return false;
    const prevDef = states[current];
    prevDef?.onExit?.();
    current = to;
    const def = states[current];
    if (def?.exclusive) {
      locked = true;
      def.onEnter?.(() => {
        locked = false;
      });
    } else {
      def?.onEnter?.();
    }
    for (const l of listeners) l(current, to);
    return true;
  }

  return {
    get state() {
      return current;
    },
    can,
    go,
    onChange(fn) {
      listeners.add(fn);
      return () => listeners.delete(fn);
    },
  };
}
