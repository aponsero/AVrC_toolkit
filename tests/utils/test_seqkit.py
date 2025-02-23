# tests/utils/test_seqkit.py
import subprocess
import pytest
from pathlib import Path
from avrc.utils.seqkit import verify_seqkit, count_sequences, filter_sequences

def test_verify_seqkit_success(mocker):
    """Test successful seqkit verification."""
    mock_which = mocker.patch('shutil.which')
    mock_which.return_value = '/usr/local/bin/seqkit'
    
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.returncode = 0
    
    is_valid, msg = verify_seqkit()
    assert is_valid is True
    assert '/usr/local/bin/seqkit' in msg

def test_verify_seqkit_not_found(mocker):
    """Test seqkit not found case."""
    mock_which = mocker.patch('shutil.which')
    mock_which.return_value = None
    
    is_valid, msg = verify_seqkit()
    assert is_valid is False
    assert 'not found in PATH' in msg

def test_count_sequences(mocker, tmp_path):
    """Test sequence counting."""
    # Create mock seqkit stats output
    mock_output = (
        "file\tformat\ttype\tnum_seqs\tsum_len\tmin_len\tmax_len\tavg_len\n"
        "test.fa\tFASTA\tDNA\t4\t16\t4\t4\t4"
    )
    
    # Mock subprocess.run
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.stdout = mock_output
    mock_run.return_value.returncode = 0
    
    # Test counting sequences
    fasta_file = tmp_path / "test.fasta.gz"
    count = count_sequences(fasta_file)
    
    assert count == 4
    mock_run.assert_called_once_with(
        ['seqkit', 'stats', '-T', str(fasta_file)],
        capture_output=True,
        text=True,
        check=True
    )

def test_filter_sequences(mocker, tmp_path):
    """Test sequence filtering."""
    # Setup test files
    input_file = tmp_path / "input.fasta.gz"
    output_file = tmp_path / "output.fasta.gz"
    id_list_file = tmp_path / "ids.txt"
    
    # Create test ID list
    with open(id_list_file, 'w') as f:
        f.write("seq1\nseq2\n")
    
    # Mock subprocess.run
    mock_run = mocker.patch('subprocess.run')
    mock_run.return_value.returncode = 0
    
    # Run filter
    filter_sequences(input_file, output_file, id_list_file)
    
    # Verify subprocess.run was called with correct arguments
    mock_run.assert_called_once_with([
        'seqkit', 'grep',
        '-f', str(id_list_file),
        str(input_file),
        '-o', str(output_file)
    ], check=True)

def test_count_sequences_error(mocker):
    """Test error handling in count_sequences."""
    # Mock subprocess.run to raise an error
    mock_run = mocker.patch('subprocess.run')
    mock_run.side_effect = subprocess.SubprocessError("Mock error")
    
    # Test error handling
    with pytest.raises(RuntimeError, match="Error running seqkit"):
        count_sequences("test.fasta")

def test_filter_sequences_error(mocker):
    """Test error handling in filter_sequences."""
    # Mock subprocess.run to raise an error
    mock_run = mocker.patch('subprocess.run')
    mock_run.side_effect = subprocess.SubprocessError("Mock error")
    
    # Test error handling
    with pytest.raises(RuntimeError, match="Error filtering sequences"):
        filter_sequences("input.fasta", "output.fasta", "ids.txt")