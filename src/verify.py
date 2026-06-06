import gzip
import bz2
import lzma
import json
import shutil
from pathlib import Path
import zstandard as zstd
import brotli
from src.compress import generate_sha256

def decompress_file(src: str, target_extraction_directory: str) -> str:
    """Safely extracts native payloads from custom compressed binaries."""
    src_path = Path(src)
    dest_dir = Path(target_extraction_directory)
    dest_dir.mkdir(parents=True, exist_ok=True)

    suffix = src_path.suffix
    base_name = src_path.stem if suffix in {".zst", ".br", ".gz", ".bz2", ".xz", ".store"} else src_path.name + ".extracted"
    output_path = dest_dir / base_name

    if suffix == ".store":
        shutil.copy2(src, output_path)
        return str(output_path)

    if suffix == ".zst":
        decompressor = zstd.ZstdDecompressor()
        with open(src, "rb") as fi, open(output_path, "wb") as fo:
            decompressor.copy_stream(fi, fo)

    elif suffix == ".br":
        with open(src, "rb") as fi, open(output_path, "wb") as fo:
            fo.write(brotli.decompress(fi.read()))

    elif suffix == ".gz":
        with gzip.open(src, "rb") as fi, open(output_path, "wb") as fo:
            shutil.copyfileobj(fi, fo)

    elif suffix == ".bz2":
        with bz2.open(src, "rb") as fi, open(output_path, "wb") as fo:
            shutil.copyfileobj(fi, fo)

    elif suffix == ".xz":
        with lzma.open(src, "rb") as fi, open(output_path, "wb") as fo:
            shutil.copyfileobj(fi, fo)
            
    else:
        raise ValueError(f"Encountered unknown binary source file extension: {suffix}")

    return str(output_path)

def verify_integrity(manifest_path: str, extraction_test_directory: str) -> bool:
    """Cross-validates live extraction footprints against historical cryptographic signatures."""
    try:
        with open(manifest_path, "r") as f:
            manifest = json.load(f)
        
        compressed_target = manifest["compressed_file_path"]
        expected_checksum = manifest["source_cryptographic_sha256"]
        
        temporary_extraction = decompress_file(compressed_target, extraction_test_directory)
        generated_checksum = generate_sha256(temporary_extraction)
        
        Path(temporary_extraction).unlink(missing_ok=True)
        return expected_checksum == generated_checksum
    except Exception:
        return False