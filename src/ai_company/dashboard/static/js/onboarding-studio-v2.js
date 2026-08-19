/* ═══════════════════════════════════════════════════════════════
   Light Speed Holdings — Agent Onboarding Studio v2
   Alpine.js component: registry-first UI for agent provisioning

   Features:
     1. Persona template selection grid (Executive, Leader, Dept Head, Specialist, Scratch)
     2. Multi-step wizard (Identity → Capabilities → Permissions → Reporting → Preview & Generate)
     3. Preview panel (generated YAML + generated markdown + diff view)
     4. Generate action (POST /api/v1/onboarding/generate)
     5. Regeneration sync (status indicator, last-regen time, diff of changes)

   Design tokens: uses J.A.R.V.I.S. CSS variables from control-plane-theme.css.
   No new dependencies beyond Alpine.js + Tailwind CSS.
   ═══════════════════════════════════════════════════════════════ */

function onboardingStudioV2() {
  return {
    // ── Wizard State ───────────────────────────────────────────
    currentStep: 0,          // 0 = template picker, 1-4 = wizard steps, 5 = post-generate
    steps: [
      { id: 'identity',       label: 'Identity',       icon: 'user' },
      { id: 'capabilities',   label: 'Capabilities',   icon: 'wrench' },
      { id: 'permissions',    label: 'Permissions',    icon: 'shield' },
      { id: 'reporting',      label: 'Reporting',      icon: 'org' },
      { id: 'preview',        label: 'Preview & Generate', icon: 'eye' },
    ],

    // ── Template Grid ──────────────────────────────────────────
    templates: [
      {
        id: 'executive',
        label: 'Executive',
        icon: 'crown',
        description: 'C-suite / VP level. High-level strategy, delegation, KPIs.',
        color: 'amber',
        defaults: {
          type: 'executive',
          seniority: 'senior',
          tools: ['read', 'edit', 'bash', 'webfetch'],
          tier: 3,
        },
      },
      {
        id: 'leader',
        label: 'Leader',
        icon: 'users',
        description: 'Department lead. Cross-team coordination, planning, reporting.',
        color: 'cyan',
        defaults: {
          type: 'specialist',
          seniority: 'senior',
          tools: ['read', 'edit', 'bash', 'grep', 'list'],
          tier: 2,
        },
      },
      {
        id: 'department',
        label: 'Department Head',
        icon: 'building',
        description: 'Owns a functional department. Deep domain, team oversight.',
        color: 'purple',
        defaults: {
          type: 'department',
          seniority: 'mid',
          tools: ['read', 'edit', 'bash', 'grep', 'list', 'webfetch'],
          tier: 2,
        },
      },
      {
        id: 'specialist',
        label: 'Specialist',
        icon: 'cpu',
        description: 'Domain expert. Focused deliverables, well-scoped permissions.',
        color: 'emerald',
        defaults: {
          type: 'specialist',
          seniority: 'mid',
          tools: ['read', 'edit', 'grep', 'list', 'bash'],
          tier: 1,
        },
      },
      {
        id: 'scratch',
        label: 'Start from Scratch',
        icon: 'plus',
        description: 'Blank slate. Define everything from zero.',
        color: 'slate',
        defaults: {
          type: 'specialist',
          seniority: 'mid',
          tools: [],
          tier: 1,
        },
      },
    ],
    selectedTemplate: null,

    // ── Form Model (synced to registry YAML schema) ────────────
    form: {
      // Identity
      id: '',
      name: '',
      title: '',
      description: '',
      type: 'specialist',          // executive | specialist | department | board | default
      department: '',
      seniority: 'mid',            // junior | mid | senior | executive
      hitl_tier: 1,

      // Capabilities
      tools: [],                   // canonical: read, edit, grep, list, bash, webfetch, task
      template: '',                // optional Jinja2 template override
      responsibilities: [],        // newline-separated in textarea → array
      guidelines: '',              // plain string (matches registry YAML / onboarding service)

      // Permissions (matched to tool permission map)
      permissions: {
        read:   { enabled: true,  paths: [] },
        edit:   { enabled: false, paths: [] },
        bash:   { enabled: false, patterns: [] },
        grep:   { enabled: true,  paths: [] },
        list:   { enabled: true,  paths: [] },
        webfetch: { enabled: false },
        task:   { enabled: false },
      },

      // Reporting
      reports_to: '',              // agent id
      direct_reports: [],          // newline-separated agent ids
    },

    // ── Preview State ──────────────────────────────────────────
    previewTab: 'yaml',            // yaml | markdown | diff
    previewYaml: '',               // generated registry entry YAML
    previewMarkdown: '',           // generated .opencode/agents/*.md
    previewDiff: '',               // unified diff of changes (update mode)
    isGenerating: false,
    generateError: '',
    generateResult: null,          // { agent_id, files_changed, status }

    // ── Regeneration Sync ──────────────────────────────────────
    regenStatus: 'idle',           // idle | regenerating | done | error
    regenLastTime: null,
    regenChanges: null,            // { added: [], modified: [], removed: [] }
    showRegenPanel: false,

    // ── Registry Agents (for dropdowns) ────────────────────────
    registryAgents: [],

    // ── UI State ───────────────────────────────────────────────
    loading: false,
    showWizard: false,             // false = show template grid, true = show wizard
    toasts: [],

    // ── Canonical Tool Map (mirrors generator.py _TOOL_MAP) ────
    TOOL_MAP: {
      read:     { label: 'Read',     category: 'filesystem', description: 'Read file contents' },
      edit:     { label: 'Edit',     category: 'filesystem', description: 'Exact string replacement in files' },
      grep:     { label: 'Grep',     category: 'filesystem', description: 'Search file contents with regex' },
      list:     { label: 'List',     category: 'filesystem', description: 'List directory entries' },
      bash:     { label: 'Bash',     category: 'execution',  description: 'Execute shell commands' },
      webfetch: { label: 'Web Fetch',category: 'network',    description: 'Fetch web content (HTTP/HTTPS)' },
      task:     { label: 'Task',     category: 'delegation', description: 'Launch sub-agent for complex work' },
    },
    ALL_TOOLS: ['read', 'edit', 'grep', 'list', 'bash', 'webfetch', 'task'],

    // Agent types from models.py
    AGENT_TYPES: ['executive', 'specialist', 'department', 'board', 'default'],
    SENIORITY_LEVELS: ['junior', 'mid', 'senior', 'executive'],
    HITL_TIERS: [1, 2, 3, 4, 5],

    // Departments derived from registry (populated on init)
    departments: [],

    // ── Lifecycle ──────────────────────────────────────────────

    async init() {
      await this.loadRegistryAgents();
      this.parseUrlState();
    },

    destroy() {
      // No WS in this component; nothing to tear down
    },

    parseUrlState() {
      const params = new URLSearchParams(window.location.search);
      if (params.get('step')) {
        this.currentStep = parseInt(params.get('step'), 10) || 0;
        this.showWizard = this.currentStep > 0;
      }
      if (params.get('template')) {
        this.selectTemplate(params.get('template'));
      }
    },

    // ── Registry Loading ───────────────────────────────────────

    async loadRegistryAgents() {
      this.loading = true;
      try {
        const res = await fetch('/api/v1/onboarding');
        if (res.ok) {
          const data = await res.json();
          // Normalize: API may return array of requests or registry snapshot
          if (Array.isArray(data)) {
            this.registryAgents = data;
          } else if (data.agents) {
            this.registryAgents = data.agents;
          } else {
            this.registryAgents = [];
          }
          this.extractDepartments();
        }
      } catch (e) {
        console.warn('[Studio v2] Failed to load registry:', e);
      }
      this.loading = false;
    },

    extractDepartments() {
      const deptSet = new Set();
      this.registryAgents.forEach(a => {
        if (a.department) deptSet.add(a.department);
      });
      this.departments = Array.from(deptSet).sort();
    },

    // ── Template Selection ─────────────────────────────────────

    selectTemplate(templateId) {
      const tpl = this.templates.find(t => t.id === templateId);
      if (!tpl) return;
      this.selectedTemplate = tpl;

      // Apply defaults
      this.form.type = tpl.defaults.type;
      this.form.seniority = tpl.defaults.seniority;
      this.form.tools = [...tpl.defaults.tools];
      this.form.hitl_tier = tpl.defaults.tier;

      // Sync permission toggles
      this.ALL_TOOLS.forEach(tool => {
        this.form.permissions[tool] = this.form.permissions[tool] || {};
        this.form.permissions[tool].enabled = tpl.defaults.tools.includes(tool);
      });

      this.showWizard = true;
      this.currentStep = 1;
    },

    // ── Wizard Navigation ──────────────────────────────────────

    get canGoNext() {
      switch (this.currentStep) {
        case 1: return this.form.id.trim() && this.form.name.trim();
        case 2: return this.form.tools.length > 0;
        case 3: return true;  // permissions always valid
        case 4: return true;  // reporting always valid
        case 5: return false; // final step
        default: return true;
      }
    },

    get totalSteps() {
      return this.steps.length;
    },

    get progressPercent() {
      return Math.round((this.currentStep / this.totalSteps) * 100);
    },

    goNext() {
      if (this.canGoNext && this.currentStep < this.totalSteps) {
        this.currentStep++;
        if (this.currentStep === this.totalSteps) {
          this.generatePreview();
        }
      }
    },

    goPrev() {
      if (this.currentStep > 1) {
        this.currentStep--;
      }
    },

    goToStep(step) {
      if (step >= 1 && step <= this.totalSteps) {
        this.currentStep = step;
      }
    },

    // ── Tool Toggle ────────────────────────────────────────────

    toggleTool(tool) {
      const idx = this.form.tools.indexOf(tool);
      if (idx >= 0) {
        this.form.tools.splice(idx, 1);
      } else {
        this.form.tools.push(tool);
      }
      // Sync permission
      this.form.permissions[tool] = this.form.permissions[tool] || {};
      this.form.permissions[tool].enabled = this.form.tools.includes(tool);
    },

    hasTool(tool) {
      return this.form.tools.includes(tool);
    },

    // ── List Field Helpers (newline-separated → array) ──────────

    setList(field, text) {
      this.form[field] = text.split('\n').map(s => s.trim()).filter(Boolean);
    },

    getListText(field) {
      return (this.form[field] || []).join('\n');
    },

    // ── ID Slug Generator ──────────────────────────────────────

    generateSlug() {
      const name = this.form.name || '';
      this.form.id = name
        .toLowerCase()
        .replace(/[^a-z0-9]+/g, '-')
        .replace(/^-|-$/g, '')
        .substring(0, 64);
    },

    // ── Preview Generation (client-side mock) ──────────────────

    generatePreview() {
      this.previewYaml = this.buildRegistryYaml();
      this.previewMarkdown = this.buildAgentMarkdown();
      this.previewDiff = this.previewYaml ? this.buildDiffPreview() : '';
    },

    buildRegistryYaml() {
      const f = this.form;
      if (!f.id || !f.name) return '';

      const lines = [];
      lines.push(`  - id: "${f.id}"`);
      lines.push(`    name: "${f.name}"`);
      if (f.title) lines.push(`    title: "${f.title}"`);
      if (f.description) lines.push(`    description: "${f.description}"`);
      lines.push(`    type: ${f.type}`);
      if (f.department) lines.push(`    department: "${f.department}"`);
      if (f.seniority) lines.push(`    seniority: ${f.seniority}`);
      if (f.reports_to) lines.push(`    reports_to: "${f.reports_to}"`);
      if (f.direct_reports.length > 0) {
        lines.push(`    direct_reports:`);
        f.direct_reports.forEach(r => lines.push(`      - "${r}"`));
      }
      if (f.tools.length > 0) {
        lines.push(`    tools:`);
        f.tools.forEach(t => lines.push(`      - ${t}`));
      }
      if (f.responsibilities.length > 0) {
        lines.push(`    responsibilities:`);
        f.responsibilities.forEach(r => lines.push(`      - "${r}"`));
      }
      if (f.guidelines) {
        lines.push(`    guidelines: "${f.guidelines}"`);
      }
      lines.push(`    hitl_tier: ${f.hitl_tier}`);

      return lines.join('\n');
    },

    buildAgentMarkdown() {
      const f = this.form;
      if (!f.id || !f.name) return '';

      // Build permission map: normalize tools via TOOL_MAP, set "allow" for enabled
      const permLines = [];
      const normalized = new Set();
      this.form.tools.forEach(tool => {
        // Mirror generator.py _TOOL_MAP normalization
        const key = (tool === 'write') ? 'edit'
                  : (tool === 'execute') ? 'bash'
                  : (tool === 'web_search' || tool === 'websearch') ? 'webfetch'
                  : (tool === 'delegate') ? 'task'
                  : tool;
        normalized.add(key);
      });
      this.ALL_TOOLS.forEach(tool => {
        const action = normalized.has(tool) ? 'allow' : 'deny';
        permLines.push(`  ${tool}: ${action}`);
      });

      const md = [];
      md.push(`---`);
      md.push(`description: ${f.description || f.title || f.name}`);
      md.push(`mode: subagent`);
      md.push(`permission:`);
      md.push(permLines.join('\n'));
      md.push(`---`);
      md.push(``);
      md.push(`# ${f.name}`);
      md.push(``);
      md.push(`## Identity`);
      md.push(``);
      md.push(`Type: ${f.title || 'AI Agent'}`);
      md.push(``);
      if (f.department) {
        md.push(`Department: ${f.department}`);
        md.push(``);
      }
      if (f.reports_to) {
        md.push(`Reports To: ${f.reports_to}`);
        md.push(``);
      }
      if (f.direct_reports.length > 0) {
        md.push(`Direct Reports: ${f.direct_reports.join(', ')}`);
        md.push(``);
      }
      md.push(`---`);
      md.push(``);
      md.push(`## Mission`);
      md.push(``);
      md.push(f.description || 'Execute tasks efficiently and accurately.');
      md.push(``);
      md.push(`---`);
      md.push(``);
      md.push(`## Responsibilities`);
      md.push(``);
      if (f.responsibilities.length > 0) {
        f.responsibilities.forEach(r => md.push(`- ${r}`));
      } else {
        md.push(`- (No responsibilities defined)`);
      }
      md.push(``);
      md.push(`---`);
      md.push(``);
      md.push(`## Operating Guidelines`);
      md.push(``);
      md.push(f.guidelines || 'Maintain professional standards and execute tasks efficiently.');
      md.push(``);
      md.push(`---`);
      md.push(``);
      md.push(`## Success Metrics`);
      md.push(``);
      md.push(`- Task completion rate`);
      md.push(`- Response quality and accuracy`);
      md.push(`- Alignment with company goals`);
      md.push(`- Cost efficiency (for executing agents)`);

      return md.join('\n');
    },

    buildDiffPreview() {
      // Show what will be ADDED to the registry (new entry)
      const yaml = this.previewYaml;
      const lines = yaml.split('\n');
      return lines.map(l => `+ ${l}`).join('\n');
    },

    // ── Generate Action ────────────────────────────────────────

    async generateAgent() {
      this.isGenerating = true;
      this.generateError = '';
      this.generateResult = null;

      const payload = {
        agent_id: this.form.id,
        name: this.form.name,
        title: this.form.title,
        description: this.form.description,
        type: this.form.type,
        department: this.form.department,
        seniority: this.form.seniority,
        hitl_tier: this.form.hitl_tier,
        tools: this.form.tools,
        template: this.form.template || undefined,
        reports_to: this.form.reports_to || undefined,
        direct_reports: this.form.direct_reports.length > 0 ? this.form.direct_reports : undefined,
        responsibilities: this.form.responsibilities.length > 0 ? this.form.responsibilities : undefined,
        guidelines: this.form.guidelines || undefined,
        permissions: this.form.permissions,
      };

      try {
        const res = await fetch('/api/v1/onboarding/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        if (res.ok) {
          this.generateResult = await res.json();
          this.currentStep = this.totalSteps; // move to success state
          this.showToast('Agent generated successfully', 'success');
          await this.loadRegistryAgents();
        } else {
          const err = await res.json().catch(() => ({}));
          this.generateError = err.detail || `Generation failed (${res.status})`;
          this.showToast(this.generateError, 'error');
        }
      } catch (e) {
        this.generateError = e.message || 'Network error';
        this.showToast('Generation failed: ' + this.generateError, 'error');
      }

      this.isGenerating = false;
    },

    // ── Regeneration Sync ──────────────────────────────────────

    async regenerateAll() {
      this.regenStatus = 'regenerating';
      this.regenChanges = null;

      try {
        const res = await fetch('/api/v1/onboarding/regenerate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
        });

        if (res.ok) {
          const data = await res.json();
          this.regenStatus = 'done';
          this.regenLastTime = new Date().toISOString();
          this.regenChanges = data.changes || { added: [], modified: [], removed: [] };
          this.showToast(`Regeneration complete: ${this.regenSummary}`, 'success');
          await this.loadRegistryAgents();
        } else {
          const err = await res.json().catch(() => ({}));
          this.regenStatus = 'error';
          this.showToast(err.detail || 'Regeneration failed', 'error');
        }
      } catch (e) {
        this.regenStatus = 'error';
        this.showToast('Regeneration failed: ' + e.message, 'error');
      }
    },

    get regenSummary() {
      if (!this.regenChanges) return '';
      const a = this.regenChanges.added?.length || 0;
      const m = this.regenChanges.modified?.length || 0;
      const r = this.regenChanges.removed?.length || 0;
      const parts = [];
      if (a) parts.push(`${a} added`);
      if (m) parts.push(`${m} modified`);
      if (r) parts.push(`${r} removed`);
      return parts.join(', ') || 'no changes';
    },

    toggleRegenPanel() {
      this.showRegenPanel = !this.showRegenPanel;
      if (this.showRegenPanel && !this.regenLastTime) {
        this.regenerateAll();
      }
    },

    // ── Reset / New Agent ──────────────────────────────────────

    resetWizard() {
      this.currentStep = 0;
      this.showWizard = false;
      this.selectedTemplate = null;
      this.form = {
        id: '', name: '', title: '', description: '',
        type: 'specialist', department: '', seniority: 'mid', hitl_tier: 1,
        tools: [], template: '', responsibilities: [], guidelines: '',
        permissions: {
          read: { enabled: true, paths: [] },
          edit: { enabled: false, paths: [] },
          bash: { enabled: false, patterns: [] },
          grep: { enabled: true, paths: [] },
          list: { enabled: true, paths: [] },
          webfetch: { enabled: false },
          task: { enabled: false },
        },
        reports_to: '', direct_reports: [],
      };
      this.previewYaml = '';
      this.previewMarkdown = '';
      this.previewDiff = '';
      this.generateResult = null;
      this.generateError = '';
      window.history.replaceState({}, '', window.location.pathname);
    },

    // ── Preview Tab Helpers ────────────────────────────────────

    setPreviewTab(tab) {
      this.previewTab = tab;
    },

    copyPreviewToClipboard() {
      const text = this.previewTab === 'yaml' ? this.previewYaml
                 : this.previewTab === 'markdown' ? this.previewMarkdown
                 : this.previewDiff;
      if (text && navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
          this.showToast('Copied to clipboard', 'success');
        });
      }
    },

    // ── Toast Helpers ──────────────────────────────────────────

    showToast(message, type = 'info') {
      const id = Date.now();
      this.toasts.push({ id, message, type });
      setTimeout(() => {
        this.toasts = this.toasts.filter(t => t.id !== id);
      }, 4000);
    },

    // ── Template Card Styling ──────────────────────────────────

    templateColorClass(color, variant) {
      const map = {
        amber:  { bg: 'bg-amber-500/10',   border: 'border-amber-500/20',  active: 'bg-amber-500/20 border-amber-500/40',  text: 'text-amber-400',   icon: 'text-amber-400' },
        cyan:   { bg: 'bg-cyan-500/10',    border: 'border-cyan-500/20',   active: 'bg-cyan-500/20 border-cyan-500/40',    text: 'text-cyan-400',    icon: 'text-cyan-400' },
        purple: { bg: 'bg-purple-500/10',  border: 'border-purple-500/20', active: 'bg-purple-500/20 border-purple-500/40',text: 'text-purple-400',  icon: 'text-purple-400' },
        emerald:{ bg: 'bg-emerald-500/10', border: 'border-emerald-500/20',active: 'bg-emerald-500/20 border-emerald-500/40',text:'text-emerald-400', icon: 'text-emerald-400' },
        slate:  { bg: 'bg-slate-500/10',   border: 'border-slate-500/20',  active: 'bg-slate-500/20 border-slate-500/40',  text: 'text-slate-400',   icon: 'text-slate-400' },
      };
      const c = map[color] || map.slate;
      return variant === 'active' ? `${c.active} ${c.text}` : `${c.bg} ${c.border} ${c.text}`;
    },

    templateIconClass(color) {
      const map = {
        amber: 'text-amber-400', cyan: 'text-cyan-400', purple: 'text-purple-400',
        emerald: 'text-emerald-400', slate: 'text-slate-400',
      };
      return map[color] || map.slate;
    },

    // ── SVG Icon Helpers (inline) ──────────────────────────────

    getIcon(name) {
      const icons = {
        user:    `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>`,
        wrench:  `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.066 2.573c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.573 1.066c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.066-2.573c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>`,
        shield:  `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"/>`,
        org:     `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>`,
        eye:     `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/>`,
        crown:   `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3l4 3-4 3V3zm14 0l-4 3 4 3V3zM3 17h18v2H3v-2zm1-4l3-8h2l1 4h4l1-4h2l3 8H4z"/>`,
        users:   `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/>`,
        building:`<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>`,
        cpu:     `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z"/>`,
        plus:    `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>`,
        refresh: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>`,
        copy:    `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/>`,
        check:   `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>`,
        x:       `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>`,
        arrow_l: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>`,
        arrow_r: `<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/>`,
        download:`<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/>`,
      };
      return icons[name] || icons.plus;
    },

    icon(name, cls = 'w-5 h-5') {
      return `<svg class="${cls}" fill="none" stroke="currentColor" viewBox="0 0 24 24">${this.getIcon(name)}</svg>`;
    },
  };
}
