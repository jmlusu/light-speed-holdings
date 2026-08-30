# Brand Deployment Guide — Email Signatures & Social Media

**Created:** 2026-08-27
**Owner:** CMO + IT
**Status:** Ready for deployment
**Checklist:** [`docs/SOCIAL_MEDIA_UPLOAD_CHECKLIST.md`](SOCIAL_MEDIA_UPLOAD_CHECKLIST.md) — step-by-step boxes for LinkedIn/Twitter/GitHub

---

## 1. Email Signature Deployment

### Files
| File | Location | Purpose |
|------|----------|---------|
| `email-signature-team.html` | `static/brand/templates/` | Team-ready page with copy buttons |
| `email-signature.html` | `static/brand/templates/` | Standalone signature template |

### How to Deploy

**Option A: Share the HTML page (Recommended)**
1. Host `email-signature-team.html` on your website or internal server
2. Share the URL with all team members
3. Each person opens the page, clicks "Copy" next to their signature variant
4. Paste into their email client settings

**Option B: Send the HTML directly**
1. Email the HTML content to each team member
2. Instruct them to paste it into their email signature settings

### Email Client Instructions

| Client | Steps |
|--------|-------|
| **Gmail** | Settings (gear) → See all settings → General → Signature → Create new → Paste HTML |
| **Outlook Desktop** | File → Options → Mail → Signatures → New → Paste in edit box |
| **Outlook Web** | Settings (gear) → View all Outlook settings → Mail → Compose and reply → Email signature → Paste HTML |
| **Apple Mail** | Mail → Preferences → Signatures → Add (+) → Paste HTML |
| **Yahoo** | Settings → More settings → Mailbox → Email signature → Paste HTML |

### Pre-Filled CEO Signature
The CEO signature is already filled in with:
- **Name:** Jack Mlusu
- **Title:** Founder & CEO
- **Email:** jmlusu@gmail.com
- **Phone:** +265 (0) 980 016 004
- **Web:** lightspeedholdings.com

### Team Template
Team members should replace these placeholders:
- `[YOUR NAME]` → Their full name
- `[YOUR TITLE]` → Their job title
- `[YOUR EMAIL]` → Their email address
- `[YOUR PHONE]` → Their phone number

---

## 2. Social Media Profile Setup

### Generated Assets

| Platform | File | Dimensions | Purpose |
|----------|------|------------|---------|
| LinkedIn Profile | `linkedin-profile.png` | 400×400px | Profile photo |
| LinkedIn Banner | `linkedin-banner.png` | 1584×396px | Background photo |
| Twitter/X Profile | `twitter-profile.png` | 400×400px | Profile photo |
| Twitter/X Header | `twitter-header.png` | 1500×500px | Header image |
| GitHub Avatar | `github-profile.png` | 400×400px | Profile photo |
| General Avatar | `avatar-1024.png` | 1024×1024px | High-res for any use |

All files are in: `static/brand/social/`

### LinkedIn Setup

**Profile Photo:**
1. Go to https://www.linkedin.com/in/settings/profile-photo/
2. Click "Change photo"
3. Upload `linkedin-profile.png`
4. Adjust crop and save

**Background Photo (Banner):**
1. Go to your LinkedIn profile
2. Click the pencil icon on the background area
3. Upload `linkedin-banner.png`
4. Adjust and save

### Twitter/X Setup

**Profile Photo:**
1. Go to https://twitter.com/settings/profile
2. Click "Change photo"
3. Upload `twitter-profile.png`
4. Adjust and save

**Header Image:**
1. Go to https://twitter.com/settings/header
2. Click "Change photo"
3. Upload `twitter-header.png`
4. Adjust and save

### GitHub Setup

**Avatar:**
1. Go to https://github.com/settings/profile
2. Click "Edit profile"
3. Click the camera icon on the avatar
4. Upload `github-profile.png`
5. Save

---

## 3. Checklist

### Email Signatures
- [ ] Host or share `email-signature-team.html` with team
- [ ] CEO signature installed and tested
- [ ] All team members have installed their signatures
- [ ] Test email sent to verify signature renders correctly

### LinkedIn
- [ ] Profile photo uploaded
- [ ] Background banner uploaded
- [ ] Company name and description updated
- [ ] Tagline added to profile

### Twitter/X
- [ ] Profile photo uploaded
- [ ] Header image uploaded
- [ ] Bio updated with company tagline
- [ ] Pinned tweet or first post with brand assets

### GitHub
- [ ] Organization avatar uploaded
- [ ] README.md updated with brand assets
- [ ] Repository headers use official logo

---

## 4. Asset Locations Quick Reference

```
static/brand/
├── social/
│   ├── linkedin-profile.png      (400×400)
│   ├── linkedin-banner.png       (1584×396)
│   ├── twitter-profile.png       (400×400)
│   ├── twitter-header.png        (1500×500)
│   ├── github-profile.png        (400×400)
│   ├── avatar-1024.png           (1024×1024)
│   ├── facebook-cover-3.svg      (existing)
│   └── facebook-cover-3.pdf      (existing)
├── templates/
│   ├── email-signature-team.html  (team deployment page)
│   ├── email-signature.html       (standalone template)
│   └── generate-social-assets.py  (regenerate if needed)
```

---

## 5. Troubleshooting

| Issue | Solution |
|-------|----------|
| Email signature HTML doesn't paste correctly | Use "Paste as HTML" or "Source" mode in email editor |
| Profile image looks blurry | Use the 1024×1024 avatar and let the platform resize |
| Banner image is cropped | Re-upload and adjust the crop area |
| Colors look different | Ensure you're uploading PNG, not JPG (PNG preserves colors) |
| Need to regenerate assets | Run `python generate-social-assets.py` in `static/brand/templates/` |

---

*For questions, contact the CMO or IT team.*
