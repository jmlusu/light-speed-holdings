import React, { useEffect, useRef, useState, useId } from 'react';
import * as THREE from 'three';
import {
  TactileRockerSwitch,
  TactileRotaryKnob,
  AcousticVentGrille,
  StatusLedPip,
  MachineScrewHead
} from './TactileHardwareElements';
import {
  Activity,
  ShieldCheck,
  Zap,
  RefreshCw,
  Compass,
  Layers,
  Lock,
  Radio,
  Maximize2
} from 'lucide-react';

interface ActiveEngineCoreProps {
  theme?: 'light' | 'dark';
  className?: string;
  onInspectSystem?: () => void;
}

export const ActiveEngineCore: React.FC<ActiveEngineCoreProps> = ({
  theme = 'dark',
  className = '',
  onInspectSystem,
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const isLight = theme === 'light';

  // Hardware State Controls
  const [hyperFlux, setHyperFlux] = useState<boolean>(false);
  const [swarmFrequency, setSwarmFrequency] = useState<number>(68); // 0 to 100
  const [orbitLock, setOrbitLock] = useState<boolean>(false);
  const [telemetryBurst, setTelemetryBurst] = useState<boolean>(false);
  const [activeNodesCount, setActiveNodesCount] = useState<number>(1420);
  const [latencyMs, setLatencyMs] = useState<number>(14);

  // References for Three.js objects
  const sceneRef = useRef<THREE.Scene | null>(null);
  const particlesRef = useRef<THREE.Points | null>(null);
  const coreMeshRef = useRef<THREE.Mesh | null>(null);
  const ringGroupRef = useRef<THREE.Group | null>(null);
  const burstTimeRef = useRef<number>(0);
  const mousePosRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const isDraggingRef = useRef<boolean>(false);
  const dragStartRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });
  const rotationOffsetRef = useRef<{ x: number; y: number }>({ x: 0, y: 0 });

  // Fluctuate telemetry readouts realistically
  useEffect(() => {
    const interval = setInterval(() => {
      setLatencyMs(prev => Math.max(11, Math.min(22, prev + (Math.random() > 0.5 ? 1 : -1))));
      setActiveNodesCount(prev => Math.max(1400, Math.min(1450, prev + (Math.random() > 0.5 ? 2 : -2))));
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    // Dimensions
    const width = container.clientWidth || 600;
    const height = container.clientHeight || 420;

    // Scene & Camera
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    const camera = new THREE.PerspectiveCamera(45, width / height, 1, 1000);
    camera.position.set(0, 0, 320);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // Group for entire interactive core
    const coreMasterGroup = new THREE.Group();
    scene.add(coreMasterGroup);

    // Scene Lighting
    const ambientLight = new THREE.AmbientLight(0xffffff, isLight ? 1.4 : 1.0);
    scene.add(ambientLight);

    const corePointLight = new THREE.PointLight(isLight ? 0xc1121f : 0xe63946, isLight ? 2.2 : 3.0, 450);
    corePointLight.position.set(0, 0, 80);
    scene.add(corePointLight);

    // 1. Central Sovereign Engine Nucleus (Large 3D Transparent Volumetric Company Icon Logo)
    const logoGroup = new THREE.Group();
    coreMasterGroup.add(logoGroup);
    coreMeshRef.current = logoGroup as unknown as THREE.Mesh;

    const textureLoader = new THREE.TextureLoader();
    const logoTexture = textureLoader.load(
      '/static/brand/logos/icononly/icononly_transparent_nobuffer.png',
      () => {
        renderer.render(scene, camera);
      },
      undefined,
      () => {
        // Fallback paths
        textureLoader.load('/brand/logos/icononly/icononly_transparent_nobuffer.png', (fallbackTex) => {
          logoMatFront.map = fallbackTex;
          logoMatBack.map = fallbackTex;
          logoMatMid.map = fallbackTex;
          logoMatFront.needsUpdate = true;
          logoMatBack.needsUpdate = true;
          logoMatMid.needsUpdate = true;
        });
      }
    );
    logoTexture.colorSpace = THREE.SRGBColorSpace;
    logoTexture.minFilter = THREE.LinearFilter;
    logoTexture.magFilter = THREE.LinearFilter;

    // Aspect ratio: 1280 x 1667 (~0.7678). Sized tall and bold to command the central core
    const logoHeight = 175;
    const logoWidth = logoHeight * (1280 / 1667); // ~134.4
    const logoDepth = 18;

    // Front Face Material & Mesh (Transparent Holographic)
    const logoMatFront = new THREE.MeshBasicMaterial({
      map: logoTexture,
      transparent: true,
      opacity: 0.9,
      depthWrite: false,
      side: THREE.FrontSide,
    });
    const frontGeo = new THREE.PlaneGeometry(logoWidth, logoHeight);
    const frontPlane = new THREE.Mesh(frontGeo, logoMatFront);
    frontPlane.position.z = logoDepth / 2;
    logoGroup.add(frontPlane);

    // Mid-plane translucent volumetric slice for 3D holographic depth
    const logoMatMid = new THREE.MeshBasicMaterial({
      map: logoTexture,
      transparent: true,
      opacity: 0.45,
      depthWrite: false,
      side: THREE.DoubleSide,
    });
    const midPlane = new THREE.Mesh(frontGeo.clone(), logoMatMid);
    midPlane.position.z = 0;
    logoGroup.add(midPlane);

    // Back Face Material & Mesh (with horizontally inverted UVs so icon is never mirrored backwards)
    const logoMatBack = new THREE.MeshBasicMaterial({
      map: logoTexture,
      transparent: true,
      opacity: 0.9,
      depthWrite: false,
      side: THREE.FrontSide,
    });
    const backGeo = new THREE.PlaneGeometry(logoWidth, logoHeight);
    const uvs = backGeo.attributes.uv;
    for (let i = 0; i < uvs.count; i++) {
      uvs.setX(i, 1 - uvs.getX(i));
    }
    uvs.needsUpdate = true;
    const backPlane = new THREE.Mesh(backGeo, logoMatBack);
    backPlane.rotation.y = Math.PI;
    backPlane.position.z = -logoDepth / 2;
    logoGroup.add(backPlane);

    // 3D Transparent Hologram Crystal Chassis & Edge Chamfer Frame
    const boxGeo = new THREE.BoxGeometry(logoWidth + 14, logoHeight + 14, logoDepth + 4);
    const boxMat = new THREE.MeshBasicMaterial({
      color: isLight ? 0xe63946 : 0xc1121f,
      transparent: true,
      opacity: 0.06,
      depthWrite: false,
      side: THREE.DoubleSide,
    });
    const boxMesh = new THREE.Mesh(boxGeo, boxMat);
    logoGroup.add(boxMesh);

    // Luminous 3D Edge Wireframe Lines
    const edgesGeo = new THREE.EdgesGeometry(boxGeo);
    const edgesMat = new THREE.LineBasicMaterial({
      color: isLight ? 0xc1121f : 0xe63946,
      transparent: true,
      opacity: 0.45,
      linewidth: 1.5,
    });
    const edgesMesh = new THREE.LineSegments(edgesGeo, edgesMat);
    logoGroup.add(edgesMesh);

    // 4 Corner Machined 3D Titanium Brackets
    const bracketGeo = new THREE.CylinderGeometry(2.5, 2.5, logoDepth + 6, 12);
    const bracketMat = new THREE.MeshBasicMaterial({
      color: isLight ? 0x64748b : 0xa1a1aa,
      transparent: true,
      opacity: 0.8,
    });
    const halfW = (logoWidth + 14) / 2;
    const halfH = (logoHeight + 14) / 2;
    [
      [-halfW, -halfH],
      [halfW, -halfH],
      [-halfW, halfH],
      [halfW, halfH],
    ].forEach(([cx, cy]) => {
      const bMesh = new THREE.Mesh(bracketGeo, bracketMat);
      bMesh.position.set(cx, cy, 0);
      logoGroup.add(bMesh);
    });

    // Triple Ambient Luminous Kinetic Orbital Halo Rings surrounding the enlarged 3D nucleus
    const haloGroup = new THREE.Group();
    logoGroup.add(haloGroup);

    const nucleusRingGeo1 = new THREE.TorusGeometry(116, 1.6, 16, 64);
    const nucleusRingMat1 = new THREE.MeshBasicMaterial({
      color: isLight ? 0xc1121f : 0xe63946,
      transparent: true,
      opacity: 0.6,
      wireframe: true,
    });
    const nucleusRingMesh1 = new THREE.Mesh(nucleusRingGeo1, nucleusRingMat1);
    nucleusRingMesh1.rotation.x = Math.PI / 3;
    haloGroup.add(nucleusRingMesh1);

    const nucleusRingGeo2 = new THREE.TorusGeometry(128, 1.4, 16, 64);
    const nucleusRingMat2 = new THREE.MeshBasicMaterial({
      color: isLight ? 0x059669 : 0x10b981,
      transparent: true,
      opacity: 0.5,
      wireframe: true,
    });
    const nucleusRingMesh2 = new THREE.Mesh(nucleusRingGeo2, nucleusRingMat2);
    nucleusRingMesh2.rotation.y = Math.PI / 4;
    nucleusRingMesh2.rotation.x = -Math.PI / 6;
    haloGroup.add(nucleusRingMesh2);

    const nucleusRingGeo3 = new THREE.TorusGeometry(140, 1.2, 16, 64);
    const nucleusRingMat3 = new THREE.MeshBasicMaterial({
      color: isLight ? 0x0284c7 : 0x38bdf8,
      transparent: true,
      opacity: 0.4,
      wireframe: true,
    });
    const nucleusRingMesh3 = new THREE.Mesh(nucleusRingGeo3, nucleusRingMat3);
    nucleusRingMesh3.rotation.x = Math.PI / 2;
    haloGroup.add(nucleusRingMesh3);

    // 2. Concentric Orbital Telemetry Rings (Expanded around enlarged logo)
    const ringGroup = new THREE.Group();
    coreMasterGroup.add(ringGroup);
    ringGroupRef.current = ringGroup;

    const ringRadiusList = [155, 205, 260];
    ringRadiusList.forEach((rad, idx) => {
      const ringGeo = new THREE.BufferGeometry();
      const segments = 64;
      const positions = new Float32Array(segments * 3);
      for (let i = 0; i < segments; i++) {
        const theta = (i / segments) * Math.PI * 2;
        positions[i * 3] = Math.cos(theta) * rad;
        positions[i * 3 + 1] = Math.sin(theta) * rad;
        positions[i * 3 + 2] = 0;
      }
      ringGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));

      const ringMat = new THREE.LineBasicMaterial({
        color: idx === 1 ? (isLight ? 0xe63946 : 0xf5838f) : (isLight ? 0x94a3b8 : 0x52525b),
        transparent: true,
        opacity: idx === 1 ? 0.75 : 0.4,
      });
      const ringLine = new THREE.LineLoop(ringGeo, ringMat);
      ringLine.rotation.x = idx * 0.4 + 0.2;
      ringLine.rotation.y = idx * 0.5;
      ringGroup.add(ringLine);
    });

    // 3. Multi-Agent Autonomous Particle Swarm (Orbiting outside the enlarged core)
    const particleCount = 750;
    const particleGeometry = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const initialRadii = new Float32Array(particleCount);
    const particleSpeeds = new Float32Array(particleCount);
    const particleAngles = new Float32Array(particleCount);
    const particleColors = new Float32Array(particleCount * 3);

    const amberColor = new THREE.Color(isLight ? 0xc1121f : 0xe63946);
    const emeraldColor = new THREE.Color(isLight ? 0x059669 : 0x10b981);
    const slateColor = new THREE.Color(isLight ? 0x64748b : 0x71717a);

    for (let i = 0; i < particleCount; i++) {
      const r = 135 + Math.random() * 140;
      const theta = Math.random() * Math.PI * 2;
      const phi = (Math.random() - 0.5) * Math.PI;

      particlePositions[i * 3] = r * Math.cos(theta) * Math.cos(phi);
      particlePositions[i * 3 + 1] = r * Math.sin(theta) * Math.cos(phi);
      particlePositions[i * 3 + 2] = r * Math.sin(phi);

      initialRadii[i] = r;
      particleSpeeds[i] = 0.005 + Math.random() * 0.012;
      particleAngles[i] = theta;

      // Color distribution: 50% Slate / 30% Amber / 20% Emerald
      const randType = Math.random();
      const chosenColor = randType > 0.5 ? slateColor : (randType > 0.2 ? amberColor : emeraldColor);
      particleColors[i * 3] = chosenColor.r;
      particleColors[i * 3 + 1] = chosenColor.g;
      particleColors[i * 3 + 2] = chosenColor.b;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeometry.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

    const particleMaterial = new THREE.PointsMaterial({
      size: 3.2,
      vertexColors: true,
      transparent: true,
      opacity: 0.85,
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    coreMasterGroup.add(particles);
    particlesRef.current = particles;

    // Drag-to-Rotate handlers
    const handleMouseDown = (e: MouseEvent) => {
      isDraggingRef.current = true;
      dragStartRef.current = { x: e.clientX, y: e.clientY };
    };

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      mousePosRef.current = {
        x: ((e.clientX - rect.left) / rect.width) * 2 - 1,
        y: -(((e.clientY - rect.top) / rect.height) * 2 - 1),
      };

      if (isDraggingRef.current) {
        const dx = e.clientX - dragStartRef.current.x;
        const dy = e.clientY - dragStartRef.current.y;
        rotationOffsetRef.current.y += dx * 0.008;
        rotationOffsetRef.current.x += dy * 0.008;
        dragStartRef.current = { x: e.clientX, y: e.clientY };
      }
    };

    const handleMouseUp = () => {
      isDraggingRef.current = false;
    };

    container.addEventListener('mousedown', handleMouseDown);
    window.addEventListener('mousemove', handleMouseMove);
    window.addEventListener('mouseup', handleMouseUp);

    // Resize Handler with ResizeObserver
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      if (w > 0 && h > 0) {
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      }
    };
    window.addEventListener('resize', handleResize);

    const resizeObserver = new ResizeObserver(() => {
      handleResize();
    });
    resizeObserver.observe(container);

    // Animation Loop
    let animationId: number;
    let clock = new THREE.Clock();

    const renderLoop = () => {
      animationId = requestAnimationFrame(renderLoop);
      const elapsed = clock.getElapsedTime();

      // Velocity scaling from Hardware controls
      const speedMultiplier = (hyperFlux ? 2.8 : 1.0) * (swarmFrequency / 60);

      // Graceful floating & rotation of the enlarged brand nucleus
      if (!orbitLock) {
        // Continuous smooth yaw rotation
        logoGroup.rotation.y += 0.005 * speedMultiplier;

        // Harmonic floating levitation & subtle banking tilt
        logoGroup.position.y = Math.sin(elapsed * 1.4) * 4.5;
        logoGroup.rotation.z = Math.sin(elapsed * 0.9) * 0.04;

        // Kinetic halo rings counter-precession
        nucleusRingMesh1.rotation.z += 0.008 * speedMultiplier;
        nucleusRingMesh2.rotation.z -= 0.006 * speedMultiplier;
        nucleusRingMesh3.rotation.z += 0.005 * speedMultiplier;

        // Outer orbital telemetry rings rotation
        ringGroup.rotation.z += 0.0025 * speedMultiplier;
        ringGroup.rotation.x += 0.0015 * speedMultiplier;
      }

      // Gyro gimbal orientation from mouse & drag
      coreMasterGroup.rotation.x = rotationOffsetRef.current.x + mousePosRef.current.y * 0.25;
      coreMasterGroup.rotation.y = rotationOffsetRef.current.y + mousePosRef.current.x * 0.35;

      // Particle pulse & orbital flow
      const posAttr = particleGeometry.attributes.position;
      for (let i = 0; i < particleCount; i++) {
        particleAngles[i] += particleSpeeds[i] * speedMultiplier;
        const baseR = initialRadii[i] * (0.8 + (swarmFrequency / 100) * 0.4);

        // Burst wave effect
        let burstOffset = 0;
        if (burstTimeRef.current > 0) {
          const dt = elapsed - burstTimeRef.current;
          if (dt < 1.5) {
            burstOffset = Math.sin(dt * Math.PI) * 45;
          }
        }

        const currentR = baseR + burstOffset + Math.sin(elapsed * 2 + i) * 3;
        const theta = particleAngles[i];
        const y = posAttr.getY(i);
        const phi = Math.asin(Math.max(-1, Math.min(1, y / (currentR || 1))));

        posAttr.setX(i, currentR * Math.cos(theta) * Math.cos(phi));
        posAttr.setZ(i, currentR * Math.sin(theta) * Math.cos(phi));
      }
      posAttr.needsUpdate = true;

      renderer.render(scene, camera);
    };

    renderLoop();

    return () => {
      cancelAnimationFrame(animationId);
      container.removeEventListener('mousedown', handleMouseDown);
      window.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('mouseup', handleMouseUp);
      window.removeEventListener('resize', handleResize);
      resizeObserver.disconnect();
      renderer.dispose();
    };
  }, [theme, hyperFlux, swarmFrequency, orbitLock]);

  // Handle Trigger Burst
  const handleTriggerBurst = () => {
    burstTimeRef.current = performance.now() / 1000;
    setTelemetryBurst(true);
    setTimeout(() => setTelemetryBurst(false), 1400);
  };

  // Reset Orientation
  const handleResetOrientation = () => {
    rotationOffsetRef.current = { x: 0, y: 0 };
  };

  return (
    <div className={`rounded-3xl border relative overflow-hidden transition-all duration-300 select-none ${
      isLight ? 'chassis-milled-light text-slate-900' : 'chassis-milled-dark text-zinc-100'
    } ${className}`}>

      {/* 4 Corner Machine Screws */}
      <MachineScrewHead isLight={isLight} className="absolute top-4 left-4 z-20" />
      <MachineScrewHead isLight={isLight} className="absolute top-4 right-4 z-20" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-4 left-4 z-20" />
      <MachineScrewHead isLight={isLight} className="absolute bottom-4 right-4 z-20" />

      {/* Flight-Deck Command Console Header */}
      <div className={`px-6 py-4 border-b flex flex-wrap items-center justify-between gap-4 relative z-10 ${
        isLight ? 'border-slate-200/90 bg-slate-100/60' : 'border-zinc-800/90 bg-zinc-900/60'
      }`}>
        <div className="flex items-center gap-3">
          <StatusLedPip
            status={telemetryBurst ? 'amber' : 'emerald'}
            label={telemetryBurst ? 'FLUX BURST ACTIVE' : 'ENGINE CORE: OPERATIONAL'}
            isLight={isLight}
          />
          <div className="hidden sm:flex items-center gap-2">
            <span className="text-zinc-500 font-mono text-[10px]">•</span>
            <span className="text-[10px] font-mono tracking-wider text-amber-500 font-bold uppercase">
              Sovereign Node Core // Lilongwe HQ
            </span>
          </div>
        </div>

        {/* Telemetry Coordinate Badges */}
        <div className="flex items-center gap-2">
          <span className={`px-2.5 py-1 rounded text-[9px] font-mono tracking-wider font-semibold uppercase ${
            isLight ? 'telemetry-tag-light' : 'telemetry-tag-dark'
          }`}>
            SYS::COORD // 13.9899° S, 33.7741° E
          </span>
          <AcousticVentGrille cols={6} rows={2} isLight={isLight} />
        </div>
      </div>

      {/* Main 3D Canvas Viewport + Overlay HUD Diagnostics */}
      <div className="relative w-full h-[360px] sm:h-[420px] overflow-hidden cursor-grab active:cursor-grabbing">

        {/* Three.js Canvas Container */}
        <div ref={mountRef} className="w-full h-full" />

        {/* Tactical Crosshair / Coordinate Overlay */}
        <div className="absolute inset-0 pointer-events-none flex items-center justify-center opacity-25">
          <div className={`w-48 h-48 rounded-full border border-dashed ${isLight ? 'border-slate-700' : 'border-zinc-400'}`} />
          <div className={`absolute w-full h-[1px] ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`} />
          <div className={`absolute h-full w-[1px] ${isLight ? 'bg-slate-300' : 'bg-zinc-800'}`} />
        </div>

        {/* Top-Left Telemetry Readout */}
        <div className="absolute top-4 left-6 pointer-events-none z-10 space-y-1 text-left">
          <div className="text-[10px] font-mono font-bold text-amber-500 tracking-wider">
            [ SOVEREIGN ENGINE MATRIX ]
          </div>
          <div className={`text-xs font-mono font-bold ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>
            ACTIVE SWARM: <span className="text-emerald-500">{activeNodesCount} NODES</span>
          </div>
          <div className="text-[10px] font-mono text-zinc-400">
            LATENCY: <span className="text-amber-500 font-bold">{latencyMs}ms</span> (SADC FIBRE)
          </div>
        </div>

        {/* Top-Right Telemetry Readout */}
        <div className="absolute top-4 right-6 pointer-events-none z-10 text-right space-y-1">
          <div className="text-[10px] font-mono font-bold text-emerald-500 tracking-wider">
            HITL GOVERNANCE: 100%
          </div>
          <div className={`text-[11px] font-mono ${isLight ? 'text-slate-700' : 'text-zinc-300'}`}>
            GATE: <span className="font-bold text-amber-500">TIER-5 DUAL SIGN-OFF</span>
          </div>
          <div className="text-[10px] font-mono text-zinc-500">
            CHANNEL: MW-LLW-01 // AIRTEL-TNM
          </div>
        </div>

        {/* Center Prompt Helper (Draggable Cue) */}
        <div className="absolute bottom-3 left-6 pointer-events-none z-10 flex items-center gap-2">
          <span className={`text-[9px] font-mono px-2 py-0.5 rounded uppercase tracking-wider ${
            isLight ? 'bg-slate-200/80 text-slate-700' : 'bg-zinc-900/80 text-zinc-400 border border-zinc-800'
          }`}>
            INTERACTIVE: DRAG TO ROTATE ENGINE CORE • HOVER TO ORIENT
          </span>
        </div>

      </div>

      {/* Physical Hardware Instrumentation Deck */}
      <div className={`p-5 sm:p-6 border-t relative z-10 transition-colors ${
        isLight ? 'border-slate-200 bg-slate-50' : 'border-zinc-800/90 bg-[#0c0d10]'
      }`}>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 items-center">

          {/* Hardware Control 1: Physical Rocker Switch for Hyper Flux */}
          <div className={`p-4 rounded-xl border flex items-center justify-between gap-4 ${
            isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
          }`}>
            <div className="text-left">
              <span className="text-[9px] font-mono uppercase font-bold text-zinc-500 block tracking-widest">
                CORE FLUX
              </span>
              <span className={`text-xs font-mono font-bold ${hyperFlux ? 'text-orange-500' : (isLight ? 'text-slate-800' : 'text-zinc-200')}`}>
                {hyperFlux ? 'HYPER FLUX [2.8X]' : 'NOMINAL [1.0X]'}
              </span>
            </div>
            <TactileRockerSwitch
              isOn={hyperFlux}
              onToggle={() => setHyperFlux(prev => !prev)}
              labelLeft="NORM"
              labelRight="HYPR"
              size="sm"
              isLight={isLight}
            />
          </div>

          {/* Hardware Control 2: Precision Rotary Dial for Swarm Frequency */}
          <div className={`p-4 rounded-xl border flex items-center justify-between gap-4 ${
            isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
          }`}>
            <div className="text-left">
              <span className="text-[9px] font-mono uppercase font-bold text-zinc-500 block tracking-widest">
                SWARM DENSITY
              </span>
              <span className={`text-xs font-mono font-bold ${isLight ? 'text-slate-800' : 'text-zinc-200'}`}>
                {swarmFrequency}% <span className="text-[10px] text-zinc-500">HARMONIC</span>
              </span>
            </div>
            <TactileRotaryKnob
              value={swarmFrequency}
              onChange={(val) => setSwarmFrequency(val)}
              size={52}
              isLight={isLight}
            />
          </div>

          {/* Hardware Control 3: Tactile Push Buttons (Burst & Lock) */}
          <div className={`p-3.5 rounded-xl border flex items-center justify-between gap-2 ${
            isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
          }`}>
            <button
              onClick={handleTriggerBurst}
              className={`flex-1 py-2 px-2.5 rounded-lg text-[10px] font-mono font-bold tracking-wider uppercase transition-all flex items-center justify-center gap-1.5 ${
                telemetryBurst
                  ? 'bg-amber-500 text-slate-950 shadow-inner'
                  : isLight
                    ? 'tactile-btn-inactive-light text-slate-800 hover:text-amber-600'
                    : 'tactile-btn-inactive-dark text-zinc-200 hover:text-amber-400'
              }`}
            >
              <Zap className="w-3.5 h-3.5" />
              <span>BURST</span>
            </button>

            <button
              onClick={() => setOrbitLock(prev => !prev)}
              className={`flex-1 py-2 px-2.5 rounded-lg text-[10px] font-mono font-bold tracking-wider uppercase transition-all flex items-center justify-center gap-1.5 ${
                orbitLock
                  ? 'bg-emerald-500 text-slate-950 shadow-inner'
                  : isLight
                    ? 'tactile-btn-inactive-light text-slate-800 hover:text-emerald-600'
                    : 'tactile-btn-inactive-dark text-zinc-200 hover:text-emerald-400'
              }`}
            >
              <Lock className="w-3.5 h-3.5" />
              <span>{orbitLock ? 'LOCKED' : 'ORBIT'}</span>
            </button>
          </div>

          {/* Hardware Control 4: Gyro Reset & Inspect Action */}
          <div className={`p-3.5 rounded-xl border flex items-center justify-between gap-2 ${
            isLight ? 'flight-deck-well-light' : 'flight-deck-well-dark'
          }`}>
            <button
              onClick={handleResetOrientation}
              title="Reset Gimbal Gyro"
              className={`py-2 px-3 rounded-lg text-[10px] font-mono font-bold tracking-wider uppercase transition-all flex items-center justify-center gap-1.5 ${
                isLight ? 'tactile-btn-inactive-light text-slate-700' : 'tactile-btn-inactive-dark text-zinc-300'
              }`}
            >
              <Compass className="w-3.5 h-3.5 text-zinc-400" />
              <span>RESET</span>
            </button>

            {onInspectSystem && (
              <button
                onClick={onInspectSystem}
                className="flex-1 py-2 px-3 rounded-lg bg-amber-500 hover:bg-amber-400 text-slate-950 text-[10px] font-mono font-extrabold tracking-wider uppercase transition-all shadow-md shadow-amber-500/20 flex items-center justify-center gap-1"
              >
                <span>RUN SPECS</span>
                <Maximize2 className="w-3.5 h-3.5" />
              </button>
            )}
          </div>

        </div>
      </div>

    </div>
  );
};
