/**
 * Org Chart Alpine.js component
 * Interactive hierarchical organization chart with drag-and-drop reassignment
 */
function orgChart() {
  return {
    tree: [],
    allAgents: [],
    selectedNode: null,
    zoom: 100,
    loading: true,
    showReassignModal: false,
    reassigningAgent: null,
    newManager: '',
    draggedNode: null,

    async init() {
      await this.loadOrgChart();
      await this.loadAllAgents();
    },

    async loadOrgChart() {
      this.loading = true;
      try {
        const res = await fetch('/api/v1/org-chart');
        this.tree = await res.json();
      } catch (e) {
        console.error('Failed to load org chart:', e);
        this.tree = [];
      }
      this.loading = false;
    },

    async loadAllAgents() {
      try {
        const res = await fetch('/api/v1/agents');
        this.allAgents = await res.json();
      } catch (e) {
        console.error('Failed to load agents:', e);
      }
    },

    selectNode(node) {
      this.selectedNode = node;
    },

    getTypeClass(type) {
      const classes = {
        Executive: 'bg-purple-500/20 text-purple-400',
        executive: 'bg-purple-500/20 text-purple-400',
        Department: 'bg-blue-500/20 text-blue-400',
        Specialist: 'bg-green-500/20 text-green-400',
        specialist: 'bg-green-500/20 text-green-400',
        Board: 'bg-amber-500/20 text-amber-400',
        board: 'bg-amber-500/20 text-amber-400'
      };
      return classes[type] || 'bg-gray-500/20 text-gray-400';
    },

    fitToView() {
      this.zoom = 100;
    },

    resetZoom() {
      this.zoom = 75;
    },

    onDragStart(event, node) {
      this.draggedNode = node;
      event.dataTransfer.effectAllowed = 'move';
    },

    onDragOver(event) {
      event.preventDefault();
    },

    async onDrop(event, targetNode) {
      event.preventDefault();
      if (!this.draggedNode || this.draggedNode.name === targetNode.name) return;

      // Confirm reassignment
      this.reassigningAgent = this.draggedNode;
      this.newManager = targetNode.name;
      this.showReassignModal = true;
    },

    startReassign(agent) {
      this.reassigningAgent = agent;
      this.newManager = '';
      this.showReassignModal = true;
    },

    async confirmReassign() {
      if (!this.reassigningAgent || !this.newManager) return;

      try {
        const res = await fetch(`/api/v1/agents/${this.reassigningAgent.name}/reports-to`, {
          method: 'PATCH',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ reports_to: this.newManager })
        });

        if (res.ok) {
          this.showReassignModal = false;
          await this.loadOrgChart();
          if (typeof showToast === 'function') {
            showToast('Agent reassigned successfully', 'success');
          } else {
            // Fallback if showToast is not available
            alert('Agent reassigned successfully');
          }
        } else {
          const error = await res.json();
          if (typeof showToast === 'function') {
            showToast(error.detail || 'Failed to reassign agent', 'error');
          } else {
            alert(error.detail || 'Failed to reassign agent');
          }
        }
      } catch (e) {
        console.error('Reassign error:', e);
        if (typeof showToast === 'function') {
          showToast('Failed to reassign agent', 'error');
        } else {
          alert('Failed to reassign agent');
        }
      }
    },

    viewAgentDetails(agent) {
      // Navigate to agents page with this agent selected
      window.location.href = `/agents?agent=${agent.name}`;
    }
  };
}
