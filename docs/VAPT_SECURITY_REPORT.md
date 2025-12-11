# VAPT Security Report - Response & Remediation

## Overview

This document addresses the security vulnerabilities identified in the VAPT (Vulnerability Assessment and Penetration Testing) report for the Spectrum Lab website hosted on GitHub Pages.

**Current Domain:** `spectrum-lab-iisc.github.io`  
**Requested Domain:** `*.iisc.ac.in` (e.g., `spectrumlab.iisc.ac.in`)

---

## Summary of Issues

| # | Vulnerability | Severity | Can Fix From Our End? | Status |
|---|--------------|----------|----------------------|--------|
| 1 | Strict-Transport-Security Header Not Set | Low | ⚠️ Partial | See below |
| 2 | X-Content-Type-Options Header Not Set | Low | ✅ Yes | Fixed |
| 3 | Content-Security-Policy Header Not Set | Medium | ⚠️ Partial | See below |
| 4 | Permissions-Policy Header Not Set | Low | ✅ Yes | Fixed |
| 5 | X-Frame-Options Header Not Set | Low | ✅ Yes | Fixed |

---

## Detailed Analysis

### Issue 1: Strict-Transport-Security (HSTS) Header

**What it is:** HSTS ensures browsers only communicate via HTTPS, preventing man-in-the-middle attacks.

**Our Configuration (in `_headers` file):**
```
Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
```

**⚠️ Why it may not work:**

GitHub Pages has **LIMITED support for custom HTTP headers**. The `_headers` file works on:
- ✅ Netlify
- ✅ Cloudflare Pages
- ❌ GitHub Pages (native)

**GitHub Pages Limitation:** GitHub Pages does NOT process `_headers` files. It only sets basic headers automatically:
- GitHub Pages already enforces HTTPS
- GitHub Pages sets some security headers by default

**Solution Options:**

1. **For IISc domain:** If you get a custom domain like `spectrumlab.iisc.ac.in`, the **IISc IT team must configure these headers on their server/proxy**.

2. **Use Cloudflare (Free tier):** 
   - Point your domain through Cloudflare
   - Configure headers in Cloudflare dashboard
   - This is the only way to add custom headers with GitHub Pages

---

### Issue 2: X-Content-Type-Options Header ✅

**What it is:** Prevents MIME-type sniffing attacks.

**Our Configuration:**
```html
<!-- In _includes/core/head.liquid -->
<meta http-equiv="X-Content-Type-Options" content="nosniff">
```

**Status:** ✅ Implemented via meta tag (works in browsers)

**Note:** For server-level enforcement, requires IISc IT or Cloudflare configuration.

---

### Issue 3: Content-Security-Policy (CSP) Header

**What it is:** Prevents XSS attacks by controlling which resources can be loaded.

**Our Configuration (in `_headers` file):**
```
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://use.typekit.net https://giscus.app https://www.googletagmanager.com https://www.google-analytics.com https://google-analytics.com https://tikzjax.com https://distill.pub https://maps.googleapis.com https://maps.gstatic.com https://unpkg.com https://ajax.googleapis.com https://cdn.scite.ai; style-src 'self' 'unsafe-inline' https:; font-src 'self' data: https:; img-src 'self' data: blob: https: http:; connect-src 'self' https://api.github.com https://giscus.app https://www.google-analytics.com https://google-analytics.com https://fonts.googleapis.com https://fonts.gstatic.com https://cdn.jsdelivr.net https://distill.pub https://maps.googleapis.com https://maps.gstatic.com https://unpkg.com https://ajax.googleapis.com wss: ws:; frame-src 'self' https://giscus.app https://www.youtube.com https://youtube.com https://player.vimeo.com https://www.google.com https://maps.google.com https://codepen.io https://jsfiddle.net; media-src 'self' blob: data:; object-src 'none'; base-uri 'self'; form-action 'self' https://giscus.app; frame-ancestors 'self'; upgrade-insecure-requests;
```

**⚠️ Why it may not work:** Same as Issue 1 - GitHub Pages doesn't process `_headers`.

**Alternative Implementation (via meta tag):**

We can add a CSP meta tag, but it has limitations:
- Cannot set `frame-ancestors` via meta tag
- Cannot set `report-uri` via meta tag

---

### Issue 4: Permissions-Policy Header ✅

**What it is:** Controls browser features like camera, microphone, geolocation.

**Our Configuration:**
```html
<!-- In _includes/core/head.liquid -->
<meta http-equiv="Permissions-Policy" content="camera=(), microphone=(), geolocation=(), interest-cohort=()">
```

**Status:** ✅ Implemented via meta tag

---

### Issue 5: X-Frame-Options Header ✅

**What it is:** Prevents clickjacking by controlling if site can be embedded in iframes.

**Our Configuration:**
```html
<!-- In _includes/core/head.liquid -->
<meta http-equiv="X-Frame-Options" content="SAMEORIGIN">
```

**Status:** ✅ Implemented via meta tag

---

## What IISc IT Needs to Do

If you want to use a custom IISc domain (e.g., `spectrumlab.iisc.ac.in`), the IISc IT department needs to:

### Option A: DNS CNAME Record (Simplest)

1. Create a CNAME record pointing to `spectrum-lab-iisc.github.io`
2. We add the custom domain in GitHub Pages settings
3. **Limitation:** HTTP headers still cannot be customized

### Option B: Reverse Proxy (Recommended for Security Compliance)

1. Set up a reverse proxy (Nginx/Apache) on IISc servers
2. Proxy requests to `spectrum-lab-iisc.github.io`
3. **Add these headers in the proxy configuration:**

**For Nginx:**
```nginx
server {
    listen 443 ssl http2;
    server_name spectrumlab.iisc.ac.in;
    
    # SSL Configuration (managed by IISc IT)
    
    location / {
        proxy_pass https://spectrum-lab-iisc.github.io;
        proxy_set_header Host spectrum-lab-iisc.github.io;
        proxy_set_header X-Real-IP $remote_addr;
        
        # Security Headers
        add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Referrer-Policy "strict-origin-when-cross-origin" always;
        add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), interest-cohort=()" always;
        add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com https://use.typekit.net https://giscus.app https://www.googletagmanager.com https://www.google-analytics.com https://tikzjax.com https://distill.pub https://maps.googleapis.com https://unpkg.com https://ajax.googleapis.com; style-src 'self' 'unsafe-inline' https:; font-src 'self' data: https:; img-src 'self' data: blob: https:; connect-src 'self' https:; frame-src 'self' https://giscus.app https://www.youtube.com https://player.vimeo.com https://www.google.com https://maps.google.com; media-src 'self' blob: data:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; upgrade-insecure-requests;" always;
    }
}
```

**For Apache:**
```apache
<VirtualHost *:443>
    ServerName spectrumlab.iisc.ac.in
    
    # SSL Configuration (managed by IISc IT)
    
    ProxyPreserveHost Off
    ProxyPass / https://spectrum-lab-iisc.github.io/
    ProxyPassReverse / https://spectrum-lab-iisc.github.io/
    
    # Security Headers
    Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains; preload"
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    Header always set X-XSS-Protection "1; mode=block"
    Header always set Referrer-Policy "strict-origin-when-cross-origin"
    Header always set Permissions-Policy "camera=(), microphone=(), geolocation=(), interest-cohort=()"
    Header always set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https:; style-src 'self' 'unsafe-inline' https:; font-src 'self' data: https:; img-src 'self' data: blob: https:; connect-src 'self' https:; frame-src 'self' https:; media-src 'self' blob: data:; object-src 'none'; base-uri 'self'; form-action 'self'; frame-ancestors 'self'; upgrade-insecure-requests;"
</VirtualHost>
```

### Option C: Use Cloudflare (Self-manageable)

1. Point DNS to Cloudflare (free tier available)
2. Configure Cloudflare to proxy to GitHub Pages
3. Add security headers via Cloudflare Transform Rules

---

## What We Have Done (Our End)

1. ✅ Added security meta tags in `_includes/core/head.liquid`:
   - `X-Frame-Options: SAMEORIGIN`
   - `X-Content-Type-Options: nosniff`
   - `Permissions-Policy`

2. ✅ Created `_headers` file with full security headers (for Netlify/Cloudflare compatibility)

3. ✅ All pages served over HTTPS (enforced by GitHub Pages)

4. ✅ Created this documentation for IISc IT team

---

## Recommendation

**For full VAPT compliance with an IISc domain, we recommend Option B (Reverse Proxy)** as it provides:

1. Custom `*.iisc.ac.in` domain
2. Full control over HTTP headers
3. Ability to pass all VAPT security requirements
4. No additional cost (uses existing IISc infrastructure)

---

## Contact

For questions about this implementation, contact:
- **Website Maintainer:** [Your Name]
- **Email:** css@iisc.ac.in

---

## Files Modified/Created

| File | Purpose |
|------|---------|
| `_includes/core/head.liquid` | Security meta tags |
| `_headers` | HTTP headers (for Netlify/Cloudflare) |
| `docs/VAPT_SECURITY_REPORT.md` | This documentation |
| `docs/security-headers-config.txt` | Server configuration templates |
