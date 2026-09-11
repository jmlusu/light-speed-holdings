import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';

interface ThreeCanvasProps {
  theme?: 'light' | 'dark';
}

export const ThreeCanvas: React.FC<ThreeCanvasProps> = ({ theme = 'dark' }) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768 || window.matchMedia('(pointer: coarse)').matches);
    };
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  useEffect(() => {
    if (isMobile) return;
    const container = mountRef.current;
    if (!container) return;

    const width = window.innerWidth;
    const height = window.innerHeight;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(theme === 'light' ? 0xE2E8F0 : 0x0F172A, 0.001);

    const camera = new THREE.PerspectiveCamera(60, width / height, 1, 2000);
    camera.position.z = 1000;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    const particleCount = 1200;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    const targetPositions = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      // Abstract Cloud (Initial state)
      positions[i * 3] = (Math.random() - 0.5) * 3000;
      positions[i * 3 + 1] = (Math.random() - 0.5) * 3000;
      positions[i * 3 + 2] = (Math.random() - 0.5) * 3000;

      // Ordered Grid (Target state)
      const gridSize = 10;
      const spacing = 150;
      const x = (i % gridSize) * spacing - (gridSize * spacing) / 2;
      const y = (Math.floor(i / gridSize) % gridSize) * spacing - (gridSize * spacing) / 2;
      const z = (Math.floor(i / (gridSize * gridSize))) * spacing - (gridSize * spacing) / 2;

      targetPositions[i * 3] = x;
      targetPositions[i * 3 + 1] = y;
      targetPositions[i * 3 + 2] = z;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    // Store original positions for lerping
    geometry.setAttribute('initialPosition', new THREE.BufferAttribute(new Float32Array(positions), 3));
    geometry.setAttribute('targetPosition', new THREE.BufferAttribute(targetPositions, 3));

    // Colors: Silver/Orange/Green mix
    const material = new THREE.PointsMaterial({
      size: 4,
      color: theme === 'light' ? 0x94A3B8 : 0xCBD5E1,
      transparent: true,
      opacity: 0.6,
      sizeAttenuation: true
    });

    const particles = new THREE.Points(geometry, material);
    scene.add(particles);

    let scrollProgress = 0;

    const handleScroll = () => {
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      scrollProgress = Math.min(Math.max(scrollTop / docHeight, 0), 1);
    };

    window.addEventListener('scroll', handleScroll, { passive: true });

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('resize', handleResize);

    let animationFrameId: number;

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);

      // Lerp particles based on scroll
      const posAttr = geometry.attributes.position;
      const initAttr = geometry.attributes.initialPosition;
      const targAttr = geometry.attributes.targetPosition;

      for (let i = 0; i < particleCount; i++) {
        const ix = initAttr.getX(i);
        const iy = initAttr.getY(i);
        const iz = initAttr.getZ(i);

        const tx = targAttr.getX(i);
        const ty = targAttr.getY(i);
        const tz = targAttr.getZ(i);

        // Smooth transition driven by scroll progress
        const targetX = ix + (tx - ix) * scrollProgress;
        const targetY = iy + (ty - iy) * scrollProgress;
        const targetZ = iz + (tz - iz) * scrollProgress;

        // Current position
        const cx = posAttr.getX(i);
        const cy = posAttr.getY(i);
        const cz = posAttr.getZ(i);

        // Ease towards target
        posAttr.setX(i, cx + (targetX - cx) * 0.05);
        posAttr.setY(i, cy + (targetY - cy) * 0.05);
        posAttr.setZ(i, cz + (targetZ - cz) * 0.05);
      }
      posAttr.needsUpdate = true;

      // Slow rotation for ambiance
      particles.rotation.y += 0.001;
      particles.rotation.x += 0.0005;

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      geometry.dispose();
      material.dispose();
      renderer.dispose();
    };
  }, [isMobile, theme]);

  if (isMobile) {
    return (
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden w-full h-full">
        {/* Mobile 2D SVG Fallback */}
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
              <path d="M 40 0 L 0 0 0 40" fill="none" stroke={theme === 'light' ? 'rgba(148, 163, 184, 0.2)' : 'rgba(148, 163, 184, 0.05)'} strokeWidth="1" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#grid)" />
        </svg>
      </div>
    );
  }

  return <div ref={mountRef} className="fixed inset-0 pointer-events-none z-0" aria-hidden="true" />;
};
