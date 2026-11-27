"""F-0107 check: run wishes.reddit() alone, no files written."""
import sys
sys.path.insert(0, "/Users/triton/PROTEUS/bin")
import wishes

items = wishes.reddit(7)
print(len(items), "reddit items")
for it in list(items.values())[:5]:
    print(it["when"], it["url"], it["text"][:80])
