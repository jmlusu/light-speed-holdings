import React, { useState, useCallback, useRef } from 'react';
import { MessageSquare, Sparkles, ArrowRight, Send, Bot, User, CheckCircle2, ShieldCheck } from 'lucide-react';
import { SectionHeading } from './site/SectionHeading';
import { CtaBand } from './site/CtaBand';
import { HonestyBadge } from './site/HonestyBadge';
import { Reveal } from './Reveal';
import { useSite } from '../site-context';
import { solutions, honestyLabel } from '../data/siteContent';
import { CTAS } from '@/data/ctas';
import { Link } from 'react-router-dom';
import { trackJourneyEvent } from '../hooks/useJourneyEvents';

/* §15 knowledge boundary: refuse out-of-scope asks instead of fabricating. */
const OUT_OF_SCOPE_RE =
  /password|passphrase|api[ _-]?key|secret|credential|access token|private prompt|system prompt|internal (docs|document|documents|strategy|information|info)|confidential|source code|client (list|data|information)|unpublished|infrastructure details/i;

const BOUNDARY_MESSAGE = `I can't help with that. By design. This assistant answers only from LightSpeed's published site content: solutions, sectors, proof and insights. Requests for secrets, credentials, private prompts, or internal information stay outside the public knowledge boundary.

What I can still do: map your challenge to our published capabilities. For anything else, a human will answer. Pick a path below or keep typing.`;

type Step = 'welcome' | 'problem' | 'context' | 'results' | 'cta' | 'boundary';

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

const WELCOME_MESSAGE = `Welcome to Ask LightSpeed. The interactive discovery layer for our AI Company Builder platform.

I'll help you understand which LightSpeed capabilities match your needs. Think of me as your executive briefing prep assistant.

To get started: what's the core challenge keeping you up at night?`;

const PROBLEM_QUESTIONS = [
  'We need to build AI-native operations but lack the expertise',
  'Our current systems are manual and we want to automate',
  'We need governance and compliance automation for our AI deployments, aligned with HAOMTGV pillar H: Human CEOs owning outcomes',
  'We want to deploy AI agents across multiple departments, aligned with HAOMTGV pillar A: 89 AI agents with canonical 7 tools',
  'We need executive-level AI strategy and a boardroom briefing, aligned with HAOMTGV pillar O: 5-tier HITL approval matrix',
  'We need digital presence and e-commerce with mobile money checkout, aligned with HAOMTGV pillar M: shared semantic memory system',
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
  const askTrackedRef = useRef(false);
  const askCompletedRef = useRef(false);

  const trackAskStarted = useCallback(() => {
    if (askTrackedRef.current) return;
    askTrackedRef.current = true;
    trackJourneyEvent({ eventType: 'ask_started', journeyStage: 'consideration' });
  }, []);

  const addMessage = useCallback((role: 'assistant' | 'user', text: string) => {
    setMessages(prev => [...prev, { id: Date.now().toString(), role, text }]);
  }, []);

  const handleSend = useCallback(() => {
    if (!inputValue.trim()) return;
    const userText = inputValue.trim();
    trackAskStarted();
    addMessage('user', userText);
    setInputValue('');

    if (OUT_OF_SCOPE_RE.test(userText)) {
      setState(prev => ({ ...prev, step: 'boundary' }));
      addMessage('assistant', BOUNDARY_MESSAGE);
      return;
    }

    if (state.step === 'context') {
      const nextField = !state.industry ? 'industry' : !state.timeline ? 'timeline' : 'timeline';
      if (nextField === 'industry') {
        setState(prev => ({ ...prev, industry: userText }));
        addMessage('assistant', `Great, ${userText}. Now, what is your target timeline?\n`);
      } else {
        const timeline = userText;
        const matchedSolutions = matchSolutions(state.problem, userText);
        setState(prev => ({
          ...prev,
          timeline,
          step: 'results',
          matchedSolutions,
        }));
        if (!askCompletedRef.current) {
          askCompletedRef.current = true;
          trackJourneyEvent({
            eventType: 'ask_completed',
            journeyStage: 'intent',
            metadata: { solutionMatches: matchedSolutions.length },
          });
        }
        addMessage('assistant', `Based on your inputs, here's what I found:\n\n`);
        setTimeout(() => {
          const resultText = buildResultsText(matchedSolutions, timeline);
          addMessage('assistant', resultText);
        }, 500);
      }
    } else {
      const problem = PROBLEM_QUESTIONS.find(q =>
        userText.toLowerCase().includes(q.toLowerCase().split(' ').slice(0, 3).join(' '))
      ) || userText;
      setState(prev => ({
        ...prev,
        step: 'context',
        problem,
        industry: '',
        timeline: '',
        matchedSolutions: [],
      }));
      addMessage('assistant', `Thank you. You mentioned: "${problem}"\n\nNow, let me narrow things down a bit:`);
      setTimeout(() => {
        addMessage('assistant', `Which sector best describes your organisation?\n`);
      }, 500);
    }
  }, [inputValue, state, addMessage, trackAskStarted]);

  const matchSolutions = useCallback((problem: string, context: string): typeof solutions => {
    const lowerProblem = problem.toLowerCase();
    return solutions.filter(s => {
      const titleMatch = s.title.toLowerCase().includes(lowerProblem.slice(0, 4)) ||
        lowerProblem.includes(s.title.toLowerCase().split(' ').slice(0, 2).join(' '));
      const descMatch = s.description.toLowerCase().slice(0, 20).includes(lowerProblem.slice(0, 4));
      return titleMatch || descMatch;
    }).length > 0 ? solutions.filter(s => {
      const titleMatch = s.title.toLowerCase().includes(lowerProblem.slice(0, 4));
      const descMatch = s.description.toLowerCase().slice(0, 30).includes(lowerProblem.slice(0, 4));
      return titleMatch || descMatch;
    }) : [];
  }, [solutions]);

  const buildResultsText = useCallback((matched: typeof solutions, timeline: string): string => {
    if (matched.length === 0) {
      return "I couldn't find a published capability that matches that closely. I'd rather say that than guess. Pick a next step below: start a conversation to scope it, or explore every published solution.";
    }
    let text = `Based on your inputs, I found ${matched.length} capability match${matched.length > 1 ? 'es' : ''}:\n\n`;
    matched.forEach((s, i) => {
      text += `${i + 1}. ${s.title}. ${s.description.slice(0, 80)}...\n`;
    });
    text += `\nWith a ${timeline.toLowerCase()}, we can start with an Executive Boardroom Briefing to align on scope, then move to ${matched[0]?.title || 'deployment'}.\n`;
    text += `\nHAOMTGV alignment: pillars H (Human CEOs), A (Agents), O (Operating Model), M (Memory), T (Tools), G (Governance), V (Visuals) guide every engagement through our 5-tier HITL and 4 governance gates (G1–G4).\n`;
    text += `\nWould you like to start a conversation?`;
    return text;
  }, []);

  const handleQuickQuestion = useCallback((question: string) => {
    trackAskStarted();
    addMessage('user', question);
    setState(prev => ({ ...prev, step: 'context', problem: question }));
    setTimeout(() => {
      addMessage('assistant', `Understood: "${question}"\n\nWhich sector best describes your organisation?\n`);
    }, 500);
  }, [addMessage, trackAskStarted]);

  const handleResultClick = useCallback((solution: typeof solutions[0]) => {
    addMessage('assistant', `You selected ${solution.title}. This is a ${solution.honestyBadge} capability.`);
    setState(prev => ({ ...prev, step: 'cta' }));
  }, [addMessage]);

  const handleStartConversation = useCallback(() => {
    onRequestBriefing('Discovery via Ask LightSpeed, matched capabilities');
  }, [onRequestBriefing]);

  return (
    <section id="ask-lightspeed" className={`min-h-screen py-12 sm:py-20 px-4 sm:px-8 ${
      isLight ? 'bg-ls-grey-light/50' : 'bg-ls-navy/90'
    }`}>
      <div className="max-w-4xl mx-auto">
        <Reveal>
          <SectionHeading
            theme={theme}
            level="h1"
            eyebrow="INTERACTIVE DISCOVERY"
            title="Ask LightSpeed"
            lead="Tell us your challenge. Our AI discovery layer maps it to proven capabilities, governance models, and engagement paths, all with explicit honesty badges."
          />
        </Reveal>

        {/* Chat Interface */}
        <div className={`rounded-3xl overflow-hidden shadow-2xl ${
          isLight ? 'bg-ls-white' : 'bg-ls-navy'
        }`}>
          {/* Chat Header */}
          <div className={`flex items-center gap-3 px-6 py-4 ${
            isLight ? 'bg-ls-grey-light/50' : 'bg-ls-navy/50'
          }`}>
            <div className="w-10 h-10 rounded-full bg-ls-red flex items-center justify-center">
              <Bot className="w-5 h-5 text-ls-white" />
            </div>
            <div>
              <h3 className="font-display font-black text-base">Ask LightSpeed</h3>
              <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                Public knowledge boundary • Honest by design
              </p>
            </div>
            <div className="ml-auto flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-ls-cyan animate-pulse" />
              <span className="text-xs font-medium text-ls-cyan">Online</span>
            </div>
          </div>

          {/* §14 public-safe knowledge boundary notice */}
          <div
            className={`px-6 py-2.5 flex items-start gap-2 text-[11px] leading-relaxed ${
              isLight
                ? 'bg-ls-cyan/5 text-ls-grey-dark'
                : 'bg-ls-cyan/5 text-ls-grey-light-text'
            }`}
            role="note"
          >
            <ShieldCheck className="w-3.5 h-3.5 shrink-0 mt-0.5 text-ls-cyan" aria-hidden="true" />
            <span>
              <strong className="text-ls-cyan">Public knowledge only.</strong> This assistant answers from
              LightSpeed&rsquo;s published site content. It cannot access secrets, credentials, private prompts,
              internal agent instructions, client information, financial data, infrastructure details, or
              unpublished strategy. Public layer in, public layer out.
            </span>
          </div>

          {/* Messages (§ aria-live on assistant turns) */}
          <div
            className="px-6 py-6 space-y-4 max-h-[400px] overflow-y-auto"
            role="log"
            aria-live="polite"
            aria-label="Ask LightSpeed conversation"
          >
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
            <div className={`px-6 py-4 ${
              isLight ? 'text-ls-navy' : 'text-ls-white'
            }`}>
              <p className={`text-xs font-body font-medium tracking-wider mb-3 ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                Quick select: what&apos;s your core challenge?
              </p>
              <div className="flex flex-wrap gap-2">
                {PROBLEM_QUESTIONS.map((q) => (
                  <button
                    key={q}
                    onClick={() => handleQuickQuestion(q)}
                    className={`btn-milled btn-milled-secondary px-3 py-1.5 rounded-full text-xs font-body font-medium transition-all cursor-pointer ${
                      isLight
                        ? 'bg-ls-grey-light/50 text-ls-navy hover:bg-ls-red hover:text-ls-white'
                        : 'bg-ls-white/5 text-ls-white hover:bg-ls-red hover:text-ls-white'
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
            <div className="px-6 py-4">
              <p className={`text-xs font-body font-medium tracking-wider mb-3 ${
                isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'
              }`}>
                Matched capabilities:
              </p>
              <div className="space-y-2 mb-6">
                {state.matchedSolutions.map((s, i) => (
                  <button
                    key={s.slug}
                    onClick={() => handleResultClick(s)}
                    className={`btn-milled btn-milled-secondary w-full text-left px-4 py-3 rounded-xl transition-all cursor-pointer ${
                      isLight
                        ? 'hover:bg-ls-red/5'
                        : 'hover:bg-ls-red/5'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="font-display font-bold text-sm">{s.title}</span>
                        <p className={`text-xs ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                          {s.description.slice(0, 60)}...
                        </p>
                      </div>
                      <HonestyBadge label={honestyLabel(s.honestyBadge)} />
                    </div>
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Honest empty state (§78): no published match → say so + next moves */}
          {state.step === 'results' &&
            state.matchedSolutions.length === 0 && (
            <div className="px-6 py-6 text-center">
              <div className="w-12 h-12 rounded-full bg-ls-red/10 text-ls-red flex items-center justify-center mx-auto mb-4">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h4 className="font-display font-black text-lg mb-2">No published match</h4>
              <p className={`text-sm mb-4 ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                Nothing in our published content matches that closely. I&apos;d rather say so than guess.
                Take one of these next steps instead.
              </p>
              <div className="flex flex-wrap items-center justify-center gap-3">
                <button
                  onClick={handleStartConversation}
                  className="btn-milled btn-milled-primary inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 hover:bg-ls-red/90 cursor-pointer"
                >
                  {CTAS.primary.label}
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <Link
                  to="/solutions"
                  className={`btn-milled btn-milled-secondary inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all cursor-pointer ${
                    isLight
                      ? 'text-ls-navy hover:bg-ls-grey-light'
                      : 'text-ls-white hover:bg-ls-white/5'
                  }`}
                >
                  Explore All Solutions
                </Link>
                <Link
                  to="/use-cases"
                  className={`btn-milled btn-milled-secondary inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all cursor-pointer ${
                    isLight
                      ? 'text-ls-navy hover:bg-ls-grey-light'
                      : 'text-ls-white hover:bg-ls-white/5'
                  }`}
                >
                  View Use Cases
                </Link>
              </div>
            </div>
          )}

          {/* CTA step */}
          {state.step === 'cta' && (
            <div className="px-6 py-6 text-center">
              <div className="w-12 h-12 rounded-full bg-ls-cyan/20 text-ls-cyan flex items-center justify-center mx-auto mb-4">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <h4 className="font-display font-black text-xl mb-2">Discovery Complete</h4>
              <p className={`text-sm ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'} mb-4`}>
                Based on your inputs, I've mapped your challenge to LightSpeed capabilities. Ready to start a conversation?
              </p>
              <button
                onClick={handleStartConversation}
                className="btn-milled btn-milled-primary inline-flex items-center gap-2.5 px-7 py-3.5 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 hover:bg-ls-red/90 cursor-pointer"
              >
                {CTAS.primary.label}
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          )}

          {/* Boundary step: refused ask → honest escalation (§15, no dead ends) */}
          {state.step === 'boundary' && (
            <div className="px-6 py-6 bg-ls-cyan/5 text-center">
              <div className="w-12 h-12 rounded-full bg-ls-cyan/20 text-ls-cyan flex items-center justify-center mx-auto mb-4">
                <ShieldCheck className="w-6 h-6" />
              </div>
              <h4 className="font-display font-black text-lg mb-2">Outside the public boundary</h4>
              <p className={`text-sm mb-4 ${isLight ? 'text-ls-grey-dark' : 'text-ls-grey-light-text'}`}>
                Ask LightSpeed answers from published content only. Secrets, credentials, prompts and
                internal information stay out. Pick a path below, or keep typing to restart discovery.
              </p>
              <div className="flex flex-wrap items-center justify-center gap-3">
                <button
                  onClick={handleStartConversation}
                  className="btn-milled btn-milled-primary inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase bg-ls-red text-ls-white shadow-lg shadow-ls-red/30 hover:bg-ls-red/90 cursor-pointer"
                >
                  {CTAS.primary.label}
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                <Link
                  to="/solutions"
                  className={`btn-milled btn-milled-secondary inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all cursor-pointer ${
                    isLight
                      ? 'text-ls-navy hover:bg-ls-grey-light'
                      : 'text-ls-white hover:bg-ls-white/5'
                  }`}
                >
                  Explore Solutions
                </Link>
                <Link
                  to="/use-cases"
                  className={`btn-milled btn-milled-secondary inline-flex items-center gap-2 px-6 py-3 rounded-full font-bold text-xs tracking-widest uppercase transition-all cursor-pointer ${
                    isLight
                      ? 'text-ls-navy hover:bg-ls-grey-light'
                      : 'text-ls-white hover:bg-ls-white/5'
                  }`}
                >
                  View Use Cases
                </Link>
              </div>
            </div>
          )}

          {/* Input */}
          <div className="px-6 py-4">
            <div className="flex gap-3">
              <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                placeholder={
                  state.step === 'cta' || state.step === 'boundary'
                    ? 'Or type to ask something else...'
                    : 'Type your response...'
                }
                className={`flex-1 px-4 py-2.5 rounded-xl text-sm outline-none focus:ring-1 focus:ring-ls-red transition-all font-medium ${
                  isLight
                    ? 'bg-ls-grey-light/90 text-ls-navy placeholder:text-ls-navy/50 shadow-inner'
                    : 'bg-ls-navy text-ls-white placeholder:text-ls-white/50 shadow-inner'
                }`}
              />
              <button
                onClick={handleSend}
                disabled={!inputValue.trim()}
                className="btn-milled btn-milled-primary px-4 py-2.5 rounded-xl bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all shadow-md shadow-ls-red/25 cursor-pointer"
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
              { icon: ShieldCheck, title: 'Honesty Guaranteed', desc: 'Every recommendation carries an explicit honesty badge: proven, pilot, fieldable, or development.' },
              { icon: MessageSquare, title: 'Executive Pathway', desc: 'Discovery maps directly to our engagement models: Boardroom Briefing, Architecture Sprint, Pilot, or Deployment.' },
            ].map((item, i) => (
              <div key={i} className={`p-6 rounded-2xl ${
                isLight ? 'bg-ls-white shadow-sm' : 'bg-ls-navy shadow-xl'
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
          title={`Or Skip the Chat. ${CTAS.primary.label}`}
          text="If you prefer a human conversation immediately, our team responds within two business days."
        />
      </div>
    </section>
  );
};

export default AskLightSpeed;
