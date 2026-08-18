/**
 * Command Bar - Alpine.js Presentation Component
 * Handles UI rendering, keyboard navigation, and user interaction.
 * Uses CommandBarService for business logic.
 */

document.addEventListener('alpine:init', () => {
    Alpine.data('commandBar', () => ({
        // State
        open: false,
        query: '',
        results: [],
        selectedIndex: 0,
        isListening: false,
        supportsVoice: false,

        // Service instance
        service: null,

        // Refs
        inputRef: null,
        panelRef: null,

        // Lifecycle
        init() {
            this.service = new window.CommandBarService();
            this.service.onVoiceResultCallback = (transcript) => {
                this.query = transcript;
                this.search();
            };
            this.supportsVoice = this.service.supportsVoice;

            // Bind global hotkey
            this.bindHotkeys();

            // Close on outside click
            document.addEventListener('click', this.handleOutsideClick.bind(this));

            // Prevent event propagation on panel
            this.$watch('open', (open) => {
                if (open) {
                    document.body.style.overflow = 'hidden';
                    this.$nextTick(() => {
                        this.$refs.input?.focus();
                        this.selectedIndex = 0;
                    });
                } else {
                    document.body.style.overflow = '';
                }
            });
        },

        bindHotkeys() {
            document.addEventListener('keydown', (e) => {
                // Cmd+K / Ctrl+K to toggle
                if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
                    e.preventDefault();
                    this.toggle();
                }

                // Escape to close
                if (e.key === 'Escape' && this.open) {
                    this.close();
                }
            });
        },

        handleOutsideClick(e) {
            if (this.open && this.$refs.panel && !this.$refs.panel.contains(e.target) &&
                !e.target.closest('[x-ref="trigger"]')) {
                this.close();
            }
        },

        // Actions
        toggle() {
            this.open = !this.open;
            if (!this.open) {
                this.query = '';
                this.results = [];
                this.selectedIndex = 0;
            }
        },

        open() {
            if (!this.open) {
                this.open = true;
            }
        },

        close() {
            this.open = false;
            this.query = '';
            this.results = [];
            this.selectedIndex = 0;
            this.isListening = false;
        },

        async search() {
            if (this.query.trim().length === 0) {
                this.results = this.service.getQuickActions();
                this.selectedIndex = 0;
                return;
            }

            this.results = await this.service.search(this.query.trim(), 10);
            this.selectedIndex = 0;
        },

        get groupedResults() {
            if (this.results.length === 0) return [];
            
            const sections = [
                { key: 'actions', label: 'Quick Actions', filter: r => r.entity_type === 'action' },
                { key: 'agents', label: 'Agents', filter: r => r.entity_type === 'agent' },
                { key: 'tasks', label: 'Tasks', filter: r => r.entity_type === 'task' },
                { key: 'kpis', label: 'KPIs', filter: r => r.entity_type === 'kpi' },
                { key: 'audit', label: 'Audit', filter: r => r.entity_type === 'audit' },
            ];

            const results = [];
            let offset = 0;
            for (const section of sections) {
                const resultsInSection = this.results.filter(section.filter);
                if (resultsInSection.length > 0) {
                    results.push({
                        key: section.key,
                        label: section.label,
                        results: resultsInSection,
                        offset: offset,
                    });
                    offset += resultsInSection.length;
                }
            }
            return results;
        },

        debouncedSearch() {
            clearTimeout(this.searchDebounce);
            this.searchDebounce = setTimeout(() => this.search(), 150);
        },

        select(delta) {
            if (this.results.length === 0) return;
            this.selectedIndex = Math.max(0, Math.min(this.results.length - 1, this.selectedIndex + delta));
        },

        execute() {
            const result = this.results[this.selectedIndex];
            if (result) {
                this.service.execute(result);
                this.close();
            }
        },

        toggleVoice() {
            const isNowListening = this.service.toggleVoice();
            this.isListening = isNowListening;
        },

        // Keyboard navigation within input
        handleKeydown(e) {
            switch (e.key) {
                case 'ArrowDown':
                    e.preventDefault();
                    this.select(1);
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.select(-1);
                    break;
                case 'Enter':
                    e.preventDefault();
                    this.execute();
                    break;
                case 'Tab':
                    // Allow tab to move between quick actions and results
                    break;
                case 'Escape':
                    this.close();
                    break;
            }
        },

        // Helpers
        getIcon(iconName) {
            const icons = {
                plus: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/></svg>',
                list: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"/></svg>',
                'chart-bar': '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 012-2V9a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2z"/></svg>',
                users: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"/></svg>',
                'user-plus': '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"/></svg>',
                'check-circle': '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>',
                microphone: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h10m-4 0V11a1 1 0 112 0v4m0 0a1 1 0 01-1 1h-5a1 1 0 01-1-1"/></svg>',
                microphone_slash: '<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17c5-3.5 2-7.5-1-9.5M8 10V8a4 4 0 018 0v2m-6 0l14 14"/></svg>',
            };
            return icons[iconName] || '';
        },

        formatEntityType(type) {
            const labels = {
                action: 'Action',
                agent: 'Agent',
                task: 'Task',
                kpi: 'KPI',
                audit: 'Audit',
            };
            return labels[type] || type;
        },

        highlightMatch(text, query) {
            if (!query) return text;
            const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
            return text.replace(regex, '<mark class="bg-yellow-500/30">$1</mark>');
        },
    }));