# Performance Testing Matrix (Phase 14 — Sections 44, 29, 30)

## Test Conditions
Connectivity levels:
- [ ] Fast connection (fiber/broadband, ~50+ Mbps)
- [ ] Average connection (cable/4G, ~10-20 Mbps)
- [ ] Slow connection (2G/limited broadband, ~1-5 Mbps)
- [ ] Offline / no connectivity (fallback check)

## Device Categories
- [ ] Desktop (high-performance, modern GPU)
- [ ] Desktop (mid-range, integrated graphics)
- [ ] Laptop (typical business laptop)
- [ ] Modern iPhone (latest iOS Safari)
- [ ] Modern Android (latest Chrome)
- [ ] Low-power device (older Android, budget phone)
- [ ] iPad / tablet devices

## Display Categories
- [ ] High-resolution display (4K, Retina)
- [ ] Standard-resolution display (1080p, sRGB)
- [ ] Low-resolution display (older screens, compact)

## Core Web Vitals Targets
| Metric | Target | Measurement Tool |
|--------|--------|------------------|
| **LCP** (Largest Contentful Paint) | < 2.5s | PageSpeed Insights, Lighthouse, Web Vitals API |
| **INP** (Interaction to Next Paint) | < 200ms | Chrome DevTools, Web Vitals API |
| **CLS** (Cumulative Layout Shift) | < 0.1 | Chrome DevTools, Web Vitals API |

## Additional Performance Metrics
- [ ] JavaScript bundle size (per chunk, total)
- [ ] GPU utilization (WebGL debugging tools)
- [ ] Memory usage (JS heap, WebGL textures)
- [ ] Texture memory (total, per-asset)
- [ ] Frame rate (FPS) — Desktop: 60 FPS where practical, Mobile: 30-60 FPS
- [ ] Model loading time (GLTF/GLB parse and instantiate)
- [ ] Mobile thermal performance (sustained performance over time)
- [ ] Frustum culling effectiveness
- [ ] Animation frame timing

## Performance Testing Tools
- [ ] Lighthouse CI / automated CI integration
- [ ] Web Vitals JavaScript API
- [ ] Chrome DevTools Performance panel
- [ ] PageSpeed Insights
- [ ] GTmetrix
- [ ] WebGL Report (threejs.org/webglreport/)
- [ ] Custom performance monitoring dashboard
- [ ] Real-user monitoring (RUM) for production data

## Device-Specific Checks
### Low-Power Device
- [ ] Scene renders without freezing
- [ ] Texture memory stays within limits
- [ ] Frame rate stays at 30 FPS minimum
- [ ] No excessive thermal throttling signs
- [ ] Model loading completes within 5s

### High-Resolution Display
- [ ] No blurry textures or geometries
- [ ] Draco compression artifacts acceptable
- [ ] LCP within target on fast connection
- [ ] CLS stable (no layout shifts at large viewport)
- [ ] Asset resolution appropriate (KTX2 where applicable)

### Slow Connection
- [ ] Critical content loads first
- [ ] Non-critical 3D lazy-loaded after initial paint
- [ ] LCP < 2.5s even on 3G-like conditions
- [ ] Visual fallback shown if 3D times out
- [ ] Core content readable without 3D

## Performance Budget Enforcement
- [ ] Bundle size limits in CI (ruff/mypy don't check this, use bundle-analyzer)
- [ ] Asset weight budgets (images: < 500KB total, JS: < 150KB/gzip per chunk)
- [ ] Texture memory limit: 128MB WebGL budget
- [ ] FPS thresholds enforced in testing
- [ ] Performance budget fails PR gate if exceeded
