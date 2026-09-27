import * as THREE from 'three';
import type { MountTier } from './tiers';
import {
  AGENT_CATEGORY_COLORS,
  BRAND,
  ensureContrast,
  themeBackground,
  themeGridColor,
  themeGridOpacity,
  type StageTheme,
} from './materials';
import { CameraRig } from './CameraRig';

export interface SceneOptions {
  theme: StageTheme;
  tier: Exclude<MountTier, 'none'>;
  /** Called if the WebGL context is lost after creation — mount gate falls back to the poster. */
  onContextLost?: () => void;
}

export interface SceneHandle {
  /** Normalized page scroll progress 0..1 (already rAF-lerped by the caller). */
  setProgress(progress: number): void;
  setTheme(theme: StageTheme): void;
  /** Pause/resume the render loop (off-screen or tab hidden). */
  setVisible(visible: boolean): void;
  dispose(): void;
}

const NODE_COUNT = 90; // 90-agent workforce
const GRID_REPEAT = 30; // one texture tile = 4 world units; line step = 1 world unit (4 × brand 4px base unit)
const GRID_WORLD_SIZE = 240;
const BEACON_POSITION = new THREE.Vector3(3.4, 0.8, -9.5);
const PROOF_BEAT = 0.76; // CAMERA_BEATS proof beat — beacon is brightest near this progress
const PROOF_WINDOW = 0.22;

/** Deterministic PRNG so the constellation is identical on every visit (no per-load CLS-like jitter). */
const mulberry32 = (seed: number): (() => number) => {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

/** White-line tile; the material color tints it per theme (so theme switch never rebuilds the canvas). */
const makeGridTexture = (): THREE.CanvasTexture => {
  const size = 64;
  const step = 16; // 4 × brand 4px base unit
  const canvas = document.createElement('canvas');
  canvas.width = size;
  canvas.height = size;
  const ctx = canvas.getContext('2d');
  if (ctx) {
    ctx.clearRect(0, 0, size, size);
    ctx.strokeStyle = BRAND.white;
    ctx.lineWidth = 1;
    ctx.beginPath();
    for (let p = 0; p < size; p += step) {
      ctx.moveTo(p + 0.5, 0);
      ctx.lineTo(p + 0.5, size);
      ctx.moveTo(0, p + 0.5);
      ctx.lineTo(size, p + 0.5);
    }
    ctx.stroke();
  }
  const texture = new THREE.CanvasTexture(canvas);
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(GRID_REPEAT, GRID_REPEAT);
  texture.colorSpace = THREE.SRGBColorSpace;
  texture.needsUpdate = true;
  return texture;
};

export function createScene(container: HTMLElement, options: SceneOptions): SceneHandle {
  const { theme: initialTheme, tier } = options;

  // Clear any existing canvas from a previous incomplete mount
  const existingCanvas = container.querySelector('canvas');
  if (existingCanvas) existingCanvas.remove();

  const renderer = new THREE.WebGLRenderer({
    antialias: tier === 'full',
    alpha: false,
    powerPreference: 'high-performance',
  });
  const maxDpr = tier === 'lite' ? 1.5 : 2;
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, maxDpr));

  const canvas = renderer.domElement;
  canvas.style.position = 'absolute';
  canvas.style.inset = '0';
  canvas.style.display = 'block';
  canvas.setAttribute('aria-hidden', 'true');
  container.appendChild(canvas);

  const scene = new THREE.Scene();
  let theme: StageTheme = initialTheme;
  let background = new THREE.Color(themeBackground(theme));
  scene.background = background;
  scene.fog = new THREE.FogExp2(background.clone(), 0.03);

  const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 160);
  const rig = new CameraRig(camera);

  // ── 4px brand grid plane ────────────────────────────────────────────────
  const gridTexture = makeGridTexture();
  const gridGeometry = new THREE.PlaneGeometry(GRID_WORLD_SIZE, GRID_WORLD_SIZE);
  const gridMaterial = new THREE.MeshBasicMaterial({
    map: gridTexture,
    transparent: true,
    depthWrite: false,
    toneMapped: false,
  });
  const grid = new THREE.Mesh(gridGeometry, gridMaterial);
  grid.rotation.x = -Math.PI / 2;
  grid.position.y = -3.2;
  scene.add(grid);

  // ── 90-node agent constellation (InstancedMesh) ────────────────────────
  const nodeGeometry = new THREE.SphereGeometry(0.14, tier === 'full' ? 12 : 8, tier === 'full' ? 12 : 8);
  const nodeMaterial = new THREE.MeshBasicMaterial({ toneMapped: false });
  const nodes = new THREE.InstancedMesh(nodeGeometry, nodeMaterial, NODE_COUNT);
  nodes.frustumCulled = false;
  nodes.instanceMatrix.setUsage(THREE.DynamicDrawUsage);

  const random = mulberry32(20260926);
  const basePositions = new Float32Array(NODE_COUNT * 3);
  const nodeScales = new Float32Array(NODE_COUNT);
  const nodePhases = new Float32Array(NODE_COUNT);
  for (let i = 0; i < NODE_COUNT; i += 1) {
    basePositions[i * 3] = (random() - 0.5) * 16;
    basePositions[i * 3 + 1] = 1.2 + (random() - 0.5) * 7;
    basePositions[i * 3 + 2] = -8 + (random() - 0.5) * 12;
    nodeScales[i] = 0.7 + random() * 0.8;
    nodePhases[i] = random() * Math.PI * 2;
  }
  scene.add(nodes);

  // ── Red proof beacon ───────────────────────────────────────────────────
  const beaconGeometry = new THREE.SphereGeometry(0.42, 16, 16);
  const beaconMaterial = new THREE.MeshBasicMaterial({
    transparent: true,
    opacity: 0.85,
    toneMapped: false,
  });
  const beacon = new THREE.Mesh(beaconGeometry, beaconMaterial);
  beacon.position.copy(BEACON_POSITION);

  const haloGeometry = new THREE.SphereGeometry(1.05, 16, 16);
  const haloMaterial = new THREE.MeshBasicMaterial({
    transparent: true,
    opacity: 0.1,
    depthWrite: false,
    toneMapped: false,
  });
  const halo = new THREE.Mesh(haloGeometry, haloMaterial);
  halo.position.copy(BEACON_POSITION);
  scene.add(beacon, halo);

  // ── Theme application ──────────────────────────────────────────────────
  const applyTheme = (next: StageTheme): void => {
    theme = next;
    background.set(themeBackground(theme));
    if (scene.fog) scene.fog.color.copy(background);
    gridMaterial.color.set(themeGridColor(theme));
    gridMaterial.opacity = themeGridOpacity(theme);
    const bgHex = themeBackground(theme);
    for (let i = 0; i < NODE_COUNT; i += 1) {
      const hue = AGENT_CATEGORY_COLORS[i % AGENT_CATEGORY_COLORS.length];
      nodes.setColorAt(i, new THREE.Color(ensureContrast(hue, bgHex)));
    }
    if (nodes.instanceColor) nodes.instanceColor.needsUpdate = true;
    beaconMaterial.color.set(BRAND.red);
  };
  applyTheme(initialTheme);

  // ── Sizing / resize ────────────────────────────────────────────────────
  let resizeObserver: ResizeObserver | null = null;
  const resize = (): void => {
    const width = container.clientWidth || window.innerWidth;
    const height = container.clientHeight || window.innerHeight;
    renderer.setSize(width, height, true);
    camera.aspect = width / Math.max(1, height);
    camera.updateProjectionMatrix();
  };
  resize();
  if (typeof ResizeObserver !== 'undefined') {
    resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(container);
  } else {
    window.addEventListener('resize', resize);
  }

  // ── Render loop (pauses on hidden tab / off-screen) ────────────────────
  const dummy = new THREE.Object3D();
  let rafId = 0;
  let disposed = false;
  let sceneVisible = true;
  let progress = 0;
  const startedAt = performance.now();

  const renderFrame = (): void => {
    const elapsed = (performance.now() - startedAt) / 1000;

    rig.setProgress(progress);
    rig.update(elapsed);

    // Constellation drift (slow vertical float, deterministic phase per node)
    for (let i = 0; i < NODE_COUNT; i += 1) {
      dummy.position.set(
        basePositions[i * 3],
        basePositions[i * 3 + 1] + Math.sin(elapsed * 0.7 + nodePhases[i]) * 0.14,
        basePositions[i * 3 + 2]
      );
      dummy.scale.setScalar(nodeScales[i]);
      dummy.updateMatrix();
      nodes.setMatrixAt(i, dummy.matrix);
    }
    nodes.instanceMatrix.needsUpdate = true;

    // Beacon pulses hardest at the proof beat
    const proofFocus = Math.max(0, 1 - Math.abs(progress - PROOF_BEAT) / PROOF_WINDOW);
    const pulse = 1 + Math.sin(elapsed * 2.2) * 0.1;
    beacon.scale.setScalar(pulse);
    halo.scale.setScalar(pulse * (1 + proofFocus * 0.35));
    haloMaterial.opacity = 0.06 + 0.12 * proofFocus;
    beaconMaterial.opacity = 0.55 + 0.4 * proofFocus;

    renderer.render(scene, camera);
  };

  const stopLoop = (): void => {
    if (rafId !== 0) {
      cancelAnimationFrame(rafId);
      rafId = 0;
    }
  };

  const startLoop = (): void => {
    if (disposed || rafId !== 0 || !sceneVisible || document.hidden) return;
    const tick = (): void => {
      rafId = requestAnimationFrame(tick);
      renderFrame();
    };
    rafId = requestAnimationFrame(tick);
  };

  const onVisibilityChange = (): void => {
    if (document.hidden) stopLoop();
    else startLoop();
  };
  document.addEventListener('visibilitychange', onVisibilityChange);

  const onContextLost = (event: Event): void => {
    event.preventDefault(); // allow the browser to release the lost context
    stopLoop();
    options.onContextLost?.();
  };
  canvas.addEventListener('webglcontextlost', onContextLost);

  startLoop();

  return {
    setProgress(value: number): void {
      progress = value < 0 ? 0 : value > 1 ? 1 : value;
    },
    setTheme(next: StageTheme): void {
      if (next !== theme) applyTheme(next);
    },
    setVisible(visible: boolean): void {
      sceneVisible = visible;
      if (visible) startLoop();
      else stopLoop();
    },
    dispose(): void {
      if (disposed) return;
      disposed = true;
      stopLoop();
      document.removeEventListener('visibilitychange', onVisibilityChange);
      canvas.removeEventListener('webglcontextlost', onContextLost);
      resizeObserver?.disconnect();
      window.removeEventListener('resize', resize);

      gridGeometry.dispose();
      gridMaterial.dispose();
      gridTexture.dispose();
      nodeGeometry.dispose();
      nodeMaterial.dispose();
      nodes.dispose();
      beaconGeometry.dispose();
      beaconMaterial.dispose();
      haloGeometry.dispose();
      haloMaterial.dispose();

      renderer.dispose();
      try {
        renderer.forceContextLoss();
      } catch {
        // context already gone — nothing to release
      }
      canvas.parentElement?.removeChild(canvas);
    },
  };
}
