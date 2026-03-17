import os
import sys
import re

def fix_mojibake(content):
    # Universal fix: map characters back to bytes and re-decode as UTF-8
    # This works because:
    # 1. Mojibake chars (0-255) map back to their original bytes.
    # 2. Correct Unicode chars (>255) encode as UTF-8 bytes.
    # When we decode the resulting byte stream as UTF-8, both become correct.
    try:
        b = bytearray()
        for c in content:
            if ord(c) <= 255:
                b.append(ord(c))
            else:
                # Character already > 255, encode as UTF-8 bytes to preserve it
                b.extend(c.encode('utf-8'))
        # Re-decode as UTF-8, replacing invalid sequences
        return b.decode('utf-8', errors='replace')
    except Exception as e:
        print(f"  Warning during fixing: {e}")
        return content

def update_meta_charset(content):
    # Remove existing meta charset if it's duplicate or wrong
    content = re.sub(r'<meta charset=["\'][^"\']+["\']\s*/?>', '', content, flags=re.I)
    # Insert new one
    if not re.search(r'<meta charset=["\']utf-8["\']', content, re.I):
        content = re.sub(r'(<head[^>]*>)', r'\1\n<meta charset="utf-8"/>', content, count=1, flags=re.I)
    return content

def process_file(file_path):
    print(f"Processing {file_path}...")
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
        
        # Remove BOM if present
        if raw.startswith(b'\xef\xbb\xbf'):
            raw = raw[3:]
            print("  Removed BOM")

        # Try to decode as UTF-8
        try:
            content = raw.decode('utf-8')
        except UnicodeDecodeError:
            try:
                content = raw.decode('tis-620')
                print(f"  Decoded from TIS-620")
            except UnicodeDecodeError:
                print(f"  Failed to decode")
                return

        fixed = fix_mojibake(content)
        fixed = update_meta_charset(fixed)
        
        # Also ensure Thai characters are not escaped or anything
        # (The above fix should handle it)

        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write(fixed)
            
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    files = sys.argv[1:]
    if not files:
        for root, dirs, filenames in os.walk('.'):
            for f in filenames:
                if f.endswith('.html'):
                    files.append(os.path.join(root, f))
    
    for f in files:
        process_file(f)
