# Social Media Upload Checklist — LightSpeed Holdings

**Ready files:** `static/brand/social/`
**Time needed:** ~10 minutes (first-time provisioning ~30–60 min)
Check each box as you complete it.

---

## Account Provisioning (First Time Only)

Before any uploads, confirm each account exists and is owned by the company per
`docs/marketing/digital-identity-setup.md`. Owner: `social_media_manager`;
living register: `docs/marketing/digital-asset-register.md`.

- [ ] Accounts claimed with name LIGHTSPEED HOLDINGS LIMITED + handle `@lightspeedholdings` (Tier 1: LinkedIn, Facebook, Instagram, X)
- [ ] Accounts claimed on Tier 2/3: TikTok, YouTube, Threads (Threads = reserve only)
- [ ] 2FA enabled on the account email (`info.lightspeed@gmail.com`) and on each platform
- [ ] Business ownership set (Meta Business Suite, TikTok Business Center, Google business ownership, LinkedIn admin, X Professional)
- [ ] Digital Asset Register updated to `Live` for each provisioned platform

Then proceed with the per-platform uploads below.

---

## LinkedIn (Company page)

- [ ] Log in at https://www.linkedin.com/company and open your company page
- [ ] **Logo (profile image):** Click the logo/Edit → Upload `linkedin-profile.png` (400×400)
- [ ] **Banner:** Click the banner/Edit → Upload `linkedin-banner.png` (1584×396)
- [ ] **Name:** LIGHTSPEED HOLDINGS LIMITED
- [ ] **Tagline:** ASPIRE. ACT. ACHIEVE.
- [ ] **About:** One-para company description (can draft later)
- [ ] **Website:** https://lightspeedholdings.com
- [ ] Click **Save/Apply** — verify both images render

## Twitter/X

- [ ] Log in at https://twitter.com/settings/profile
- [ ] **Profile photo:** Change photo → Upload `twitter-profile.png` (400×400) → crop to circle
- [ ] **Header:** Change header → Upload `twitter-header.png` (1500×500)
- [ ] **Display name:** LIGHTSPEED HOLDINGS
- [ ] **Bio:** "Aspire. Act. Achieve." + short company line
- [ ] **Website:** https://lightspeedholdings.com
- [ ] Click **Save** — verify both images render

## Optional — GitHub

- [ ] Log in at https://github.com/settings/profile
- [ ] **Avatar:** Click avatar → Upload `github-profile.png`
- [ ] Save

---

**All files:** `static/brand/social/` — `linkedin-profile.png`, `linkedin-banner.png`, `twitter-profile.png`, `twitter-header.png`, `github-profile.png`
**Regenerate if needed:** `python static/brand/templates/generate-social-assets.py`

---

*Owner: `social_media_manager`. Done when all boxes are checked.*
