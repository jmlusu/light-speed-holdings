import React, { useState, useEffect, useRef } from 'react';
import {
  Compass,
  Brain,
  CheckCircle2,
  Cpu,
  Workflow,
  TrendingUp,
  Play,
  RotateCcw,
  ArrowRight,
  Layers,
  ShieldCheck,
  Zap,
  Clock,
  Building2,
  Coins,
  Globe2,
  Sparkles,
  ChevronRight
} from 'lucide-react';
import * as THREE from 'three';

export interface OperatingStage {
  id: string;
  step: number;
  title: string;
  subtitle: string;
  description: string;
  traditional: string;
  lightspeed: string;
  traditionalProblem: string;
  telemetry: {
    metric: string;
    value: string;
    delta: string;
    traditionalMetric: string;
    traditionalValue: string;
    traditionalDelta: string;
  };
  artifacts: string[];
  traditionalArtifacts: string[];
}

const STAGES: OperatingStage[] = [
  {
    id: 'strategy',
    step: 1,
    title: 'Strategy',
    subtitle: 'Enterprise Architecture & Fiduciary Intent',
    description: 'Synthesize organizational objectives, regulatory boundaries, and capital allocation into formal, computable business logic.',
    traditional: '6-9 months of static slide decks, ambiguous executive summaries, and quarterly reviews that become obsolete before implementation begins.',
    traditionalProblem: 'High strategy-execution friction, zero computable validation, and multi-million dollar consultant retainers without live operational software.',
    lightspeed: 'Continuous computable policy models updated dynamically against market signals, encoded directly into Policy-as-Code schemas and token budgets.',
    telemetry: {
      metric: 'Formulation Velocity',
      value: 'Continuous',
      delta: 'Policy-as-Code compile',
      traditionalMetric: 'Strategy Formulation Cycle',
      traditionalValue: '6–9 Months',
      traditionalDelta: 'Obsolete upon delivery'
    },
    artifacts: ['Enterprise Fiduciary Schema', 'Computable Policy-as-Code', 'Regulatory Guardrails'],
    traditionalArtifacts: ['500-Slide PowerPoint Deck', 'Unenforceable Strategy Memo', 'Subjective Steering Notes']
  },
  {
    id: 'intelligence',
    step: 2,
    title: 'Intelligence',
    subtitle: 'Sovereign Knowledge Synthesis',
    description: 'Transform siloed legacy data, unstructured filings, contracts, and market telemetry into private, real-time knowledge graphs.',
    traditional: 'Disconnected relational databases, stale monthly batch BI extracts, and unverified data dumps that create blind spots across business units.',
    traditionalProblem: 'Severe data silos, risks of public cloud SaaS leakage, and manual copy-paste spreadsheet consolidation across divisions.',
    lightspeed: 'Private semantic data fabrics with continuous vector ingestion, entity resolution, and cryptographic AST lineage under strict 100% on-premise residency.',
    telemetry: {
      metric: 'Data Ingestion Rate',
      value: 'Continuous',
      delta: 'Air-Gapped & Sovereign',
      traditionalMetric: 'Data Pipeline Latency',
      traditionalValue: '30–45 Days',
      traditionalDelta: 'Siloed & fragmented'
    },
    artifacts: ['Sovereign Vector Fabric', 'Entity Graph Linkage', 'AST Lineage Verification'],
    traditionalArtifacts: ['Stale SQL Batch Extract', 'Manual Excel Consolidation', 'Unencrypted Cloud SaaS Dump']
  },
  {
    id: 'decision',
    step: 3,
    title: 'Decision',
    subtitle: 'Scenario Simulation & Approval Gates',
    description: 'Model counterfactual scenarios, quantify capital and compliance risks, and surface high-confidence recommendations to human leaders.',
    traditional: 'Subjective intuition debated across lengthy committee sessions with unquantified assumptions and no cryptographic accountability.',
    traditionalProblem: 'Analysis paralysis, politicized committee delays, and unrecorded decision rationale leading to blame-shifting during audits.',
    lightspeed: 'Deterministic Monte-Carlo simulations with verified Human-in-the-Loop (HITL) approval gates and mathematical risk bounds.',
    telemetry: {
      metric: 'Approval Fidelity',
      value: '5-Tier HITL',
      delta: 'Every decision auditable',
      traditionalMetric: 'Decision Deliberation Time',
      traditionalValue: '8–12 Weeks',
      traditionalDelta: 'Subjective guesswork'
    },
    artifacts: ['Multi-Branch Simulations', 'Fiduciary Risk Matrix', 'Signed Cryptographic Gate'],
    traditionalArtifacts: ['Committee Meeting Minutes', 'Unverified ROI Estimates', 'Verbal Unrecorded Sign-offs']
  },
  {
    id: 'automation',
    step: 4,
    title: 'AI / Automation',
    subtitle: 'Deterministic Multi-Agent Orchestration',
    description: 'Decompose validated decisions into coordinated specialist agents operating under strict security, tool, and rate budgets.',
    traditional: 'Manual email chains, unmonitored shadow scripts, and disjointed point-tool chatbots that hallucinate and lack organizational context.',
    traditionalProblem: 'Fragile RPA bots that break on schema shifts, ungoverned AI consumer tools leaking trade secrets, and zero task orchestration.',
    lightspeed: 'Deterministic OpenCode agent hierarchies constrained to 7 canonical tools, Directed Acyclic Graph (DAG) orchestration, and task rate limits.',
    telemetry: {
      metric: 'Agent Concurrency',
      value: '144 Active',
      delta: '100% auditable DAGs',
      traditionalMetric: 'Workflow Orchestration',
      traditionalValue: 'Manual Handoffs',
      traditionalDelta: 'High error & leak risk'
    },
    artifacts: ['Specialist Task DAGs', 'Canonical Tool Contracts', 'Automated Unit Verification'],
    traditionalArtifacts: ['Unbounded Email Chains', 'Ad-hoc Unmonitored Scripts', 'Brittle Fragile RPA Bots']
  },
  {
    id: 'execution',
    step: 5,
    title: 'Execution',
    subtitle: 'Direct Enterprise Integration & Settlement',
    description: 'Execute transactions, issue letters of credit, rebalance inventories, and interact directly with core ERPs and payment rails.',
    traditional: 'Manual dual-entry into legacy green-screen mainframes, physical paper manifests, and multi-day settlement delays across borders.',
    traditionalProblem: 'Crippling administrative overhead, demurrage fines at ports, human transcription errors, and days of floating capital settlement.',
    lightspeed: 'Direct API execution, automated customs EDI clearing, and real-time core banking settlement with zero-trust ledger writes.',
    telemetry: {
      metric: 'Settlement Path',
      value: 'Direct API',
      delta: '5-tier HITL gated',
      traditionalMetric: 'Settlement Clearance Time',
      traditionalValue: 'Multi-Day',
      traditionalDelta: 'Crippling capital float'
    },
    artifacts: ['Core Banking Settlement', 'Customs EDI Clearing', 'Smart Contract Dispatch'],
    traditionalArtifacts: ['Manual Dual Data Entry', 'Physical Paper Bills of Lading', 'Delayed Postal Mail Filing']
  },
  {
    id: 'outcomes',
    step: 6,
    title: 'Measurable Outcomes',
    subtitle: 'Verifiable Business Impact',
    description: 'Continuously measure bottom-line returns, compliance fidelity, customer satisfaction, and capital velocity across the enterprise.',
    traditional: 'Retrospective post-mortems conducted 12 months after capital deployment, discovering budget overruns when it is too late to remediate.',
    traditionalProblem: 'Zero operational visibility, consultant fee disputes, and inability to trace which business decisions drove financial returns.',
    lightspeed: 'Real-time telemetry dashboards for live outcome tracking, continuous model drift detection, and automated closed-loop policy self-tuning.',
    telemetry: {
      metric: 'Delivery Status',
      value: 'In Development',
      delta: 'No client deliveries yet',
      traditionalMetric: 'Audit & Outcome Cadence',
      traditionalValue: 'Annual / Post-Facto',
      traditionalDelta: 'Write-downs & regret'
    },
    artifacts: ['Audited Cryptographic Ledgers', 'Executive Telemetry Feeds', 'Continuous Closed-Loop Tuning'],
    traditionalArtifacts: ['Annual Retrospective Binder', 'Consultant Billing Dispute', 'Unverified Spend Receipts']
  }
];

const USE_CASES = [
  {
    id: 'financial-inclusion',
    icon: Coins,
    name: 'Financial Inclusion',
    sector: 'Savings groups, microfinance, cooperatives',
    headline: 'Agentic workflows over mobile-money rails for savings groups',
    challenge: 'Informal savings groups and cooperatives manage money across fragmented mobile-money platforms with limited automation and auditability.',
    solution: 'In pilot — agentic workflows over mobile-money rails (Airtel Money, TNM Mpamba) with micro-loan risk assessment for smallholder farmers.'
  },
  {
    id: 'government',
    icon: Building2,
    name: 'Government Services',
    sector: 'Governance, compliance, legal at scale',
    headline: 'In active development — governance framework mapped to Malawi DPA and SADC standards',
    challenge: 'Government agencies need compliance monitoring, contract review, and citizen services delivered under strict regulatory guardrails.',
    solution: 'In active development — 5-tier human-in-the-loop approval gates with every decision auditable, mapped to Malawi DPA and SADC standards.'
  },
  {
    id: 'corridor-logistics',
    icon: Globe2,
    name: 'Corridor Logistics',
    sector: 'Supply chain, corridor traders, logistics companies',
    headline: 'Corridor routing and ledger-auditing agents for the Nacala and Beira corridors',
    challenge: 'Corridor traders and logistics companies route cargo between ports and inland processing centers with limited end-to-end visibility.',
    solution: 'In active development — deterministic corridor routing and ledger-auditing agents with human approval gates on high-value writes.'
  }
];

interface InteractiveOperatingModelProps {
  theme?: 'light' | 'dark';
  onRequestBriefing?: () => void;
}

export const InteractiveOperatingModel: React.FC<InteractiveOperatingModelProps> = ({
  theme = 'dark',
  onRequestBriefing
}) => {
  const [activeStepIndex, setActiveStepIndex] = useState<number>(0);
  const [selectedUseCase, setSelectedUseCase] = useState<number>(0);
  const [modelMode, setModelMode] = useState<'lightspeed' | 'traditional'>('lightspeed');
  const [isPlaying, setIsPlaying] = useState<boolean>(true);

  const mountRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const nodesRef = useRef<THREE.Mesh[]>([]);
  const connectorLineRef = useRef<THREE.LineSegments | null>(null);
  const particlesRef = useRef<THREE.Points | null>(null);
  const activeStepRef = useRef<number>(activeStepIndex);
  const modelModeRef = useRef<'lightspeed' | 'traditional'>(modelMode);

  useEffect(() => {
    activeStepRef.current = activeStepIndex;
  }, [activeStepIndex]);

  useEffect(() => {
    modelModeRef.current = modelMode;
  }, [modelMode]);

  // Auto-play stepper if enabled
  useEffect(() => {
    if (!isPlaying) return;
    const interval = setInterval(() => {
      setActiveStepIndex(prev => (prev + 1) % STAGES.length);
    }, 4500);
    return () => clearInterval(interval);
  }, [isPlaying]);

  // Three.js 3D Operating Model Canvas: 3D Infographic Radial Topology with Numbered 01-06 Capsules
  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 340;

    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.fog = new THREE.FogExp2(0x0a0c10, 0.08);

    const camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
    camera.position.set(0, 0, 5.2);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    rendererRef.current = renderer;

    container.appendChild(renderer.domElement);

    // Studio Lighting setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 1.4);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xfff5e6, 2.8);
    keyLight.position.set(2, 4, 5);
    scene.add(keyLight);

    const goldPointLight = new THREE.PointLight(0x00bfff, 3.8, 12);
    goldPointLight.position.set(0, 0, 3);
    scene.add(goldPointLight);

    // =========================================================================
    // 1. CENTRAL CORE HUB (BUSINESS STEPS INFOGRAPHIC CORE)
    // =========================================================================
    const createCentralHubTexture = () => {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 512;
      const ctx = canvas.getContext('2d')!;

      // Outer glowing yellow ring
      const gradOuter = ctx.createRadialGradient(256, 256, 180, 256, 256, 250);
      gradOuter.addColorStop(0, '#00BFFF');
      gradOuter.addColorStop(0.7, '#00BFFF');
      gradOuter.addColorStop(1, '#00BFFF');
      ctx.fillStyle = gradOuter;
      ctx.beginPath();
      ctx.arc(256, 256, 250, 0, Math.PI * 2);
      ctx.fill();

      // Black Bevel Shadow
      ctx.fillStyle = '#0f141c';
      ctx.beginPath();
      ctx.arc(256, 256, 215, 0, Math.PI * 2);
      ctx.fill();

      // Inner Dark Surface Gradient
      const gradInner = ctx.createRadialGradient(210, 210, 20, 256, 256, 210);
      gradInner.addColorStop(0, '#27272a');
      gradInner.addColorStop(0.6, '#18181b');
      gradInner.addColorStop(1, '#09090b');
      ctx.fillStyle = gradInner;
      ctx.beginPath();
      ctx.arc(256, 256, 205, 0, Math.PI * 2);
      ctx.fill();

      // Center Typography
      ctx.fillStyle = '#00BFFF';
      ctx.font = '800 24px "Plus Jakarta Sans", sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('LIGHTSPEED', 256, 190);

      ctx.fillStyle = '#ffffff';
      ctx.font = '900 48px "Plus Jakarta Sans", sans-serif';
      ctx.shadowColor = 'rgba(0,0,0,0.8)';
      ctx.shadowBlur = 10;
      ctx.fillText('OPERATING', 256, 245);
      ctx.fillText('MODEL', 256, 295);

      ctx.fillStyle = '#a1a1aa';
      ctx.font = '700 18px "JetBrains Mono", monospace';
      ctx.fillText('CLOSED-LOOP PIPELINE', 256, 345);

      const texture = new THREE.CanvasTexture(canvas);
      texture.needsUpdate = true;
      return texture;
    };

    const hubGeo = new THREE.CircleGeometry(0.85, 64);
    const hubMat = new THREE.MeshBasicMaterial({
      map: createCentralHubTexture(),
      transparent: true,
      side: THREE.DoubleSide
    });
    const centralHubMesh = new THREE.Mesh(hubGeo, hubMat);
    centralHubMesh.position.set(0, 0, 0);
    scene.add(centralHubMesh);

    // Orbital Ring encircling the Core Hub
    const orbitRingGeo = new THREE.RingGeometry(1.5, 1.52, 96);
    const orbitRingMat = new THREE.MeshBasicMaterial({
      color: 0x00bfff,
      transparent: true,
      opacity: 0.35,
      side: THREE.DoubleSide
    });
    const orbitRingMesh = new THREE.Mesh(orbitRingGeo, orbitRingMat);
    scene.add(orbitRingMesh);

    // =========================================================================
    // 2. SIX RADIAL 3D STEP CAPSULES (01 TO 06 INFOGRAPHIC STYLE)
    // =========================================================================
    // Stage Icon Drawer Helper
    const drawStageIcon = (ctx: CanvasRenderingContext2D, cx: number, cy: number, idx: number) => {
      ctx.save();
      ctx.translate(cx, cy);
      ctx.strokeStyle = '#ffffff';
      ctx.fillStyle = '#ffffff';
      ctx.lineWidth = 3;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';

      if (idx === 0) {
        // Brain / Strategy
        ctx.beginPath();
        ctx.arc(-8, -4, 10, 0.5, Math.PI * 1.5);
        ctx.arc(8, -4, 10, -Math.PI * 0.5, 0.5);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(-6, 6, 8, 0, Math.PI * 2);
        ctx.arc(6, 6, 8, 0, Math.PI * 2);
        ctx.stroke();
      } else if (idx === 1) {
        // Document / Magnifying Glass
        ctx.strokeRect(-12, -14, 16, 22);
        ctx.beginPath();
        ctx.arc(6, 4, 8, 0, Math.PI * 2);
        ctx.moveTo(12, 10);
        ctx.lineTo(18, 16);
        ctx.stroke();
      } else if (idx === 2) {
        // Gears / Human-in-the-Loop Gate
        ctx.beginPath();
        ctx.arc(-6, -4, 7, 0, Math.PI * 2);
        ctx.arc(6, 6, 7, 0, Math.PI * 2);
        ctx.stroke();
      } else if (idx === 3) {
        // Growth Chart / DAG Agent Execution
        ctx.beginPath();
        ctx.moveTo(-16, 12);
        ctx.lineTo(-8, 2);
        ctx.lineTo(0, 6);
        ctx.lineTo(12, -10);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(4, -10);
        ctx.lineTo(12, -10);
        ctx.lineTo(12, -2);
        ctx.stroke();
      } else if (idx === 4) {
        // Currency Cycle / Real-Time Settlement
        ctx.font = '900 24px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('$', 0, 1);
        ctx.beginPath();
        ctx.arc(0, 0, 16, 0.2, Math.PI * 1.8);
        ctx.stroke();
      } else {
        // Target / Continuous Yield Audit
        ctx.beginPath();
        ctx.arc(0, 0, 16, 0, Math.PI * 2);
        ctx.arc(0, 0, 9, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(0, 0, 3, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    };

    const createCapsuleTexture = (idx: number, active: boolean) => {
      const canvas = document.createElement('canvas');
      canvas.width = 512;
      canvas.height = 160;
      const ctx = canvas.getContext('2d')!;

      ctx.clearRect(0, 0, 512, 160);

      // Main Pill Capsule
      const fillGrad = ctx.createLinearGradient(0, 0, 512, 0);
      if (active) {
        fillGrad.addColorStop(0, '#00BFFF');
        fillGrad.addColorStop(0.5, '#00BFFF');
        fillGrad.addColorStop(1, '#00BFFF');
      } else {
        fillGrad.addColorStop(0, '#27272a');
        fillGrad.addColorStop(0.7, '#18181b');
        fillGrad.addColorStop(1, '#09090b');
      }

      // Outer Bevel Pill Shape
      ctx.fillStyle = fillGrad;
      ctx.beginPath();
      ctx.roundRect(8, 8, 496, 144, 72);
      ctx.fill();

      // High-Contrast Border
      ctx.strokeStyle = active ? '#ffffff' : '#00BFFF';
      ctx.lineWidth = active ? 6 : 3;
      ctx.stroke();

      // Stage Number (01-06)
      ctx.fillStyle = active ? '#000000' : '#00BFFF';
      ctx.font = '900 76px "JetBrains Mono", monospace';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.shadowColor = active ? 'rgba(255,255,255,0.4)' : 'rgba(0,0,0,0.8)';
      ctx.shadowBlur = 6;
      ctx.fillText(`0${idx + 1}`, 36, 82);

      // Title & Subtitle
      const stage = STAGES[idx];
      ctx.fillStyle = active ? '#0f172a' : '#ffffff';
      ctx.font = '900 24px "Plus Jakarta Sans", sans-serif';
      ctx.shadowBlur = 0;
      const titleText = stage.title.length > 20 ? stage.title.substring(0, 18) + '..' : stage.title;
      ctx.fillText(titleText, 145, 68);

      ctx.fillStyle = active ? '#451a03' : '#a1a1aa';
      ctx.font = '700 16px "JetBrains Mono", monospace';
      const subLabels = ['FIDUCIARY', 'SOVEREIGN', 'HITL GATE', 'AGENT DAG', 'SETTLEMENT', 'YIELD AUDIT'];
      ctx.fillText(subLabels[idx] || 'STAGE', 145, 102);

      // Right 3D Dark Disc Icon Button
      const discCx = 430;
      const discCy = 80;
      const discR = 52;

      ctx.fillStyle = '#09090b';
      ctx.beginPath();
      ctx.arc(discCx, discCy, discR, 0, Math.PI * 2);
      ctx.fill();

      ctx.strokeStyle = active ? '#00BFFF' : '#52525b';
      ctx.lineWidth = 4;
      ctx.stroke();

      drawStageIcon(ctx, discCx, discCy, idx);

      const texture = new THREE.CanvasTexture(canvas);
      texture.needsUpdate = true;
      return texture;
    };

    // Stage Capsule Spatial Positions (Left 3, Right 3 radially encircling central core hub)
    const capsuleCoords = [
      { x: -2.35, y:  0.95, z: 0 },  // 01 Top Left
      { x: -2.65, y:  0.00, z: 0 },  // 02 Mid Left
      { x: -2.35, y: -0.95, z: 0 },  // 03 Bot Left
      { x:  2.35, y:  0.95, z: 0 },  // 04 Top Right
      { x:  2.65, y:  0.00, z: 0 },  // 05 Mid Right
      { x:  2.35, y: -0.95, z: 0 }   // 06 Bot Right
    ];

    const capsuleGeo = new THREE.PlaneGeometry(1.85, 0.58);
    const capsuleMeshes: THREE.Mesh[] = [];
    const connectingLines: THREE.Line[] = [];

    capsuleCoords.forEach((pos, idx) => {
      const texture = createCapsuleTexture(idx, idx === 0);
      const mat = new THREE.MeshBasicMaterial({
        map: texture,
        transparent: true,
        side: THREE.DoubleSide
      });
      const mesh = new THREE.Mesh(capsuleGeo, mat);
      mesh.position.set(pos.x, pos.y, pos.z);
      mesh.userData = { stepIndex: idx, baseX: pos.x, baseY: pos.y };
      scene.add(mesh);
      capsuleMeshes.push(mesh);

      // Direct Geometric Ray Line connecting central hub to capsule
      const lineGeo = new THREE.BufferGeometry().setFromPoints([
        new THREE.Vector3(0, 0, 0),
        new THREE.Vector3(pos.x * 0.65, pos.y * 0.65, 0)
      ]);
      const lineMat = new THREE.LineBasicMaterial({
        color: idx === 0 ? 0x00bfff : 0x3f3f46,
        transparent: true,
        opacity: idx === 0 ? 0.9 : 0.4,
        linewidth: 2
      });
      const line = new THREE.Line(lineGeo, lineMat);
      scene.add(line);
      connectingLines.push(line);
    });

    nodesRef.current = capsuleMeshes;

    // Interactive Raycaster for clicking directly on 3D Stage Capsules
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();

    const handleCanvasClick = (event: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(capsuleMeshes);
      if (intersects.length > 0) {
        const clickedMesh = intersects[0].object as THREE.Mesh;
        if (clickedMesh.userData && typeof clickedMesh.userData.stepIndex === 'number') {
          setActiveStepIndex(clickedMesh.userData.stepIndex);
          setIsPlaying(false);
        }
      }
    };

    renderer.domElement.addEventListener('click', handleCanvasClick);

    let animFrameId: number;
    const clock = new THREE.Clock();

    const animate = () => {
      animFrameId = requestAnimationFrame(animate);
      const elapsedTime = clock.getElapsedTime();
      const currentActive = activeStepRef.current;

      // Rotate central orbital ring
      orbitRingMesh.rotation.z = elapsedTime * 0.15;

      // Animate Capsule Meshes
      capsuleMeshes.forEach((mesh, idx) => {
        const isActive = idx === currentActive;

        // Subtle floating motion
        mesh.position.y = mesh.userData.baseY + Math.sin(elapsedTime * 1.8 + idx) * 0.025;

        // Update active vs inactive textures & scale dynamically
        if (isActive) {
          mesh.scale.lerp(new THREE.Vector3(1.1, 1.1, 1.1), 0.12);
          mesh.position.z = 0.15;
          if (connectingLines[idx]) {
            const lMat = connectingLines[idx].material as THREE.LineBasicMaterial;
            lMat.color.setHex(0x00bfff);
            lMat.opacity = 0.9 + Math.sin(elapsedTime * 4) * 0.1;
          }
        } else {
          mesh.scale.lerp(new THREE.Vector3(0.96, 0.96, 0.96), 0.12);
          mesh.position.z = 0;
          if (connectingLines[idx]) {
            const lMat = connectingLines[idx].material as THREE.LineBasicMaterial;
            lMat.color.setHex(0x3f3f46);
            lMat.opacity = 0.35;
          }
        }
      });

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      renderer.domElement.removeEventListener('click', handleCanvasClick);
      cancelAnimationFrame(animFrameId);
      if (renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
      hubGeo.dispose();
      hubMat.dispose();
      orbitRingGeo.dispose();
      orbitRingMat.dispose();
      capsuleGeo.dispose();
      connectingLines.forEach(l => {
        l.geometry.dispose();
        (l.material as THREE.Material).dispose();
      });
    };
  }, []);

  const isLight = theme === 'light';
  const currentStage = STAGES[activeStepIndex];

  return (
    <div className="w-full space-y-8">
      {/* Operating Model Introduction & Executive Thesis Framing */}
      <div className="space-y-6 pb-6 border-b border-white/10">
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
          <div className="space-y-3 max-w-3xl">
            <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full border border-ls-red/40 bg-ls-red/10 text-ls-red font-mono text-[11px] tracking-widest shadow-sm">
              <span className="w-2 h-2 rounded-full bg-ls-red shadow-[0_0_8px_rgba(230,57,70,1)] animate-pulse" />
              <span>THE LIGHTSPEED THESIS IN ACTION</span>
            </div>

            <h3 className={`text-3xl sm:text-4xl lg:text-5xl font-black tracking-tight font-display leading-[1.05] ${
              isLight ? 'text-slate-900' : 'text-white'
            }`}>
              Collapsing Strategy <br />
              <span className={isLight
                ? 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-cyan to-slate-900'
                : 'text-transparent bg-clip-text bg-gradient-to-r from-ls-red via-ls-cyan to-orange-200'
              }>
                Into Computable Execution
              </span>
            </h3>

            <p className={`text-justify text-sm sm:text-base leading-relaxed ${
              isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
            }`}>
              Traditional enterprises lose 6 to 18 months in the friction between boardroom formulation and operational delivery.
              LIGHTSPEED's operating thesis replaces static slide decks and siloed handoffs with a <strong>continuous, computable closed loop</strong>—compiling fiduciary intent directly into bounded multi-agent DAGs, sovereign data fabrics, and verifiable settlements in real time.
            </p>
          </div>

          {/* Operating Model Comparison Toggle: Traditional vs LIGHTSPEED (Tactile Hardware Toggle Switch) */}
          <div className="shrink-0 space-y-2">
            <div className="text-[11px] font-mono tracking-wider text-zinc-400 font-bold flex items-center justify-between">
              <span>Operating Paradigm</span>
              <span className="text-ls-red text-[10px]">Active: {modelMode === 'lightspeed' ? 'AI-Native' : 'Traditional'}</span>
            </div>
            <div className={`flex flex-wrap items-center p-1.5 rounded-2xl shrink-0 ${
              isLight ? 'tactile-chassis-light shadow-md' : 'tactile-chassis-dark shadow-xl'
            }`}>
              <button
                onClick={() => setModelMode('lightspeed')}
                className={`flex-1 min-w-0 justify-center px-2 sm:px-4 py-2 rounded-xl text-xs font-mono font-bold tracking-wide transition-all duration-200 cursor-pointer flex items-center gap-1.5 sm:gap-2 relative ${
                  modelMode === 'lightspeed'
                    ? isLight
                      ? 'tactile-btn-active-light text-slate-900 border-ls-red/60 shadow-md'
                      : 'tactile-btn-active-dark text-white border-ls-red/60 shadow-md'
                    : isLight
                      ? 'tactile-btn-inactive-light text-slate-600 hover:text-slate-900'
                      : 'tactile-btn-inactive-dark text-zinc-400 hover:text-white'
                }`}
              >
                <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  modelMode === 'lightspeed' ? 'tactile-pip-active shadow-[0_0_8px_rgba(230,57,70,1)]' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                }`} />
                <span className="whitespace-nowrap">LIGHTSPEED AI-Native</span>
              </button>
              <button
                onClick={() => setModelMode('traditional')}
                className={`flex-1 min-w-0 justify-center px-2 sm:px-4 py-2 rounded-xl text-xs font-mono font-bold tracking-wide transition-all duration-200 cursor-pointer flex items-center gap-1.5 sm:gap-2 relative ${
                  modelMode === 'traditional'
                    ? isLight
                      ? 'tactile-btn-active-light text-slate-900 border-ls-cyan/60 shadow-md'
                      : 'tactile-btn-active-dark text-white border-ls-cyan/60 shadow-md'
                    : isLight
                      ? 'tactile-btn-inactive-light text-slate-600 hover:text-slate-900'
                      : 'tactile-btn-inactive-dark text-zinc-400 hover:text-white'
                }`}
              >
                <span className={`w-2 h-2 rounded-full transition-all duration-300 ${
                  modelMode === 'traditional' ? 'tactile-pip-active bg-ls-cyan shadow-[0_0_8px_rgba(0,191,255,1)]' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                }`} />
                <span className="whitespace-nowrap">Traditional Consulting</span>
              </button>
            </div>
          </div>
        </div>

        {/* 4 Comparative Thesis Pillar Metric Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-2">
          <div className={`p-3.5 rounded-2xl border transition-all ${
            modelMode === 'lightspeed'
              ? isLight ? 'bg-orange-50/70 border-orange-200' : 'bg-orange-950/20 border-ls-red/30'
              : isLight ? 'bg-slate-100 border-slate-200' : 'bg-ls-navy border-white/10'
          }`}>
            <div className="text-[10px] font-mono tracking-wider text-zinc-500 font-bold mb-1">
              Cycle Velocity
            </div>
            <div className={`text-xl sm:text-2xl font-black font-mono tracking-tight ${
              modelMode === 'lightspeed' ? 'text-ls-red' : 'text-ls-cyan'
            }`}>
              {modelMode === 'lightspeed' ? 'Real-Time' : '6–9 Months'}
            </div>
            <div className="text-[11px] text-zinc-400 mt-1 font-medium">
              {modelMode === 'lightspeed' ? 'Continuous DAG compile' : 'Static quarterly review slides'}
            </div>
          </div>

          <div className={`p-3.5 rounded-2xl border transition-all ${
            modelMode === 'lightspeed'
              ? isLight ? 'bg-ls-cyan/70 border-ls-cyan' : 'bg-emerald-950/20 border-ls-cyan/30'
              : isLight ? 'bg-slate-100 border-slate-200' : 'bg-ls-navy border-white/10'
          }`}>
            <div className="text-[10px] font-mono tracking-wider text-zinc-500 font-bold mb-1">
              Fiduciary Assurance
            </div>
            <div className={`text-xl sm:text-2xl font-black font-mono tracking-tight ${
              modelMode === 'lightspeed' ? 'text-ls-cyan' : 'text-rose-500'
            }`}>
              {modelMode === 'lightspeed' ? '100% Cryptographic' : 'Unverified Sign-offs'}
            </div>
            <div className="text-[11px] text-zinc-400 mt-1 font-medium">
              {modelMode === 'lightspeed' ? 'Deterministic HITL approval' : 'Subjective committee politics'}
            </div>
          </div>

          <div className={`p-3.5 rounded-2xl border transition-all ${
            modelMode === 'lightspeed'
              ? isLight ? 'bg-ls-cyan/70 border-ls-cyan' : 'bg-amber-950/20 border-ls-cyan/30'
              : isLight ? 'bg-slate-100 border-slate-200' : 'bg-ls-navy border-white/10'
          }`}>
            <div className="text-[10px] font-mono tracking-wider text-zinc-500 font-bold mb-1">
              Data Sovereignty
            </div>
            <div className={`text-xl sm:text-2xl font-black font-mono tracking-tight ${
              modelMode === 'lightspeed' ? 'text-ls-cyan' : 'text-zinc-400'
            }`}>
              {modelMode === 'lightspeed' ? 'Air-Gapped On-Soil' : 'Cloud SaaS Leakage'}
            </div>
            <div className="text-[11px] text-zinc-400 mt-1 font-medium">
              {modelMode === 'lightspeed' ? 'Zero third-party exfiltration' : 'Exposed to foreign jurisdictions'}
            </div>
          </div>

          <div className={`p-3.5 rounded-2xl border transition-all ${
            modelMode === 'lightspeed'
              ? isLight ? 'bg-sky-50/70 border-sky-200' : 'bg-sky-950/20 border-sky-500/30'
              : isLight ? 'bg-slate-100 border-slate-200' : 'bg-ls-navy border-white/10'
          }`}>
            <div className="text-[10px] font-mono tracking-wider text-zinc-500 font-bold mb-1">
              Capital Efficiency
            </div>
            <div className={`text-xl sm:text-2xl font-black font-mono tracking-tight ${
              modelMode === 'lightspeed' ? 'text-sky-500' : 'text-ls-cyan'
            }`}>
              {modelMode === 'lightspeed' ? 'No Consulting Bloat' : 'High-Cost Retainers'}
            </div>
            <div className="text-[11px] text-zinc-400 mt-1 font-medium">
              {modelMode === 'lightspeed' ? 'Zero consulting bloat' : 'High cost with zero code delivery'}
            </div>
          </div>
        </div>
      </div>

      {/* Main Interactive Stage Demonstration Frame */}
      <div className={`p-6 sm:p-8 rounded-3xl border relative overflow-hidden transition-all duration-300 ${
        modelMode === 'traditional'
          ? isLight
            ? 'bg-ls-cyan/40 border-ls-cyan/80 shadow-2xl text-slate-900'
            : 'bg-ls-navy border-ls-cyan/20 shadow-2xl text-zinc-400'
          : isLight
            ? 'bg-white/95 border-slate-300 shadow-2xl text-slate-900'
            : 'bg-ls-navy border-white/15 shadow-2xl text-zinc-400'
      }`}>
        {/* Subtle architectural background grid */}
        <div className="absolute inset-0 pointer-events-none opacity-[0.03] bg-grain" />

        {/* TOP ROW: 3D Spatial Canvas Stage */}
        <div className="relative w-full h-64 sm:h-72 rounded-2xl overflow-hidden border border-white/10 bg-gradient-to-b from-ls-navy to-ls-navy mb-8">
          <div ref={mountRef} className="w-full h-full cursor-grab active:cursor-grabbing" />

          {/* Canvas Floating Stage Badge */}
          <div className="absolute top-3 left-3 z-10 flex flex-wrap items-center gap-2 px-3 py-1.5 rounded-full bg-black/70 border border-white/15 backdrop-blur-md text-[11px] font-mono">
            <span className={`w-2 h-2 rounded-full ${modelMode === 'lightspeed' ? 'tactile-pip-active' : 'bg-ls-cyan shadow-[0_0_6px_rgba(0,191,255,0.9)]'}`} />
            <span className={`font-bold ${modelMode === 'lightspeed' ? 'text-ls-red' : 'text-ls-cyan'}`}>
              STAGE 0{currentStage.step} / 06
            </span>
            <span className="text-zinc-400">•</span>
            <span className="text-white font-medium">{currentStage.title.toUpperCase()}</span>
            <span className="text-zinc-500 hidden sm:inline">|</span>
            <span className={`text-[10px] font-bold hidden sm:inline ${
              modelMode === 'lightspeed' ? 'text-ls-cyan' : 'text-ls-cyan'
            }`}>
              {modelMode === 'lightspeed' ? 'CLOSED-LOOP PIPELINE' : 'FRAGMENTED BATCH SILO'}
            </span>
          </div>

          {/* Stepper Transport Controls Deck (Analog Hardware Audio Transport) */}
          <div className="absolute top-3 right-3 z-10 flex items-center gap-1.5 p-1 rounded-full tactile-chassis-dark">
            {/* Live Audit Record Indicator */}
            <div className="hidden sm:flex items-center gap-1 px-2 py-1 rounded-full bg-black/40 border border-white/10 text-[9px] font-mono text-zinc-400">
              <span className={`w-1.5 h-1.5 rounded-full ${modelMode === 'lightspeed' ? 'bg-rose-500 animate-pulse shadow-[0_0_6px_rgba(244,63,94,0.9)]' : 'bg-ls-cyan'}`} />
              <span>{modelMode === 'lightspeed' ? 'DAG REC' : 'MANUAL'}</span>
            </div>

            {/* Prev Step */}
            <button
              onClick={() => {
                setActiveStepIndex(prev => (prev > 0 ? prev - 1 : STAGES.length - 1));
                setIsPlaying(false);
              }}
              className="p-1.5 rounded-full tactile-btn-inactive-dark text-zinc-300 hover:text-white transition-all cursor-pointer"
              title="Previous Stage"
            >
              <span className="text-[10px] font-mono font-bold px-0.5">◀</span>
            </button>

            {/* Play / Pause Toggle */}
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className={`px-3 py-1 rounded-full transition-all duration-200 cursor-pointer flex items-center gap-1.5 ${
                isPlaying ? 'tactile-btn-active-dark text-ls-red' : 'tactile-btn-inactive-dark text-white'
              }`}
              title={isPlaying ? 'Pause Auto-Walkthrough' : 'Play Auto-Walkthrough'}
            >
              <span className={`w-1.5 h-1.5 rounded-full transition-all duration-300 ${
                isPlaying ? 'tactile-pip-active' : 'tactile-pip-inactive-dark'
              }`} />
              <span className="font-mono text-[10px] font-bold">{isPlaying ? 'PAUSE' : 'PLAY'}</span>
            </button>

            {/* Next Step */}
            <button
              onClick={() => {
                setActiveStepIndex(prev => (prev < STAGES.length - 1 ? prev + 1 : 0));
                setIsPlaying(false);
              }}
              className="p-1.5 rounded-full tactile-btn-inactive-dark text-zinc-300 hover:text-white transition-all cursor-pointer"
              title="Next Stage"
            >
              <span className="text-[10px] font-mono font-bold px-0.5">▶</span>
            </button>

            {/* Reset */}
            <button
              onClick={() => {
                setActiveStepIndex(0);
                setIsPlaying(false);
              }}
              className="p-1.5 rounded-full tactile-btn-inactive-dark text-zinc-300 hover:text-white transition-all cursor-pointer"
              title="Reset to Stage 1"
            >
              <RotateCcw className="w-3 h-3" />
            </button>
          </div>

          {/* Bottom Canvas Quick Indicator */}
          <div className="absolute bottom-3 inset-x-3 z-10 px-3 py-1.5 rounded-xl bg-black/60 border border-white/10 backdrop-blur-md flex items-center justify-between text-[11px] font-mono text-[#2D3748]">
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-ls-cyan animate-pulse" />
              <span className="text-white font-bold">3D INFOGRAPHIC STAGE TOPOLOGY</span>
              <span className="hidden sm:inline text-[#2D3748]">• Click any 01-06 3D capsule or dock below to navigate</span>
            </div>
            <span className="text-ls-cyan font-bold">STAGE 0{activeStepIndex + 1} / 06</span>
          </div>
        </div>

        {/* NUMBERED WAVE GLASS EFFECT SPHERES DECK (1 TO 6) */}
        <div className="mb-5">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-2">
              <span className="font-mono text-xs font-bold tracking-wider text-ls-red flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-ls-red animate-ping" />
                NUMBERED WAVE GLASS SPHERES (1 TO 6)
              </span>
              <span className="text-xs text-[#2D3748] font-mono hidden sm:inline">| Real-Time Closed-Loop Stages</span>
            </div>
            <span className="text-[10px] font-mono px-2 py-0.5 rounded-full border bg-slate-100 text-[#2D3748] border-slate-300">
              INTERACTIVE COGNITIVE TOPOLOGY
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5">
            {STAGES.map((s, idx) => {
              const isActive = idx === activeStepIndex;
              const isPassed = idx < activeStepIndex;
              return (
                <button
                  key={s.id}
                  onClick={() => {
                    setActiveStepIndex(idx);
                    setIsPlaying(false);
                  }}
                  className={`group relative py-2 px-2.5 rounded-xl border transition-all duration-300 cursor-pointer flex flex-col items-center text-center overflow-hidden ${
                    isActive
                      ? isLight
                        ? 'bg-gradient-to-b from-orange-50/90 to-amber-100/70 border-ls-red shadow-md shadow-ls-red/15 scale-[1.02]'
                        : 'bg-gradient-to-b from-orange-950/40 to-ls-navy border-ls-red/80 shadow-lg shadow-ls-red/20 scale-[1.02]'
                      : isLight
                        ? 'bg-white/90 hover:bg-slate-50/90 border-slate-300/80 hover:border-ls-red/50'
                        : 'bg-ls-navy hover:bg-ls-navy border-white/10 hover:border-white/20'
                  }`}
                >
                  {/* Glowing Caustic Light Accent for Active Sphere */}
                  {isActive && (
                    <div className="absolute -top-4 -right-4 w-12 h-12 bg-ls-red/20 rounded-full blur-lg pointer-events-none" />
                  )}

                  {/* 3D Wave Glass Effect Sphere (1 to 6) */}
                  <div className="relative mb-1.5 flex items-center justify-center">
                    {/* Animated Concentric Wave Ripple Ring for Active Sphere */}
                    {isActive && (
                      <div className="wave-glass-ripple-active" />
                    )}

                    {/* The Wave Glass Sphere Orb */}
                    <div className={`w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center transition-all duration-300 relative ${
                      isActive
                        ? 'wave-glass-sphere-active'
                        : isLight
                          ? 'wave-glass-sphere-inactive-light group-hover:scale-105'
                          : 'wave-glass-sphere-inactive-dark group-hover:scale-105'
                    }`}>
                      {/* Crisp Bold Numeral 1-6 */}
                      <span className={`font-black text-xs sm:text-sm font-mono tracking-tighter ${
                        isActive
                          ? 'text-white drop-shadow-[0_1px_2px_rgba(0,0,0,0.8)]'
                          : isLight
                            ? 'text-slate-900'
                            : 'text-zinc-200'
                      }`}>
                        {s.step}
                      </span>
                    </div>
                  </div>

                  {/* Stage Title and Sub-label */}
                  <span className={`text-[11px] font-bold tracking-tight font-display transition-colors leading-tight line-clamp-1 ${
                    isActive
                      ? 'text-ls-red'
                      : isLight
                        ? 'text-slate-900 group-hover:text-ls-red'
                        : 'text-zinc-200 group-hover:text-white'
                  }`}>
                    {s.title}
                  </span>

                  <span className={`text-[9px] font-mono leading-tight mt-0.5 ${
                    isActive
                      ? isLight ? 'text-slate-800 font-semibold' : 'text-zinc-300'
                      : isLight ? 'text-slate-700' : 'text-zinc-400'
                  }`}>
                    {idx === 0 ? 'Fiduciary' : idx === 1 ? 'Sovereign' : idx === 2 ? 'HITL Gate' : idx === 3 ? 'Agent DAG' : idx === 4 ? 'Settlement' : 'Yield Audit'}
                  </span>

                  {/* Status Pip */}
                  <div className="mt-1 flex items-center gap-1">
                    <span className={`w-1.5 h-1.5 rounded-full ${
                      isActive
                        ? 'bg-ls-red shadow-[0_0_6px_rgba(230,57,70,1)] animate-pulse'
                        : isPassed
                          ? 'bg-ls-cyan'
                          : 'bg-zinc-600'
                    }`} />
                    <span className={`text-[8px] font-mono font-bold ${
                      isLight ? 'text-slate-700' : 'text-zinc-400'
                    }`}>
                      {isActive ? 'ACTIVE' : isPassed ? 'COMPLETE' : 'STANDBY'}
                    </span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* BOTTOM ROW: Deep Stage Breakdown & Architectural Blueprint */}
        <div className="space-y-6">

          {/* Stage Header Banner */}
          <div className={`p-5 rounded-2xl border flex flex-col md:flex-row md:items-center justify-between gap-4 ${
            isLight ? 'bg-slate-50/90 border-slate-300' : 'bg-ls-navy border-white/10'
          }`}>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className={`px-2.5 py-0.5 rounded-full border text-[11px] font-mono font-bold tracking-wider ${
                  modelMode === 'lightspeed'
                    ? 'bg-ls-red/15 text-ls-red border-ls-red/30'
                    : 'bg-ls-cyan/15 text-ls-cyan border-ls-cyan/30'
                }`}>
                  STAGE 0{currentStage.step} OF 06
                </span>
                <span className="text-zinc-500 font-mono text-xs">•</span>
                <span className="text-xs font-mono text-ls-red tracking-wider font-bold">
                  {currentStage.subtitle}
                </span>
              </div>
              <h4 className={`text-2xl sm:text-3xl font-black tracking-tight font-display ${
                isLight ? 'text-slate-900' : 'text-white'
              }`}>
                {currentStage.title}
              </h4>
            </div>

            <div className="text-xs font-mono flex items-center gap-3">
              <div className="text-right">
                <span className="text-zinc-500 block text-[10px]">Active Stage Mode</span>
                <span className={`font-bold ${modelMode === 'lightspeed' ? 'text-ls-cyan' : 'text-ls-cyan'}`}>
                  {modelMode === 'lightspeed' ? 'CLOSED-LOOP TOPOLOGY' : 'DISCONNECTED BATCH SILO'}
                </span>
              </div>
            </div>
          </div>

          {/* Side-by-Side Paradigm Contrast & Architectural Breakdown */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">

            {/* Left Column: Side-by-Side Operating Realities (7 cols) */}
            <div className="lg:col-span-7 space-y-5">

              {/* Core Description */}
              <p className={`text-justify text-sm sm:text-base leading-relaxed ${
                isLight ? 'text-slate-700 font-medium' : 'text-zinc-300'
              }`}>
                {currentStage.description}
              </p>

              {/* Side-by-Side Comparison Cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                {/* LIGHTSPEED AI-Native Card */}
                <div className={`p-4 rounded-2xl border transition-all ${
                  modelMode === 'lightspeed'
                    ? isLight
                      ? 'bg-orange-50/80 border-ls-red/80 shadow-md ring-1 ring-ls-red/20'
                      : 'bg-orange-950/25 border-ls-red/50 shadow-lg shadow-orange-950/30'
                    : isLight
                      ? 'bg-white/60 border-slate-200 opacity-75'
                      : 'bg-ls-navy border-white/5 opacity-70'
                }`}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="inline-flex items-center gap-1.5 text-xs font-mono font-bold tracking-wider text-ls-red">
                      <Zap className="w-3.5 h-3.5" />
                      LIGHTSPEED Closed Loop
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-ls-cyan/15 text-ls-cyan border border-ls-cyan/30 font-bold">
                      PROVABLE
                    </span>
                  </div>
                  <p className={`text-justify text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-slate-800' : 'text-zinc-200'
                  }`}>
                    {currentStage.lightspeed}
                  </p>

                  {/* Verified Output Artifacts */}
                  <div className="mt-3 pt-3 border-t border-ls-red/20 space-y-1.5">
                    <span className="text-[10px] font-mono tracking-wider text-ls-red font-bold block">
                      Deterministic Output Artifacts:
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {currentStage.artifacts.map((art, aIdx) => (
                        <span
                          key={aIdx}
                          className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg border border-ls-cyan/30 bg-ls-cyan/10 text-[11px] font-mono text-ls-cyan font-medium"
                        >
                          <CheckCircle2 className="w-3 h-3 shrink-0" />
                          <span>{art}</span>
                        </span>
                      ))}
                    </div>
                  </div>
                </div>

                {/* Traditional Consulting Card */}
                <div className={`p-4 rounded-2xl border transition-all ${
                  modelMode === 'traditional'
                    ? isLight
                      ? 'bg-ls-cyan/90 border-ls-cyan shadow-md ring-1 ring-ls-cyan/20'
                      : 'bg-amber-950/30 border-ls-cyan/50 shadow-lg shadow-amber-950/30'
                    : isLight
                      ? 'bg-white/60 border-slate-200 opacity-75'
                      : 'bg-ls-navy border-white/5 opacity-70'
                }`}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="inline-flex items-center gap-1.5 text-xs font-mono font-bold tracking-wider text-ls-cyan">
                      <Clock className="w-3.5 h-3.5" />
                      Traditional Consulting Trap
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-400 border border-rose-500/30 font-bold">
                      HIGH FRICTION
                    </span>
                  </div>
                  <p className={`text-justify text-xs sm:text-sm leading-relaxed ${
                    isLight ? 'text-slate-800' : 'text-zinc-300'
                  }`}>
                    {currentStage.traditional}
                  </p>

                  {/* Core Failure Mode Highlight */}
                  <div className="mt-3 pt-3 border-t border-ls-cyan/20 space-y-1.5">
                    <span className="text-[10px] font-mono tracking-wider text-rose-400 font-bold block">
                      Core Institutional Bottleneck:
                    </span>
                    <p className="text-justify text-[11px] leading-relaxed text-rose-400 font-mono">
                      {currentStage.traditionalProblem}
                    </p>
                  </div>
                </div>

              </div>

              {/* 4-Pillar Stage Verification Matrix */}
              <div className={`p-4 rounded-2xl border ${
                isLight ? 'bg-slate-50/70 border-slate-200' : 'bg-ls-navy border-white/10'
              }`}>
                <div className="text-xs font-mono tracking-wider text-zinc-500 font-bold mb-3 flex items-center justify-between">
                  <span>Stage 0{currentStage.step} Closed-Loop Verification Pipeline</span>
                  <span className="text-ls-red text-[10px]">End-to-End AST Proof</span>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="flex items-start gap-2.5">
                    <div className="w-5 h-5 rounded-md bg-ls-red/15 text-ls-red flex items-center justify-center shrink-0 font-mono text-[10px] font-bold">
                      01
                    </div>
                    <div>
                      <span className="font-bold font-mono text-zinc-300 block text-[11px]">
                        Fiduciary Mandate Ingestion
                      </span>
                      <span className="text-[11px] text-zinc-400">
                        Board governance and statutory guidelines compiled to machine-readable rules.
                      </span>
                    </div>
                  </div>

                  <div className="flex items-start gap-2.5">
                    <div className="w-5 h-5 rounded-md bg-ls-red/15 text-ls-red flex items-center justify-center shrink-0 font-mono text-[10px] font-bold">
                      02
                    </div>
                    <div>
                      <span className="font-bold font-mono text-zinc-300 block text-[11px]">
                        Bounded Agent DAGs (7 Tools)
                      </span>
                      <span className="text-[11px] text-zinc-400">
                        Constrained execution via canonical tools (read, edit, grep, list, bash, webfetch, task).
                      </span>
                    </div>
                  </div>

                  <div className="flex items-start gap-2.5">
                    <div className="w-5 h-5 rounded-md bg-ls-red/15 text-ls-red flex items-center justify-center shrink-0 font-mono text-[10px] font-bold">
                      03
                    </div>
                    <div>
                      <span className="font-bold font-mono text-zinc-300 block text-[11px]">
                        Cryptographic HITL Approval
                      </span>
                      <span className="text-[11px] text-zinc-400">
                        Zero automated drift; transactions signed with mathematical governance gates.
                      </span>
                    </div>
                  </div>

                  <div className="flex items-start gap-2.5">
                    <div className="w-5 h-5 rounded-md bg-ls-red/15 text-ls-red flex items-center justify-center shrink-0 font-mono text-[10px] font-bold">
                      04
                    </div>
                    <div>
                      <span className="font-bold font-mono text-zinc-300 block text-[11px]">
                        Real-Time Production Settlement
                      </span>
                      <span className="text-[11px] text-zinc-400">
                        Direct API integration into core ERPs, payment rails, and customs ledgers.
                      </span>
                    </div>
                  </div>
                </div>
              </div>

            </div>

            {/* Right Column: Quantitative Telemetry & Regional Proof (5 cols) */}
            <div className="lg:col-span-5 space-y-4">

              {/* Primary KPI Card (Reacts to Model Mode) */}
              <div className={`p-5 rounded-2xl border transition-all ${
                modelMode === 'lightspeed'
                  ? isLight ? 'bg-slate-50 border-slate-300' : 'bg-ls-navy border-white/15 shadow-xl'
                  : isLight ? 'bg-ls-cyan/80 border-ls-cyan' : 'bg-amber-950/20 border-ls-cyan/30'
              }`}>
                <div className="flex items-center justify-between text-xs font-mono text-zinc-500 font-semibold mb-1">
                  <span>
                    {modelMode === 'lightspeed'
                      ? currentStage.telemetry.metric.toUpperCase()
                      : currentStage.telemetry.traditionalMetric.toUpperCase()}
                  </span>
                  <span className={`font-bold ${
                    modelMode === 'lightspeed' ? 'text-ls-cyan' : 'text-rose-400'
                  }`}>
                    {modelMode === 'lightspeed'
                      ? currentStage.telemetry.delta
                      : currentStage.telemetry.traditionalDelta}
                  </span>
                </div>

                <div className={`text-3xl sm:text-4xl font-black font-mono tracking-tight my-1 ${
                  modelMode === 'lightspeed'
                    ? isLight ? 'text-slate-900' : 'text-white'
                    : 'text-ls-cyan'
                }`}>
                  {modelMode === 'lightspeed'
                    ? currentStage.telemetry.value
                    : currentStage.telemetry.traditionalValue}
                </div>

                <div className="text-[11px] text-zinc-500 font-medium">
                  {modelMode === 'lightspeed'
                    ? 'Audited against institutional production benchmarks'
                    : 'Traditional consulting industry baseline (Slide decks / Siloed teams)'}
                </div>
              </div>

              {/* Verified SADC / Africa Enterprise Scenarios */}
              <div className={`p-5 rounded-2xl border ${
                isLight ? 'bg-slate-50 border-slate-300' : 'bg-ls-navy border-white/15'
              }`}>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-xs font-mono tracking-wider text-zinc-500 font-bold">
                    Regional Vertical Scenarios
                  </span>
                  <span className="text-[10px] font-mono text-ls-red font-bold">VERT-01..07 MAP</span>
                </div>

                {/* Case Tabs (Tactile Segmented Radio) */}
                <div className={`flex items-center p-1 rounded-xl gap-1 mb-3 ${
                  isLight ? 'tactile-chassis-light' : 'tactile-chassis-dark'
                }`}>
                  {USE_CASES.map((uc, idx) => {
                    const isSelected = selectedUseCase === idx;
                    return (
                      <button
                        key={uc.id}
                        onClick={() => setSelectedUseCase(idx)}
                        className={`flex-1 py-1.5 px-2 rounded-lg text-[10px] font-mono font-bold transition-all duration-200 cursor-pointer truncate flex items-center justify-center gap-1.5 ${
                          isSelected
                            ? isLight ? 'tactile-btn-active-light text-slate-900' : 'tactile-btn-active-dark text-white'
                            : isLight ? 'tactile-btn-inactive-light text-slate-600' : 'tactile-btn-inactive-dark text-zinc-400'
                        }`}
                      >
                        <span className={`w-1.5 h-1.5 rounded-full shrink-0 transition-all duration-300 ${
                          isSelected ? 'tactile-pip-active' : isLight ? 'tactile-pip-inactive-light' : 'tactile-pip-inactive-dark'
                        }`} />
                        <span className="truncate">{uc.name}</span>
                      </button>
                    );
                  })}
                </div>

                {/* Active Use Case Highlight */}
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    {React.createElement(USE_CASES[selectedUseCase].icon, { className: 'w-4 h-4 text-ls-red shrink-0' })}
                    <div className={`text-xs font-bold leading-tight ${isLight ? 'text-slate-900' : 'text-zinc-100'}`}>
                      {USE_CASES[selectedUseCase].headline}
                    </div>
                  </div>
                  <p className={`text-justify text-xs leading-relaxed font-normal ${isLight ? 'text-slate-700' : 'text-zinc-400'}`}>
                    {modelMode === 'lightspeed'
                      ? USE_CASES[selectedUseCase].solution
                      : USE_CASES[selectedUseCase].challenge}
                  </p>
                </div>
              </div>

              {/* Call to Action Button */}
              {onRequestBriefing && (
                <button
                  onClick={onRequestBriefing}
                  className="w-full py-3.5 px-5 rounded-full font-bold text-xs tracking-widest bg-ls-red hover:bg-ls-red text-white shadow-lg shadow-ls-red/25 transition-all flex items-center justify-center gap-2 cursor-pointer group"
                >
                  <span>Request Operating Model Briefing</span>
                  <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
                </button>
              )}

            </div>

          </div>

        </div>

      </div>
    </div>
  );
};
