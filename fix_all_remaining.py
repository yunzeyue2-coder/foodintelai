#!/usr/bin/env python3
"""
Fix all remaining cards with unlockBtn issues.
1. Remove unlockBtn button + optional note
2. Remove unlockBtn script block (even malformed - missing </script>)
"""

import os
import re

CARDS_DIR = '/Users/mac/foodintelai-site/catalog/其他'

def fix_card(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Step 1: Remove unlockBtn button + optional note div after price-tag
    # Matches both same-line and next-line variants
    content = re.sub(
        r'(<div class="price-tag">.*?</div>)\s*\n?\s*<button[^>]*id="unlockBtn"[^>]*>[^<]*</button>(?:\s*\n?\s*<div class="note"[^>]*>[^<]*</div>)?\s*\n?',
        r'\1\n  ',
        content
    )
    
    # Step 2: Remove unlockBtn script block (handles malformed too)
    # Matches from <script> through getElementById('unlockBtn') up to next tag boundary
    content = re.sub(
        r'<script>[\s\S]*?getElementById\(\'unlockBtn\'\)[\s\S]*?(?:</script>|(?=</div>))',
        '',
        content
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    import subprocess
    result = subprocess.run([
        'grep', '-rl', 'unlockBtn', CARDS_DIR, '--include=*.html'
    ], capture_output=True, text=True)
    
    all_cards = [c for c in result.stdout.strip().split('\n') if c]
    
    fixed = 0
    remaining = 0
    
    for c in all_cards:
        with open(c, 'r') as f:
            content = f.read()
        
        # Only process cards that still have unlockBtn AND the 展开 button
        if '展开完整出摊包' not in content:
            continue  # single-button cards, skip
        
        name = os.path.basename(c)
        
        changed = fix_card(c)
        
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
    
    print(f"\n完成: {fixed}张OK, {remaining}张残留")

if __name__ == '__main__':
    main()
