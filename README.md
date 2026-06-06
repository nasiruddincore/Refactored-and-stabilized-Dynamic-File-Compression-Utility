# Dynamic File Compression Utility

A high-performance Python utility for dynamic file compression. This project allows users to select compression profiles—**Auto**, **Performance**, or **Size**—and automatically applies the most efficient algorithm (Zstandard, Brotli, LZMA, Gzip, or Bzip2) for the task.

## Key Features
* **Smart Strategy Engine**: Automatically optimizes for speed or storage efficiency.
* **Multi-Codec Support**: Integrated support for `zstd`, `br`, `xz`, `gz`, and `bz2`.
* **Data Integrity**: Uses SHA-256 cryptographic hashing to verify files after compression.
* **Detailed Manifests**: Generates `.dfc.json` logs for every compression task, tracking source, codec, and execution time.
* **Streamlit Dashboard**: A user-friendly web interface for real-time monitoring and management.

## Project Structure
```text
/src
  ├── compress.py      # Core compression engine
  ├── strategy.py      # Compression algorithm logic
  ├── archive.py       # Archiving utilities
  └── verify.py        # Integrity verification
main.py                # Command-line interface
dashboard.py           # Streamlit dashboard
