"""Patch Ren'Py web build index.html:
- Remove hamburger menu (☰)
- Set custom page title
- Inject CSS to ensure menu stays hidden
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

# 2. Inject CSS to force-hide any remaining hamburger elements
css_block = """
<style>
  #menu, .hamburger, #menu-button, #menu-toggle,
  [id*="hamburger"], [class*="hamburger"] {
    display: none !important;
    visibility: hidden !important;
  }
  body { background-color: #0F172A; }
</style>
"""
html = html.replace("</head>", css_block + "\n</head>")

# 3. Replace page title
html = re.sub(
    r"<title>.*?</title>",
    "<title>Чистый берег: ДЗЗ и Челлендж</title>",
    html,
    count=1,
)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Patching complete!")
