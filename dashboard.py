import streamlit as st
import os
import json
from pathlib import Path
from src.compress import compress_file
from src.verify import decompress_file, verify_integrity
from src.detector import sample_stats, guess_mime

st.set_page_config(page_title="DFC Engine Utility Dashboard", layout="wide")

st.title("⚡ Dynamic File Compression Utility Control Center")
st.subheader("Enterprise Adaptive Data Packaging Pipeline Analytics Dashboard")

# Initialize base testing folders if missing from system environment maps
for f in ["input_files", "compressed_files", "decompressed_files", "outputs"]:
    Path(f).mkdir(exist_ok=True)

tab1, tab2 = st.tabs(["🗜️ Core Compression Matrix Engine", "🔍 Archive Verification & Audit Trails"])

with tab1:
    st.header("Execute Adaptive Optimization Engine passes")
    uploaded_file = st.file_uploader("Drop target asset directly into storage lines", type=None)
    
    if uploaded_file is not None:
        save_path = Path("input_files") / uploaded_file.name
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.success(f"Asset safely saved on disk: `{save_path}`")
        
        # Display live file data metrics
        metrics = sample_stats(str(save_path))
        mime = guess_mime(str(save_path))
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Calculated Shannon Data Entropy", f"{metrics['entropy']} / 8.0")
        col2.metric("Calculated Text Stream Content Balance", f"{int(metrics['text_ratio'] * 100)}%")
        col3.metric("Resolved Content MIME String", mime)
        
        execution_profile = st.selectbox("Assign operational priority layouts", ["auto", "fast", "max"])
        
        if st.button("Launch System Engine Compression Processing"):
            with st.spinner("Processing stream blocks..."):
                manifest = compress_file(str(save_path), "compressed_files", execution_profile)
                
            st.balloons()
            st.success("Compression process completed successfully.")
            st.json(manifest)

with tab2:
    st.header("Ledger Signatures Audits & Reversing Utilities")
    manifest_targets = list(Path("compressed_files").glob("*.dfc.json"))
    
    if manifest_targets:
        target_manifest = st.selectbox("Select historical processing log to analyze", [f.name for f in manifest_targets])
        manifest_full_path = Path("compressed_files") / target_manifest
        
        with open(manifest_full_path, "r") as f:
            manifest_data = json.load(f)
            
        st.write("### Extracted Active Ledger Parameters Details")
        st.dataframe([manifest_data])
        
        col1, col2 = st.columns(2)
        
        if col1.button("Verify Payload Transaction Authenticity Checksums"):
            if verify_integrity(str(manifest_full_path), "outputs"):
                st.success("INTEGRITY CONFIRMED: SHA-256 matches the manifest profile.")
            else:
                st.error("INTEGRITY CRITICAL FAILURE: Checksum mismatch discovered.")
                
        if col2.button("Run Inverse Extraction Pipeline Passes"):
            extracted_output = decompress_file(manifest_data["compressed_file_path"], "decompressed_files")
            st.info(f"File extracted to disk storage array target location:\n`{extracted_output}`")
    else:
        st.warning("No active processing logs found on disk.")