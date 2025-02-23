# AVrC Toolkit

A Python package for downloading and filtering sequences from the Aggregated Gut Viral Catalogue (AVrC). This toolkit provides command-line utilities to:
- Download complete or subset data from AVrC
- Filter sequences based on quality metrics
- Select sequences based on taxonomy and host information
- Extract specific viral groups

## Installation

### Requirements
- Python ≥ 3.8
- seqkit

### Quick Installation
```bash
# Create and activate conda environment (recommended)
conda create -n avrc python=3.9
conda activate avrc

# Install seqkit
conda install -c bioconda seqkit

# Install AVrC toolkit
pip install git+https://github.com/aponsero/AVrC_toolkit.git
```

## Usage

### Downloading Data

List available subsets:
```bash
avrc download --list
```

Download complete dataset:
```bash
avrc download all -o data/
```

Available subsets:
- `all`: Complete dataset with all representative sequences
- `hq`: High-quality sequences subset
- `phage`: Bacteriophage sequences subset

### Filtering Sequences

After downloading the complete dataset ("all"), it is possible to filter sequences based on various criteria:

```bash
# Basic quality filtering
avrc filter data/ \
  --quality High-quality \
  --no-plasmids \
  --output fasta

# Host-specific filtering
avrc filter data/ \
  --host-domain Bacteria \
  --host-phylum Firmicutes \
  --output both \
  --output-dir filtered/
```

#### Filtering Options
- Quality: `--quality [Complete|High-quality|Medium-quality|Low-quality]`
- Length: `--min-length INT`
- Plasmids: `--no-plasmids`
- Taxonomy:
  - `--realm TEXT`
  - `--phylum TEXT`
  - `--class TEXT`
- Lifestyle: `--lifestyle [temperate|virulent|uncertain]`
- Host:
  - `--host-domain TEXT`
  - `--host-phylum TEXT`
  - `--host-genus TEXT`

#### Output Options
- `--output [fasta|metadata|both]`: Output format
- `--output-dir PATH`: Output directory

## Output Files

When using `--output both`, the following files are generated:
- `filtered_sequences.fasta.gz`: Filtered sequences
- `filtered_quality.csv`: Quality metrics
- `filtered_viral_desc.csv`: Taxonomic information
- `filtered_hosts.csv`: Host predictions

## Resource Requirements

- Disk Space:
  - Complete dataset: ~10GB
  - High-quality subset: ~5GB
  - Phage subset: ~3GB
- Memory: 4-8GB recommended for filtering

## Citation

If you use this toolkit in your research, please cite:
```bibtex
[Citation will be added upon publication]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Support

If you encounter any issues:
1. Check the [Issues](https://github.com/aponsero/AVrC_toolkit/issues) page
2. Search for similar problems
3. Open a new issue with:
   - Your system information
   - Command used
   - Complete error message
   - Example data if possible