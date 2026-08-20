/**
 * Command Bar - Vanilla JS Service Layer
 * Handles search, keyboard navigation, quick actions, and voice input.
 * Used by the Alpine.js presentation component.
 */

class CommandBarService {
    constructor() {
        this.quickActions = [
            // Task mutations
            { id: 'new-task', label: 'New Task', icon: 'plus', action: () => this.openTaskModal(), category: 'task', minRole: 'approve' },
            { id: 'task-assign', label: 'Assign Task', icon: 'user', action: () => this.dispatch('command-bar:assign-task'), category: 'task', minRole: 'approve' },
            { id: 'task-cancel', label: 'Cancel Task', icon: 'x-circle', action: () => this.dispatch('command-bar:cancel-task'), category: 'task', minRole: 'approve' },
            { id: 'task-priority', label: 'Set Priority', icon: 'arrow-up', action: () => this.dispatch('command-bar:set-priority'), category: 'task', minRole: 'approve' },
            // Agent control
            { id: 'agents', label: 'Agents', icon: 'users', url: '/agents', category: 'agent', minRole: 'admin' },
            { id: 'agent-pause', label: 'Pause Agent', icon: 'pause', action: () => this.dispatch('command-bar:pause-agent'), category: 'agent', minRole: 'admin' },
            { id: 'agent-resume', label: 'Resume Agent', icon: 'play', action: () => this.dispatch('command-bar:resume-agent'), category: 'agent', minRole: 'admin' },
            { id: 'agent-status', label: 'Agent Status', icon: 'activity', action: () => this.dispatch('command-bar:agent-status'), category: 'agent', minRole: 'run' },
            // Memory
            { id: 'memory-search', label: 'Search Memory', icon: 'search', action: () => this.dispatch('command-bar:memory-search'), category: 'memory', minRole: 'run' },
            { id: 'memory-recent', label: 'Recent Memory', icon: 'clock', action: () => this.dispatch('command-bar:memory-recent'), category: 'memory', minRole: 'run' },
            // Ops
            { id: 'ops-state', label: 'System State', icon: 'server', url: '/ops', category: 'ops', minRole: 'admin' },
            { id: 'ops-health', label: 'Health Check', icon: 'heart', action: () => this.dispatch('command-bar:health-check'), category: 'ops', minRole: 'admin' },
            // Navigation
            { id: 'tasks', label: 'Tasks', icon: 'list', url: '/tasks', category: 'nav', minRole: 'run' },
            { id: 'kpis', label: 'KPIs Dashboard', icon: 'chart-bar', url: '/kpis', category: 'nav', minRole: 'run' },
            { id: 'onboarding', label: 'Onboarding Studio', icon: 'user-plus', url: '/onboarding', category: 'nav', minRole: 'run' },
            { id: 'approvals', label: 'Pending Approvals', icon: 'check-circle', url: '/escalations', category: 'nav', minRole: 'approve' },
            { id: 'costs', label: 'Cost Tracker', icon: 'dollar-sign', url: '/costs', category: 'nav', minRole: 'run' },
            { id: 'timeline', label: 'Execution Timeline', icon: 'git-branch', url: '/timeline', category: 'nav', minRole: 'run' },
            { id: 'command-center', label: 'Command Center', icon: 'terminal', url: '/command-center', category: 'nav', minRole: 'admin' },
            // Finance
            { id: 'revenue', label: 'Revenue', icon: 'trending-up', url: '/finance', category: 'finance', minRole: 'run' },
        ];

        this.supportsVoice = 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;
        this.recognition = null;
        this.isListening = false;
        this.debounceTimer = null;
        this.lastQuery = '';

        // Feature flag: voice disabled by default
        this.voiceEnabled = false;

        if (this.supportsVoice && this.voiceEnabled) {
            this.initVoiceRecognition();
        }
    }

    initVoiceRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) return;

        this.recognition = new SpeechRecognition();
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = navigator.language || 'en-US';

        this.recognition.onresult = (event) => {
            const transcript = Array.from(event.results)
                .map(r => r[0].transcript)
                .join(' ');
            this.onVoiceResult(transcript);
        };

        this.recognition.onerror = (event) => {
            console.warn('Voice recognition error:', event.error);
            this.isListening = false;
        };

        this.recognition.onend = () => {
            this.isListening = false;
        };
    }

    onVoiceResult(transcript) {
        // Callback will be set by Alpine component
        if (this.onVoiceResultCallback) {
            this.onVoiceResultCallback(transcript);
        }
    }

    setVoiceResultCallback(callback) {
        this.onVoiceResultCallback = callback;
    }

    async search(query, limit = 10) {
        if (!query || query.trim().length < 1) {
            const recent = this.getRecentCommands().map(r => ({
                ...r,
                score: 0.9,
                entity_type: 'recent',
            }));
            const quick = this.getQuickActions();
            // Deduplicate: recent commands that overlap with quick actions
            const quickIds = new Set(quick.map(a => a.id));
            const uniqueRecent = recent.filter(r => !quickIds.has(r.id));
            return [...uniqueRecent, ...quick];
        }

        try {
            const response = await fetch(`/api/v1/search/quick?q=${encodeURIComponent(query.trim())}&limit=${limit}`);
            if (!response.ok) {
                throw new Error(`Search failed: ${response.status}`);
            }
            const data = await response.json();
            return data.results || [];
        } catch (error) {
            console.error('Search error:', error);
            return this.getQuickActions(); // Fallback to quick actions
        }
    }

    getQuickActions() {
        const userRole = this.getUserRole();
        const hierarchy = ['run', 'approve', 'admin'];
        const roleIndex = hierarchy.indexOf(userRole);

        return this.quickActions
            .filter(action => {
                if (!action.minRole) return true;
                return roleIndex >= hierarchy.indexOf(action.minRole);
            })
            .map(action => ({
                ...action,
                score: 1.0,
                entity_type: 'action',
            }));
    }

    getUserRole() {
        return window.dashboardUserRole || 'run';
    }

    dispatch(eventName, detail = {}) {
        window.dispatchEvent(new CustomEvent(eventName, { detail }));
    }

    getRecentCommands() {
        try {
            const raw = localStorage.getItem('jarvis-recent-commands');
            return raw ? JSON.parse(raw) : [];
        } catch {
            return [];
        }
    }

    addRecentCommand(action) {
        const recent = this.getRecentCommands().filter(r => r.id !== action.id);
        recent.unshift({ id: action.id, label: action.label, icon: action.icon, url: action.url, timestamp: Date.now() });
        localStorage.setItem('jarvis-recent-commands', JSON.stringify(recent.slice(0, 10)));
    }

    execute(result) {
        this.addRecentCommand(result);
        if (result.url) {
            window.location.href = result.url;
        } else if (result.action && this.quickActions.find(a => a.id === result.action)) {
            this.quickActions.find(a => a.id === result.action).action();
        } else if (result.action) {
            this.dispatch(result.action, result);
        }
    }

    openTaskModal() {
        // Dispatch custom event for Alpine component to handle
        window.dispatchEvent(new CustomEvent('command-bar:new-task'));
    }

    toggleVoice() {
        if (!this.supportsVoice || !this.voiceEnabled || !this.recognition) {
            console.warn('Voice recognition not supported or not enabled');
            return false;
        }

        if (this.isListening) {
            this.recognition.stop();
            this.isListening = false;
        } else {
            try {
                this.recognition.start();
                this.isListening = true;
            } catch (error) {
                console.warn('Voice recognition start failed:', error);
                this.isListening = false;
            }
        }
        return this.isListening;
    }
}

// Export for Alpine component
window.CommandBarService = CommandBarService;
