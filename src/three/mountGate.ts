import type { SceneHandle } from './Scene';
import { getMountTier, type MountTier } from './tiers';

export interface MountStageOptions {
  container: HTMLElement;
  theme: 'light' | 'dark';
  /** Called once the WebGL scene is live. */
  onReady: (handle: SceneHandle) => void;
  /** Called when the stage must fall back to the static poster (reason supplied). */
  onFallback: (reason: string) => void;
}

const IDLE_TIMEOUT_MS = 2000;

/**
 * Mount gate (plan.md / ADR-036): `tier → IntersectionObserver → requestIdleCallback
 * → import('./three/Scene')`. The three.js bundle is never fetched before all
 * three conditions pass; any failure resolves to the theme-aware static poster.
 *
 * Returns a dispose function that cancels pending work and tears down a live scene.
 */
export const mountStage = (options: MountStageOptions): (() => void) => {
  let cancelled = false;
  let sceneHandle: SceneHandle | null = null;
  let observer: IntersectionObserver | null = null;
  let idleId: number | null = null;
  let timeoutId: number | null = null;
  let bootCalled = false;

  const tier: MountTier = getMountTier();
  if (tier === 'none') {
    options.onFallback('tier:none');
    return () => undefined;
  }

  const teardownScene = (): void => {
    if (sceneHandle) {
      sceneHandle.dispose();
      sceneHandle = null;
    }
  };

  const fail = (reason: string): void => {
    if (cancelled) return;
    teardownScene();
    options.onFallback(reason);
  };

  const boot = (): void => {
    if (cancelled) return;
    import('./Scene')
      .then(({ createScene }) => {
        if (cancelled) return;
        try {
          sceneHandle = createScene(options.container, {
            theme: options.theme,
            tier,
            onContextLost: () => fail('webgl:context-lost'),
          });
          options.onReady(sceneHandle);
        } catch (error) {
          fail(`webgl:init:${error instanceof Error ? error.message : String(error)}`);
        }
      })
      .catch((error: unknown) => {
        fail(`import:${error instanceof Error ? error.message : String(error)}`);
      });
  };

  const startWhenIdle = (): void => {
    if (cancelled || bootCalled) return;
    bootCalled = true;
    if (typeof window.requestIdleCallback === 'function') {
      idleId = window.requestIdleCallback(boot, { timeout: IDLE_TIMEOUT_MS });
    } else {
      timeoutId = window.setTimeout(boot, 1);
    }
  };

  const observe = (): void => {
    if (cancelled) return;
    if (typeof IntersectionObserver === 'function') {
      observer = new IntersectionObserver(
        (entries) => {
          if (entries.some((entry) => entry.isIntersecting)) {
            observer?.disconnect();
            observer = null;
            startWhenIdle();
          }
        },
        { threshold: 0 }
      );
      observer.observe(options.container);
    } else {
      startWhenIdle();
    }
  };

  observe();

  return () => {
    cancelled = true;
    observer?.disconnect();
    observer = null;
    if (idleId !== null && typeof window.cancelIdleCallback === 'function') {
      window.cancelIdleCallback(idleId);
    }
    if (timeoutId !== null) window.clearTimeout(timeoutId);
    teardownScene();
  };
};
