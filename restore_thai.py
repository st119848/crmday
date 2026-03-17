
import os
import re

CP1252_TO_THAI = {
    0x80: (None, 'เ'),
    0x81: ('ก', 'แ'),
    0x82: ('ข', 'โ'),
    0x83: ('ฃ', 'ใ'),
    0x84: ('ค', 'ไ'),
    0x85: ('ฅ', 'ๅ'),
    0x86: ('ฆ', 'ๆ'),
    0x87: ('ง', '็'),
    0x88: ('จ', '่'),
    0x89: ('ฉ', '้'),
    0x8A: ('ช', '๊'),
    0x8B: ('ซ', '๋'),
    0x8C: ('ฌ', '์'),
    0x8D: ('ญ', 'ํ'),
    0x8E: ('ฎ', '๎'),
    0x90: ('ฐ', '๐'),
    0x91: ('ฑ', '๑'),
    0x92: ('ฒ', '๒'),
    0x93: ('ณ', '๓'),
    0x94: ('ด', '๔'),
    0x95: ('ต', '๕'),
    0x96: ('ถ', '๖'),
    0x97: ('ท', '๗'),
    0x98: ('ธ', '๘'),
    0x99: ('น', '๙'),
    0x9A: ('บ', None),
    0x9B: ('ป', None),
    0x9C: ('ผ', None),
    0x9D: ('ฝ', None),
    0x9E: ('พ', None),
    0x9F: ('ฟ', None),
}

BYTE_TO_UTF8 = {}
for i in range(0x80, 0x100):
    try:
        c = bytes([i]).decode('cp1252')
        BYTE_TO_UTF8[i] = c.encode('utf-8')
    except:
        # Fallback to latin-1 if cp1252 fails
        c = bytes([i]).decode('latin-1')
        BYTE_TO_UTF8[i] = c.encode('utf-8')

def fix_thai(content):
    def m(b):
        if b in BYTE_TO_UTF8:
            return b'\xef\xbf\xbd' + BYTE_TO_UTF8[b]
        return b'\xef\xbf\xbd' + bytes([b])

    # Pre-replace common strings to reduce ambiguity
    replacements = [
        (m(0x84) + 'ะ'.encode('utf-8'), 'คะ'.encode('utf-8')),
        (m(0x84) + 'า'.encode('utf-8'), 'ค่า'.encode('utf-8')),
        (m(0x84) + 'ำ'.encode('utf-8'), 'คำ'.encode('utf-8')),
        (m(0x88) + 'ั'.encode('utf-8') + m(0x94), 'จัด'.encode('utf-8')),
        (m(0x88) + 'ั'.encode('utf-8') + 'ด'.encode('utf-8'), 'จัด'.encode('utf-8')),
        (m(0x84) + 'ว'.encode('utf-8') + 'า'.encode('utf-8') + 'ม'.encode('utf-8'), 'ความ'.encode('utf-8')),
        (m(0x82) + 'า'.encode('utf-8'), 'ขา'.encode('utf-8')),
        (m(0x81) + 'จ'.encode('utf-8'), 'แจ'.encode('utf-8')),
        ('แ'.encode('utf-8') + m(0x88) + m(0x87), 'แจ้ง'.encode('utf-8')),
        ('กิ'.encode('utf-8') + m(0x88) + 'ก'.encode('utf-8'), 'กิจกรรม'.encode('utf-8')),
        ('สํ'.encode('utf-8') + m(0x82) + 'ร'.encode('utf-8') + m(0x88), 'สำเร็จ'.encode('utf-8')),
        (m(0x88) + 'า'.encode('utf-8') + m(0x97), 'จ่าย'.encode('utf-8')),
        (m(0x88) + 'า'.encode('utf-8') + 'ย'.encode('utf-8'), 'จ่าย'.encode('utf-8')),
        (m(0x88) + 'ื'.encode('utf-8') + m(0x94), 'ชื่อ'.encode('utf-8')),
    ]
    for old, new in replacements:
        content = content.replace(old, new)

    # Generic replacement
    pattern = b'\xef\xbf\xbd(?:[\x00-\x7f]|[\xc2-\xdf][\x80-\xbf]|[\xe0-\xef][\x80-\xbf]{2})'
    
    def sub_func(m_obj):
        mangled = m_obj.group(0)
        char_part = mangled[3:]
        byte_val = None
        for b, u8 in BYTE_TO_UTF8.items():
            if u8 == char_part:
                byte_val = b
                break
        if byte_val is None: return mangled
        cons, vowel = CP1252_TO_THAI.get(byte_val, (None, None))
        if not vowel: return (cons or '?').encode('utf-8')
        if not cons: return (vowel or '?').encode('utf-8')
        
        start = m_obj.start()
        end = m_obj.end()
        prev_bytes = content[max(0, start-3):start]
        next_bytes = content[end:end+3]
        
        is_next_cons = next_bytes.startswith(b'\xe0\xb8') and (0x81 <= next_bytes[2] <= 0xAE)
        is_next_mangled = next_bytes.startswith(b'\xef\xbf\xbd')
        is_prev_cons = prev_bytes.startswith(b'\xe0\xb8') and (0x81 <= prev_bytes[2] <= 0xAE)
        
        if byte_val in [0x80, 0x81, 0x82, 0x83, 0x84]:
            if is_next_cons or is_next_mangled: return vowel.encode('utf-8')
            return cons.encode('utf-8')
        if byte_val in [0x87, 0x88, 0x89, 0x8A, 0x8B, 0x8C]:
            if is_prev_cons: return vowel.encode('utf-8')
            return cons.encode('utf-8')
        return cons.encode('utf-8')

    result = re.sub(pattern, sub_func, content)
    return result

def process_file(file_path):
    print(f"Processing {file_path}")
    with open(file_path, 'rb') as f:
        content = f.read()
    fixed_content = fix_thai(content)
    try:
        text = fixed_content.decode('utf-8')
    except UnicodeDecodeError:
        text = fixed_content.decode('utf-8', errors='replace')
    new_font_link = '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" rel="stylesheet" />'
    text = re.sub(r'<link href="https://fonts\.googleapis\.com/css2\?family=Material\+Symbols\+Outlined[^"]*" rel="stylesheet"\s*/?>', new_font_link, text)
    if not re.search(r'<meta charset="utf-8"', text, re.I):
        text = re.sub(r'(<head[^>]*>)', r'\1\n<meta charset="utf-8"/>', text, count=1, flags=re.I)
    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)

if __name__ == "__main__":
    html_dir = r'E:\work\crmday\html'
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file == 'code.html':
                process_file(os.path.join(root, file))
