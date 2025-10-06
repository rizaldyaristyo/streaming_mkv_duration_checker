def read_mkv_duration(path, tail_size=1024*1024):
    with open(path, 'rb') as f:
        f.seek(0, 2)
        filesize = f.tell()
        read_size = min(tail_size, filesize)
        f.seek(filesize - read_size)
        data = f.read()
    CLUSTER_ID = b'\x1F\x43\xB6\x75'
    TIMECODE_ID = b'\xE7'
    last_timecode = None
    i = 0
    while i < len(data):
        if data[i:i+4] == CLUSTER_ID:
            sub = data[i:i+256]
            j = sub.find(TIMECODE_ID)
            if j != -1 and j + 3 < len(sub):
                size = sub[j+1] & 0x7F
                val = int.from_bytes(sub[j+2:j+2+size], 'big')
                last_timecode = val
            i += 4
        else:
            i += 1
    if last_timecode is None:
        return None
    duration_s = last_timecode / 1000.0
    return duration_s

print(f"Approximate duration: {read_mkv_duration("recording_2025-10-06_10-03-41.mkv"):.2f} seconds")
