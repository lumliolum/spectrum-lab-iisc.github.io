# Cross-Domain Configuration Guide

This document explains the cross-domain configuration setup for the Spectrum Lab website, allowing safe cross-origin requests while maintaining security.

## Files Added/Modified

### 1. `_includes/cross-domain-config.liquid`
Contains the HTML meta tags for CORS headers and security policies. Uses the data from `_data/cross_domain.yml` for configuration.

### 2. `_data/cross_domain.yml`
Central configuration file for all cross-domain settings. Modify this file to adjust CORS policies, security headers, and trusted domains.

### 3. `_headers`
GitHub Pages compatible headers file that sets HTTP headers at the server level for better cross-domain support.

### 4. Enhanced CSP in `_includes/metadata.liquid`
Updated Content Security Policy to include additional trusted CDN domains while maintaining security.

## Configuration Options

### CORS Settings (`_data/cross_domain.yml`)

```yaml
cors:
  enabled: true
  allow_origin: "*"  # or specific domain like "https://example.com"
  allow_methods: "GET, POST, OPTIONS, HEAD"
  allow_headers: "Origin, X-Requested-With, Content-Type, Accept, Authorization, Cache-Control"
  allow_credentials: false
  max_age: 86400
```

### Security Headers

```yaml
security:
  x_frame_options: "SAMEORIGIN"  # Legacy anti-clickjacking header
  frame_ancestors: "'self'"  # Modern CSP anti-clickjacking directive
  x_content_type_options: "nosniff"
  referrer_policy: "strict-origin-when-cross-origin"
  x_xss_protection: "1; mode=block"
```

## Usage Examples

### For API Calls
If you're making AJAX requests from external sites:
```javascript
fetch('https://spectrum-lab-iisc.github.io/data/some-data.json')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));
```

### For Embedding Resources
External sites can now safely include your CSS, JS, fonts, and images:
```html
<link rel="stylesheet" href="https://spectrum-lab-iisc.github.io/assets/css/main.css">
<script src="https://spectrum-lab-iisc.github.io/assets/js/theme.js"></script>
```

### For iFrames (with restrictions)
Your pages can be embedded in iframes from the same origin:
```html
<iframe src="https://spectrum-lab-iisc.github.io/publications/"></iframe>
```

## Security Considerations

### What's Protected
- **X-Frame-Options**: Legacy anti-clickjacking header that prevents embedding in malicious iframes
- **Content-Security-Policy: frame-ancestors**: Modern anti-clickjacking protection with better browser support
- **X-Content-Type-Options**: Prevents MIME sniffing attacks
- **X-XSS-Protection**: Enables XSS filtering in browsers
- **Referrer-Policy**: Controls referrer information sent with requests

### Anti-Clickjacking Protection
The configuration includes both legacy and modern anti-clickjacking headers:
- `X-Frame-Options: SAMEORIGIN` - Allows framing only from the same origin
- `Content-Security-Policy: frame-ancestors 'self'` - Modern equivalent with better control

To allow specific domains to embed your content:
```yaml
security:
  x_frame_options: "ALLOW-FROM https://trusted-domain.com"
  frame_ancestors: "'self' https://trusted-domain.com"
```

### What's Allowed
- Cross-origin requests for static assets (CSS, JS, images, fonts)
- AJAX requests from any domain (configurable)
- Resource embedding for development and integration

### Customizing for Specific Domains

To restrict CORS to specific domains, modify `_data/cross_domain.yml`:

```yaml
cors:
  enabled: true
  allow_origin: "https://yourdomain.com"  # Only allow this domain
  # ... other settings
```

For multiple specific domains, you'd need to implement server-side logic or use a more advanced configuration.

## Testing Cross-Domain Setup

### 1. Test CORS Headers
```bash
curl -H "Origin: https://example.com" \
     -H "Access-Control-Request-Method: GET" \
     -I https://spectrum-lab-iisc.github.io/
```

### 2. Test Resource Loading
```javascript
// Test from browser console on a different domain
fetch('https://spectrum-lab-iisc.github.io/assets/css/main.css', {
  mode: 'cors'
}).then(response => {
  console.log('CORS working:', response.ok);
});
```

### 3. Check Security Headers
Use online tools like:
- [SecurityHeaders.com](https://securityheaders.com/)
- [Mozilla Observatory](https://observatory.mozilla.org/)

## Deployment Notes

### GitHub Pages
The `_headers` file will be processed by GitHub Pages and deployed with your site. The configuration will take effect after your next deployment.

### Local Development
When running locally with Jekyll:
```bash
JEKYLL_ENV=development bundle exec jekyll serve --livereload --port 8080
```

The cross-domain headers will be included in the HTML but may not be enforced the same way as in production.

## Troubleshooting

### Common Issues

1. **CORS errors persist**: Check that `_data/cross_domain.yml` has `cors.enabled: true`
2. **Resources blocked**: Verify the domain is in `external_cdns` or `trusted_domains`
3. **iFrame embedding fails**: Check `x_frame_options` setting in security config
4. **Headers not applied**: Ensure files are properly included and site is redeployed

### Browser Tools
- Use browser developer tools Network tab to inspect request/response headers
- Check Console for CORS-related error messages
- Use Application tab to verify CSP policies

## Maintenance

### Regular Updates
- Review `trusted_domains` list periodically
- Update CDN domains when adding new external resources
- Monitor security headers for compliance with current best practices

### Security Audits
- Test with security scanning tools
- Review access logs for suspicious cross-origin requests
- Keep CSP and CORS policies as restrictive as possible while maintaining functionality

## Need More Restrictive Settings?

If you need tighter security, consider:
1. Setting specific domains instead of `*` for `allow_origin`
2. Reducing allowed HTTP methods
3. Adding domain validation logic
4. Implementing rate limiting for cross-origin requests

For questions or issues, refer to the main project documentation or create an issue in the repository.