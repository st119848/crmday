
with open(r'E:\work\crmday\html\account_history\code.html', 'rb') as f:
    content = f.read()

# Find the <h2>šัญŠีและ›ระวั•ิ</h2> part
# In the previous read, it was around line 43.
# Let's just look for 'text-center pr-10' which is unique.
index = content.find(b'text-center pr-10')
if index != -1:
    start = index - 50
    end = index + 100
    print(f"Hex at {index}:")
    print(content[start:end].hex(' '))
    print(content[start:end])
else:
    print("Not found")
