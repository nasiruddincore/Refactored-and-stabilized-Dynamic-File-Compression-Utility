import random
from pathlib import Path
import zstandard as zstd

def train_custom_dictionary(glob_pattern: str, output_dictionary_name: str, target_dict_bytes: int = 112 * 1024) -> str:
    """Builds highly focused data prefix maps across repeating data fields like system log dumps."""
    search_path = Path(".")
    resolved_files = list(search_path.glob(glob_pattern))
    
    if not resolved_files:
        raise FileNotFoundError(f"No match profiles uncovered for target glob expression: {glob_pattern}")
        
    training_samples = []
    for file_path in resolved_files:
        try:
            file_bytes = file_path.read_bytes()
            if len(file_bytes) < 256:
                continue
            for _ in range(min(40, len(file_bytes) // 1024)):
                start_offset = random.randrange(0, len(file_bytes) - 256)
                training_samples.append(file_bytes[start_offset : start_offset + 1024])
        except IOError:
            continue

    if not training_samples:
        raise ValueError("Structural file contents are too small to build a dictionary model.")

    compiled_dictionary = zstd.train_dictionary(target_dict_bytes, training_samples)
    output_path = Path(output_dictionary_name).with_suffix(".dict")
    output_path.write_bytes(compiled_dictionary.as_bytes())
    
    return str(output_path)