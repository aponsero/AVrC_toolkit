# AVrC Toolkit

[![Python package](https://github.com/aponsero/AVrC_toolkit/actions/workflows/python-package.yml/badge.svg)](https://github.com/aponsero/AVrC_toolkit/actions/workflows/python-package.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.11426065.svg)](https://doi.org/10.5281/zenodo.11426065)
# AVrC Toolkit

A Python package for downloading and filtering sequences from the Aggregated Gut Viral Catalogue (AVrC).

## Overview

The AVrC Toolkit provides command-line utilities to:
* Download complete or subset data from the AVrC database
* Filter sequences based on quality metrics, taxonomy, and host information
* Extract specific viral groups for analysis

## Data Source

The AVrC dataset is available through Zenodo: https://doi.org/10.5281/zenodo.11426065

## Quick Links

- [**Complete Documentation**](https://github.com/aponsero/AVrC_toolkit/wiki) - Comprehensive wiki with tutorials and reference guides
- [**Installation Guide**](https://github.com/aponsero/AVrC_toolkit/wiki/Installation-Guide) - Detailed setup instructions
- [**Command Reference**](https://github.com/aponsero/AVrC_toolkit/wiki/Command-Reference) - Complete command documentation
- [**Tutorials**](https://github.com/aponsero/AVrC_toolkit/wiki/Tutorials-and-Examples) - Step-by-step guides and examples

## Quick Start

```bash
# Install the toolkit
pip install git+https://github.com/aponsero/AVrC_toolkit.git

# List available datasets
avrc download --list

# Download high-quality subset
avrc download hq -o data/

# Filter for specific viral groups
avrc filter data/ --host-phylum Firmicutes --output both
```

## Citation

If you use this toolkit or the AVrC dataset in your research, please cite:

```
Galperina, A., Lugli, G. A., Milani, C., De Vos, W. M., Ventura, M., Salonen, A., Hurwitz, B., & Ponsero, A. J. (2024). The Aggregated Gut Viral Catalogue (AVrC): A Unified Resource for Exploring the Viral Diversity of the Human Gut. bioRxiv. https://doi.org/10.1101/2024.06.24.600367
```

## Issues and Support

If you encounter any issues with the AVrC or the AVrC toolkit:
1. Check the [Issues](https://github.com/aponsero/AVrC_toolkit/issues) page
2. Search for similar problems
3. Open a new issue with:
   - Your system information
   - Command used
   - Complete error message
   - Example data if possible
