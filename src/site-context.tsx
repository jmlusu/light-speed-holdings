import { createContext, useContext } from 'react';
import type { ComponentType } from 'react';

export type Theme = 'light' | 'dark';

export interface SiteContextValue {
  theme: Theme;
  onToggleTheme: () => void;
  onRequestBriefing: (summary?: string) => void;
  isBriefingOpen: boolean;
  briefingSummary: string;
  closeBriefing: () => void;
}

export const SiteContext = createContext<SiteContextValue | null>(null);

export function useSite(): SiteContextValue {
  const ctx = useContext(SiteContext);
  if (!ctx) throw new Error('useSite must be used within SiteProvider');
  return ctx;
}

export const withSite = <P extends object>(Page: ComponentType<P>): React.FC => {
  const Wrapped: React.FC = () => {
    const { theme, onRequestBriefing } = useSite();
    const pageProps = { theme, onRequestBriefing } as P;
    return <Page {...pageProps} />;
  };
  Wrapped.displayName = `WithSite(${Page.displayName || Page.name || 'Page'})`;
  return Wrapped;
};

export default useSite;
