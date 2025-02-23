# src/avrc/utils/seqkit.py
import subprocess
import shutil
import sys
import os
from pathlib import Path

def verify_seqkit():
    """
    Verify seqkit installation and provide detailed feedback.
    
    Returns:
        tuple: (bool, str) - (True if seqkit is working, status message)
    """
    # Check if seqkit is in PATH
    seqkit_path = shutil.which('seqkit')
    if not seqkit_path:
        msg = [
            "seqkit not found in PATH.",
            "Please install seqkit using one of these methods:",
            "",
            "1. Using conda:",
            "   conda install -c bioconda seqkit",
            "",
            "Current environment:",
            f"- Conda env: {os.environ.get('CONDA_DEFAULT_ENV') or 'Not in conda environment'}",
            f"- Python: {sys.executable}"
        ]
        return False, "\n".join(msg)
    
    # Try running seqkit
    try:
        subprocess.run(
            ['seqkit', 'version'],
            capture_output=True,
            text=True,
            check=True
        )
        return True, f"seqkit found at {seqkit_path}"
    except subprocess.SubprocessError as e:
        msg = [
            f"seqkit found at {seqkit_path} but failed to run.",
            f"Error: {str(e)}",
            "",
            "Try reinstalling seqkit:",
            "conda install -c bioconda seqkit --force-reinstall"
        ]
        return False, "\n".join(msg)

def count_sequences(file_path):
    """
    Count sequences in a FASTA/FASTQ file using seqkit.
    
    Args:
        file_path (str or Path): Path to sequence file
        
    Returns:
        int: Number of sequences in the file
        
    Raises:
        RuntimeError: If seqkit command fails
    """
    try:
        result = subprocess.run(
            ['seqkit', 'stats', '-T', str(file_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split('\t')
            return int(parts[3])  # num_seqs column is 4th (0-based)
        raise ValueError("Unexpected output format from seqkit stats")
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Error running seqkit: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error counting sequences: {str(e)}")

def filter_sequences(input_file, output_file, id_list_file):
    """
    Filter sequences using seqkit based on ID list.
    
    Args:
        input_file (str or Path): Path to input sequence file
        output_file (str or Path): Path to output filtered sequence file
        id_list_file (str or Path): Path to file containing sequence IDs to keep
        
    Raises:
        RuntimeError: If seqkit command fails
    """
    try:
        subprocess.run([
            'seqkit', 'grep',
            '-f', str(id_list_file),
            str(input_file),
            '-o', str(output_file)
        ], check=True)
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Error filtering sequences with seqkit: {str(e)}")