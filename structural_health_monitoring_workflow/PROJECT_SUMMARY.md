# Structural Health Monitoring Workflow - Complete Package

## Project Overview

This repository contains a complete, production-ready structural health monitoring workflow that has been generalized and cleaned from the original private implementation. It provides an end-to-end solution for processing acceleration data through operational modal analysis with advanced outlier detection.

## What's Included

### 📁 Project Structure
```
structural_health_monitoring_workflow/
├── README.md                          # Comprehensive documentation
├── requirements.txt                   # Dependencies
├── config/
│   └── config.yaml                   # Main configuration file
├── src/
│   ├── processing/
│   │   ├── step1_data_filtering_qc.py    # Data quality control
│   │   ├── step2_data_processing_oma.py  # OMA analysis  
│   │   └── step3_modal_analysis.py       # Modal analysis & outliers
│   └── utils/
│       ├── data_processing_utilities.py  # Core utilities
│       └── oma_utilities.py             # OMA algorithms
├── examples/
│   ├── generate_sample_data.py          # Synthetic data generator
│   ├── bridge_config.yaml              # Bridge monitoring example
│   └── building_config.yaml            # Building monitoring example
└── docs/
    ├── QUICKSTART.md                   # 5-minute setup guide
    └── DATA_FORMAT.md                  # Data specification
```

### 🔧 Core Features

#### Step 1: Data Filtering & Quality Control
- **Intelligent data cleaning** with configurable amplitude bounds
- **Edge artifact removal** for sensor attachment/detachment
- **Systematic shift detection** and replacement with interpolation
- **Window-based quality validation** with customizable thresholds
- **Comprehensive statistics** and metadata tracking

#### Step 2: Operational Modal Analysis (OMA)
- **Multiple algorithms**: SSI-COV and FSDD support
- **Automatic mode clustering** using DBSCAN
- **Flexible sensor geometry** configuration
- **Signal filtering** (highpass/bandpass) with customizable parameters
- **Modal parameter extraction**: frequencies, damping, mode shapes

#### Step 3: Advanced Modal Analysis
- **Three outlier detection methods**:
  - Standard deviation based (z-score)
  - Curve fitting with confidence intervals  
  - MAC-frequency combined analysis with Mahalanobis distance
- **Best MAC filtering** for closely-spaced modes
- **Comprehensive visualizations** and statistical reports
- **Mode shape comparison** against reference shapes

### 🎯 Key Improvements from Original

#### Generalization
- ✅ **Removed all private/specific references** (paths, project names, etc.)
- ✅ **Configurable through YAML files** - no hardcoded parameters
- ✅ **Flexible sensor layouts** - easily adaptable to different structures
- ✅ **Generic naming conventions** - works with any sensor naming scheme

#### Usability
- ✅ **Comprehensive documentation** with examples and troubleshooting
- ✅ **Command-line interfaces** with helpful argument parsing
- ✅ **Sample data generator** for testing and demonstration
- ✅ **Multiple configuration examples** (bridge, building)
- ✅ **Quick start guide** for immediate testing

#### Robustness  
- ✅ **Error handling and validation** throughout the workflow
- ✅ **Detailed logging and progress reporting**
- ✅ **Graceful failure handling** with informative messages
- ✅ **Data format validation** with clear error messages

#### Extensibility
- ✅ **Modular design** - each step can run independently
- ✅ **Plugin architecture** for adding new outlier detection methods
- ✅ **Configurable processing parameters** - no code changes needed
- ✅ **Standard data formats** for easy integration

## Quick Usage Example

```bash
# 1. Generate sample data
python examples/generate_sample_data.py --config config/config.yaml --n-segments 5

# 2. Run complete workflow
python src/processing/step1_data_filtering_qc.py --config config/config.yaml
python src/processing/step2_data_processing_oma.py --config config/config.yaml --case-name demo
python src/processing/step3_modal_analysis.py --config config/config.yaml --mode 6 --best-mac-only
```

## Customization for Your Project

### 1. Update Configuration
Edit `config/config.yaml` to match your:
- Sensor names and layout
- Quality control thresholds  
- Expected mode characteristics
- File paths and naming conventions

### 2. Prepare Your Data
Format your acceleration data as pickle files with the structure:
```python
{
    'accelerations': pandas.DataFrame,  # Time-indexed sensor data
    'metadata': {'tag_columns': [...]}  # Additional metadata
}
```

### 3. Run Analysis
Execute the three-step workflow with your configuration.

## Dependencies

### Core Requirements
- numpy, pandas, scipy, matplotlib, scikit-learn, PyYAML
- **pyoma2**: For operational modal analysis

### Optional
- seaborn, plotly: Enhanced plotting
- joblib: Parallel processing

## Documentation

- **[README.md](README.md)**: Complete documentation with examples
- **[QUICKSTART.md](docs/QUICKSTART.md)**: 5-minute setup guide  
- **[DATA_FORMAT.md](docs/DATA_FORMAT.md)**: Detailed data specifications
- **Configuration examples**: Bridge and building monitoring setups
- **Inline documentation**: Comprehensive docstrings throughout code

## Research Applications

This workflow is suitable for:
- **Bridge monitoring**: Long-span bridges, cable-stayed bridges
- **Building monitoring**: High-rise buildings, historic structures
- **Industrial structures**: Towers, offshore platforms, wind turbines
- **Research studies**: Modal parameter tracking, damage detection
- **Educational purposes**: Teaching OMA and structural dynamics

## Original Workflow Mapping

The cleaned workflow maintains full compatibility with the original analysis approach:

| Original File | New File | Key Changes |
|---------------|----------|-------------|
| `01_filtering_data_with_qc.py` | `step1_data_filtering_qc.py` | Configurable paths, generalized QC bounds |
| `utilities_dataprocess.py` | `data_processing_utilities.py` | Modularized, removed hardcoded settings |
| `03_mode_analysis.py` | `step3_modal_analysis.py` | Flexible mode configs, enhanced outlier detection |
| N/A | `oma_utilities.py` | Extracted OMA functionality into separate module |

## Publication Ready

This workflow is ready for:
- ✅ **Open source release** (all private references removed)
- ✅ **Research publication** (comprehensive methodology documentation)
- ✅ **Educational use** (examples and tutorials included)
- ✅ **Commercial application** (robust error handling and validation)

## Support and Contribution

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Documentation**: Comprehensive guides and examples provided
- **Extensibility**: Modular design allows easy customization and extension
- **Community**: Welcomes contributions for additional algorithms and features

## License

MIT License - Free for academic, commercial, and personal use.

---

**Ready to use immediately** - The workflow can be deployed and used on new datasets without any code modifications, only configuration file adjustments.
