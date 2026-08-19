# scratch: confirm the cache TTL logic ages out correctly
import time
from pathlib import Path

cache_file = Path("cache/forecast.json")
if cache_file.exists():
    age = time.time() - cache_file.stat().st_mtime
    print(f"cache age: {age:.0f}s ({'fresh' if age < 3600 else 'stale'})")
else:
    print("no cache file yet")
