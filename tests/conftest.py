# tests/conftest.py
"""Shared pytest fixtures."""

import pytest
import pandas as pd
from pathlib import Path
import gzip
import shutil
import os

@pytest.fixture
def test_data_dir(tmp_path):
    """Create a temporary directory with test data."""
    data_dir = tmp_path / "test_data"
    data_dir.mkdir()
    
    # Create sequence mapping file
    mapping_data = pd.DataFrame({
        'contig_id': ['seq1', 'seq2', 'seq3', 'seq4'],
        'vOTU_ID': ['vOTU1', 'vOTU2', 'vOTU3', 'vOTU4'],
        'representative': ['seq1', 'seq2', 'seq3', 'seq4']
    })
    mapping_data.to_csv(data_dir / 'AvRCv1.SequenceTable.csv', index=False)
    
    # Create quality metadata
    quality_data = pd.DataFrame({
        'contig_id': ['seq1', 'seq2', 'seq3', 'seq4'],
        'vOTU_ID': ['vOTU1', 'vOTU2', 'vOTU3', 'vOTU4'],
        'checkv_quality': ['High-quality', 'Medium-quality', 'Low-quality', 'Complete'],
        'contig_length': [1000, 2000, 3000, 4000],
        'Plasmid': [False, False, True, False]
    })
    quality_data.to_csv(data_dir / 'AvRCv1.Merged_Quality.csv', index=False)
    
    # Create viral description metadata
    viral_desc_data = pd.DataFrame({
        'contig_id': ['seq1', 'seq2', 'seq3', 'seq4'],
        'vOTU_ID': ['vOTU1', 'vOTU2', 'vOTU3', 'vOTU4'],
        'pred_lifestyle': ['temperate', 'virulent', 'uncertain', 'temperate'],
        'Realm': ['Duplodnaviria', 'Duplodnaviria', None, 'Duplodnaviria'],
        'Phylum': ['Uroviricota', 'Uroviricota', None, 'Uroviricota'],
        'Class': ['Caudoviricetes', 'Caudoviricetes', None, 'Caudoviricetes']
    })
    viral_desc_data.to_csv(data_dir / 'AvRCv1.Merged_ViralDesc.csv', index=False)
    
    # Create host metadata
    host_data = pd.DataFrame({
        'contig_id': ['seq1', 'seq2', 'seq3', 'seq4'],
        'vOTU_ID': ['vOTU1', 'vOTU2', 'vOTU3', 'vOTU4'],
        'Host_Domain': ['Bacteria', 'Bacteria', None, 'Bacteria'],
        'Host_Phylum': ['Firmicutes', 'Bacteroidetes', None, 'Proteobacteria'],
        'Host_Genus': ['Bacillus', 'Bacteroides', None, 'Escherichia']
    })
    host_data.to_csv(data_dir / 'AvRCv1.Merged_PredictedHosts.csv', index=False)
    
    # Create test FASTA file
    fasta_content = (
        ">seq1\nATGC\n"
        ">seq2\nGTAC\n"
        ">seq3\nCGTA\n"
        ">seq4\nTACG\n"
    )
    with gzip.open(data_dir / 'AVrC_allrepresentatives.fasta.gz', 'wt') as f:
        f.write(fasta_content)
    
    return data_dir

@pytest.fixture
def mock_seqkit(mocker):
    """Mock seqkit command execution."""
    def mock_run(*args, **kwargs):
        class MockResult:
            stdout = "file\tformat\ttype\tnum_seqs\tsum_len\tmin_len\tmax_len\tavg_len\n" \
                    "test.fa\tFASTA\tDNA\t4\t16\t4\t4\t4"
            returncode = 0
        return MockResult()
    
    mocker.patch('subprocess.run', side_effect=mock_run)
    return mock_run
