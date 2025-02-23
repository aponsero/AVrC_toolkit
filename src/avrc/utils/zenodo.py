# src/avrc/utils/zenodo.py
import os
import requests
import hashlib
import shutil
import tarfile
import urllib3
from pathlib import Path
from tqdm import tqdm

ZENODO_API_BASE = "https://zenodo.org/api/records/11426065"

ZENODO_SUBSETS = {
    "all": {
        "files": [
            {
                "filename": "AVrC_allrepresentatives.fasta.gz",
                "type": "sequence"
            },
            {
                "filename": "database_csv.tar.gz",
                "type": "metadata_archive",
                "extract": True,
                "extract_path": "database_csv"  # Added to track the extracted folder name
            }
        ],
        "description": "All representative sequences with metadata"
    },
    "hq": {
        "files": [{
            "filename": "subset1_HighQuality.tar.gz",
            "type": "archive",
            "extract": True
        }],
        "description": "High quality sequences"
    },
    "phage": {
        "files": [{
            "filename": "subset2_Bacteriophages.tar.gz",
            "type": "archive",
            "extract": True
        }],
        "description": "Bacteriophage sequences"
    }
}

def get_file_info():
    """Get file information including checksums from Zenodo API"""
    try:
        response = requests.get(f"{ZENODO_API_BASE}")
        response.raise_for_status()
        data = response.json()
        
        return {
            file['key']: {
                'checksum': file['checksum'],
                'size': file['size'],
                'download_url': file['links']['self']
            }
            for file in data['files']
        }
    except Exception as e:
        raise RuntimeError(f"Error fetching file information: {str(e)}")

def verify_checksum(file_path, expected_checksum):
    """Verify file MD5 checksum"""
    md5_hash = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            md5_hash.update(chunk)
    return f"md5:{md5_hash.hexdigest()}" == expected_checksum

def extract_archive(archive_path, output_dir, extract_path=None):
    """
    Extract tar.gz archive and move CSV files if needed.
    
    Args:
        archive_path (Path): Path to the archive file
        output_dir (Path): Directory where files should be extracted
        extract_path (str, optional): Subfolder name where files are extracted
    """
    try:
        # Extract the archive
        with tarfile.open(archive_path, 'r:gz') as tar:
            tar.extractall(path=output_dir)
        
        # If this is the database_csv archive, move files to parent directory
        if extract_path == "database_csv":
            csv_dir = output_dir / extract_path
            if csv_dir.exists():
                # Move all CSV files to the parent directory
                for csv_file in csv_dir.glob("*.csv"):
                    shutil.move(str(csv_file), str(output_dir / csv_file.name))
                # Remove the now-empty directory
                shutil.rmtree(csv_dir)
        
        return True
    except Exception as e:
        raise RuntimeError(f"Error extracting archive: {str(e)}")
    
def download_file(filename, file_info, output_path, chunk_size=1024*1024):
    """
    Download a file from Zenodo with progress bar, resume capability, and checksum verification
    """
    output_path = Path(output_path)
    temp_path = output_path.with_suffix(output_path.suffix + '.tmp')
    download_url = file_info['download_url']
    total_size = file_info['size']
    expected_checksum = file_info['checksum']
    
    # Check disk space
    try:
        total, used, free = shutil.disk_usage(output_path.parent)
        if free < total_size:
            raise RuntimeError(
                f"Not enough disk space. Required: {total_size/1e9:.1f}GB, Available: {free/1e9:.1f}GB"
            )
    except Exception as e:
        raise RuntimeError(f"Error checking disk space: {str(e)}")

    # Resume download if temp file exists
    initial_pos = 0
    if temp_path.exists():
        initial_pos = temp_path.stat().st_size
        if initial_pos >= total_size:
            if verify_checksum(temp_path, expected_checksum):
                temp_path.rename(output_path)
                return True
            else:
                temp_path.unlink()
                initial_pos = 0

    try:
        http = urllib3.PoolManager()
        headers = {'Range': f'bytes={initial_pos}-'} if initial_pos > 0 else {}
        
        response = http.request(
            'GET',
            download_url,
            preload_content=False,
            headers=headers
        )
        
        mode = 'ab' if initial_pos > 0 else 'wb'
        with open(temp_path, mode) as f, tqdm(
            desc=filename,
            initial=initial_pos,
            total=total_size,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            while True:
                data = response.read(chunk_size)
                if not data:
                    break
                size = f.write(data)
                pbar.update(size)
        
        response.release_conn()
        
        if verify_checksum(temp_path, expected_checksum):
            temp_path.rename(output_path)
            return True
        else:
            temp_path.unlink()
            raise RuntimeError(f"Checksum verification failed for {filename}")
            
    except Exception as e:
        if temp_path.exists():
            temp_path.unlink()
        raise RuntimeError(f"Error downloading {filename}: {str(e)}")
    
def download_subset(subset_name, output_dir="."):
    """
    Download a specific subset and its associated files
    
    Args:
        subset_name (str): Name of the subset to download
        output_dir (str or Path): Directory to save downloaded files
        
    Returns:
        bool: True if download was successful
    """
    if subset_name not in ZENODO_SUBSETS:
        raise ValueError(f"Unknown subset '{subset_name}'")
        
    file_info = get_file_info()
    if file_info is None:
        raise RuntimeError("Failed to get file information from Zenodo")

    subset = ZENODO_SUBSETS[subset_name]
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    for file_spec in subset["files"]:
        filename = file_spec["filename"]
        if filename not in file_info:
            raise RuntimeError(f"File information not found for {filename}")
            
        output_path = output_dir / filename
        
        # Download file
        if not download_file(filename, file_info[filename], output_path):
            raise RuntimeError(f"Failed to download {filename}")
            
        # Extract if needed
        if file_spec.get("extract", False):
            extract_path = file_spec.get("extract_path")
            if not extract_archive(output_path, output_dir, extract_path):
                raise RuntimeError(f"Failed to extract {filename}")
            # Remove archive after extraction
            try:
                output_path.unlink()
            except Exception:
                pass  # Non-critical error, can continue

    return True