# tests/utils/test_metadata.py
"""Test metadata handling utilities."""

import pytest
from avrc.utils.metadata import load_sequence_mapping, load_metadata, apply_filters

def test_load_sequence_mapping(test_data_dir):
    """Test loading sequence mapping."""
    rep_ids, votu_map = load_sequence_mapping(test_data_dir)
    
    assert len(rep_ids) == 4
    assert 'seq1' in rep_ids
    assert votu_map['vOTU1'] == 'seq1'

def test_load_metadata(test_data_dir):
    """Test loading metadata for representative sequences."""
    rep_ids = {'seq1', 'seq2', 'seq3', 'seq4'}
    metadata = load_metadata(test_data_dir, rep_ids)
    
    assert 'quality' in metadata
    assert 'viral_desc' in metadata
    assert 'hosts' in metadata
    assert len(metadata['quality']) == 4

def test_apply_filters(test_data_dir):
    """Test applying various filters to metadata."""
    rep_ids = {'seq1', 'seq2', 'seq3', 'seq4'}
    metadata = load_metadata(test_data_dir, rep_ids)
    
    # Test quality filter
    filtered_ids = apply_filters(metadata, quality='High-quality')
    assert len(filtered_ids) == 1
    assert 'seq1' in filtered_ids
    
    # Test length filter
    filtered_ids = apply_filters(metadata, min_length=3000)
    assert len(filtered_ids) == 2
    assert 'seq3' in filtered_ids
    assert 'seq4' in filtered_ids
    
    # Test combined filters
    filtered_ids = apply_filters(
        metadata,
        quality='Complete',
        no_plasmids=True,
        host_domain='Bacteria'
    )
    assert len(filtered_ids) == 1
    assert 'seq4' in filtered_ids
