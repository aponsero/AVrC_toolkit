# src/avrc/commands/filter.py
import click
from pathlib import Path
from ..utils.metadata import load_sequence_mapping, load_metadata, apply_filters
from ..utils.seqkit import verify_seqkit, filter_sequences, count_sequences

@click.command(name="filter")
@click.argument('input_dir', type=click.Path(exists=True))
@click.option('--quality', 
              type=click.Choice(['Complete', 'High-quality', 'Medium-quality', 'Low-quality']),
              help='Filter by sequence quality')
@click.option('--min-length', type=int, help='Minimum sequence length')
@click.option('--no-plasmids', is_flag=True, help='Exclude potential plasmids')
@click.option('--realm', help='Filter by viral realm (case-insensitive)')
@click.option('--phylum', help='Filter by viral phylum (case-insensitive)')
@click.option('--class', 'viral_class', help='Filter by viral class (case-insensitive)')
@click.option('--lifestyle', 
              type=click.Choice(['temperate', 'virulent', 'uncertain']),
              help='Filter by predicted lifestyle')
@click.option('--host-domain', help='Filter by host domain (case-insensitive)')
@click.option('--host-phylum', help='Filter by host phylum (case-insensitive)')
@click.option('--host-genus', help='Filter by host genus (case-insensitive)')
@click.option('--output', 
              type=click.Choice(['fasta', 'metadata', 'both']),
              required=True,
              help='Output format')
@click.option('--output-dir', 
              default='.',
              help='Output directory',
              type=click.Path())
def filter_cmd(input_dir, quality, min_length, no_plasmids, realm, phylum,
               viral_class, lifestyle, host_domain, host_phylum, host_genus,
               output, output_dir):
    """Filter AVrC sequences based on metadata criteria."""
    # Check seqkit if needed
    if output in ['fasta', 'both']:
        seqkit_ok, msg = verify_seqkit()
        if not seqkit_ok:
            raise click.UsageError(msg)

    try:
        # Load sequence mapping
        click.echo("Loading sequence mapping...")
        representative_ids, votu_to_rep = load_sequence_mapping(input_dir)

        # Load metadata
        click.echo("Loading metadata...")
        metadata = load_metadata(input_dir, representative_ids)

        # Apply filters
        click.echo("Applying filters...")
        filter_params = {
            'quality': quality,
            'min_length': min_length,
            'no_plasmids': no_plasmids,
            'realm': realm,
            'phylum': phylum,
            'class': viral_class,
            'lifestyle': lifestyle,
            'host_domain': host_domain,
            'host_phylum': host_phylum,
            'host_genus': host_genus
        }
        filtered_ids = apply_filters(metadata, **filter_params)
        click.echo(f"Found {len(filtered_ids)} sequences matching criteria")

        # Create output directory
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True)

        # Write outputs
        if output in ['metadata', 'both']:
            click.echo("Writing filtered metadata...")
            for name, df in metadata.items():
                filtered_df = df[df['contig_id'].isin(filtered_ids)]
                output_file = output_dir / f'filtered_{name}.csv'
                filtered_df.to_csv(output_file, index=False)
                click.echo(f"Wrote {len(filtered_df)} records to {output_file}")

        if output in ['fasta', 'both']:
            click.echo("Writing filtered sequences...")
            sequence_file = Path(input_dir) / 'AVrC_allrepresentatives.fasta.gz'
            output_file = output_dir / 'filtered_sequences.fasta.gz'
            id_list_file = output_dir / 'filtered_ids.txt'

            # Write filtered IDs to a text file
            with open(id_list_file, 'w') as f:
                for seq_id in filtered_ids:
                    f.write(f"{seq_id}\n")

            try:
                # Filter sequences
                filter_sequences(sequence_file, output_file, id_list_file)
                
                # Clean up ID list file
                id_list_file.unlink()
                
                # Count and report filtered sequences
                count = count_sequences(output_file)
                click.echo(f"Wrote {count} sequences to {output_file}")

            except Exception as e:
                if id_list_file.exists():
                    id_list_file.unlink()
                raise

    except Exception as e:
        raise click.ClickException(str(e))