import { describe, expect, it } from 'vitest';
import { CAMERA_BEATS, sampleBeats } from './CameraRig';

const closeToVec = (actual: readonly number[], expected: readonly number[]) => {
  expect(actual).toHaveLength(3);
  expect(actual[0]).toBeCloseTo(expected[0], 5);
  expect(actual[1]).toBeCloseTo(expected[1], 5);
  expect(actual[2]).toBeCloseTo(expected[2], 5);
};

describe('sampleBeats', () => {
  it('pins progress 0 to the hero beat', () => {
    const s = sampleBeats(0);
    closeToVec(s.position, CAMERA_BEATS[0].position);
    closeToVec(s.look, CAMERA_BEATS[0].look);
  });

  it('clamps negative progress to the hero beat', () => {
    closeToVec(sampleBeats(-5).position, CAMERA_BEATS[0].position);
  });

  it('clamps progress > 1 to the CTA beat', () => {
    const s = sampleBeats(3);
    const last = CAMERA_BEATS[CAMERA_BEATS.length - 1];
    closeToVec(s.position, last.position);
    closeToVec(s.look, last.look);
  });

  it('hits every intermediate beat exactly at its progress value', () => {
    for (const beat of CAMERA_BEATS) {
      const s = sampleBeats(beat.at);
      closeToVec(s.position, beat.position);
      closeToVec(s.look, beat.look);
    }
  });

  it('interpolates monotonically between adjacent beats', () => {
    const a = CAMERA_BEATS[1];
    const b = CAMERA_BEATS[2];
    const mid = sampleBeats((a.at + b.at) / 2).position;
    // midpoint must sit strictly between the two beats on the x axis
    const minX = Math.min(a.position[0], b.position[0]);
    const maxX = Math.max(a.position[0], b.position[0]);
    expect(mid[0]).toBeGreaterThanOrEqual(minX);
    expect(mid[0]).toBeLessThanOrEqual(maxX);
  });

  it('aims the proof beat at the red beacon', () => {
    const proof = CAMERA_BEATS.find((beat) => beat.at === 0.76);
    expect(proof).toBeDefined();
    closeToVec(proof!.look, [3.4, 0.8, -9.5]);
  });
});
