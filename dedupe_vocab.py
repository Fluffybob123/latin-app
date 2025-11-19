import json
import sys

file_path = r"c:\Users\fluff\OneDrive\Desktop\latin app\latin_vocab.json"

text = open(file_path, "r", encoding="utf-8").read()

arrs = []
i = 0
n = len(text)
while i < n:
    if text[i] == "[":
        start = i
        depth = 1
        i += 1
        while i < n and depth > 0:
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
            i += 1
        if depth == 0:
            chunk = text[start:i]
            try:
                data = json.loads(chunk)
                if isinstance(data, list):
                    arrs.extend(data)
            except Exception as e:
                print("Failed to parse chunk:", e, file=sys.stderr)
        continue
    i += 1

# Remove exact duplicates (by canonical JSON)
seen = set()
unique = []
for obj in arrs:
    try:
        key = json.dumps(obj, sort_keys=True, ensure_ascii=False)
    except Exception:
        key = str(obj)
    if key in seen:
        continue
    seen.add(key)
    unique.append(obj)

# Write back a single JSON array
with open(file_path, "w", encoding="utf-8") as f:
    json.dump(unique, f, indent=2, ensure_ascii=False)

print(f"Read {len(arrs)} entries across arrays; wrote {len(unique)} unique entries to {file_path}")
