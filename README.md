# streaming_mkv_duration_checker

Check Still-Writing-MKV Video Duration using RFC8794

```py
from check_mkv_duration import get_mkv_duration
dur = get_mkv_duration("recording_2025-10-06_10-03-41.mkv")
print(f"Duration so far: {dur:.3f} s" if dur else "No clusters found.")
```
