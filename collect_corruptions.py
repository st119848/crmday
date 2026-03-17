
import os
import re

def collect_corruptions():
    corruptions = {}
    html_dir = r'E:\work\crmday\html'
    for root, dirs, files in os.walk(html_dir):
        for file in files:
            if file == 'code.html':
                path = os.path.join(root, file)
                with open(path, 'rb') as f:
                    content = f.read()
                
                # Find \xef\xbf\xbd and the following character (if any)
                i = 0
                while True:
                    i = content.find(b'\xef\xbf\xbd', i)
                    if i == -1: break
                    
                    # Get the sequence following \xef\xbf\xbd
                    # Usually it's a UTF-8 character
                    seq = b''
                    j = i + 3
                    if j < len(content):
                        # Read one UTF-8 character
                        first = content[j]
                        if first < 0x80:
                            seq = content[j:j+1]
                        elif 0xC0 <= first < 0xE0:
                            seq = content[j:j+2]
                        elif 0xE0 <= first < 0xF0:
                            seq = content[j:j+3]
                        elif 0xF0 <= first < 0xF8:
                            seq = content[j:j+4]
                        
                    context = content[max(0, i-20):min(len(content), i+20)]
                    key = seq
                    if key not in corruptions:
                        corruptions[key] = []
                    corruptions[key].append(context)
                    i += 3 + len(seq)
    
    for seq, contexts in corruptions.items():
        print(f"Sequence: {seq.hex(' ')} ({seq})")
        for ctx in contexts[:3]:
            print(f"  Context: {ctx}")
        print("-" * 20)

if __name__ == "__main__":
    collect_corruptions()
