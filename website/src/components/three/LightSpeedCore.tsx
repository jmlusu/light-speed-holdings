"use client";

import { useRef, useEffect } from "react";
import { Canvas, useFrame } from "@react-three/fiber";
import * as THREE from "three";

const PARTICLE_COUNT = 3000;

function createParticleData() {
  const pos = new Float32Array(PARTICLE_COUNT * 3);
  const col = new Float32Array(PARTICLE_COUNT * 3);

  const c1 = new THREE.Color("#ffffff");
  const c2 = new THREE.Color("#52525b");

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    const radius = 3 + Math.random() * 5;
    const theta = Math.random() * Math.PI * 2;
    const phi = (Math.random() - 0.5) * Math.PI;

    pos[i * 3] = radius * Math.cos(theta) * Math.cos(phi);
    pos[i * 3 + 1] = radius * Math.sin(phi);
    pos[i * 3 + 2] = radius * Math.sin(theta) * Math.cos(phi);

    const color = Math.random() > 0.5 ? c1 : c2;
    col[i * 3] = color.r;
    col[i * 3 + 1] = color.g;
    col[i * 3 + 2] = color.b;
  }
  return { positions: pos, colors: col };
}

const PARTICLES = createParticleData();

function DynamicScrollCore() {
  const meshRef = useRef<THREE.Mesh>(null!);
  const particlesRef = useRef<THREE.Points>(null!);
  const scrollY = useRef(0);

  // Sync window scroll
  useEffect(() => {
    const handleScroll = () => {
      scrollY.current = window.scrollY;
    };
    window.addEventListener("scroll", handleScroll, { passive: true });
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

// Generate surrounding stone/dust particles (static data, built once at module scope)
  const { positions, colors } = PARTICLES;

  useFrame((state) => {
    const time = state.clock.getElapsedTime();
    const scrollFactor = scrollY.current * 0.002;

    // Cinematic rotation and scroll-driven displacement
    if (meshRef.current) {
      meshRef.current.rotation.y = time * 0.2 + scrollFactor * 1.5;
      meshRef.current.rotation.x = Math.sin(time * 0.1) * 0.2 + scrollFactor * 0.8;
      meshRef.current.position.y = -scrollFactor * 0.5;
      meshRef.current.scale.setScalar(1 + Math.sin(scrollFactor) * 0.2);
    }

    if (particlesRef.current) {
      particlesRef.current.rotation.y = -time * 0.05 + scrollFactor * 0.5;
    }

    // Scroll-driven camera movement
    state.camera.position.z = THREE.MathUtils.lerp(state.camera.position.z, 6 + scrollFactor * 2, 0.05);
    state.camera.position.y = THREE.MathUtils.lerp(state.camera.position.y, -scrollFactor * 1.2, 0.05);
    state.camera.lookAt(0, -scrollFactor * 0.5, 0);
  });

  return (
    <group>
      {/* Central Monolithic Organic Geometry */}
      <mesh ref={meshRef}>
        <icosahedronGeometry args={[1.6, 2]} />
        <meshStandardMaterial
          color="#18181b"
          roughness={0.2}
          metalness={0.9}
          flatShading
        />
      </mesh>

      {/* Orbiting Particle Dust */}
      <points ref={particlesRef}>
        <bufferGeometry>
          <bufferAttribute attach="attributes-position" args={[positions, 3]} />
          <bufferAttribute attach="attributes-color" args={[colors, 3]} />
        </bufferGeometry>
        <pointsMaterial size={0.025} vertexColors transparent opacity={0.6} sizeAttenuation />
      </points>
    </group>
  );
}

export default function LightSpeedCore() {
  return (
    <div className="fixed inset-0 w-full h-full -z-10 pointer-events-none">
      <Canvas camera={{ position: [0, 0, 6], fov: 45 }}>
        <color attach="background" args={["#09090b"]} />
        <ambientLight intensity={0.6} />
        <directionalLight position={[10, 10, 10]} intensity={3} color="#ffffff" />
        <pointLight position={[-10, -10, -5]} intensity={2} color="#71717a" />
        <DynamicScrollCore />
      </Canvas>
      {/* Background Dark Vignette */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_0%,rgba(9,9,11,0.85)_100%)]" />
    </div>
  );
}
