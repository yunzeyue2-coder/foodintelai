#!/usr/bin/env python3
"""
Fix duplicate buttons in V5.1 pay-area cards.
Pattern to fix: has BOTH unlockBtn AND 展开完整出摊包 button.
Remove unlockBtn + its note + the separate inline script block.
"""

import os
import re
import sys

CARDS_DIR = '/Users/mac/foodintelai-site/catalog'

def fix_card(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern 1: Remove unlockBtn button + its following note
    # Variant A: <button class="btn" id="unlockBtn">...\n  <div class="note">...
    content = re.sub(
        r'  <button class="btn" id="unlockBtn">[^<]+</button>\n  <div class="note">[^<]+</div>\n',
        '',
        content
    )
    
    # Variant B: <button class="btn" id="unlockBtn">... followed by <div class="note"> on next line
    content = re.sub(
        r'  <button class="btn" id="unlockBtn">[^<]+</button>\n',
        '',
        content
    )
    
    # Pattern 2: Remove the separate script block that references unlockBtn
    # Match <script> ... getElementById('unlockBtn') ... </script>
    content = re.sub(
        r'<script>\s*\n\s*document\.getElementById\(\'unlockBtn\'\)[^<]+</script>\s*\n?',
        '',
        content,
        flags=re.DOTALL
    )
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def verify_card(filepath):
    """Verify the fix was applied correctly"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    if 'id="unlockBtn"' in content:
        issues.append('仍有unlockBtn')
    if "getElementById('unlockBtn')" in content:
        issues.append('仍有unlockBtn脚本')
    
    # Count buttons in pay-area
    pay_btn = [m.start() for m in re.finditer(r'<button', content)]
    
    if issues:
        return False, ', '.join(issues)
    return True, f'ok ({len(pay_btn)}个button)'

def main():
    dry = '--dry-run' in sys.argv
    
    # Find all cards with the duplicate issue
    from subprocess import run, PIPE
    result = run([
        'grep', '-rl', 'unlockBtn', CARDS_DIR, '--include=*.html'
    ], capture_output=True, text=True)
    
    cards_with_unlock = result.stdout.strip().split('\n')
    
    # Filter to cards that also have the second button
    duplicate_cards = []
    for c in cards_with_unlock:
        if not c:
            continue
        with open(c, 'r', encoding='utf-8') as f:
            content = f.read()
        if '展开完整出摊包' in content:
            duplicate_cards.append(c)
    
    print(f"找到{len(duplicate_cards)}张重复按钮卡\n")
    
    fixed_count = 0
    error_count = 0
    
    for i, c in enumerate(duplicate_cards):
        name = os.path.basename(c)
        
        if dry:
            print(f"  [{i+1}] {name} → 待修复")
            fixed_count += 1
            continue
        
        try:
            changed = fix_card(c)
            if changed:
                ok, msg = verify_card(c)
                if ok:
                    print(f"  [{i+1}] ✅ {name} — {msg}")
                    fixed_count += 1
                else:
                    print(f"  [{i+1}] ⚠️ {name} — 改了但{msg}")
                    error_count += 1
            else:
                print(f"  [{i+1}] — {name} 无变化")
        except Exception as e:
            print(f"  [{i+1}] ❌ {name} — {e}")
            error_count += 1
    
    print(f"\n完成: {fixed_count}张修复, {error_count}张错误")
    if dry:
        print("(干跑 — 未实际修改)")

if __name__ == '__main__':
    main()
