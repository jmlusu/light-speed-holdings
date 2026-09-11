/* ═══════════════════════════════════════════════════════════════
   Light Speed Holdings — Onboarding Studio
   Alpine.js component for the agent onboarding lifecycle UI
   ═══════════════════════════════════════════════════════════════ */

function onboardingStudio() {
  return {
    // ── State ─────────────────────────────────────────────────
    requests: [],
    loading: true,
    stateFilter: '',
    agentFilter: '',
    showRejectModal: false,
    rejectingRequest: null,
    rejectReason: '',
    wsConnection: null,

    // ── Lifecycle ─────────────────────────────────────────────

    async init() {
      await this.loadRequests();
      this.connectOnboardingWS();
    },

    destroy() {
      if (this.wsConnection) {
        try {
          this.wsConnection.onclose = null;
          this.wsConnection.close();
        } catch (_) { /* best-effort */ }
      }
    },

    // ── Computed ──────────────────────────────────────────────

    get filteredRequests() {
      return this.requests.filter(r => {
        if (this.stateFilter && r.state !== this.stateFilter) return false;
        if (this.agentFilter) {
          const q = this.agentFilter.toLowerCase();
          const matchId = (r.agent_id || '').toLowerCase().includes(q);
          const matchName = (r.name || '').toLowerCase().includes(q);
          const matchDept = (r.department || '').toLowerCase().includes(q);
          if (!matchId && !matchName && !matchDept) return false;
        }
        return true;
      });
    },

    get visibleStates() {
      return [
        'requested',
        'config_review',
        'security_review',
        'generating',
        'testing',
        'approval',
        'active',
      ];
    },

    // ── Data loading ──────────────────────────────────────────

    async loadRequests() {
      this.loading = true;
      try {
        const res = await fetch('/api/v1/onboarding');
        if (res.ok) {
          this.requests = await res.json();
        } else {
          console.warn('[Onboarding] API returned', res.status);
          this.requests = [];
        }
      } catch (e) {
        console.error('[Onboarding] Failed to load requests:', e);
        this.requests = [];
      }
      this.loading = false;
    },

    // ── Grouping / counting ───────────────────────────────────

    getRequestsByState(state) {
      return this.filteredRequests.filter(r => r.state === state);
    },

    countByState(state) {
      return this.requests.filter(r => r.state === state).length;
    },

    // ── Labels / styling ──────────────────────────────────────

    getStateLabel(state) {
      const labels = {
        requested:        'Requested',
        config_review:    'Config Review',
        security_review:  'Security Review',
        generating:       'Generating',
        testing:          'Testing',
        approval:         'Pending Approval',
        active:           'Active',
        rejected:         'Rejected',
        failed:           'Failed',
        archived:         'Archived',
      };
      return labels[state] || state;
    },

    getStateClass(state) {
      const classes = {
        requested:       'bg-blue-500/15 text-blue-400',
        config_review:   'bg-purple-500/15 text-purple-400',
        security_review: 'bg-yellow-500/15 text-yellow-400',
        generating:      'bg-cyan-500/15 text-cyan-400',
        testing:         'bg-indigo-500/15 text-indigo-400',
        approval:        'bg-amber-500/15 text-amber-400',
        active:          'bg-emerald-500/15 text-emerald-400',
      };
      return classes[state] || 'bg-surface-700/50 text-slate-400';
    },

    getTierClass(tier) {
      if (tier >= 3) return 'bg-red-500/15 text-red-400';
      if (tier >= 2) return 'bg-amber-500/15 text-amber-400';
      return 'bg-emerald-500/15 text-emerald-400';
    },

    getProgress(req) {
      const stateProgress = {
        requested:       10,
        config_review:   20,
        security_review: 30,
        generating:      60,
        testing:         80,
        approval:        90,
        active:          100,
      };
      return stateProgress[req.state] || 0;
    },

    // ── Time formatting ───────────────────────────────────────

    formatTime(isoString) {
      if (!isoString) return '--';
      const date = new Date(isoString);
      const now = new Date();
      const diffMs = now - date;
      const diffSecs = Math.floor(diffMs / 1000);
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      if (diffSecs < 60) return 'just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 30) return `${diffDays}d ago`;
      return date.toLocaleDateString();
    },

    // ── Actions ───────────────────────────────────────────────

    async approveRequest(id) {
      try {
        const res = await fetch(`/api/v1/onboarding/${id}/approve`, {
          method: 'POST',
        });
        if (res.ok) {
          await this.loadRequests();
          if (typeof showToast === 'function') {
            showToast('Request approved', 'success');
          }
        } else {
          const err = await res.json().catch(() => ({}));
          if (typeof showToast === 'function') {
            showToast(err.detail || 'Failed to approve request', 'error');
          }
        }
      } catch (e) {
        console.error('[Onboarding] Approve failed:', e);
        if (typeof showToast === 'function') {
          showToast('Failed to approve request', 'error');
        }
      }
    },

    confirmReject(req) {
      this.rejectingRequest = req;
      this.rejectReason = '';
      this.showRejectModal = true;
    },

    async rejectRequest() {
      if (!this.rejectingRequest) return;
      try {
        const res = await fetch(`/api/v1/onboarding/${this.rejectingRequest.id}/reject`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reason: this.rejectReason }),
        });
        if (res.ok) {
          this.showRejectModal = false;
          await this.loadRequests();
          if (typeof showToast === 'function') {
            showToast('Request rejected', 'success');
          }
        } else {
          const err = await res.json().catch(() => ({}));
          if (typeof showToast === 'function') {
            showToast(err.detail || 'Failed to reject request', 'error');
          }
        }
      } catch (e) {
        console.error('[Onboarding] Reject failed:', e);
        if (typeof showToast === 'function') {
          showToast('Failed to reject request', 'error');
        }
      }
    },

    // ── WebSocket ─────────────────────────────────────────────

    connectOnboardingWS() {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const wsUrl = `${protocol}//${window.location.host}/ws/v1/dashboard?topics=onboarding`;

      try {
        this.wsConnection = new WebSocket(wsUrl);
      } catch (e) {
        console.warn('[Onboarding] WS connection failed:', e);
        return;
      }

      this.wsConnection.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.type === 'onboarding_update') {
            this.loadRequests();
          }
        } catch (_) { /* ignore parse errors */ }
      };

      this.wsConnection.onclose = () => {
        // Reconnect after a delay
        setTimeout(() => this.connectOnboardingWS(), 5000);
      };

      this.wsConnection.onerror = () => {
        // onerror is always followed by onclose
      };
    },
  };
}
