import json
import re
import hashlib
import html
import urllib.request
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/private_audit_draft_218725796.json", "r", encoding="utf-8") as f:
    data = json.load(f)

content = data["content"]["raw"]

pattern = re.compile(r'<details\b[^>]*\bid="(rcf-computational-[^"]+)"[^>]*>([\s\S]*?)</details>', re.I)

panels = {}
for m in pattern.finditer(content):
    pid = m.group(1)
    block = m.group(2)
    textareas = re.findall(r"<textarea\b[^>]*>([\s\S]*?)</textarea>", block, re.I)
    if not textareas:
        continue
    prompt_text = html.unescape(textareas[0])
    h = hashlib.sha256(prompt_text.encode('utf-8')).hexdigest()
    
    # extract URLs
    urls = re.findall(r"https://[^\s<>\"']+", prompt_text)
    primary = [u for u in urls if "raw.githubusercontent.com" in u and u.endswith(".zip")]
    backup = [u for u in urls if "sweetrationalism.com/wp-content/uploads" in u and u.endswith(".zip")]
    
    panels[pid] = {
        "sha256": h,
        "length": len(prompt_text),
        "primary_url": primary[0] if primary else None,
        "backup_url": backup[0] if backup else None,
        "prompt_snippet": prompt_text[:200]
    }

print(f"Total panels parsed: {len(panels)}")
for pid, info in sorted(panels.items()):
    print(f"\n[{pid}]")
    print(f"  SHA-256: {info['sha256']}")
    print(f"  Primary: {info['primary_url']}")
    print(f"  Backup:  {info['backup_url']}")

# Test HTTP availability of the unique zip URLs
all_urls = set()
for info in panels.values():
    if info['primary_url']: all_urls.add(info['primary_url'])
    if info['backup_url']: all_urls.add(info['backup_url'])

print(f"\n=== TESTING {len(all_urls)} UNIQUE ZIP URLS ===")
for url in sorted(all_urls):
    try:
        req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
        res = urllib.request.urlopen(req, timeout=10)
        print(f"  [OK {res.status}] {url}")
    except Exception as e:
        print(f"  [FAIL {e}] {url}")
