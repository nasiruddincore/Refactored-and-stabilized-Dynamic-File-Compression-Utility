from dataclasses import dataclass
from src.detector import magic_type, sample_stats, guess_mime

@dataclass(frozen=True)
class Plan:
    codec: str
    level: int
    chunk_size: int
    threads: int
    store_only: bool = False

def choose_strategy(path: str, profile_mode: str = "auto") -> Plan:
    """Resolves operational metric traces into an explicit hardware execution target blueprint."""
    detected_signature = magic_type(path)
    
    # FIX (sonar:python:S8513) - Unified execution validation using tuple containment
    if detected_signature in {"gzip", "bz2", "xz", "zstd", "png", "jpeg", "zip"}:
        return Plan(codec="store", level=0, chunk_size=0, threads=0, store_only=True)

    mime_string = guess_mime(path)
    metrics = sample_stats(path)

    if profile_mode == "fast":
        return Plan(codec="zstd", level=3, chunk_size=1024 * 1024, threads=2)
    if profile_mode == "max":
        return Plan(codec="lzma", level=7, chunk_size=1024 * 1024, threads=1)

    is_textual_payload = metrics["text_ratio"] > 0.75 and metrics["entropy"] < 7.6
    
    # FIX (sonar:python:S8513) - Grouped chained startswith queries into elegant tuple layouts
    if mime_string.startswith(("text/", "application/json", "text/csv")) or is_textual_payload:
        if metrics["entropy"] < 5.0:
            return Plan(codec="brotli", level=5, chunk_size=2 * 1024 * 1024, threads=0)
        return Plan(codec="zstd", level=7, chunk_size=4 * 1024 * 1024, threads=4)

    if mime_string.startswith(("image/", "video/")):
        return Plan(codec="store", level=0, chunk_size=0, threads=0, store_only=True)

    return Plan(codec="zstd", level=5, chunk_size=2 * 1024 * 1024, threads=2)