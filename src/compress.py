import gzip, bz2, lzma, json, time, shutil, hashlib
from pathlib import Path
import zstandard as zstd
import brotli
from src.strategy import choose_strategy

def generate_sha256(path: str) -> str:
    sha = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()

def _run_zstd(src, dest, plan):
    compressor = zstd.ZstdCompressor(level=plan.level, threads=plan.threads)
    with open(src, "rb") as fi, open(dest, "wb") as fo:
        with compressor.stream_writer(fo) as sw:
            for block in iter(lambda: fi.read(plan.chunk_size), b""): sw.write(block)

def compress_file(src: str, dest_dir: str, mode: str = "auto") -> dict:
    src_path = Path(src)
    dest_path = Path(dest_dir)
    dest_path.mkdir(parents=True, exist_ok=True)
    plan = choose_strategy(src, mode)
    
    out = dest_path / (src_path.name + f".{plan.codec}")
    
    if plan.codec == "zstd": _run_zstd(src, str(out), plan)
    # Add other codecs here...
    
    manifest = {"src": src, "out": str(out), "codec": plan.codec, "sha256": generate_sha256(src)}
    with open(str(out) + ".json", "w") as f: json.dump(manifest, f)
    return manifest