import React, { useState, useEffect, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ChevronLeft, Download, Save, Loader2, Eye, EyeOff, Copy, Check, FileText, Image, RotateCcw, ZoomIn, ZoomOut } from 'lucide-react';
import { cn } from '@/lib/athena/utils';
import { ATSGauge } from '@/components/athena/ATSGauge';
import type { Document } from '@/lib/athena/types';

type EditorMode = 'resume' | 'cover_letter';
type ViewMode = 'split' | 'preview' | 'editor';

interface DocumentEditorProps {
  initialContent?: string;
  documentType: EditorMode;
  jobId?: string;
}

export const DocumentEditor: React.FC<DocumentEditorProps> = ({
  initialContent = '',
  documentType = 'resume',
  jobId
}) => {
  const navigate = useNavigate();
  const [content, setContent] = useState(initialContent);
  const [aiContent, setAiContent] = useState(initialContent);
  const [humanizedContent, setHumanizedContent] = useState('');
  const [viewMode, setViewMode] = useState<ViewMode>('split');
  const [atsScore, setAtsScore] = useState(75);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const editorRef = useRef<HTMLTextAreaElement>(null);
  const previewRef = useRef<HTMLIFrameElement>(null);

  // Toolbar actions
  const [toolbarActions] = useState<Array<{ key: string; label: string; icon: React.ReactNode; hotkey?: string }>>([
    { key: 'bold', label: 'Bold', icon: <strong>B</strong>, hotkey: '⌘B' },
    { key: 'italic', label: 'Italic', icon: <em>I</em>, hotkey: '⌘I' },
    { key: 'underline', label: 'Underline', icon: <u>U</u>, hotkey: '⌘U' },
    { key: 'heading1', label: 'Heading 1', icon: <span className="font-bold text-xs">H1</span> },
    { key: 'heading2', label: 'Heading 2', icon: <span className="font-bold text-xs">H2</span> },
    { key: 'bullet', label: 'Bullet List', icon: <span className="text-xs">• List</span> },
    { key: 'numbered', label: 'Numbered List', icon: <span className="text-xs">1. List</span> },
    { key: 'link', label: 'Insert Link', icon: <span className="text-xs">🔗</span> },
  ]);

  const handleToolbarAction = (action: string) => {
    const textarea = editorRef.current;
    if (!textarea) return;

    const start = textarea.selectionStart;
    const end = textarea.selectionEnd;
    const selectedText = content.substring(start, end);
    let newText = '';
    let cursorOffset = 0;

    switch (action) {
      case 'bold':
        newText = `**${selectedText || 'bold text'}**`;
        cursorOffset = selectedText ? 0 : -2;
        break;
      case 'italic':
        newText = `*${selectedText || 'italic text'}*`;
        cursorOffset = selectedText ? 0 : -1;
        break;
      case 'underline':
        newText = `<u>${selectedText || 'underlined text'}</u>`;
        cursorOffset = selectedText ? 0 : -4;
        break;
      case 'heading1':
        newText = `# ${selectedText || 'Heading 1'}`;
        cursorOffset = selectedText ? 0 : 0;
        break;
      case 'heading2':
        newText = `## ${selectedText || 'Heading 2'}`;
        cursorOffset = selectedText ? 0 : 0;
        break;
      case 'bullet':
        newText = selectedText
          ? selectedText.split('\n').map(line => `- ${line}`).join('\n')
          : '- Item 1\n- Item 2';
        break;
      case 'numbered':
        newText = selectedText
          ? selectedText.split('\n').map((line, i) => `${i + 1}. ${line}`).join('\n')
          : '1. Item 1\n2. Item 2';
        break;
      case 'link':
        const url = prompt('Enter URL:');
        if (url) {
          newText = `[${selectedText || 'link text'}](${url})`;
        }
        break;
    }

    if (newText) {
      const newContent = content.substring(0, start) + newText + content.substring(end);
      setContent(newContent);
      setTimeout(() => {
        textarea.focus();
        textarea.setSelectionRange(
          start + newText.length + cursorOffset,
          start + newText.length + cursorOffset
        );
      }, 0);
    }
  };

  const generateAIContent = async () => {
    setLoading(true);
    // Simulate AI generation
    await new Promise(resolve => setTimeout(resolve, 2000));

    const templates = {
      resume: `# ${documentType === 'resume' ? 'Professional Resume' : 'Cover Letter'}

## Summary
Experienced professional with a proven track record in delivering high-quality results. Skilled in modern technologies and passionate about continuous learning.

## Experience
**Senior Developer** | Tech Company | 2022–Present
- Led development of scalable web applications
- Mentored junior developers
- Improved system performance by 40%

**Developer** | Startup Inc | 2020–2022
- Built responsive user interfaces
- Collaborated with cross-functional teams
- Implemented CI/CD pipelines

## Education
**Bachelor of Science in Computer Science** | University | 2020

## Skills
- **Languages:** JavaScript, TypeScript, Python
- **Frameworks:** React, Node.js, Express
- **Tools:** Git, Docker, AWS
`,
      cover_letter: `Dear Hiring Manager,

I am writing to express my strong interest in the position at your company. With my background in software development and passion for creating innovative solutions, I believe I would be a valuable addition to your team.

In my current role as a Senior Developer, I have led multiple projects from conception to deployment, consistently delivering high-quality code on schedule. My experience with React, TypeScript, and cloud technologies aligns well with your requirements.

I am particularly drawn to your company's mission and would welcome the opportunity to contribute to your continued success.

Thank you for your consideration.

Sincerely,
[Your Name]`
    };

    setAiContent(templates[documentType]);
    setLoading(false);
  };

  const humanizeContent = async () => {
    setLoading(true);
    await new Promise(resolve => setTimeout(resolve, 1500));

    // Simulate humanization - make it more natural
    const humanized = aiContent
      .replace(/Experienced professional with a proven track record/gi, 'I\'ve spent years building')
      .replace(/passionate about continuous learning/gi, 'always learning something new')
      .replace(/Led development of/gi, 'I led the development of')
      .replace(/Mentored junior developers/gi, 'I mentored junior developers')
      .replace(/Improved system performance by 40%/gi, 'boosted system performance by 40%')
      .replace(/Built responsive user interfaces/gi, 'I built responsive interfaces')
      .replace(/Collaborated with cross-functional teams/gi, 'worked closely with designers and product managers')
      .replace(/Implemented CI\/CD pipelines/gi, 'set up CI/CD pipelines');

    setHumanizedContent(humanized);
    setLoading(false);
  };

  const updateATSScore = () => {
    // Simulate ATS scoring based on content
    const keywords = ['react', 'typescript', 'node', 'python', 'aws', 'docker', 'git', 'sql', 'api', 'rest'];
    const contentLower = content.toLowerCase();
    const matches = keywords.filter(k => contentLower.includes(k)).length;
    const score = Math.min(95, 40 + matches * 5 + content.length / 100);
    setAtsScore(Math.round(score));
  };

  useEffect(() => {
    updateATSScore();
  }, [content]);

  const handleSave = async () => {
    setSaving(true);
    await new Promise(resolve => setTimeout(resolve, 1000));
    setSaving(false);
    // Would call API to save document
  };

  const handleDownload = (format: 'docx' | 'pdf') => {
    // Would generate and download document
    console.log(`Download as ${format.toUpperCase()}`);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(viewMode === 'split' ? humanizedContent || content : content);
  };

  const renderPreview = () => {
    // Simple markdown-like rendering for preview
    return content
      .split('\n')
      .map(line => {
        if (line.startsWith('# ')) return `<h1>${line.slice(2)}</h1>`;
        if (line.startsWith('## ')) return `<h2>${line.slice(3)}</h2>`;
        if (line.startsWith('### ')) return `<h3>${line.slice(4)}</h3>`;
        if (line.startsWith('- ')) return `<li>${line.slice(2)}</li>`;
        if (line.match(/^\d+\. /)) return `<li>${line.replace(/^\d+\. /, '')}</li>`;
        if (line.startsWith('**') && line.endsWith('**')) return `<p><strong>${line.slice(2, -2)}</strong></p>`;
        if (line.startsWith('*') && line.endsWith('*')) return `<p><em>${line.slice(1, -1)}</em></p>`;
        return `<p>${line}</p>`;
      })
      .join('\n');
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="mb-4 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div className="flex items-center gap-4">
          <button
            onClick={() => navigate(-1)}
            className="p-2 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors"
            aria-label="Back"
          >
            <ChevronLeft className="w-5 h-5" />
          </button>
          <div>
            <h1 className="font-display font-black text-xl sm:text-2xl text-ls-navy">
              {documentType === 'resume' ? 'Resume Editor' : 'Cover Letter Editor'}
            </h1>
            <p className="font-body text-sm text-ls-grey-dark">
              {viewMode === 'split' ? 'Side-by-side: AI vs Humanized' : viewMode === 'preview' ? 'Live preview' : 'Full editor'}
            </p>
          </div>
        </div>

        {/* ATS Score & Actions */}
        <div className="flex flex-wrap items-center justify-between gap-4">
          <ATSGauge score={atsScore} size={60} strokeWidth={6} showLabel label="ATS Score" />

          <div className="flex items-center gap-2">
            <button
              onClick={() => setViewMode('editor')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                viewMode === 'editor'
                  ? 'bg-ls-red text-ls-white'
                  : 'bg-ls-grey-light text-ls-grey-dark hover:bg-ls-grey-light/80'
              )}
            >
              <FileText className="w-4 h-4 mr-1" /> Editor
            </button>
            <button
              onClick={() => setViewMode('split')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                viewMode === 'split'
                  ? 'bg-ls-red text-ls-white'
                  : 'bg-ls-grey-light text-ls-grey-dark hover:bg-ls-grey-light/80'
              )}
            >
              <RotateCcw className="w-4 h-4 mr-1" /> Split View
            </button>
            <button
              onClick={() => setViewMode('preview')}
              className={cn(
                'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors',
                viewMode === 'preview'
                  ? 'bg-ls-red text-ls-white'
                  : 'bg-ls-grey-light text-ls-grey-dark hover:bg-ls-grey-light/80'
              )}
            >
              <Eye className="w-4 h-4 mr-1" /> Preview
            </button>
          </div>

          <div className="flex items-center gap-2 ml-auto">
            <button
              onClick={generateAIContent}
              disabled={loading}
              className="px-4 py-2 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-medium text-sm hover:border-ls-cyan hover:text-ls-cyan transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4 text-ls-cyan" />}
              <span>Generate AI</span>
            </button>
            <button
              onClick={humanizeContent}
              disabled={loading || !aiContent}
              className="px-4 py-2 rounded-lg border border-ls-grey-dark/30 bg-ls-white text-ls-grey-dark font-medium text-sm hover:border-emerald-500 hover:text-emerald-600 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Check className="w-4 h-4 text-emerald-600" />}
              <span>Humanize</span>
            </button>
            <button
              onClick={handleSave}
              disabled={saving}
              className="px-4 py-2 rounded-lg bg-ls-red text-ls-white font-bold text-sm hover:bg-ls-red/90 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {saving ? <Loader2 className="w-4 h-4 animate-spin" /> : <Save className="w-4 h-4" />}
              <span>Save</span>
            </button>
            <div className="flex items-center gap-1 border border-ls-grey-dark/30 rounded-lg overflow-hidden">
              <button
                onClick={() => handleDownload('docx')}
                className="px-3 py-2 text-sm font-medium text-ls-grey-dark hover:bg-ls-grey-light transition-colors flex items-center gap-1"
              >
                <Download className="w-4 h-4" />
                <span>.docx</span>
              </button>
              <button
                onClick={() => handleDownload('pdf')}
                className="px-3 py-2 text-sm font-medium text-ls-grey-dark hover:bg-ls-grey-light transition-colors flex items-center gap-1"
              >
                <Image className="w-4 h-4" />
                <span>.pdf</span>
              </button>
            </div>
          </div>
        </div>

        {/* Toolbar */}
        <div className="flex flex-wrap gap-1 mb-3 p-3 bg-ls-white rounded-xl border border-ls-grey-dark/30" role="toolbar" aria-label="Editor toolbar">
          {toolbarActions.map(action => (
            <button
              key={action.key}
              onClick={() => handleToolbarAction(action.key)}
              className="px-3 py-1.5 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors flex items-center gap-1.5"
              aria-label={`${action.label}${action.hotkey ? ` (${action.hotkey})` : ''}`}
            >
              {action.icon}
              <span className="hidden sm:inline font-body text-xs">{action.label}</span>
              {action.hotkey && <span className="hidden md:inline text-[10px] text-ls-grey-light-text px-1.5 py-0.5 rounded bg-ls-grey-light">{action.hotkey}</span>}
            </button>
          ))}
          <div className="w-px h-6 bg-ls-grey-dark/30 mx-2" />
          <button
            onClick={handleCopy}
            className="px-3 py-1.5 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors flex items-center gap-1.5"
            aria-label="Copy content"
          >
            <Copy className="w-4 h-4" />
            <span className="hidden sm:inline font-body text-xs">Copy</span>
          </button>
          <button
            onClick={() => setShowPreview(!showPreview)}
            className="px-3 py-1.5 rounded-lg text-ls-grey-dark hover:text-ls-red hover:bg-ls-red/10 transition-colors flex items-center gap-1.5"
            aria-label={showPreview ? 'Hide preview' : 'Show preview'}
          >
            {showPreview ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            <span className="hidden sm:inline font-body text-xs">{showPreview ? 'Hide' : 'Preview'}</span>
          </button>
        </div>

        {/* Editor Area */}
        <div className="flex-1 overflow-hidden bg-ls-white rounded-xl border border-ls-grey-dark/30 flex">
          {/* Left Panel - Editor or AI Content */}
          <div className={cn(
            'flex-1 flex flex-col min-w-0',
            viewMode === 'split' && 'border-r border-ls-grey-dark/30',
            viewMode === 'preview' && 'hidden'
          )}>
            <div className="px-4 py-2 border-b border-ls-grey-dark/30 flex items-center justify-between">
              <h3 className="font-display font-bold text-sm text-ls-navy">
                {viewMode === 'split' ? 'Your Version' : 'Editor'}
              </h3>
              <div className="flex items-center gap-1 text-[10px] text-ls-grey-light-text">
                {content.length} chars • {content.split('\n').length} lines
              </div>
            </div>
            <textarea
              ref={editorRef}
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="flex-1 p-4 font-body text-sm text-ls-navy bg-transparent resize-none focus:outline-none font-mono leading-relaxed"
              placeholder={`Start writing your ${documentType}...`}
              spellCheck={true}
              aria-label={`${documentType} editor`}
            />
          </div>

          {/* Right Panel - AI/Humanized or Preview */}
          {viewMode === 'split' && (
            <div className="flex-1 flex flex-col min-w-0 border-l border-ls-grey-dark/30 bg-ls-grey-light/30">
              <div className="px-4 py-2 border-b border-ls-grey-dark/30 flex items-center justify-between">
                <h3 className="font-display font-bold text-sm text-ls-navy">AI vs Humanized</h3>
              </div>
              <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {/* AI Version */}
                <div className="bg-ls-white rounded-lg border border-ls-grey-dark/30 p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-bold text-sm text-ls-navy flex items-center gap-2">
                      <Sparkles className="w-4 h-4 text-ls-cyan" />
                      AI Generated
                    </h4>
                    <ATSGauge score={Math.min(atsScore + 5, 95)} size={40} strokeWidth={4} showLabel={false} />
                  </div>
                  <pre className="whitespace-pre-wrap font-body text-sm text-ls-grey-dark max-h-64 overflow-y-auto">{aiContent}</pre>
                </div>

                {/* Humanized Version */}
                <div className="bg-ls-white rounded-lg border border-ls-grey-dark/30 p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-display font-bold text-sm text-ls-navy flex items-center gap-2">
                      <Check className="w-4 h-4 text-emerald-600" />
                      Humanized
                    </h4>
                    <ATSGauge score={atsScore} size={40} strokeWidth={4} showLabel={false} />
                  </div>
                  {humanizedContent ? (
                    <pre className="whitespace-pre-wrap font-body text-sm text-ls-grey-dark max-h-64 overflow-y-auto">{humanizedContent}</pre>
                  ) : (
                    <div className="text-center py-8 text-ls-grey-light-text">
                      <RotateCcw className="w-12 h-12 mx-auto mb-2 opacity-50" />
                      <p>Click "Humanize" to create a natural version</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {viewMode === 'preview' && (
            <div className="flex-1 flex flex-col min-w-0 bg-ls-white">
              <div className="px-4 py-2 border-b border-ls-grey-dark/30 flex items-center justify-between">
                <h3 className="font-display font-bold text-sm text-ls-navy">Live Preview</h3>
                <div className="flex items-center gap-2">
                  <button className="p-1 rounded hover:bg-ls-grey-light" aria-label="Zoom in"><ZoomIn className="w-4 h-4" /></button>
                  <button className="p-1 rounded hover:bg-ls-grey-light" aria-label="Zoom out"><ZoomOut className="w-4 h-4" /></button>
                </div>
              </div>
              <div className="flex-1 p-6 overflow-y-auto" style={{ maxWidth: '210mm', margin: '0 auto', backgroundColor: 'white', boxShadow: '0 0 20px rgba(0,0,0,0.1)' }}>
                <div className="prose prose-sm max-w-none" dangerouslySetInnerHTML={{ __html: renderPreview() }} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

// Need to import Sparkles
import { Sparkles } from 'lucide-react';

export default DocumentEditor;
