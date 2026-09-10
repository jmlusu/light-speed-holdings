/**
 * LIGHTSPEED HOLDINGS LIMITED — 3D SCENE ENGINE
 * Central 3D Icosahedron Core & 3,000 Orbital Nodes with Scroll Lerp
 */

(function () {
  const container = document.getElementById('webgl-canvas-container');
  if (!container || typeof THREE === 'undefined') return;

  // Scene, Camera, Renderer
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(
    45,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
  camera.position.set(0, 0, 7.5);

  const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.1;
  container.appendChild(renderer.domElement);

  // Central 3D Icosahedron Monolith
  // Detail 0 for crisp architectural facets
  const icosahedronGeo = new THREE.IcosahedronGeometry(1.65, 0);
  const monolithMaterial = new THREE.MeshStandardMaterial({
    color: 0x18181b,
    roughness: 0.2,
    metalness: 0.9,
    flatShading: true,
    wireframe: false,
  });
  const monolith = new THREE.Mesh(icosahedronGeo, monolithMaterial);
  scene.add(monolith);

  // Wireframe Accent Cage
  const wireGeo = new THREE.IcosahedronGeometry(1.68, 0);
  const wireMat = new THREE.MeshBasicMaterial({
    color: 0x3f3f46,
    wireframe: true,
    transparent: true,
    opacity: 0.45,
  });
  const wireframeCage = new THREE.Mesh(wireGeo, wireMat);
  scene.add(wireframeCage);

  // 3,000 Floating Orbital Nodes
  const particleCount = 3000;
  const particlePositions = new Float32Array(particleCount * 3);
  const particleColors = new Float32Array(particleCount * 3);

  for (let i = 0; i < particleCount; i++) {
    const radius = 2.4 + Math.random() * 6.5;
    const theta = Math.random() * Math.PI * 2;
    const phi = Math.acos(Math.random() * 2 - 1);

    const x = radius * Math.sin(phi) * Math.cos(theta);
    const y = radius * Math.sin(phi) * Math.sin(theta);
    const z = radius * Math.cos(phi);

    particlePositions[i * 3] = x;
    particlePositions[i * 3 + 1] = y;
    particlePositions[i * 3 + 2] = z;

    // Zinc to white gradient
    const brightness = 0.35 + Math.random() * 0.65;
    particleColors[i * 3] = brightness;
    particleColors[i * 3 + 1] = brightness;
    particleColors[i * 3 + 2] = brightness;
  }

  const particleGeo = new THREE.BufferGeometry();
  particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
  particleGeo.setAttribute('color', new THREE.BufferAttribute(particleColors, 3));

  const particleMat = new THREE.PointsMaterial({
    size: 0.024,
    vertexColors: true,
    transparent: true,
    opacity: 0.6,
    blending: THREE.AdditiveBlending,
  });

  const particleSystem = new THREE.Points(particleGeo, particleMat);
  scene.add(particleSystem);

  // Studio Lighting
  const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
  scene.add(ambientLight);

  const mainLight = new THREE.DirectionalLight(0xffffff, 2.2);
  mainLight.position.set(5, 8, 6);
  scene.add(mainLight);

  const rimLight = new THREE.DirectionalLight(0x71717a, 1.4);
  rimLight.position.set(-6, -4, -4);
  scene.add(rimLight);

  // Scroll Tracking & Lerp State
  let scrollProgress = 0;
  let targetScroll = 0;

  function onScroll() {
    const scrollY = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    targetScroll = docHeight > 0 ? Math.min(1, Math.max(0, scrollY / docHeight)) : 0;
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  // Pointer Interaction
  let mouseX = 0;
  let mouseY = 0;
  let targetMouseX = 0;
  let targetMouseY = 0;

  window.addEventListener('mousemove', function (e) {
    targetMouseX = (e.clientX / window.innerWidth - 0.5) * 2;
    targetMouseY = (e.clientY / window.innerHeight - 0.5) * 2;
  });

  // Resize Listener
  window.addEventListener('resize', function () {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });

  // Clock & Animation Loop
  const clock = new THREE.Clock();

  function animate() {
    requestAnimationFrame(animate);
    const delta = clock.getDelta();
    const elapsedTime = clock.getElapsedTime();

    // Lerp scroll and mouse
    scrollProgress += (targetScroll - scrollProgress) * 0.06;
    mouseX += (targetMouseX - mouseX) * 0.05;
    mouseY += (targetMouseY - mouseY) * 0.05;

    // Monolith base rotation + accelerated scroll spin
    const spinFactor = 0.35 + scrollProgress * 1.5;
    monolith.rotation.y = elapsedTime * spinFactor * 0.5 + mouseX * 0.3;
    monolith.rotation.x = Math.sin(elapsedTime * 0.3) * 0.2 - mouseY * 0.2;
    wireframeCage.rotation.copy(monolith.rotation);

    // Subtle scale distortion along scroll
    const scaleFactor = 1.0 + Math.sin(scrollProgress * Math.PI) * 0.25;
    monolith.scale.set(scaleFactor, scaleFactor, scaleFactor);
    wireframeCage.scale.set(scaleFactor, scaleFactor, scaleFactor);

    // Particles counter-rotation
    particleSystem.rotation.y = -elapsedTime * 0.08 + scrollProgress * 0.5;
    particleSystem.rotation.x = elapsedTime * 0.03;

    // Cinematic Camera Lerp along Y and Z axes
    camera.position.y = -scrollProgress * 2.8 + mouseY * 0.3;
    camera.position.z = 7.5 - scrollProgress * 1.6;
    camera.position.x = mouseX * 0.4;
    camera.lookAt(0, -scrollProgress * 0.8, 0);

    renderer.render(scene, camera);
  }

  animate();
})();
