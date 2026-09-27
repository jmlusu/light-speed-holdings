import React, { useEffect, useRef, useState } from 'react';
import type { SceneHandle } from '../three/Scene';
import { mountStage } from '../three/mountGate';
import { posterStyles } from '../three/poster';
import { getMountTier, type MountTier } from '../three/tiers';
import { useScrollProgress } from '../hooks/useScrollProgress';

export interface ImmersiveStageProps {
  theme: 'light' | 'dark';
}

type StageMode = 'pending' | 'scene' | 'poster';

/**
 * The WebGL stage behind the homepage (plan.md Contract A → B).
 *
 * - fixed inset-0 z-0, aria-hidden, pointer-events:none — DOM owns ALL interaction
 * - mounts through the tier gate (`tiers → mountGate → dynamic import('./three/Scene')`)
 * - falls back to a theme-aware static poster on tier `none` or any WebGL failure
 * - never renders on its own without a `theme`
 */
export const ImmersiveStage: React.FC<ImmersiveStageProps> = ({ theme }) => {
  const hostRef = useRef<HTMLDivElement | null>(null);
  const handleRef = useRef<SceneHandle | null>(null);

  const [tier] = useState<MountTier>(() => (typeof window === 'undefined' ? 'none' : getMountTier()));
  const [mode, setMode] = useState<StageMode>(tier === 'none' ? 'poster' : 'pending');

  // Scroll progress → camera (no React state: the callback talks to the scene directly).
  useScrollProgress({
    enabled: mode === 'scene',
    onProgress: (progress) => handleRef.current?.setProgress(progress),
  });

  // Mount gate: IO → idle → dynamic import; failure → poster.
  useEffect(() => {
    if (tier === 'none') return undefined;
    const host = hostRef.current;
    if (!host) return undefined;

    const dispose = mountStage({
      container: host,
      theme,
      onReady: (handle) => {
        handleRef.current = handle;
        setMode('scene');
      },
      onFallback: (reason) => {
        if (import.meta.env.DEV) {
          // Visible during development only — production falls back silently.
          console.info(`[ImmersiveStage] falling back to poster: ${reason}`);
        }
        handleRef.current = null;
        setMode('poster');
      },
    });

    return () => {
      dispose();
      handleRef.current = null;
    };
    // `theme` intentionally excluded: it is propagated via the effect below.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tier]);

  // Theme changes rebuild lighting/background without re-booting the scene.
  useEffect(() => {
    handleRef.current?.setTheme(theme);
  }, [theme]);

  // Pause the render loop while the stage itself is off-screen.
  useEffect(() => {
    if (mode !== 'scene') return undefined;
    if (typeof IntersectionObserver !== 'function') return undefined;
    const host = hostRef.current;
    if (!host) return undefined;

    const observer = new IntersectionObserver(
      ([entry]) => handleRef.current?.setVisible(entry?.isIntersecting ?? true),
      { threshold: 0 }
    );
    observer.observe(host);
    return () => observer.disconnect();
  }, [mode]);

  return (
    <div aria-hidden="true" className="pointer-events-none fixed inset-0 z-0">
      <div ref={hostRef} className="absolute inset-0" />
      {mode === 'poster' ? <div className="absolute inset-0" style={posterStyles(theme)} /> : null}
    </div>
  );
};

export default ImmersiveStage;
