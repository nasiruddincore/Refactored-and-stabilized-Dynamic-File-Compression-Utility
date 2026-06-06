import math
from collections import Counter
import mimetypes

# Core production file signatures mapped directly to codec platforms
MAGIC_MAPPING = {
    b"\x1f\x8b": "gzip",
    b"\x42\x5a\x68": "bz2",
    b"\xfd\x37\x7a\x58\x5a\x00": "xz",
    b"\x28\xb5\x2f\xfd": "zstd",
    b"\x89PNG\r\n\x1a\n": "png",
    b"\xff\xd8\xff": "jpeg",
    b"PK\x03\x04": "zip"
}

def magic_type(path: str) -> str | None:
    """Reads leading file header bytes to discover data types."""
    try:
        with open(path, "rb") as f:
            header = f.read(16)
        for signature, codec in MAGIC_MAPPING.items():
            if header.startswith(signature):
                return codec
    except IOError:
        return None
    return None

def sample_stats(path: str, block_sample_bytes: int = 256 * 1024) -> dict:
    """Computes empirical Shannon Entropy and text ratio balances over an isolated data chunk."""
    try:
        with open(path, "rb") as f:
            buffer = f.read(block_sample_bytes)
    except IOError:
        return {"entropy": 0.0, "text_ratio": 0.0, "newlines": 0}

    total_len = len(buffer)
    if total_len == 0:
        return {"entropy": 0.0, "text_ratio": 0.0, "newlines": 0}

    # Shannon Entropy formula calculation block
    frequencies = Counter(buffer)
    entropy = -sum((count / total_len) * math.log2(count / total_len) for count in frequencies.values())

    # Calculate text balance metric arrays
    text_byte_count = sum(1 for b in buffer if 32 <= b <= 126 or b in (9, 10, 13))
    text_ratio = text_byte_count / total_len
    newlines = buffer.count(b"\n")

    return {
        "entropy": round(entropy, 4),
        "text_ratio": round(text_ratio, 4),
        "newlines": newlines
    }

def guess_mime(path: str) -> str:
    """Provides file type fallback mappings using the system extension index."""
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "application/octet-stream"