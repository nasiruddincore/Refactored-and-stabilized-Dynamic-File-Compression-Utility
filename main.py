import os
from dotenv import load_dotenv
from src.compress import compress_file

# Initialize environment variables
load_dotenv()

def main():
    """Main execution point with input safety checks."""
    print("--- Dynamic File Compression Utility ---")
    
    source = input("Enter the file path to compress: ").strip()
    
    # Validation: Check if the file actually exists
    if not source or not os.path.exists(source):
        print(f"Error: The file '{source}' was not found. Please check the path.")
        return

    dest = input("Enter the destination directory: ").strip()
    # If no destination provided, default to current folder
    if not dest:
        dest = "./compressed_output"
        print(f"No destination provided. Using default: {dest}")

    mode = input("Enter mode (auto/performance/size): ").strip().lower() or "auto"

    try:
        result = compress_file(source, dest, mode)
        print(f"\nSuccess! File compressed using: {result['codec']}")
        print(f"Manifest saved to: {result['output']}.dfc.json")
    except Exception as e:
        print(f"Critical error during compression: {e}")

if __name__ == "__main__":
    main()