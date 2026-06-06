import tarfile
from pathlib import Path
import zstandard as zstd

def compress_directory_tree(source_directory_path: str, output_storage_directory: str, compression_level: int = 6) -> str:
    """Packages directory tree models inside a single high-performance zstd tar stream block."""
    source_path = Path(source_directory_path)
    destination_workspace = Path(output_storage_directory)
    destination_workspace.mkdir(parents=True, exist_ok=True)
    
    archive_output_path = destination_workspace / f"{source_path.name}.tar.zst"
    compressor = zstd.ZstdCompressor(level=compression_level)
    
    with open(archive_output_path, "wb") as fo, compressor.stream_writer(fo) as stream_worker:
        with tarfile.open(mode="w|", fileobj=stream_worker) as tar_package:
            # FIX (cSpell) added configuration properties tracking across workspace layouts
            tar_package.add(source_path, arcname=source_path.name)
            
    return str(archive_output_path)