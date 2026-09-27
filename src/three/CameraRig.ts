import * as THREE from 'three';

export type Vec3 = readonly [number, number, number];

/**
 * Authored camera beats (research doc §7 + plan.md). One continuous,
 * deterministic path — no free orbit, no scroll hijack: scroll progress 0..1
 * selects a point on this path and the camera *damps toward it*, so fast
 * scrolling stays readable and native scrolling is never intercepted.
 */
export interface CameraBeat {
  /** Scroll progress at which the camera should be at this beat (ascending, 0..1). */
  at: number;
  position: Vec3;
  look: Vec3;
}

export const CAMERA_BEATS: readonly CameraBeat[] = [
  { at: 0.0, position: [0, 2.4, 13.5], look: [0, 1.2, -2] }, // hero drift
  { at: 0.26, position: [3.2, 1.7, 8.0], look: [-0.5, 1.0, -6] }, // builder spotlight (slow dolly, hero moment)
  { at: 0.52, position: [0, 5.5, 8.5], look: [0, 1.0, -8] }, // cyan constellation overview
  { at: 0.76, position: [-3.6, 1.6, 4.5], look: [3.4, 0.8, -9.5] }, // red beacon at proof
  { at: 1.0, position: [0, 1.5, 2.0], look: [0, 1.4, -14] }, // resolve toward CTA
];

const clamp01 = (value: number): number => (value < 0 ? 0 : value > 1 ? 1 : value);

const smoothstep = (t: number): number => t * t * (3 - 2 * t);

const lerp3 = (a: Vec3, b: Vec3, t: number): [number, number, number] => [
  a[0] + (b[0] - a[0]) * t,
  a[1] + (b[1] - a[1]) * t,
  a[2] + (b[2] - a[2]) * t,
];

export interface SampledBeat {
  position: [number, number, number];
  look: [number, number, number];
}

/** Pure interpolation over CAMERA_BEATS at `progress` (0..1), eased per segment. */
export const sampleBeats = (progress: number): SampledBeat => {
  const p = clamp01(progress);
  const beats = CAMERA_BEATS;
  if (p <= beats[0].at) {
    return { position: [...beats[0].position], look: [...beats[0].look] };
  }
  for (let i = 0; i < beats.length - 1; i += 1) {
    const a = beats[i];
    const b = beats[i + 1];
    if (p <= b.at) {
      const span = b.at - a.at;
      const t = span <= 0 ? 1 : smoothstep((p - a.at) / span);
      return { position: lerp3(a.position, b.position, t), look: lerp3(a.look, b.look, t) };
    }
  }
  const last = beats[beats.length - 1];
  return { position: [...last.position], look: [...last.look] };
};

// Per-frame scratch vectors (no allocation in the render loop).
const SCRATCH_POS = new THREE.Vector3();
const SCRATCH_LOOK = new THREE.Vector3();

/**
 * Damps the camera toward the sampled beat. Scroll progress itself is
 * already rAF-lerped by `useScrollProgress`; this second damp (≈0.12/frame)
 * keeps motion cinematic when progress jumps (fast scroll, anchor link).
 */
export class CameraRig {
  private readonly lookTarget = new THREE.Vector3();

  private progress = 0;

  constructor(
    private readonly camera: THREE.PerspectiveCamera,
    private readonly lerpFactor = 0.12
  ) {
    const start = sampleBeats(0);
    camera.position.set(...start.position);
    this.lookTarget.set(...start.look);
    camera.lookAt(this.lookTarget);
  }

  setProgress(progress: number): void {
    this.progress = clamp01(progress);
  }

  getProgress(): number {
    return this.progress;
  }

  /** `elapsed` is seconds since scene start (used for the hero idle drift). */
  update(elapsed: number): void {
    const { position, look } = sampleBeats(this.progress);

    // Gentle hero drift — fades out by progress 0.18, disabled under reduced motion (tier gate handles that).
    const drift = Math.max(0, 1 - this.progress / 0.18);
    if (drift > 0) {
      position[0] += Math.sin(elapsed * 0.35) * 0.5 * drift;
      position[1] += Math.sin(elapsed * 0.5) * 0.25 * drift;
    }

    this.camera.position.lerp(SCRATCH_POS.set(position[0], position[1], position[2]), this.lerpFactor);
    this.lookTarget.lerp(SCRATCH_LOOK.set(look[0], look[1], look[2]), this.lerpFactor);
    this.camera.lookAt(this.lookTarget);
  }
}
