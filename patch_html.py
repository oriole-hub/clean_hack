"""Patch Ren'Py web build index.html:
- Remove hamburger menu (☰)
- Set custom page title
- Inject mobile viewport, touch scaling, and WebApp meta tags
- Inject CSS for responsive 100vw/100vh canvas fitting on all mobile devices
"""
import re
import sys
import os
import glob

# Find index.html in the output directory
output_dir = sys.argv[1] if len(sys.argv) > 1 else "/output"
html_files = glob.glob(os.path.join(output_dir, "**", "index.html"), recursive=True)

if not html_files:
    print(f"WARNING: No index.html found in {output_dir}")
    sys.exit(0)

html_path = html_files[0]
print(f"Patching: {html_path}")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Remove hamburger menu elements by ID/class
patterns = [
    r'<div[^>]*id=["\']menu["\'][^>]*>.*?</div>',
    r'<div[^>]*class=["\'][^"\']*hamburger[^"\']*["\'][^>]*>.*?</div>',
    r'<button[^>]*id=["\']menu-button["\'][^>]*>.*?</button>',
    r'<a[^>]*id=["\']menu-toggle["\'][^>]*>.*?</a>',
]
for pattern in patterns:
    html = re.sub(pattern, "", html, flags=re.DOTALL)

# 2. Inject mobile web app meta tags
mobile_meta = """
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="theme-color" content="#060d19">
"""
# Replace or inject viewport meta
if '<meta name="viewport"' in html:
    html = re.sub(r'<meta name="viewport"[^>]*>', mobile_meta.strip(), html, count=1)
else:
    html = html.replace("<head>", "<head>\n" + mobile_meta)

# 3. Inject CSS for full-screen responsive mobile canvas scaling
css_block = """
<style>
  #menu, .hamburger, #menu-button, #menu-toggle,
  [id*="hamburger"], [class*="hamburger"] {
    display: none !important;
    visibility: hidden !important;
  }
  
  html, body {
    width: 100% !important;
    height: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
    background-color: #060d19 !important;
    touch-action: none !important;
    -webkit-touch-callout: none !important;
    -webkit-user-select: none !important;
    user-select: none !important;
    position: fixed !important;
    left: 0;
    top: 0;
  }

  #canvas, canvas, #presplash, .presplash {
    display: block !important;
    margin: auto !important;
    position: absolute !important;
    top: 0 !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    max-width: 100vw !important;
    max-height: 100vh !important;
    object-fit: contain !important;
  }
</style>
<script>
  // Prevent double-tap zoom on iOS/Android
  document.addEventListener('touchstart', function(e) {
    if (e.touches.length > 1) {
      e.preventDefault();
    }
  }, { passive: false });

  let lastTouchEnd = 0;
  document.addEventListener('touchend', function(e) {
    const now = (new Date()).getTime();
    if (now - lastTouchEnd <= 300) {
      e.preventDefault();
    }
    lastTouchEnd = now;
  }, false);

  // Auto-resize canvas on orientation change or screen resize
  window.addEventListener('resize', function() {
    window.scrollTo(0, 0);
  });
  window.addEventListener('orientationchange', function() {
    setTimeout(function() { window.scrollTo(0, 0); }, 200);
  });
</script>
"""
html = html.replace("</head>", css_block + "\n</head>")

# 4. Replace page title
html = re.sub(
    r"<title>.*?</title>",
    "<title>Чистый берег: ДЗЗ и Челлендж</title>",
    html,
    count=1,
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Mobile adaptation patch complete!")
