import React, { useState, useCallback } from 'react';
import { MessageSquare, Sparkles, ArrowRight, Send, Bot, User, CheckCircle2, ShieldCheck } from 'lucide-react';
import { SectionHeading } from './site/SectionHeading';
import { CtaBand } from './site/CtaBand';
import { HonestyBadge } from './site/HonestyBadge';
import { Reveal } from './Reveal';
import { useSite } from '../site-context';
import { solutions } from '../data/siteContent';

type Step = 'welcome' | 'problem' | 'context' | 'results' | 'cta';

interface ChatMessage {
  id: string;
  role: 'assistant' | 'user';
  text: string;
}

interface DiscoveryState {
  step: Step;
  problem: string;
  industry: string;
  timeline: string;
  matchedSolutions: typeof solutions;
}

const WELCOME_MESSAGE = `Welcome to Ask LightSpeed — the interactive discovery layer for our AI Company Builder platform.

I'll help you understand which LightSpeed capabilities match your needs. Think of me as your executive briefing prep assistant.

To get started: what's the core challenge keeping you up at night?`;

const PROBLEM_QUESTIONS = [
  'We need to build AI-native operations but lack the expertise',
  'Our current systems are manual and we want to automate',
  'We need governance and compliance automation for our AI deployments',
  'We want to deploy AI agents across multiple departments',
  'We need executive-level AI strategy and a boardroom briefing',
  'We need digital presence and e-commerce with mobile money checkout',
];

const CONTEXT_QUESTIONS = [
  { field: 'industry', label: 'Which sector best describes you?', options: ['Financial Services', 'Healthcare', 'Agriculture', 'Education', 'Government', 'Other'] },
  { field: 'timeline', label: 'What is your target timeline?', options: ['Within 30 days', 'Within 3 months', 'Within 6 months', 'Exploring — no rush'] },
];

export const AskLightSpeed: React.FC = () => {
  const { theme, onRequestBriefing } = useSite();
  const isLight = theme === 'light';
  const [messages, setMessages] = useState<ChatMessage[]>([
    { id: '1', role: 'assistant', text: WELCOME_MESSAGE },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [state, setState] = useState<DiscoveryState>({
    step: 'welcome',
    problem: '',
    industry: '',
    timeline: '',
    matchedSolutions: [],
  });
  const [showQuickQuestions, setShowQuickQuestions] = useState(true);

  const addMessage = useCallback((role: 'assistant' | 'user', text: string) => {
    setMessages(prev => [...prev, { id: Date.now().toString(), role, text }]);
  }, []);

  const handleSend = useCallback(() => {
    if (!inputValue.trim()) return;
    const userText = inputValue.trim();
    addMessage('user', userText);
    setInputValue('');

    if (state.step === 'welcome' || state.step === 'problem') {
      const problem = PROBLEM_QUESTIONS.find(q =>
        userText.toLowerCase().includes(q.toLowerCase().split(' ').slice(0, 3).join(' '))
      ) || userText;
      setState(prev => ({ ...prev, step: 'context', problem }));
      addMessage('assistant', `Thank you. You mentioned: "${problem}"\n\nNow, let me narrow things down a bit:`);
      setTimeout(() => {
        addMessage('assistant', `Which sector best describes your organisation?\n`);
      }, 500);
    } else if (state.step === 'context') {
      const nextField = !state.industry ? 'industry' : !state.timeline ? 'timeline' : 'timeline';
      if (nextField === 'industry') {
        setState(prev => ({ ...prev, industry: userText }));
        addMessage('assistant', `Great — ${userText}. Now, what is your target timeline?\n`);
      } else {
        setState(prev => ({ ...prev, timeline: userText, step: 'results' }));
        const matched = matchSolutions(state.problem, userText);
        addMessage('assistant', `Based on your inputs, here's what I found:\n\n`);
        setTimeout(() => {
          setState(prev => ({ ...prev, matchedSolutions: matched }));
          const resultText = buildResultsText(matched, userText);
          addMessage('assistant', resultText);
        }, 500);
      }
    }
  }, [inputValue, state, addMessage]);

  const matchSolutions = useCallback((problem: string, context: string): typeof solutions => {
    const lowerProblem = problem.toLowerCase();
    const lowerContext = context.toLowerCase();
    return solutions.filter(s => {
      const titleMatch = s.title.toLowerCase().includes(lowerProblem.slice(0, 4)) ||
        lowerProblem.includes(s.title.toLowerCase().split(' ').slice(0, 2).join(' '));
      const descMatch = s.description.toLowerCase().slice(0, 20).includes(lowerProblem.slice(0, 4));
      return titleMatch || descMatch;
    }).length > 0 ? solutions.filter(s => {
      const titleMatch = s.title.toLowerCase().includes(lowerProblem.slice(0, 4));
      const descMatch = s.description.toLowerCase().slice(0, 30).includes(lowerProblem.slice(0, 4));
      return titleMatch || descMatch;
    }) : solutions.slice(0, 3);
  }, [solutions]);

  const buildResultsText = useCallback((matched: typeof solutions, timeline: string): string => {
    if (matched.length === 0) return 'Based on your inputs, I recommend our Executive Boardroom Briefing to clarify scope, or our AI Company Builder platform for enterprise deployment.';
    let text = `Based on your inputs, I found ${matched.length} capability match${matched.length > 1 ? 'es' : ''}:\n\n`;
    matched.forEach((s, i) => {
      text += `${i + 1}. **${s.title}** — ${s.description.slice(0, 80)}...\n`;
    });
    text += `\nWith a ${timeline.toLowerCase()}, we can start with an Executive Boardroom Briefing to align on scope, then move to ${matched[0]?.title || 'deployment'}.\n\nWould you like to start a conversation?`;
    return text;
  }, []);

  const handleQuickQuestion = useCallback((question: string) => {
    addMessage('user', question);
    setState(prev => ({ ...prev, step: 'context', problem: question }));
    setTimeout(() => {
      addMessage('assistant', `Understanding — "${question}"\n\nWhich sector best describes your organisation?\n`);
    }, 500);
  }, [addMessage]);

  const handleResultClick = useCallback((solution: typeof solutions[0]) => {
    addMessage('assistant', `You selected ${solution.title}. This is a ${solution.honestyBadge} capability.`);
    setState(prev => ({ ...prev, step: 'cta' }));
  }, [addMessage]);

  const handleStartConversation = useCallback(() => {
    onRequestBriefing('Discovery via Ask LightSpeed — matched capabilities');
  }, [onRequestBriefing]);

  return (
    <section id="ask-lightspeed" className={`min-h-screen py-12 sm:py-20 px-4 sm:px-8 border-t ${
      isLight ? 'border-ls-grey-dark/40 bg-ls-grey-light/50' : 'border-ls-white/10 bg-ls-navy/90'
    }`}>
      <div className="max-w-4xl mx-auto">
        <Reveal>
          <SectionHeading
            theme={theme}
            eyebrow="INTERACTIVE DISCOVERY"
            title="Ask LightSpeed"
            lead="Tell us your challenge. Our AI discovery layer maps it to proven capabilities, governance models, and engagement paths — all with explicit honesty badges."
          />
        </Reveal>

        {/* Chat Interface */}
        <div className={`rounded-3xl overflow-hidden shadow-2xl border ${
          isLight ? 'bg-ls-white border-ls-grey-dark/30' : 'bg-ls-navy border-ls-white/15'
        }`}>
          {/* Chat Header */}
          <div className={`flex items-center gap-3 px-6 py-4 border-b ${
            isLight ? 'border-ls-grey-dark/20 bg-ls-grey-light/50' : 'border-ls-white/10 bg-ls-navy/50'
          }`}>
            <div className="w-10 h-10 rounded-full bg-ls-red flex items-center justify-center">
              <Bot className="w-5 h-5 text-ls-white" />
            </div>
            <div>
              <h3 className="font-display font-black text-base">Ask LightSpeed</h3>
              <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                AI Discovery Layer • Honest by design
              </p>
            </div>
            <div className="ml-auto flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-ls-cyan animate-pulse" />
              <span className="text-xs font-medium text-ls-cyan">Online</span>
            </div>
          </div>

          {/* Messages */}
          <div className="px-6 py-6 space-y-4 max-h-[400px] overflow-y-auto">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex gap-3 ${msg.role === 'user' ? 'flex-row-reverse' : ''}`}>
                <div className={`w-8 h-8 rounded-full shrink-0 flex items-center justify-center ${
                  msg.role === 'assistant' ? 'bg-ls-red' : 'bg-ls-cyan/20'
                }`}>
                  {msg.role === 'assistant' ? (
                    <Bot className="w-4 h-4 text-ls-white" />
                  ) : (
                    <User className="w-4 h-4 text-ls-cyan" />
                  )}
                </div>
                <div className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  msg.role === 'assistant'
                    ? isLight ? 'bg-ls-grey-light/50 text-ls-navy' : 'bg-ls-white/10 text-ls-white'
                    : 'bg-ls-red text-ls-white'
                }`}>
                  {msg.text.split('\n').map((line, i) => (
                    <React.Fragment key={i}>
                      {line.startsWith('**') && line.endsWith('**') ? (
                        <strong>{line.slice(2, -2)}</strong>
                      ) : (
                        <p>{line}</p>
                      )}
                    </React.Fragment>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Quick Questions (welcome/problem step) */}
          {(state.step === 'welcome' || state.step === 'problem') && (
            <div className={`px-6 py-4 border-t ${
              isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'
            }`}>
              <p className={`text-xs font-body font-medium tracking-wider mb-3 ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                Quick select — what's your core challenge?
              </p>
              <div className="flex flex-wrap gap-2">
                {PROBLEM_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => handleQuickQuestion(q)}
                    className={`px-3 py-1.5 rounded-full text-xs font-body font-medium border transition-all cursor-pointer ${
                      isLight
                        ? 'border-ls-grey-dark/30 bg-ls-grey-light/50 text-ls-navy hover:bg-ls-red hover:text-ls-white hover:border-ls-red'
                        : 'border-ls-white/20 bg-ls-white/5 text-ls-white hover:bg-ls-red hover:text-ls-white hover:border-ls-red'
                    }`}
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Results (step: results) */}
          {state.step === 'results' && state.matchedSolutions.length > 0 && (
            <div className={`px-6 py-4 border-t ${
              isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'
            }`}>
              <p className={`text-xs font-body font-medium tracking-wider mb-3 ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                Matched capabilities:
              </p>
              <div className="space-y-2">
                {state.matchedSolutions.map((s, i) => (
                  <button
                    key={s.slug}
                    onClick={() => handleResultClick(s)}
                    className={`w-full text-left px-4 py-3 rounded-xl border transition-all cursor-pointer ${
                      isLight
                        ? 'border-ls-grey-dark/20 hover:border-ls-red/50 hover:bg-ls-red/5'
                        : 'border-ls-white/10 hover:border-ls-red/50 hover:bg-ls-red/5'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="font-display font-bold text-sm">{s.title}</span>
                        <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                          {s.description.slice(0, 60)}...
                        </p>
                      </div>
                      <HonestyBadge label={{ label: s.honestyBadge, tone: s.honestyBadge.includes('proven') ? 'proven' : s.honestyBadge.includes('pilot') ? 'pilot' : s.honestyBadge.includes('Fieldable') ? 'fieldable' : 'development' }} />
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* CTA step */}
          {state.step === 'cta' && (
            <div className="px-6 py-6 border-t border-ls-red/20 text-center">
              <div className="w-12 h-12 rounded-full bg-ls-cyan/20 text-ls-cyan border border-ls-cyan/40 flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h4 className="font-display font-black text-xl mb-2">Discovery Complete</h4>
              <p className={`text-sm ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'} mb-4`}>
                Based on your inputs, I've mapped your challenge to LightSpeed capabilities. Ready to start a conversation?
              </p>
              <button
                onClick={handleStartConversation}
                className="inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 hover:bg-ls-red/90 hover:scale-[1.02] active:scale-[0.98] cursor-pointer"
              >
                Start a Conversation
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {/* Input */}
          <div className={`px-6 py-4 border-t ${
            isLight ? 'border-ls-grey-dark/20' : 'border-ls-white/10'
          }`}>
            <div className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder={state.step === 'cta' ? 'Or type to ask something else...' : 'Type your response...'}
                className={`flex-1 px-4 py-2.5 rounded-xl border text-sm outline-none focus:border-ls-red transition-colors font-medium ${
                  isLight
                    ? 'bg-ls-grey-light/90 border-ls-grey-dark text-ls-navy placeholder:text-ls-grey-light-text shadow-inner'
                    : 'bg-ls-navy border-ls-white/20 text-ls-white placeholder:text-ls-grey-light-text shadow-inner'
                }`}
              />
              <button
                onClick={handleSend}
                disabled={!inputValue.trim()}
                className="px-4 py-2.5 rounded-xl bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-md shadow-ls-red/25 active:scale-95 cursor-pointer"
              >
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>

        {/* Trust indicators */}
        <Reveal delay={0.3}>
          <div className="mt-8 grid grid-cols-1 sm:grid-cols-3 gap-6">
            {[
              { icon: Sparkles, title: 'Structured Discovery', desc: 'Our AI discovery layer asks targeted questions to match your challenge to proven capabilities.' },
              { icon: ShieldCheck, title: 'Honesty Guaranteed', desc: 'Every recommendation carries an explicit honesty badge — proven, pilot, fieldable, or development.' },
              { icon: MessageSquare, title: 'Executive Pathway', desc: 'Discovery maps directly to our engagement models: Boardroom Briefing, Architecture Sprint, Pilot, or Deployment.' },
            ].map((item, i) => (
              <div key={i} className={`p-6 rounded-2xl border ${
                isLight ? 'bg-ls-white border-ls-grey-dark/20 shadow-sm' : 'bg-ls-navy border-ls-white/10 shadow-xl'
              }`}>
                <item.icon className="w-8 h-8 text-ls-red mb-3" />
                <h4 className="font-display font-bold text-sm mb-1">{item.title}</h4>
                <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>{item.desc}</p>
              </div>
            ))}
          </div>
        </Reveal>

        <CtaBand
          theme={theme}
          title="Or Skip the Chat — Book Directly"
          text="If you prefer a human conversation immediately, our Executive Briefing team responds within two business days."
          ctaLabel="Book an Executive Briefing"
          ctaTo="/contact"
        />
      </div>
    </section>
  );
};

export default AskLightSpeed;