# tests/commands/test_filter.py
"""Test filter command."""

import pytest
from click.testing import CliRunner
from avrc.commands.filter import filter_cmd

def test_filter_command_basic(test_data_dir, mock_seqkit):
    """Test basic filter command execution."""
    runner = CliRunner()
    result = runner.invoke(filter_cmd, [
        str(test_data_dir),
        '--quality', 'High-quality',
        '--output', 'both'
    ])
    
    assert result.exit_code == 0
    assert "Found 1 sequences matching criteria" in result.output

def test_filter_command_multiple_filters(test_data_dir, mock_seqkit):
    """Test filter command with multiple criteria."""
    runner = CliRunner()
    result = runner.invoke(filter_cmd, [
        str(test_data_dir),
        '--quality', 'Complete',
        '--no-plasmids',
        '--host-domain', 'Bacteria',
        '--output', 'metadata'
    ])
    
    assert result.exit_code == 0
    assert "Found 1 sequences matching criteria" in result.output

def test_filter_command_invalid_input(test_data_dir):
    """Test filter command with invalid input directory."""
    runner = CliRunner()
    result = runner.invoke(filter_cmd, [
        'nonexistent_dir',
        '--output', 'metadata'
    ])
    
    assert result.exit_code != 0
    assert "Error" in result.output
