"""Metadata handling utilities for AVrC data."""

import pandas as pd
from pathlib import Path

def load_sequence_mapping(input_dir):
    """
    Load sequence mapping table and get representative sequences.
    
    Args:
        input_dir (str): Path to input directory containing metadata files
        
    Returns:
        tuple: (set of representative IDs, dict mapping vOTU_ID to representative ID)
    """
    try:
        seq_table = pd.read_csv(Path(input_dir) / 'AvRCv1.SequenceTable.csv')
        votu_to_rep = seq_table[seq_table['contig_id'] == seq_table['representative']][['vOTU_ID', 'contig_id']]
        return set(votu_to_rep['contig_id']), dict(zip(votu_to_rep['vOTU_ID'], votu_to_rep['contig_id']))
    except Exception as e:
        raise RuntimeError(f"Error loading sequence mapping: {str(e)}")

def load_metadata(input_dir, representative_ids):
    """
    Load metadata only for representative sequences.
    
    Args:
        input_dir (str): Path to input directory containing metadata files
        representative_ids (set): Set of representative sequence IDs to filter for
        
    Returns:
        dict: Dictionary containing filtered metadata DataFrames
    """
    metadata = {}
    try:
        # Load and pre-filter quality data
        metadata['quality'] = pd.read_csv(
            Path(input_dir) / 'AvRCv1.Merged_Quality.csv', 
            usecols=['contig_id', 'vOTU_ID', 'checkv_quality', 'contig_length', 'Plasmid']
        )
        metadata['quality'] = metadata['quality'][
            metadata['quality']['contig_id'].isin(representative_ids)
        ]
        
        # Load and pre-filter viral description data
        metadata['viral_desc'] = pd.read_csv(
            Path(input_dir) / 'AvRCv1.Merged_ViralDesc.csv', 
            usecols=['contig_id', 'vOTU_ID', 'pred_lifestyle', 'Realm', 'Phylum', 'Class']
        )
        metadata['viral_desc'] = metadata['viral_desc'][
            metadata['viral_desc']['contig_id'].isin(representative_ids)
        ]
        
        # Load and pre-filter host prediction data
        metadata['hosts'] = pd.read_csv(
            Path(input_dir) / 'AvRCv1.Merged_PredictedHosts.csv', 
            usecols=['contig_id', 'vOTU_ID', 'Host_Domain', 'Host_Phylum', 'Host_Genus']
        )
        metadata['hosts'] = metadata['hosts'][
            metadata['hosts']['contig_id'].isin(representative_ids)
        ]
        
        return metadata
    except Exception as e:
        raise RuntimeError(f"Error loading metadata: {str(e)}")

def apply_filters(metadata, **filter_params):
    """
    Apply filters to metadata and return filtered sequence IDs.
    
    Args:
        metadata (dict): Dictionary containing metadata DataFrames
        **filter_params: Filter parameters as keyword arguments
        
    Returns:
        set: Set of sequence IDs passing all filters
    """
    filtered_ids = set(metadata['quality']['contig_id'])
    
    # Quality filters
    quality = metadata['quality']
    if filter_params.get('quality'):
        filtered_ids &= set(quality[quality['checkv_quality'] == filter_params['quality']]['contig_id'])
    
    if filter_params.get('min_length'):
        filtered_ids &= set(quality[quality['contig_length'] >= filter_params['min_length']]['contig_id'])
    
    if filter_params.get('no_plasmids'):
        filtered_ids &= set(quality[~quality['Plasmid']]['contig_id'])
    
    # Taxonomy/lifestyle filters
    viral_desc = metadata['viral_desc']
    if filter_params.get('realm'):
        realm_mask = viral_desc['Realm'].fillna('').str.contains(filter_params['realm'], case=False)
        filtered_ids &= set(viral_desc[realm_mask]['contig_id'])
    
    if filter_params.get('phylum'):
        phylum_mask = viral_desc['Phylum'].fillna('').str.contains(filter_params['phylum'], case=False)
        filtered_ids &= set(viral_desc[phylum_mask]['contig_id'])
    
    if filter_params.get('class'):
        class_mask = viral_desc['Class'].fillna('').str.contains(filter_params['class'], case=False)
        filtered_ids &= set(viral_desc[class_mask]['contig_id'])
    
    if filter_params.get('lifestyle'):
        lifestyle_mask = viral_desc['pred_lifestyle'] == filter_params['lifestyle']
        filtered_ids &= set(viral_desc[lifestyle_mask]['contig_id'])
    
    # Host filters
    hosts = metadata['hosts']
    if filter_params.get('host_domain'):
        domain_mask = hosts['Host_Domain'].fillna('').str.contains(filter_params['host_domain'], case=False)
        filtered_ids &= set(hosts[domain_mask]['contig_id'])
    
    if filter_params.get('host_phylum'):
        phylum_mask = hosts['Host_Phylum'].fillna('').str.contains(filter_params['host_phylum'], case=False)
        filtered_ids &= set(hosts[phylum_mask]['contig_id'])
    
    if filter_params.get('host_genus'):
        genus_mask = hosts['Host_Genus'].fillna('').str.contains(filter_params['host_genus'], case=False)
        filtered_ids &= set(hosts[genus_mask]['contig_id'])
    
    return filtered_ids
