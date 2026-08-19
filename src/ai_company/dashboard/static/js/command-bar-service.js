/**
 * Command Bar - Vanilla JS Service Layer
 * Handles search, keyboard navigation, quick actions, and voice input.
 * Used by the Alpine.js presentation component.
 */

class CommandBarService {
    constructor() {
        this.quickActions = [
            { id: 'new-task', label: 'New Task', icon: 'plus', action: () => this.openTaskModal() },
            { id: 'tasks', label: 'Tasks', icon: 'list', url: '/tasks' },
            { id: 'kpis', label: 'KPIs Dashboard', icon: 'chart-bar', url: '/kpis' },
            { id: 'agents', label: 'Agents', icon: 'users', url: '/agents' },
            { id: 'onboarding', label: 'Onboarding Studio', icon: 'user-plus', url: '/onboarding' },
            { id: 'approvals', label: 'Pending Approvals', icon: 'check-circle', url: '/escalations' },
        ];

        this.supportsVoice = 'SpeechRecognition' in window || 'webkitSpeechRecognition' in window;
        this.recognition = null;
        this.isListening = false;
        this.debounceTimer = null;
        this.lastQuery = '';

        if (this.supportsVoice) {
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
            return this.getQuickActions();
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
        return this.quickActions.map(action => ({
            ...action,
            score: 1.0,
            entity_type: 'action',
        }));
    }

    execute(result) {
        if (result.url) {
            window.location.href = result.url;
        } else if (result.action && this.quickActions.find(a => a.id === result.action)) {
            this.quickActions.find(a => a.id === result.action).action();
        }
    }

    openTaskModal() {
        // Dispatch custom event for Alpine component to handle
        window.dispatchEvent(new CustomEvent('command-bar:new-task'));
    }

    toggleVoice() {
        if (!this.supportsVoice || !this.recognition) {
            console.warn('Voice recognition not supported');
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
