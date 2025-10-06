# streaming_mkv_duration_checker

Check Still-Writing-MKV Video Duration using RFC8794

```py
from check_mkv_duration import read_mkv_duration
print(f"Approximate duration: {read_mkv_duration("recording_2025-10-06_10-03-41.mkv"):.2f} seconds")
```
