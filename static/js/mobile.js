/* ============================================================
   Mobile Dashboard — Alpine.js Component
   Pull-to-refresh, swipe approvals, offline support, bottom nav
   ============================================================ */

function mobileDashboard() {
  return {
    // ── State ──────────────────────────────────────────────
    activeTab: "dashboard",
    isOnline: navigator.onLine,
    isSyncing: false,
    lastSyncAt: null,

    tabs: [
      { id: "dashboard", label: "Home", icon: "home" },
      { id: "approvals", label: "Approve", icon: "check" },
      { id: "tasks", label: "Tasks", icon: "list" },
      { id: "agents", label: "Agents", icon: "users" },
    ],

    // ── Dashboard Data ─────────────────────────────────────
    kpis: { pending: 0, completed: 0, escalations: 0, approvals: 0, agents: 0 },
    urgent: { approval_count: 0, escalation_count: 0, failed_count: 0 },
    recentTasks: [],

    // ── Approvals ──────────────────────────────────────────
    approvalStack: { current: null, stack: [], total_pending: 0, remaining_count: 0 },
    swipeOffset: 0,
    swipeStartX: 0,
    isSwiping: false,

    // ── Tasks ──────────────────────────────────────────────
    tasks: [],
    taskCursor: null,
    tasksLoading: false,
    hasMoreTasks: true,
    taskFilter: "all",

    // ── Agents ─────────────────────────────────────────────
    agents: [],

    // ── Toast Notifications ────────────────────────────────
    toasts: [],

    // ── Offline Queue ──────────────────────────────────────
    pendingActions: JSON.parse(localStorage.getItem("pending_actions") || "[]"),

    // ── Initialization ─────────────────────────────────────
    async init() {
      // Register service worker
      if ("serviceWorker" in navigator) {
        try {
          const reg = await navigator.serviceWorker.register("/js/service-worker.js");
          console.log("[Mobile] Service worker registered");

          // Listen for sync completion
          navigator.serviceWorker.addEventListener("message", (event) => {
            if (event.data?.type === "SYNC_COMPLETE") {
              this.handleSyncComplete(event.data.payload);
            }
          });
        } catch (e) {
          console.warn("[Mobile] SW registration failed:", e);
        }
      }

      // Online/offline listeners
      window.addEventListener("online", () => this.handleOnline());
      window.addEventListener("offline", () => this.handleOffline());

      // Initial data load
      await this.loadTab("dashboard");

      // Periodic refresh
      setInterval(() => this.refreshCurrentTab(), 15000);
    },

    // ── Tab Navigation ─────────────────────────────────────
    async loadTab(tab) {
      this.activeTab = tab;
      switch (tab) {
        case "dashboard":
          await this.loadDashboard();
          break;
        case "approvals":
          await this.loadApprovalStack();
          break;
        case "tasks":
          this.tasks = [];
          this.taskCursor = null;
          this.hasMoreTasks = true;
          await this.loadTasks();
          break;
        case "agents":
          await this.loadAgents();
          break;
      }
    },

    async refreshCurrentTab() {
      if (!this.isOnline) return;
      await this.loadTab(this.activeTab);
    },

    // ── Dashboard ──────────────────────────────────────────
    async loadDashboard() {
      const data = await this.fetchJSON("/api/mobile/dashboard");
      if (data) {
        this.kpis = data.kpis;
        this.urgent = data.urgent;
        this.recentTasks = data.recent_tasks;
        this.lastSyncAt = data.updated_at;
        this.cacheData("dashboard", data);
      } else {
        // Load from cache
        const cached = this.getCachedData("dashboard");
        if (cached) {
          this.kpis = cached.kpis;
          this.urgent = cached.urgent;
          this.recentTasks = cached.recent_tasks;
        }
      }
    },

    // ── Approval Stack ─────────────────────────────────────
    async loadApprovalStack() {
      const data = await this.fetchJSON("/api/mobile/approvals/stack?limit=5");
      if (data) {
        this.approvalStack = data;
      }
    },

    get hasCurrentApproval() {
      return this.approvalStack.current !== null;
    },

    get currentApproval() {
      return this.approvalStack.current;
    },

    get nextInStack() {
      return this.approvalStack.stack?.[0] || null;
    },

    // Swipe gesture handling
    onSwipeStart(event) {
      this.swipeStartX = event.touches?.[0]?.clientX || event.clientX;
      this.isSwiping = true;
    },

    onSwipeMove(event) {
      if (!this.isSwiping) return;
      const x = event.touches?.[0]?.clientX || event.clientX;
      this.swipeOffset = x - this.swipeStartX;
    },

    async onSwipeEnd() {
      if (!this.isSwiping) return;
      this.isSwiping = false;

      const threshold = 100;

      if (this.swipeOffset > threshold) {
        // Swipe right → Approve
        await this.swipeAction("approve");
      } else if (this.swipeOffset < -threshold) {
        // Swipe left → Reject
        await this.swipeAction("reject");
      }

      this.swipeOffset = 0;
    },

    async swipeAction(decision) {
      if (!this.currentApproval) return;

      const requestId = this.currentApproval.id;

      if (!this.isOnline) {
        // Queue for later
        this.queueAction({ type: decision, target_id: requestId });
        this.showToast(`Queued for ${decision} (offline)`, "warning");
        // Optimistically remove from stack
        this.advanceStack();
        return;
      }

      try {
        const res = await fetch("/api/mobile/approvals/swipe", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            request_id: requestId,
            decision: decision,
            notes: "",
          }),
        });

        if (res.ok) {
          const result = await res.json();
          this.approvalStack.current = result.next;
          this.approvalStack.remaining_count = result.remaining_count;
          // Pop first from stack
          this.approvalStack.stack.shift();
          this.showToast(`${decision === "approve" ? "Approved" : "Rejected"}`, "success");
        }
      } catch (e) {
        this.showToast("Action failed", "error");
      }
    },

    advanceStack() {
      if (this.approvalStack.stack.length > 0) {
        this.approvalStack.current = this.approvalStack.stack.shift();
      } else {
        this.approvalStack.current = null;
      }
    },

    async tapApprove() {
      await this.swipeAction("approve");
    },

    async tapReject() {
      await this.swipeAction("reject");
    },

    async tapSkip() {
      if (!this.currentApproval) return;
      this.advanceStack();
      this.showToast("Skipped", "info");
    },

    getSwipeIndicatorClass() {
      if (this.swipeOffset > 50) return "swipe-indicator--approve";
      if (this.swipeOffset < -50) return "swipe-indicator--reject";
      return "";
    },

    getSwipeIndicatorOpacity() {
      return Math.min(Math.abs(this.swipeOffset) / 100, 1);
    },

    getSwipeCardStyle() {
      if (!this.isSwiping) return "";
      const rotation = this.swipeOffset * 0.05;
      return `transform: translateX(${this.swipeOffset}px) rotate(${rotation}deg)`;
    },

    // ── Tasks ──────────────────────────────────────────────
    async loadTasks(append = false) {
      if (this.tasksLoading) return;
      this.tasksLoading = true;

      let url = "/api/mobile/tasks?limit=20";
      if (this.taskFilter !== "all") url += `&status=${this.taskFilter}`;
      if (this.taskCursor && append) url += `&cursor=${this.taskCursor}`;

      const data = await this.fetchJSON(url);
      if (data) {
        if (append) {
          this.tasks = [...this.tasks, ...data.items];
        } else {
          this.tasks = data.items;
        }
        this.taskCursor = data.next_cursor;
        this.hasMoreTasks = data.has_more;
      }

      this.tasksLoading = false;
    },

    async loadMoreTasks() {
      if (this.hasMoreTasks && !this.tasksLoading) {
        await this.loadTasks(true);
      }
    },

    async setTaskFilter(filter) {
      this.taskFilter = filter;
      this.taskCursor = null;
      this.hasMoreTasks = true;
      await this.loadTasks();
    },

    // ── Agents ─────────────────────────────────────────────
    async loadAgents() {
      const data = await this.fetchJSON("/api/agents");
      if (data) this.agents = data;
    },

    // ── Pull-to-Refresh ────────────────────────────────────
    ptrActive: false,
    ptrPulling: false,
    ptrStartY: 0,
    ptrOffset: 0,

    onPtrTouchStart(event) {
      if (window.scrollY > 0) return;
      this.ptrStartY = event.touches[0].clientY;
      this.ptrPulling = true;
    },

    onPtrTouchMove(event) {
      if (!this.ptrPulling) return;
      const y = event.touches[0].clientY;
      const diff = y - this.ptrStartY;

      if (diff > 0 && diff < 120) {
        this.ptrOffset = diff;
        event.preventDefault();
      }
    },

    async onPtrTouchEnd() {
      if (!this.ptrPulling) return;
      this.ptrPulling = false;

      if (this.ptrOffset > 60) {
        this.ptrActive = true;
        await this.refreshCurrentTab();
        this.showToast("Refreshed", "success");
      }

      this.ptrOffset = 0;
      this.ptrActive = false;
    },

    get ptrIndicatorStyle() {
      if (this.ptrOffset > 0) {
        return `top: ${Math.min(this.ptrOffset - 48, 12)}px`;
      }
      return "";
    },

    // ── Online / Offline ───────────────────────────────────
    handleOnline() {
      this.isOnline = true;
      this.showToast("Back online", "success");
      this.syncPendingActions();
    },

    handleOffline() {
      this.isOnline = false;
      this.showToast("You are offline. Actions will be queued.", "warning");
    },

    async syncPendingActions() {
      if (this.pendingActions.length === 0) return;
      this.isSyncing = true;

      try {
        const res = await this.fetchJSON("/api/mobile/sync", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            last_sync_at: this.lastSyncAt,
            pending_actions: this.pendingActions,
          }),
        });

        if (res) {
          this.pendingActions = [];
          localStorage.setItem("pending_actions", "[]");
          this.lastSyncAt = res.synced_at;
          this.showToast("Synced offline actions", "success");
          await this.refreshCurrentTab();
        }
      } catch (e) {
        this.showToast("Sync failed, will retry", "error");
      }

      this.isSyncing = false;
    },

    handleSyncComplete(result) {
      this.lastSyncAt = result.synced_at;
      this.showToast("Background sync complete", "success");
    },

    queueAction(action) {
      action.queued_at = new Date().toISOString();
      action.id = `local_${Date.now()}`;
      this.pendingActions.push(action);
      localStorage.setItem("pending_actions", JSON.stringify(this.pendingActions));

      // Try background sync
      if ("serviceWorker" in navigator && "SyncManager" in window) {
        navigator.serviceWorker.ready.then((reg) => {
          reg.sync.register("sync-pending-actions");
        });
      }
    },

    // ── API Helper ─────────────────────────────────────────
    async fetchJSON(url, opts = {}) {
      try {
        const res = await fetch(url, opts);
        if (!res.ok) throw new Error(res.statusText);
        return await res.json();
      } catch (e) {
        console.warn("[Mobile] fetch failed:", url, e.message);
        return null;
      }
    },

    // ── Cache Helpers ──────────────────────────────────────
    cacheData(key, data) {
      try {
        localStorage.setItem(`cache_${key}`, JSON.stringify(data));
      } catch (e) { /* quota exceeded */ }
    },

    getCachedData(key) {
      try {
        const raw = localStorage.getItem(`cache_${key}`);
        return raw ? JSON.parse(raw) : null;
      } catch (e) {
        return null;
      }
    },

    // ── Toast Notifications ────────────────────────────────
    showToast(message, type = "info") {
      const id = Date.now();
      this.toasts.push({ id, message, type });
      setTimeout(() => {
        this.toasts = this.toasts.filter((t) => t.id !== id);
      }, 3000);
    },

    // ── Formatting Helpers ─────────────────────────────────
    formatPriority(p) {
      return { low: "Low", medium: "Med", high: "High", critical: "!!" }[p] || p;
    },

    priorityBadgeClass(p) {
      return {
        low: "badge--gray",
        medium: "badge--blue",
        high: "badge--amber",
        critical: "badge--red",
      }[p] || "badge--gray";
    },

    statusBadgeClass(s) {
      return {
        pending: "badge--amber",
        in_progress: "badge--blue",
        completed: "badge--green",
        failed: "badge--red",
        escalated: "badge--red",
      }[s] || "badge--gray";
    },

    truncate(text, max = 60) {
      if (!text) return "";
      return text.length > max ? text.slice(0, max - 3) + "..." : text;
    },

    urgentBadgeCount() {
      return this.urgent.approval_count + this.urgent.escalation_count;
    },
  };
}
