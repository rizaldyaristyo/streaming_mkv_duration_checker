from pathlib import Path

def _find_element(data: bytes, element_id: bytes, maxlen=8):
    pos = data.find(element_id)
    if pos == -1:
        return None
    size_byte = data[pos + len(element_id)]
    size_len = 1
    size = size_byte & 0x7F
    return int.from_bytes(
        data[pos + len(element_id) + size_len : pos + len(element_id) + size_len + size],
        "big",
        signed=False,
    )

def _get_timecode_scale(path: Path, head_size=64 * 1024) -> int:
    with open(path, "rb") as f:
        data = f.read(head_size)
    val = _find_element(data, b"\x2A\xD7\xB1")
    return val if val else 1_000_000

def _get_last_cluster_timecode(path: Path, tail_size=1024 * 1024) -> int | None:
    CLUSTER_ID = b"\x1F\x43\xB6\x75"
    TIMECODE_ID = b"\xE7"

    with open(path, "rb") as f:
        f.seek(0, 2)
        filesize = f.tell()
        read_size = min(tail_size, filesize)
        f.seek(filesize - read_size)
        data = f.read()

    pos = data.rfind(CLUSTER_ID)
    if pos == -1:
        return None

    search_window = data[pos : pos + 512]
    j = search_window.find(TIMECODE_ID)
    if j == -1 or j + 3 >= len(search_window):
        return None

    size = search_window[j + 1] & 0x7F
    return int.from_bytes(search_window[j + 2 : j + 2 + size], "big")


def get_mkv_duration(path: str | Path) -> float | None:
    path = Path(path)
    scale = _get_timecode_scale(path)
    timecode = _get_last_cluster_timecode(path)
    if timecode is None:
        return None
    return timecode * scale / 1e9

if __name__ == "__main__":
    import time
    mkv = "recording_2025-10-09_16-45-19.mkv"
    start_time = time.time()
    for _ in range(40):
        dur = get_mkv_duration(mkv)
        print(f"Duration so far: {dur:.3f} s" if dur else "No clusters found.")
    print(f"Total time: {time.time() - start_time:.3f} s")