# Structural Health Monitoring Workflow

A comprehensive, open-source workflow for automated structural health monitoring analysis using operational modal analysis (OMA) and advanced outlier detection methods.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Workflow Steps](#workflow-steps)
- [Configuration](#configuration)
- [Data Format](#data-format)
- [Usage Examples](#usage-examples)
- [Advanced Features](#advanced-features)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

This workflow provides an end-to-end solution for structural health monitoring analysis, from raw acceleration data processing to modal parameter identification and outlier detection. It's designed to be:

- **Configurable**: All parameters controlled through YAML configuration files
- **Modular**: Each step can be run independently or as part of a complete workflow
- **Extensible**: Easy to adapt for different sensor configurations and structures
- **Reproducible**: Comprehensive logging and metadata tracking

## Features

### Data Processing
- **Quality Control**: Automated data cleaning with configurable amplitude bounds
- **Edge Detection**: Intelligent removal of sensor attachment/detachment artifacts
- **Signal Processing**: Highpass and bandpass filtering with configurable parameters
- **Data Validation**: Window-based quality assessment and continuity checking

### Operational Modal Analysis (OMA)
- **Multiple Algorithms**: Support for SSI-COV and FSDD algorithms
- **Automated Clustering**: DBSCAN-based automatic mode clustering
- **Flexible Geometry**: Configurable sensor layouts and background geometry
- **Modal Parameter Extraction**: Frequency, damping, and mode shape identification

### Advanced Outlier Detection
- **Method 1**: Standard deviation-based detection with configurable thresholds
- **Method 2**: Curve fitting with confidence intervals using polynomial regression
- **Method 3**: MAC-frequency combined analysis with Mahalanobis distance
- **Combined Analysis**: Ensemble approach using all three methods

### Visualization and Reporting
- **Comprehensive Plots**: Time series, frequency domain, and outlier analysis plots
- **Statistical Reports**: Detailed CSV reports with processing statistics
- **Mode Shape Visualization**: Comparison between detected and reference mode shapes
- **Quality Metrics**: MAC values, detection percentages, and confidence intervals

## Installation

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Required packages
pip install numpy pandas scipy matplotlib scikit-learn pyyaml
```

### OMA Library (Required for Step 2)

Install the pyoma2 library for operational modal analysis:

```bash
pip install pyoma2
```

### Optional Dependencies

```bash
# For enhanced plotting capabilities
pip install seaborn plotly

# For parallel processing (if enabled in config)
pip install joblib
```

### Clone the Repository

```bash
git clone https://github.com/your-username/structural-health-monitoring-workflow.git
cd structural-health-monitoring-workflow
```

## Quick Start

### 1. Prepare Your Data

Place your acceleration data files (in pickle format) in the `data/raw` directory:

```
data/
├── raw/
│   ├── segment1_20231201120000_20231201125000.pickle
│   ├── segment2_20231201130000_20231201135000.pickle
│   └── ...
├── filtered/     # Created automatically
├── processed/    # Created automatically
└── ...
```

### 2. Configure the Workflow

Copy and modify the configuration file:

```bash
cp config/config.yaml config/my_project_config.yaml
# Edit config/my_project_config.yaml to match your setup
```

### 3. Run the Complete Workflow

```bash
# Step 1: Data filtering and quality control
python src/processing/step1_data_filtering_qc.py --config config/my_project_config.yaml

# Step 2: OMA processing
python src/processing/step2_data_processing_oma.py --config config/my_project_config.yaml --case-name my_structure

# Step 3: Modal analysis and outlier detection
python src/processing/step3_modal_analysis.py --config config/my_project_config.yaml --mode 6
```

### 4. View Results

Results will be saved in the `results/` directory:

```
results/
├── mode_6_analysis/
│   ├── mode_6_outliers.csv
│   ├── mode_6_comprehensive_analysis.png
│   ├── mode_6_outlier_methods_comparison.png
│   └── ...
└── ...
```

## Workflow Steps

### Step 1: Data Filtering and Quality Control

**File**: `src/processing/step1_data_filtering_qc.py`

This step processes raw acceleration data to:
- Filter channels based on mean value thresholds
- Apply quality control with configurable amplitude bounds
- Remove edge artifacts from sensor attachment/detachment
- Replace systematic shifts with interpolated values
- Validate data quality using window-based analysis

**Key Parameters** (configured in `quality_control` section):
- `mean_threshold`: Channel filtering bounds
- `amplitude_bounds`: Quality control limits
- `required_channels`: Must-have sensor channels
- `cleaning`: Edge detection and drift removal parameters
- `validation`: Window-based quality assessment

**Output**: Cleaned acceleration data in `data/filtered/` directory

### Step 2: Data Processing and OMA Analysis

**File**: `src/processing/step2_data_processing_oma.py`

This step performs operational modal analysis:
- Applies signal filtering (highpass/bandpass)
- Runs SSI-COV and/or FSDD algorithms
- Performs automatic mode clustering using DBSCAN
- Extracts modal parameters (frequencies, damping, mode shapes)
- Optionally splits data into subsections for analysis

**Key Parameters** (configured in `oma` section):
- `settings`: OMA algorithm parameters
- `geometry`: Sensor layout and coordinates
- Signal filtering options (configured in `signal_processing`)

**Output**: OMA results in `data/processed/` directory

### Step 3: Modal Analysis and Outlier Detection

**File**: `src/processing/step3_modal_analysis.py`

This step performs advanced modal analysis:
- Collects mode data across all processed segments
- Applies multiple outlier detection methods
- Creates comprehensive visualizations
- Generates detailed statistical reports
- Analyzes outlier mode shapes vs. reference shapes

**Key Parameters** (configured in `modal_analysis` section):
- `mac_threshold`: Modal Assurance Criterion threshold
- `outlier_detection`: Parameters for each detection method
- `mode_configs`: Mode shape configurations

**Output**: Analysis results in `results/` directory

## Configuration

### Main Configuration File: `config/config.yaml`

The workflow is controlled through a comprehensive YAML configuration file with the following sections:

#### Project Information
```yaml
project:
  name: "structural_health_monitoring"
  description: "Automated SHM analysis workflow"
  version: "1.0.0"
```

#### File Paths
```yaml
paths:
  input_data_dir: "data/raw"
  filtered_data_dir: "data/filtered"
  processed_data_dir: "data/processed"
  analysis_output_dir: "results"
  use_relative_paths: true
```

#### Quality Control Parameters
```yaml
quality_control:
  mean_threshold:
    lower: -1.1
    upper: -0.9
  amplitude_bounds:
    lower: -1.1
    upper: -0.9
  required_channels: ['p_1_1', 'p_1_5', 'p_1_7', 'p_1_11']
  cleaning:
    min_shift_duration: 10
    edge_buffer_ratio: 0.25
    drift_threshold: 0.01
  validation:
    window_size: '10S'
    quality_threshold: 80
```

#### Signal Processing
```yaml
signal_processing:
  sampling_frequency: 250
  filters:
    highpass:
      cutoff: 25
      order: 4
    bandpass:
      lowcut: 40
      highcut: 70
      order: 4
```

#### OMA Settings
```yaml
oma:
  settings:
    fs: 250
    decimation_order: 1
    min_percentage_mode_occurence: 0.2
    ssicov:
      name: "SSIcov"
      method: "cov"
      br: 100
      ordmax: 100
      orderin: 40
  geometry:
    sensor_names: ['p_1_1', 'p_1_3', 'p_1_5', 'p_1_7', 'p_1_9', 'p_1_11']
    sensor_coordinates: [...]  # [x, y, z] coordinates
    sensor_directions: [...]   # [x, y, z] unit vectors
```

#### Modal Analysis Parameters
```yaml
modal_analysis:
  mac_threshold: 0.6
  max_outliers_to_analyze: 10
  outlier_detection:
    std_dev:
      threshold: 2.0
    curve_fitting:
      confidence_level: 0.95
      polynomial_degree: 2
    mac_frequency:
      mac_threshold: 0.6
      freq_std_threshold: 1.5
  mode_configs:
    '1': {'indices': [0, 1, 2], 'labels': ['1.1', '1.2', '1.3']}
    # ... additional modes
```

### Customizing for Your Structure

1. **Sensor Configuration**: Update `oma.geometry` section with your sensor layout
2. **Quality Thresholds**: Adjust `quality_control` bounds based on your sensor characteristics
3. **Mode Definitions**: Modify `modal_analysis.mode_configs` for your expected mode shapes
4. **Processing Range**: Set `processing.segment_range` for your data segments

## Data Format

### Input Data Format

The workflow expects input data as Python pickle files with the following structure:

```python
{
    'accelerations': pandas.DataFrame,  # Time-indexed acceleration data
    'metadata': {
        'tag_columns': list,            # Non-acceleration columns to exclude
        # ... other metadata
    }
}
```

**DataFrame Requirements**:
- **Index**: DateTime index with consistent sampling rate
- **Columns**: Sensor channel names (e.g., 'p_1_1', 'p_1_5', etc.)
- **Values**: Acceleration values in appropriate units (typically m/s²)

### Filename Convention

Input files should follow the naming pattern:
```
{prefix}_segment{N}_{start_datetime}_{end_datetime}.pickle
```

Example:
```
project_segment1_20231201120000_20231201125000.pickle
```

Where:
- `{N}`: Segment number
- `{start_datetime}`, `{end_datetime}`: YYYYMMDDHHMMSS format

### Output Data Structures

#### Step 1 Output (Filtered Data)
Original structure plus:
```python
{
    'accelerations': pandas.DataFrame,  # Cleaned acceleration data
    'qc_metadata': {
        'cleaning_stats': dict,         # Per-channel cleaning statistics
        'quality_score': float,         # Overall quality percentage
        'window_stats': dict,           # Window-based validation results
        'qc_bounds': list,              # Applied quality control bounds
        'processing_timestamp': str     # ISO format timestamp
    }
}
```

#### Step 2 Output (OMA Results)
Filtered data plus:
```python
{
    'oma_results': {
        'SSIcov': {
            'Fn': list,                 # Natural frequencies
            'Xi': list,                 # Damping ratios
            'Phi': array,               # Mode shapes
            # ... other OMA parameters
        },
        'metadata': {
            'representative_modes': list,
            'autoclustered_frequencies': list,
            'detection_percentages': list,
            'settings_used': dict
        }
    }
}
```

## Usage Examples

### Basic Workflow Execution

```bash
# Complete workflow with default settings
python src/processing/step1_data_filtering_qc.py --config config/config.yaml
python src/processing/step2_data_processing_oma.py --config config/config.yaml --case-name bridge_test
python src/processing/step3_modal_analysis.py --config config/config.yaml --mode 6
```

### Custom Processing Options

```bash
# Process specific segment range
python src/processing/step1_data_filtering_qc.py \
    --config config/config.yaml \
    --segment-start 10 \
    --segment-end 50

# Use highpass filtering instead of bandpass
python src/processing/step2_data_processing_oma.py \
    --config config/config.yaml \
    --filter-type highpass \
    --case-name bridge_highpass

# Split data into subsections for OMA analysis
python src/processing/step2_data_processing_oma.py \
    --config config/config.yaml \
    --use-subsections \
    --n-splits 4 \
    --case-name bridge_subsections
```

### Advanced Modal Analysis

```bash
# Analyze mode 3 with standard deviation outlier detection only
python src/processing/step3_modal_analysis.py \
    --config config/config.yaml \
    --mode 3 \
    --outlier-method 1 \
    --std-threshold 2.5

# Mode 6 analysis with best MAC filtering
python src/processing/step3_modal_analysis.py \
    --config config/config.yaml \
    --mode 6 \
    --best-mac-only \
    --outlier-method all

# Custom MAC and confidence thresholds
python src/processing/step3_modal_analysis.py \
    --config config/config.yaml \
    --mode 4 \
    --mac-threshold 0.7 \
    --confidence-level 0.99 \
    --max-outliers 15
```

### Batch Processing Multiple Modes

```bash
#!/bin/bash
# Process all modes with combined outlier detection
for mode in 1 2 3 4 5 6; do
    python src/processing/step3_modal_analysis.py \
        --config config/config.yaml \
        --mode $mode \
        --outlier-method all
done
```

## Advanced Features

### Outlier Detection Methods

#### Method 1: Standard Deviation Based
- Uses z-score thresholds to identify outliers
- Configurable standard deviation multiplier
- Fast and simple, good for obvious outliers
- Best for: Initial screening, large datasets

```python
# Configuration
outlier_detection:
  std_dev:
    threshold: 2.0  # Number of standard deviations
```

#### Method 2: Curve Fitting with Confidence Intervals
- Fits polynomial to frequency vs. segment trend
- Uses t-distribution for confidence intervals
- Accounts for temporal trends in the data
- Best for: Time-dependent behavior, drift detection

```python
# Configuration
outlier_detection:
  curve_fitting:
    confidence_level: 0.95    # Confidence level
    polynomial_degree: 2      # Polynomial order
```

#### Method 3: MAC-Frequency Combined Analysis
- Uses 2D analysis of MAC values and frequencies
- Includes Mahalanobis distance calculations
- Accounts for mode shape quality (MAC)
- Best for: Quality-aware detection, modal analysis

```python
# Configuration
outlier_detection:
  mac_frequency:
    mac_threshold: 0.6           # Minimum MAC value
    freq_std_threshold: 1.5      # Frequency deviation threshold
```

#### Combined Method
- Uses ensemble of all three methods
- Identifies outliers found by any method
- Provides comprehensive analysis
- Best for: Thorough analysis, research applications

### Best MAC Filtering (Mode 6)

For structures with multiple closely-spaced modes (e.g., modes 6.1, 6.2, 6.3), the workflow can automatically select the mode with the highest MAC value per segment:

```bash
python src/processing/step3_modal_analysis.py \
    --config config/config.yaml \
    --mode 6 \
    --best-mac-only
```

This feature:
- Groups data by segment
- Finds the sub-mode with highest MAC value per segment
- Provides mode selection statistics
- Reduces data scatter and improves analysis quality

### Parallel Processing

Enable parallel processing for large datasets:

```yaml
processing:
  use_parallel: true
  max_workers: 4
```

### Custom Mode Shapes

Define your own reference mode shapes by modifying the predefined mode arrays in `step3_modal_analysis.py`:

```python
# Example: 4-sensor setup
predefined_modes_4 = np.array([
    [1, 0, -1, 0],      # Mode 1: First bending
    [1, -1, -1, 1],     # Mode 2: Second bending  
    [1, -1, 1, -1],     # Mode 3: Third bending
    [1, 1, 1, 1],       # Mode 4: First torsion
])
```

### Extensibility

The workflow is designed for easy extension:

1. **New Outlier Detection Methods**: Add to `detect_outliers_comprehensive()`
2. **Additional OMA Algorithms**: Extend `oma_utilities.py`
3. **Custom Quality Metrics**: Modify `validate_data_quality()`
4. **New Visualization Types**: Add to plotting functions

## Troubleshooting

### Common Issues

#### Import Errors

```
ImportError: No module named 'pyoma2'
```
**Solution**: Install the OMA library:
```bash
pip install pyoma2
```

#### Configuration Errors

```
KeyError: 'required_channels'
```
**Solution**: Ensure your configuration file includes all required sections. Compare with the reference `config/config.yaml`.

#### Data Format Issues

```
ValueError: 'accelerations' is not a DataFrame
```
**Solution**: Verify your input pickle files contain the correct data structure. See [Data Format](#data-format) section.

#### No Files Processed

```
Processing complete. Total files processed: 0
```
**Possible causes**:
1. Wrong input directory path
2. No files match the expected naming pattern
3. All files fail quality control thresholds

**Solution**: Check file paths, naming conventions, and quality control settings.

### Debugging Tips

1. **Enable Debug Logging**:
   ```yaml
   processing:
     log_level: "DEBUG"
   ```

2. **Process Single Segment**:
   ```bash
   python src/processing/step1_data_filtering_qc.py \
       --config config/config.yaml \
       --segment-start 1 \
       --segment-end 1
   ```

3. **Check Intermediate Results**:
   - Step 1: Check `data/filtered/` for cleaned data
   - Step 2: Check `data/processed/` for OMA results
   - Step 3: Check `results/` for analysis outputs

4. **Validate Configuration**:
   ```python
   import yaml
   with open('config/config.yaml', 'r') as f:
       config = yaml.safe_load(f)
   # Check config structure
   ```

### Performance Optimization

1. **Large Datasets**:
   - Enable parallel processing
   - Use subsection analysis
   - Increase quality thresholds to filter more aggressively

2. **Memory Issues**:
   - Process segments in batches
   - Reduce maximum model orders in OMA settings
   - Use decimation to reduce data size

3. **Slow Analysis**:
   - Reduce polynomial degree for curve fitting
   - Lower maximum outliers to analyze
   - Use single outlier detection method instead of combined

### Getting Help

1. **Check Examples**: Review the `examples/` directory for sample configurations
2. **Documentation**: Refer to the detailed docstrings in each module
3. **Configuration Reference**: Use `config/config.yaml` as a complete reference
4. **Issue Reporting**: Create GitHub issues with:
   - Configuration file (with sensitive data removed)
   - Error messages and stack traces  
   - Sample data structure (if possible)

## Contributing

We welcome contributions to improve the workflow! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/your-username/structural-health-monitoring-workflow.git
cd structural-health-monitoring-workflow

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -r requirements-dev.txt
```

### Areas for Contribution

- Additional outlier detection algorithms
- Support for more data formats
- Enhanced visualization capabilities
- Performance optimizations
- Documentation improvements
- Test coverage expansion

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this workflow in your research, please cite:

```bibtex
@software{shm_workflow,
  title = {Structural Health Monitoring Workflow: An Open-Source Analysis Pipeline},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/your-username/structural-health-monitoring-workflow}
}
```

## Acknowledgments

- pyoma2 library for operational modal analysis capabilities
- scikit-learn for machine learning algorithms
- The structural health monitoring community for research foundations
