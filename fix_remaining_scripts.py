#!/usr/bin/env python3
"""
Fix remaining duplicate button issues - handles ALL script variants.
Pattern: remove <script>...getElementById('unlockBtn')...{any content}...</script> or </div>
"""

import os
import re

CARDS_DIR = '/Users/mac/foodintelai-site/catalog/其他'

def fix_script(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Handle all 3 variants of unlockBtn script blocks.
    # Variant A: <script>...getElementById('unlockBtn')...  multi-line ...</script>
    # Variant B: single-line minified
    # Variant C: malformed (no </script>, ends with </div> or other tag)
    
    # Strategy: find the unlockBtn script and remove from <script> to next tag
    content = re.sub(
        r'<script>[\s\S]*?document\.getElementById\(\'unlockBtn\'\)[\s\S]*?(?:</script>|</div>|</body>|</html>)',
        '',
        content
    )
    
    # Also try: remove any remaining unlockBtn references
    content = re.sub(
        r'<script>[\s\S]*?getElementById\(\'unlockBtn\'\)[\s\S]*?</script>\s*\n?',
        '',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def verify(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    if 'getElementById(\'unlockBtn\')' in content:
        issues.append('脚本残留')
    if 'id="unlockBtn"' in content:
        issues.append('按钮残留')
    
    btn_count = content.count('<button')
    
    if issues:
        return False, ', '.join(issues)
    return True, f'{btn_count}个button'

def main():
    import subprocess
    result = subprocess.run([
        'grep', '-rl', 'unlockBtn', CARDS_DIR, '--include=*.html'
    ], capture_output=True, text=True)
    
    cards = [c for c in result.stdout.strip().split('\n') if c]
    print(f"找到{len(cards)}张含unlockBtn的卡\n")
    
    fixed = 0
    remaining = 0
    
    for c in cards:
        name = os.path.basename(c)
        
        # First remove the button if present
        with open(c, 'r', encoding='utf-8') as f:
            content = f.read()
        
        has_btn = 'id="unlockBtn"' in content
        has_script = "getElementById('unlockBtn')" in content
        
        if not has_script:
            print(f"  — {name} 无脚本残留")
            continue
        
        changed = fix_script(c)
        if changed:
            ok, msg = verify(c)
            if ok:
                print(f"  ✅ {name} — {msg}")
                fixed += 1
            else:
                print(f"  ⚠️ {name} — 改了但{msg}")
                remaining += 1
        else:
            print(f"  ❌ {name} — 改不了")
            remaining += 1
    
    print(f"\n完成: {fixed}张修复, {remaining}张残留")

if __name__ == '__main__':
    main()
