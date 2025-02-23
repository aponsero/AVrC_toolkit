# Changelog

All notable changes to the AVrC toolkit will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-02-23

### Added
- Initial release of AVrC toolkit
- Download functionality for AVrC datasets
  - Complete dataset download
  - High-quality subset download
  - Phage subset download
  - Automatic checksum verification
  - Resume capability for interrupted downloads
- Sequence filtering capabilities
  - Quality-based filtering
  - Length-based filtering
  - Plasmid exclusion
  - Taxonomy-based filtering
  - Host-based filtering
  - Lifestyle-based filtering
- Output formats
  - FASTA sequence output
  - CSV metadata output
  - Combined output option
- Basic command-line interface
  - download command with list option
  - filter command with multiple criteria
- Automatic handling of compressed files
- Progress bars for downloads
- Error handling and user feedback

### Dependencies
- Python ≥3.8
- click
- pandas
- requests
- tqdm
- urllib3
- seqkit (external requirement)