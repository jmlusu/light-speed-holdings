import { useEffect, useState } from 'react';

/**
 * Page Meta Tags Hook
 *
 - Sets <title>, meta description, Open Graph, and Twitter cards for the current page.
 - Usage: const { title, description } = usePageMeta('/what-we-do');
 *
 - Uses only built-in browser APIs (document.title, document.querySelector, etc.)
 - No external dependencies.
 */
export interface PageMeta {
  title: string;
  description: string;
  image?: string;
  type?: 'website' | 'article' | 'product';
  siteName?: string;
}

export function usePageMeta(route: string): PageMeta {
  const [meta, setMeta] = useState<PageMeta>({
    title: 'LightSpeed Holdings Limited',
    description:
      'LightSpeed Holdings Limited is an AI-native operator and partner helping organisations design, build, and govern sovereign agentic enterprises across Malawi and Africa.',
  });

  useEffect(() => {
    const routeMap: Record<string, PageMeta> = {
      '/': {
        title: 'LightSpeed Holdings Limited - AI-Native Operator and Partner',
        description:
          'LightSpeed Holdings Limited is an AI-native operator and partner helping organisations design, build, and govern sovereign agentic enterprises across Malawi and Africa.',
      },
      '/what-we-do': {
        title: 'What We Do | LightSpeed Holdings',
        description:
          'We design and build sovereign agentic enterprises for organisations across Malawi and Africa, combining AI agents, automation, and strategic governance.',
      },
      '/ai-company-builder': {
        title: 'AI Company Builder | LightSpeed Holdings',
        description:
          'Create and orchestrate AI agent hierarchies with our open-source CLI tool. Define agents in company-registry.yaml and generate OpenCode‑compatible markdown.',
      },
      '/solutions': {
        title: 'Solutions | LightSpeed Holdings',
        description:
          'Explore our AI-native solutions for agent orchestration, automation, data analytics, and research. Proven patterns for organisational transformation.',
      },
      '/sectors': {
        title: 'Sectors | LightSpeed Holdings',
        description:
          'Deep expertise across agriculture, finance, healthcare, education, energy, and government sectors. Tailored AI solutions for African markets.',
      },
      '/ai-assessment': {
        title: 'AI Readiness Assessment | LightSpeed Holdings',
        description:
          'Request a structured AI readiness assessment. We evaluate data, infrastructure, talent, and governance — and deliver a prioritised roadmap to an AI-native operating model.',
      },
      '/insights': {
        title: 'Insights | LightSpeed Holdings',
        description:
          'Thought leadership, research perspectives, and practical analysis on agentic AI, organisational design, and AI-native operations from a Malawian and African viewpoint.',
      },
      '/about': {
        title: 'About | LightSpeed Holdings',
        description:
          'We build practical AI-native systems from Malawi, helping organisations operate, decide, and grow with intelligent systems that are accessible, trustworthy, and designed for their market realities.',
      },
      '/contact': {
        title: 'Contact | LightSpeed Holdings',
        description:
          'Get in touch with LightSpeed Holdings. Discuss AI-native partnerships, explore use cases, or explore collaboration opportunities.',
      },
      '/use-cases': {
        title: 'Use Cases | LightSpeed Holdings',
        description:
          'Real-world AI-native use cases and deployments. See how organisations are using intelligent agents to automate work, improve decisions, and grow with AI.',
      },
      '/legal/privacy': {
        title: 'Privacy Policy | LightSpeed Holdings',
        description:
          'LightSpeed Holdings Privacy Policy. How we collect, use, disclose, and safeguard data for organisations and individuals we serve.',
      },
      '/legal/terms': {
        title: 'Terms of Service | LightSpeed Holdings',
        description:
          'LightSpeed Holdings Terms of Service. Governing the use of our platforms, services, and AI-native systems.',
      },
    };

    const pageMeta = routeMap[route];
    if (pageMeta) {
      setMeta(pageMeta);
    }

    // Apply meta tags to document
    const updateMeta = () => {
      const titleEl = document.querySelector('title');
      if (titleEl) titleEl.textContent = meta.title;

      const descEl = document.querySelector('meta[name="description"]');
      if (descEl) descEl.setAttribute('content', meta.description);

      // Open Graph
      const ogTitle = document.querySelector('meta[property="og:title"]');
      if (ogTitle) ogTitle.setAttribute('content', meta.title);

      const ogDesc = document.querySelector('meta[property="og:description"]');
      if (ogDesc) ogDesc.setAttribute('content', meta.description);

      const ogImage = document.querySelector('meta[property="og:image"]');
      if (ogImage && meta.image) ogImage.setAttribute('content', meta.image);

      const ogType = document.querySelector('meta[property="og:type"]');
      if (ogType && meta.type) ogType.setAttribute('content', meta.type);

      const ogSiteName = document.querySelector('meta[property="og:site_name"]');
      if (ogSiteName && meta.siteName) ogSiteName.setAttribute('content', meta.siteName);

      // Twitter cards
      const twitterCard = document.querySelector('meta[name="twitter:card"]');
      if (twitterCard) twitterCard.setAttribute('content', 'summary_large_image');

      const twitterTitle = document.querySelector('meta[name="twitter:title"]');
      if (twitterTitle) twitterTitle.setAttribute('content', meta.title);

      const twitterDesc = document.querySelector('meta[name="twitter:description"]');
      if (twitterDesc) twitterDesc.setAttribute('content', meta.description);

      const twitterImage = document.querySelector('meta[name="twitter:image"]');
      if (twitterImage && meta.image) twitterImage.setAttribute('content', meta.image);
    };

    updateMeta();

    // Also update the document title via the hook's title
    document.title = meta.title;

    return () => {
      // Cleanup on unmount - restore original title
      document.title = 'LightSpeed Holdings Limited - AI-Native Operator and Partner';
    };
  }, [route]);

  return meta;
}
