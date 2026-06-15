#!/usr/bin/env python3
"""
Fix version A cards: single-line unlockBtn + single-line script.
Handles both with and without arrow emoji in button text.
"""

import os
import re
import sys

CARDS_DIR = '/Users/mac/foodintelai-site/catalog/其他'

def fix_a(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Step 1: Remove the unlockBtn button and optional following note
    content = re.sub(
        r'(<div class="price-tag">.*?</div>)\s*\n?\s*<button class="btn" id="unlockBtn">[^<]*</button>(?:\s*\n?\s*<div class="note"[^>]*>[^<]*</div>)?\s*\n?',
        r'\1\n  ',
        content
    )
    
    # Step 2: Remove single-line script
    content = re.sub(
        r'<script>document\.getElementById\(\'unlockBtn\'\)[^<]+</script>\s*\n?',
        '',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    from subprocess import run, PIPE
    result = run(['grep', '-rl', 'unlockBtn', CARDS_DIR, '--include=*.html'], capture_output=True, text=True)
    cards = [c for c in result.stdout.strip().split('\n') if c]
    
    fixed = 0
    remaining = 0
    
    for c in cards:
        with open(c, 'r') as f:
            content = f.read()
        
        if '展开完整出摊包' not in content:
            continue  # skip single-button cards
        
        # Check if it's version A (single-line script)
        if '<script>document.getElementById' not in content:
            continue  # skip non-A versions
            
        name = os.path.basename(c)
        
        changed = fix_a(c)
        if changed:
            # Verify
            with open(c, 'r') as f:
                content = f.read()
            has_btn = 'id="unlockBtn"' in content
            has_script = "getElementById('unlockBtn')" in content
            btn_count = content.count('<button')
            
            if not has_btn and not has_script:
                print(f"✅ {name} — {btn_count}个button")
                fixed += 1
            else:
                issues = []
                if has_btn: issues.append('按钮残留')
                if has_script: issues.append('脚本残留')
                print(f"⚠️ {name} — {', '.join(issues)}")
                remaining += 1
        else:
            print(f"— {name} 无变化")
    
    print(f"\n版本A完成: {fixed}张OK, {remaining}张残留")

if __name__ == '__main__':
    main()
