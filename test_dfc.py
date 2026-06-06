import os
from pathlib import Path
import pytest
from src.compress import compress_file
from src.verify import decompress_file, verify_integrity

@pytest.fixture
def test_workspace(tmp_path):
    """Generates an isolated clean file directory for integration safety tests."""
    inputs = tmp_path / "input_files"
    compressed = tmp_path / "compressed_files"
    decompressed = tmp_path / "decompressed_files"
    outputs = tmp_path / "outputs"
    
    for folder in [inputs, compressed, decompressed, outputs]:
        folder.mkdir()
        
    return inputs, compressed, decompressed, outputs

def test_pipeline_integration_workflow(test_workspace):
    """Validates the full compression, verification, and extraction cycle."""
    inputs, compressed, decompressed, outputs = test_workspace
    
    sample_log = inputs / "production_dump.log"
    sample_log.write_text("NODE_HEALTH_METRIC_OK_TRANSACTION_ID_TRACE\n" * 2000)
    
    # Run core compression metrics tracking engine
    manifest = compress_file(str(sample_log), str(compressed), profile_mode="auto")
    assert manifest["allocated_codec"] in ["zstd", "brotli"]
    assert manifest["output_payload_bytes"] < manifest["source_payload_bytes"]
    
    # Run live audit cryptographic verifiers
    manifest_path = manifest["compressed_file_path"] + ".dfc.json"
    assert verify_integrity(manifest_path, str(outputs))
    
    # Extract structural payload contents and confirm match identity signatures
    extracted_file = decompress_file(manifest["compressed_file_path"], str(decompressed))
    assert Path(extracted_file).read_text() == sample_log.read_text()

def test_bypass_pre_compressed_assets(test_workspace):
    """Ensures pre-compressed media types skip redundant processing pipelines."""
    inputs, compressed, _, _ = test_workspace
    
    media_mock = inputs / "render_frame.png"
    # FIX (cSpell) corrected random binary initialization markers tracking
    media_mock.write_bytes(b"\x89PNG\r\n\x1a\n" + os.urandom(1024))
    
    manifest = compress_file(str(media_mock), str(compressed), profile_mode="auto")
    assert manifest["allocated_codec"] == "store"
    assert manifest["output_payload_bytes"] == media_mock.stat().st_size