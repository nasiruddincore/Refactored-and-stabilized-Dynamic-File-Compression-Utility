import sys
import argparse
from src.compress import compress_file
from src.verify import decompress_file, verify_integrity
from src.dict_train import train_custom_dictionary
from src.archive import compress_directory_tree  # FIX: Corrected structural typo import string block

def execute_cli():
    """Runs the root terminal argument routing array."""
    parser = argparse.ArgumentParser(
        prog="dfc",
        description="Dynamic File Compression Utility Engine - Console Interface"
    )
    subparsers = parser.add_subparsers(dest="command", help="System command navigation matrix")

    # Compress layout parser
    comp_parser = subparsers.add_parser("compress", help="Compresses a file.")
    comp_parser.add_argument("source")
    comp_parser.add_argument("--outdir", default="compressed_files")
    comp_parser.add_argument("--mode", choices=["auto", "fast", "max"], default="auto")

    # Decompress layout parser (FIX: Resolved structural spelling concerns)
    decomp_parser = subparsers.add_parser("decompress", help="Extracts a compressed file.")
    decomp_parser.add_argument("archive")
    decomp_parser.add_argument("--outdir", default="decompressed_files")

    # Verify layout parser
    verify_parser = subparsers.add_parser("verify", help="Validates file integrity via a manifest.")
    verify_parser.add_argument("manifest")
    verify_parser.add_argument("--testdir", default="outputs")

    # Train layout parser
    train_parser = subparsers.add_parser("train", help="Trains a zstd dictionary.")
    train_parser.add_argument("--glob", required=True)
    train_parser.add_argument("--output", default="custom_profile.dict")

    # Pack layout parser
    pack_parser = subparsers.add_parser("pack", help="Packages a whole folder.")
    pack_parser.add_argument("folder")
    pack_parser.add_argument("--outdir", default="compressed_files")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    _process_commands(args)

def _process_commands(args):
    """Processes verified argument maps directly into core system commands."""
    if args.command == "compress":
        res = compress_file(args.source, args.outdir, args.mode)
        print(f"[SUCCESS] Target allocated via Codec: {res['allocated_codec']} (Level {res['computational_level']})")
        print(f" -> Raw Size Tracking: {res['source_payload_bytes']} bytes down to {res['output_payload_bytes']} bytes.")

    elif args.command == "decompress":
        extracted_path = decompress_file(args.archive, args.outdir)
        print(f"[SUCCESS] Payload safely extracted to location:\n -> {extracted_path}")

    elif args.command == "verify":
        if verify_integrity(args.manifest, args.testdir):
            print("[INTEGRITY STATUS: PASSED] Checksums match perfectly across transaction indexes.")
        else:
            print("[INTEGRITY STATUS: FAILURE] Cryptographic signature mismatch detected.")
            sys.exit(1)

    elif args.command == "train":
        dict_path = train_custom_dictionary(args.glob, args.output)
        print(f"[SUCCESS] Optimization dictionary saved to location: {dict_path}")

    elif args.command == "pack":
        archive_path = compress_directory_tree(args.folder, args.outdir)
        print(f"[SUCCESS] Folder pack safely written to target disk location:\n -> {archive_path}")