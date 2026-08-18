/* Mission Control — Alpine.js component for workflow pipeline UI */

function missionControl() {
  return {
    /* State */
    workflows: [],
    instances: [],
    selectedWorkflow: '',
    selectedInstance: null,
    detail: {},
    starting: false,
    wsConnected: false,
    _pollInterval: null,

    /* Computed */
    get progressPercent() {
      const total = this.detail.total_steps || 1;
      return Math.round(((this.detail.completed_steps || 0) / total) * 100);
    },

    /* Init */
    async init() {
      await Promise.all([this.loadWorkflows(), this.loadInstances()]);
      this._pollInterval = setInterval(() => this.loadInstances(), 5000);
      this._connectWS();
    },

    /* API helpers */
    _api(path, opts) {
      return fetch('/api/v1' + path, {
        headers: { 'Content-Type': 'application/json' },
        ...opts,
      }).then(r => r.ok ? r.json() : Promise.reject(r));
    },

    async loadWorkflows() {
      try {
        this.workflows = await this._api('/workflows');
      } catch (e) {
        console.error('Failed to load workflows', e);
      }
    },

    async loadInstances() {
      try {
        this.instances = await this._api('/workflows/instances');
        /* Refresh detail if selected instance is still in the list */
        if (this.selectedInstance) {
          const stillExists = this.instances.some(i => i.instance_id === this.selectedInstance);
          if (stillExists) {
            await this.loadDetail(this.selectedInstance);
          } else {
            this.selectedInstance = null;
            this.detail = {};
          }
        }
      } catch (e) {
        console.error('Failed to load instances', e);
      }
    },

    async loadDetail(instanceId) {
      try {
        this.detail = await this._api('/workflows/instances/' + encodeURIComponent(instanceId));
      } catch (e) {
        console.error('Failed to load instance detail', e);
      }
    },

    async selectInstance(instanceId) {
      this.selectedInstance = instanceId;
      await this.loadDetail(instanceId);
    },

    async startWorkflow() {
      if (!this.selectedWorkflow) return;
      this.starting = true;
      try {
        const result = await this._api('/workflows/' + encodeURIComponent(this.selectedWorkflow) + '/start', {
          method: 'POST',
        });
        await this.loadInstances();
        if (result.instance_id) {
          await this.selectInstance(result.instance_id);
        }
        this.selectedWorkflow = '';
      } catch (e) {
        console.error('Failed to start workflow', e);
      } finally {
        this.starting = false;
      }
    },

    async advanceStep() {
      if (!this.selectedInstance) return;
      try {
        await this._api('/workflows/instances/' + encodeURIComponent(this.selectedInstance) + '/advance', {
          method: 'POST',
        });
        await this.loadInstances();
      } catch (e) {
        console.error('Failed to advance', e);
      }
    },

    async completeCurrentStep() {
      if (!this.selectedInstance) return;
      try {
        await this._api('/workflows/instances/' + encodeURIComponent(this.selectedInstance) + '/complete-step', {
          method: 'POST',
          body: JSON.stringify({ result: '' }),
        });
        await this.loadInstances();
      } catch (e) {
        console.error('Failed to complete step', e);
      }
    },

    async cancelInstance() {
      if (!this.selectedInstance) return;
      if (!confirm('Abort this workflow instance?')) return;
      try {
        await this._api('/workflows/instances/' + encodeURIComponent(this.selectedInstance) + '/cancel', {
          method: 'POST',
        });
        await this.loadInstances();
      } catch (e) {
        console.error('Failed to cancel', e);
      }
    },

    /* Formatting helpers */
    formatSLA(step) {
      const parts = [];
      if (step.sla_days) parts.push(step.sla_days + 'd');
      if (step.sla_hours) parts.push(step.sla_hours + 'h');
      if (step.sla_minutes) parts.push(step.sla_minutes + 'm');
      return parts.join(' ') || 'none';
    },

    formatTime(iso) {
      if (!iso) return '—';
      try {
        const d = new Date(iso);
        return d.toLocaleString();
      } catch {
        return iso;
      }
    },

    /* WebSocket */
    _connectWS() {
      try {
        const proto = location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = proto + '//' + location.host + '/ws/v1/dashboard';
        const ws = new WebSocket(wsUrl);
        ws.onopen = () => {
          this.wsConnected = true;
          ws.send(JSON.stringify({ type: 'subscribe', topics: ['workflows'] }));
        };
        ws.onmessage = (evt) => {
          try {
            const msg = JSON.parse(evt.data);
            if (msg.type === 'workflow_update') {
              this.loadInstances();
            }
          } catch { /* ignore non-JSON */ }
        };
        ws.onclose = () => {
          this.wsConnected = false;
          setTimeout(() => this._connectWS(), 5000);
        };
        ws.onerror = () => { this.wsConnected = false; };
      } catch { /* WS not available */ }
    },
  };
}
