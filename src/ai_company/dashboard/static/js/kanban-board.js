/* ═══════════════════════════════════════════════════════════════
   Kanban Board — Alpine.js component for task pipeline UX
   Issue #44 requirement F2: Columns ↔ task states mapping,
   workflow-engine decomposition, drag/drop transitions
   ═══════════════════════════════════════════════════════════════ */

function kanbanBoard() {
  return {
    // ── Board columns (maps to task states) ──────────────────
    columns: [
      { id: 'backlog',       label: 'Backlog',           state: 'pending',    color: 'amber',    icon: '📥' },
      { id: 'in_progress',   label: 'In Progress',       state: 'in_progress', color: 'blue',    icon: '⚙️' },
      { id: 'blocked',       label: 'Blocked',           state: 'blocked',    color: 'red',      icon: '🚫' },
      { id: 'pending_approval', label: 'Pending Approval', state: 'escalated', color: 'orange',  icon: '⏳' },
      { id: 'completed',     label: 'Completed',         state: 'completed',  color: 'emerald',  icon: '✅' },
    ],

    // ── Task data by column ──────────────────────────────────
    tasksByColumn: {
      backlog: [],
      in_progress: [],
      blocked: [],
      pending_approval: [],
      completed: [],
    },

    // ── Column counts (computed from tasks) ──────────────────
    columnCounts: {
      backlog: 0,
      in_progress: 0,
      blocked: 0,
      pending_approval: 0,
      completed: 0,
    },

    // ── Drag and drop state ──────────────────────────────────
    draggedTask: null,
    dragOverColumn: null,
    isDragging: false,

    // ── Task detail panel ────────────────────────────────────
    selectedTask: null,
    taskDetailOpen: false,

    // ── Decomposition panel ──────────────────────────────────
    decompositionPanelOpen: false,
    decompositionData: null,
    decompositionLoading: false,
    decompositionProgress: 0,

    // ── Agent assignment in decomposition ────────────────────
    selectedAgents: [],
    availableAgents: [],

    // ── WebSocket state ──────────────────────────────────────
    wsConnected: false,
    _wsReconnectTimer: null,
    _wsReconnectAttempts: 0,
    _wsMaxReconnectAttempts: 8,

    // ── UI state ─────────────────────────────────────────────
    isLoading: true,
    lastUpdated: null,
    _animationQueue: [],

    // ── API helper ───────────────────────────────────────────
    _api(path, opts) {
      return fetch('/api/v1' + path, {
        headers: { 'Content-Type': 'application/json' },
        ...opts,
      }).then(r => r.ok ? r.json() : Promise.reject(r));
    },

    // ── Initialization ───────────────────────────────────────
    async init() {
      this.isLoading = true;
      await Promise.all([
        this.loadTasks(),
        this.loadAgents(),
      ]);
      this.isLoading = false;
      this.lastUpdated = new Date();
      this._connectWebSocket();
    },

    // ── Load all tasks and group by column ───────────────────
    async loadTasks() {
      try {
        const data = await this._api('/tasks');
        const tasks = data.items || data.tasks || data || [];
        this._groupTasksByColumn(tasks);
      } catch (e) {
        console.error('Failed to load tasks', e);
      }
    },

    // ── Load available agents ────────────────────────────────
    async loadAgents() {
      try {
        const data = await this._api('/agents');
        this.availableAgents = data.agents || data || [];
      } catch (e) {
        console.error('Failed to load agents', e);
      }
    },

    // ── Group tasks into columns by state ────────────────────
    _groupTasksByColumn(tasks) {
      // Reset
      for (const col of this.columns) {
        this.tasksByColumn[col.id] = [];
      }

      // Map task states to column IDs
      const stateToColumn = {
        'pending': 'backlog',
        'in_progress': 'in_progress',
        'blocked': 'blocked',
        'escalated': 'pending_approval',
        'completed': 'completed',
        'failed': 'completed', // Show failed in completed with different styling
      };

      for (const task of tasks) {
        const colId = stateToColumn[task.status] || 'backlog';
        this.tasksByColumn[colId].push({
          ...task,
          _timeInColumn: this._calcTimeInColumn(task),
          _isAnimating: false,
        });
      }

      // Update counts
      for (const col of this.columns) {
        this.columnCounts[col.id] = this.tasksByColumn[col.id].length;
      }
    },

    // ── Calculate time in current column ─────────────────────
    _calcTimeInColumn(task) {
      const lastUpdate = task.updated_at || task.created_at;
      if (!lastUpdate) return '—';
      const diff = Date.now() - new Date(lastUpdate).getTime();
      const mins = Math.floor(diff / 60000);
      if (mins < 60) return `${mins}m`;
      const hrs = Math.floor(mins / 60);
      if (hrs < 24) return `${hrs}h ${mins % 60}m`;
      const days = Math.floor(hrs / 24);
      return `${days}d ${hrs % 24}h`;
    },

    // ── Drag and drop handlers ───────────────────────────────
    onDragStart(e, task, columnId) {
      this.draggedTask = task;
      this.isDragging = true;
      e.dataTransfer.effectAllowed = 'move';
      e.dataTransfer.setData('text/plain', task.id);

      // Visual feedback
      const el = e.target;
      if (el) {
        el.classList.add('opacity-50', 'scale-95');
      }
    },

    onDragEnd(e) {
      this.isDragging = false;
      this.dragOverColumn = null;

      // Remove visual feedback
      const el = e.target;
      if (el) {
        el.classList.remove('opacity-50', 'scale-95');
      }

      this.draggedTask = null;
    },

    onDragOver(e, columnId) {
      e.preventDefault();
      e.dataTransfer.dropEffect = 'move';
      this.dragOverColumn = columnId;
    },

    onDragLeave(columnId) {
      if (this.dragOverColumn === columnId) {
        this.dragOverColumn = null;
      }
    },

    async onDrop(e, targetColumnId) {
      e.preventDefault();
      this.dragOverColumn = null;

      if (!this.draggedTask) return;

      const task = this.draggedTask;
      const sourceColumnId = this._getTaskColumnId(task.id);
      const targetState = this.columns.find(c => c.id === targetColumnId)?.state;

      if (!targetState || sourceColumnId === targetColumnId) {
        this.isDragging = false;
        this.draggedTask = null;
        return;
      }

      // Optimistic update: move card immediately
      const oldState = task.status;
      const oldColumnId = this._getTaskColumnId(task.id);

      // Move task in UI
      this._moveTaskToColumn(task, targetColumnId);

      // Animate the transition
      const taskEl = document.querySelector(`[data-task-id="${task.id}"]`);
      if (taskEl) {
        taskEl.classList.add('kanban-card-transitioning');
        setTimeout(() => taskEl.classList.remove('kanban-card-transitioning'), 600);
      }

      try {
        // Update on server
        await this._api(`/tasks/${task.id}`, {
          method: 'PATCH',
          body: JSON.stringify({ status: targetState }),
        });

        // Update task state locally
        task.status = targetState;
        task._timeInColumn = 'just now';

        this.lastUpdated = new Date();
      } catch (e) {
        // Rollback on failure
        console.error('Failed to update task status', e);
        this._moveTaskToColumn(task, oldColumnId);

        // Show rollback toast
        this._showToast('error', 'Failed to move task', 'Rolled back to original column');
      }

      this.isDragging = false;
      this.draggedTask = null;
    },

    // ── Move task to a different column in UI ────────────────
    _moveTaskToColumn(task, targetColumnId) {
      // Remove from source column
      for (const col of this.columns) {
        this.tasksByColumn[col.id] = this.tasksByColumn[col.id].filter(t => t.id !== task.id);
      }

      // Add to target column
      this.tasksByColumn[targetColumnId].push({
        ...task,
        _timeInColumn: 'just now',
        _isAnimating: true,
      });

      // Update counts
      for (const col of this.columns) {
        this.columnCounts[col.id] = this.tasksByColumn[col.id].length;
      }

      // Clear animation flag after transition
      setTimeout(() => {
        const idx = this.tasksByColumn[targetColumnId].findIndex(t => t.id === task.id);
        if (idx !== -1) {
          this.tasksByColumn[targetColumnId][idx]._isAnimating = false;
        }
      }, 600);
    },

    // ── Get which column a task is in ────────────────────────
    _getTaskColumnId(taskId) {
      for (const col of this.columns) {
        if (this.tasksByColumn[col.id].some(t => t.id === taskId)) {
          return col.id;
        }
      }
      return null;
    },

    // ── Task detail panel ────────────────────────────────────
    openTaskDetail(task) {
      this.selectedTask = { ...task };
      this.taskDetailOpen = true;
      this.decompositionPanelOpen = false;
      this.decompositionData = null;
    },

    closeTaskDetail() {
      this.taskDetailOpen = false;
      this.selectedTask = null;
      this.decompositionPanelOpen = false;
      this.decompositionData = null;
    },

    // ── Decomposition panel ──────────────────────────────────
    async openDecomposition(task) {
      this.decompositionPanelOpen = true;
      this.decompositionLoading = true;
      this.decompositionData = null;
      this.selectedAgents = [];

      try {
        // Try to load existing decomposition
        const data = await this._api(`/tasks/${task.id}/decomposition`);
        this.decompositionData = data;
        this.decompositionProgress = data.progress_pct || 0;
      } catch (e) {
        // No existing decomposition — that's okay
        this.decompositionData = null;
      } finally {
        this.decompositionLoading = false;
      }
    },

    async decomposeTask(task) {
      this.decompositionLoading = true;
      try {
        const data = await this._api(`/tasks/${task.id}/decompose`, {
          method: 'POST',
          body: JSON.stringify({
            workflow: task.workflow || 'default',
            agents: this.selectedAgents,
          }),
        });

        this.decompositionData = data;
        this.decompositionProgress = data.progress_pct || 0;

        // Refresh board to show subtasks
        await this.loadTasks();
        this._showToast('success', 'Task decomposed', `${data.subtasks?.length || 0} subtasks created`);
      } catch (e) {
        console.error('Failed to decompose task', e);
        this._showToast('error', 'Decomposition failed', e.message || 'Unknown error');
      } finally {
        this.decompositionLoading = false;
      }
    },

    // ── Agent assignment in decomposition ────────────────────
    toggleAgent(agentName) {
      const idx = this.selectedAgents.indexOf(agentName);
      if (idx === -1) {
        this.selectedAgents.push(agentName);
      } else {
        this.selectedAgents.splice(idx, 1);
      }
    },

    // ── WebSocket connection ─────────────────────────────────
    _connectWebSocket() {
      const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
      const url = `${protocol}//${window.location.host}/ws`;

      try {
        this.ws = new WebSocket(url);

        this.ws.onopen = () => {
          this.wsConnected = true;
          this._wsReconnectAttempts = 0;

          // Subscribe to tasks topic
          this.ws.send(JSON.stringify({ type: 'subscribe', topic: 'tasks' }));
        };

        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            this._handleWebSocketMessage(data);
          } catch (e) {
            console.error('Failed to parse WebSocket message', e);
          }
        };

        this.ws.onclose = () => {
          this.wsConnected = false;
          this._scheduleReconnect();
        };

        this.ws.onerror = () => {
          this.wsConnected = false;
        };
      } catch (e) {
        console.error('WebSocket connection failed', e);
        this._scheduleReconnect();
      }
    },

    _scheduleReconnect() {
      if (this._wsReconnectAttempts >= this._wsMaxReconnectAttempts) {
        console.error('Max WebSocket reconnect attempts reached');
        return;
      }

      const delay = Math.min(1000 * Math.pow(2, this._wsReconnectAttempts), 30000);
      this._wsReconnectAttempts++;

      this._wsReconnectTimer = setTimeout(() => {
        this._connectWebSocket();
      }, delay);
    },

    _handleWebSocketMessage(data) {
      // Handle task updates from WebSocket
      if (data.topic === 'tasks' || data.type === 'task_update') {
        const task = data.payload || data;

        if (task.id && task.status) {
          // Update task in place
          this._updateTaskFromWebSocket(task);
        }
      }

      // Handle task creation
      if (data.type === 'task_created') {
        this.loadTasks(); // Full refresh for new tasks
      }
    },

    _updateTaskFromWebSocket(task) {
      // Find and update task in current columns
      for (const col of this.columns) {
        const idx = this.tasksByColumn[col.id].findIndex(t => t.id === task.id);
        if (idx !== -1) {
          const existing = this.tasksByColumn[col.id][idx];
          const targetState = task.status;
          const targetColumnId = this.columns.find(c => c.state === targetState)?.id;

          if (targetColumnId && targetColumnId !== col.id) {
            // Move to new column
            this.tasksByColumn[col.id].splice(idx, 1);
            this.tasksByColumn[targetColumnId].push({
              ...existing,
              ...task,
              _timeInColumn: 'just now',
              _isAnimating: true,
            });

            // Animate
            setTimeout(() => {
              const newIdx = this.tasksByColumn[targetColumnId].findIndex(t => t.id === task.id);
              if (newIdx !== -1) {
                this.tasksByColumn[targetColumnId][newIdx]._isAnimating = false;
              }
            }, 600);
          } else {
            // Update in place
            this.tasksByColumn[col.id][idx] = {
              ...existing,
              ...task,
              _timeInColumn: this._calcTimeInColumn(task),
            };
          }

          // Update counts
          for (const c of this.columns) {
            this.columnCounts[c.id] = this.tasksByColumn[c.id].length;
          }

          this.lastUpdated = new Date();
          return;
        }
      }

      // Task not found in any column — refresh
      this.loadTasks();
    },

    // ── Toast notifications ──────────────────────────────────
    _showToast(type, title, message) {
      // Use the parent dashboard's toast if available
      if (typeof dashboard !== 'undefined' && dashboard().toast) {
        dashboard().toast = { show: true, type, title, message };
        return;
      }

      // Fallback: simple console toast
      console.log(`[${type.toUpperCase()}] ${title}: ${message}`);
    },

    // ── Priority styling helpers ─────────────────────────────
    priorityClass(priority) {
      const classes = {
        critical: 'bg-red-500/20 text-red-400 border border-red-500/30',
        high: 'bg-orange-500/20 text-orange-400 border border-orange-500/30',
        medium: 'bg-amber-500/20 text-amber-400 border border-amber-500/30',
        low: 'bg-slate-500/20 text-slate-400 border border-slate-500/30',
      };
      return classes[priority] || classes.medium;
    },

    // ── Status styling helpers ───────────────────────────────
    statusClass(status) {
      const classes = {
        pending: 'bg-amber-500/10 text-amber-400',
        in_progress: 'bg-blue-500/10 text-blue-400',
        blocked: 'bg-red-500/10 text-red-400',
        escalated: 'bg-orange-500/10 text-orange-400',
        completed: 'bg-emerald-500/10 text-emerald-400',
        failed: 'bg-red-500/10 text-red-400',
      };
      return classes[status] || 'bg-slate-500/10 text-slate-400';
    },

    // ── Column header color helpers ──────────────────────────
    columnDotClass(column) {
      const classes = {
        amber: 'bg-amber-400',
        blue: 'bg-blue-400 animate-pulse',
        red: 'bg-red-400',
        orange: 'bg-orange-400',
        emerald: 'bg-emerald-400',
      };
      return classes[column.color] || 'bg-slate-400';
    },

    columnBorderClass(column) {
      const classes = {
        amber: 'border-amber-500/20',
        blue: 'border-blue-500/20',
        red: 'border-red-500/20',
        orange: 'border-orange-500/20',
        emerald: 'border-emerald-500/20',
      };
      return classes[column.color] || 'border-slate-500/20';
    },

    columnHoverClass(column) {
      const classes = {
        amber: 'hover:border-amber-500/40',
        blue: 'hover:border-blue-500/40',
        red: 'hover:border-red-500/40',
        orange: 'hover:border-orange-500/40',
        emerald: 'hover:border-emerald-500/40',
      };
      return classes[column.color] || 'hover:border-slate-500/40';
    },

    // ── Subtask status helper ────────────────────────────────
    subtaskStatusIcon(status) {
      const icons = {
        completed: '✓',
        in_progress: '◉',
        pending: '○',
        failed: '✗',
      };
      return icons[status] || '○';
    },

    // ── Cleanup ──────────────────────────────────────────────
    destroy() {
      clearTimeout(this._wsReconnectTimer);
      if (this.ws) {
        try {
          this.ws.close();
        } catch (e) { /* best-effort */ }
      }
    },
  };
}
