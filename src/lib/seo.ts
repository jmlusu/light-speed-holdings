export interface PageMeta {
  title: string;
  description: string;
  type?: string;
  image?: string;
  url?: string;
}

function upsertMeta(attr: 'name' | 'property', key: string, content: string) {
  let el = document.head.querySelector(`meta[${attr}="${key}"]`);
  if (!el) {
    el = document.createElement('meta');
    el.setAttribute(attr, key);
    document.head.appendChild(el);
  }
  el.setAttribute('content', content);
}

export function applyPageMeta(meta: PageMeta): void {
  document.title = meta.title;
  upsertMeta('name', 'description', meta.description);
  upsertMeta('property', 'og:title', meta.title);
  upsertMeta('property', 'og:description', meta.description);
  upsertMeta('property', 'og:type', meta.type ?? 'website');
  if (meta.url) upsertMeta('property', 'og:url', meta.url);
  if (meta.image) {
    const abs = meta.image.startsWith('http')
      ? meta.image
      : window.location.origin + meta.image;
    upsertMeta('property', 'og:image', abs);
    upsertMeta('name', 'twitter:image', abs);
  }
  upsertMeta('name', 'twitter:card', 'summary_large_image');
  upsertMeta('name', 'twitter:title', meta.title);
  upsertMeta('name', 'twitter:description', meta.description);
  if (meta.url) {
    let link = document.head.querySelector(
      'link[rel="canonical"]'
    ) as HTMLLinkElement | null;
    if (!link) {
      link = document.createElement('link');
      link.rel = 'canonical';
      document.head.appendChild(link);
    }
    link.href = meta.url;
  }
}
