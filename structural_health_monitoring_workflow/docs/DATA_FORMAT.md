# Data Format Specification

## Overview

The Structural Health Monitoring workflow expects acceleration data in Python pickle format with a specific dictionary structure. This document provides detailed specifications for input and output data formats.

## Input Data Format

### File Format: Pickle (.pickle)

Each data file must be a Python pickle containing a dictionary with the following structure:

```python
{
    'accelerations': pandas.DataFrame,
    'metadata': dict
}
```

### Accelerations DataFrame

The `accelerations` key must contain a pandas DataFrame with:

#### Index (Required)
- **Type**: `pandas.DatetimeIndex`
- **Description**: Timestamps for each data point
- **Sampling**: Must be uniformly sampled
- **Format**: Any timezone-aware or naive datetime format

```python
# Example index
DatetimeIndex([
    '2024-01-01 09:00:00.000',
    '2024-01-01 09:00:00.004',  # 250 Hz sampling (4ms intervals)
    '2024-01-01 09:00:00.008',
    # ...
])
```

#### Columns (Required)
- **Type**: Sensor channel names (strings)
- **Description**: Each column represents one acceleration sensor
- **Format**: Any consistent naming convention
- **Example**: `['p_1_1', 'p_1_5', 'p_1_7', 'p_1_11']` or `['sensor_1', 'sensor_2', ...]`

#### Data Values (Required)
- **Type**: Numeric (float64 recommended)
- **Units**: Acceleration (typically m/s² or g)
- **Range**: Depends on sensor characteristics (typically ±10 m/s²)
- **Missing Values**: NaN values allowed but will trigger quality control warnings

```python
# Example DataFrame structure
                        p_1_1    p_1_5    p_1_7    p_1_11
2024-01-01 09:00:00.000  -0.98   -1.02   -0.95    -1.01
2024-01-01 09:00:00.004  -0.97   -1.03   -0.94    -1.02
2024-01-01 09:00:00.008  -0.99   -1.01   -0.96    -1.00
```

### Metadata Dictionary

The `metadata` key must contain a dictionary with required and optional fields:

#### Required Fields

```python
{
    'tag_columns': list  # Column names to exclude from analysis (empty list if none)
}
```

#### Optional Fields (Recommended)

```python
{
    'sampling_frequency': float,     # Hz, used for validation
    'sensor_locations': dict,        # Mapping of sensor names to descriptions
    'measurement_units': str,        # e.g., 'm/s²', 'g'
    'acquisition_system': str,       # DAQ system identifier
    'calibration_factors': dict,     # Per-channel calibration values
    'environmental_conditions': dict, # Temperature, humidity, etc.
    'structure_info': dict,          # Information about monitored structure
    'quality_flags': dict           # Pre-processing quality indicators
}
```

### Complete Example

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Create sample data
start_time = datetime(2024, 1, 1, 9, 0, 0)
fs = 250  # Hz
duration_minutes = 25
n_samples = int(duration_minutes * 60 * fs)

# Generate time index
time_index = pd.date_range(
    start=start_time, 
    periods=n_samples, 
    freq=f'{1000/fs}ms'
)

# Generate synthetic acceleration data
np.random.seed(42)
data = {
    'p_1_1': -1.0 + 0.1 * np.random.randn(n_samples),
    'p_1_5': -1.0 + 0.1 * np.random.randn(n_samples), 
    'p_1_7': -1.0 + 0.1 * np.random.randn(n_samples),
    'p_1_11': -1.0 + 0.1 * np.random.randn(n_samples)
}

accelerations_df = pd.DataFrame(data, index=time_index)

# Create complete data structure
data_dict = {
    'accelerations': accelerations_df,
    'metadata': {
        'tag_columns': [],
        'sampling_frequency': 250.0,
        'measurement_units': 'm/s²',
        'sensor_locations': {
            'p_1_1': 'Position 1, Channel 1',
            'p_1_5': 'Position 1, Channel 5', 
            'p_1_7': 'Position 1, Channel 7',
            'p_1_11': 'Position 1, Channel 11'
        },
        'acquisition_system': 'Generic DAQ',
        'structure_info': {
            'type': 'bridge',
            'span_length_m': 50.0,
            'construction_year': 2010
        }
    }
}

# Save as pickle
import pickle
with open('sample_data.pickle', 'wb') as f:
    pickle.dump(data_dict, f)
```

## File Naming Convention

Input files should follow this naming pattern for automatic segment detection:

```
{project_name}_segment{N}_{start_datetime}_{end_datetime}.pickle
```

### Components

- `{project_name}`: Descriptive project/structure name
- `{N}`: Segment number (integer, e.g., 1, 2, 3, ...)
- `{start_datetime}`: Start time in YYYYMMDDHHMMSS format
- `{end_datetime}`: End time in YYYYMMDDHHMMSS format

### Examples

```
bridge_monitoring_segment1_20240101090000_20240101092500.pickle
building_test_segment25_20240315143000_20240315145500.pickle
structure_A_segment100_20241201120000_20241201122500.pickle
```

## Output Data Formats

### Step 1 Output: Quality-Controlled Data

Original structure enhanced with quality control metadata:

```python
{
    'accelerations': pandas.DataFrame,  # Cleaned acceleration data
    'metadata': dict,                   # Original metadata preserved
    'qc_metadata': {
        'cleaning_stats': {
            'sensor_1': {
                'original_length': 375000,
                'final_length': 365000,
                'edge_removed': 8000,
                'interior_replaced': 2000,
                'percent_valid': 97.3
            },
            # ... stats for each sensor
        },
        'quality_score': 95.2,             # Percentage of valid windows
        'window_stats': {
            'total_windows': 150,
            'valid_windows': 143,
            'invalid_windows': 7
        },
        'qc_bounds': [-1.1, -0.9],         # Applied amplitude bounds
        'processing_timestamp': '2024-01-01T10:30:00'
    }
}
```

### Step 2 Output: OMA Analysis Results

Quality-controlled data enhanced with modal analysis results:

```python
{
    'accelerations': pandas.DataFrame,   # Filtered acceleration data
    'metadata': dict,                    # Previous metadata
    'qc_metadata': dict,                 # QC results from Step 1
    'oma_results': {
        'SSIcov': {
            'Fn': [5.23, 12.45, 18.76, 25.12],     # Natural frequencies (Hz)
            'Xi': [0.015, 0.022, 0.018, 0.025],    # Damping ratios
            'Phi': array([[...], [...], [...]]),    # Mode shapes matrix
            'MAC': array([[1.0, 0.1, ...],         # Modal Assurance Criterion
                         [0.1, 1.0, ...]]),
            'stabilization_diagram': {...},         # Stabilization info
            # ... additional OMA parameters
        },
        'FSDD': {  # Optional, if FSDD algorithm enabled
            'Fn': [...],
            'Phi': [...],
            # ... FSDD-specific results
        },
        'metadata': {
            'representative_modes': [5.23, 12.45, 18.76, 25.12],
            'autoclustered_frequencies': [5.21, 5.23, 5.25, 12.44, 12.45, ...],
            'detection_percentages': [0.85, 0.92, 0.78, 0.88],
            'settings_used': {
                'fs': 250,
                'decimation_order': 1,
                'ssicov_ordmax': 100,
                # ... complete settings used
            },
            'processing_timestamp': '2024-01-01T11:15:00'
        }
    }
}
```

### Step 3 Output: Analysis Reports (CSV)

Modal analysis generates CSV files with outlier analysis:

#### `mode_N_outliers.csv`

```csv
Segment,Sub_Mode,Frequency,MAC_Value,Z_Score,Is_Outlier,Outlier_Type,Distance_from_Mean
1,6.1,25.23,0.85,0.23,False,None,0.12
2,6.2,25.89,0.72,2.15,True,Standard_Deviation,0.89
3,6.1,24.95,0.91,-0.45,False,None,-0.25
4,6.3,28.45,0.45,3.67,True,Combined,3.45
```

#### `mode_N_raw_data_summary.csv`

```csv
Segment,Sub_Mode,Frequency,MAC_Value,Num_Channels,Duration_s,Quality_Score,Processing_Status
1,6.1,25.23,0.85,4,1500,97.2,Success
2,6.2,25.89,0.72,4,1500,95.8,Success
3,6.1,24.95,0.91,4,1480,98.1,Edge_Trimmed
```

## Data Quality Requirements

### Minimum Requirements

1. **Sampling Rate**: ≥ 50 Hz (recommended ≥ 100 Hz)
2. **Duration**: ≥ 10 minutes per segment (recommended ≥ 20 minutes)
3. **Data Continuity**: < 1% missing samples
4. **Amplitude Range**: Within ±10× typical sensor range
5. **Sensor Count**: ≥ 2 channels (recommended ≥ 4)

### Quality Indicators

The workflow automatically assesses data quality based on:

1. **Window-based validation**: Percentage of time windows passing amplitude checks
2. **Continuity score**: Fraction of expected samples present
3. **Signal-to-noise ratio**: Estimated from frequency domain characteristics
4. **Edge artifacts**: Detection of sensor attachment/detachment issues

### Quality Thresholds (Configurable)

```yaml
quality_control:
  validation:
    window_size: '10S'          # Time window for validation
    quality_threshold: 80       # Minimum percentage of valid windows
    continuity_threshold: 99    # Minimum data continuity percentage
    snr_threshold: 20          # Minimum signal-to-noise ratio (dB)
```

## Data Validation Tools

### Built-in Validation

The workflow includes automatic validation:

```python
# Check data structure
def validate_pickle_structure(data_dict):
    required_keys = ['accelerations', 'metadata']
    for key in required_keys:
        if key not in data_dict:
            raise ValueError(f"Missing required key: {key}")
    
    if not isinstance(data_dict['accelerations'], pd.DataFrame):
        raise TypeError("'accelerations' must be a pandas DataFrame")
    
    # ... additional checks

# Check sampling frequency
def validate_sampling_rate(df, expected_fs):
    actual_fs = 1 / df.index.to_series().diff().dt.total_seconds().median()
    if abs(actual_fs - expected_fs) > 0.1 * expected_fs:
        print(f"Warning: Sampling rate mismatch. Expected: {expected_fs}, Actual: {actual_fs}")
```

### Manual Validation Script

Create a validation script for your data:

```python
import pickle
import pandas as pd

def validate_data_file(filepath):
    """Validate a single pickle file."""
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
        
        # Check structure
        assert 'accelerations' in data, "Missing 'accelerations' key"
        assert 'metadata' in data, "Missing 'metadata' key"
        
        df = data['accelerations']
        
        # Check DataFrame properties
        assert isinstance(df.index, pd.DatetimeIndex), "Index must be DatetimeIndex"
        assert len(df.columns) >= 2, "Need at least 2 sensor channels"
        assert len(df) >= 1000, "Need at least 1000 samples"
        
        # Check for missing data
        missing_pct = (df.isnull().sum().sum() / df.size) * 100
        if missing_pct > 1:
            print(f"Warning: {missing_pct:.1f}% missing data")
        
        # Check sampling regularity
        dt = df.index.to_series().diff().dt.total_seconds()
        if dt.std() > 0.001:  # More than 1ms jitter
            print(f"Warning: Irregular sampling detected")
        
        print(f"✓ {filepath}: Valid")
        return True
        
    except Exception as e:
        print(f"✗ {filepath}: {e}")
        return False

# Validate all files in directory
import glob
for file in glob.glob("data/raw/*.pickle"):
    validate_data_file(file)
```

## Troubleshooting Data Issues

### Common Problems and Solutions

#### 1. Wrong Data Type
```
TypeError: 'accelerations' must be a pandas DataFrame
```
**Solution**: Ensure acceleration data is stored as pandas DataFrame, not numpy array or list.

#### 2. Missing DateTime Index
```
AssertionError: Index must be DatetimeIndex
```
**Solution**: Convert index to datetime:
```python
df.index = pd.to_datetime(df.index)
```

#### 3. Irregular Sampling
```
Warning: Maximum time step exceeds expected
```
**Solution**: Resample data to uniform grid:
```python
df = df.resample('4ms').interpolate()  # For 250 Hz
```

#### 4. Excessive Missing Data
```
Warning: 15.2% missing data
```
**Solution**: Fill small gaps or exclude problematic segments:
```python
# Fill small gaps (< 10 samples)
df = df.interpolate(limit=10)
# Or exclude segments with > 5% missing
if missing_pct > 5:
    skip_segment = True
```

#### 5. Amplitude Range Issues
```
All channels are outside the mean threshold
```
**Solution**: Check and adjust quality control bounds in configuration:
```yaml
quality_control:
  amplitude_bounds:
    lower: -2.0    # Adjust based on your sensor range
    upper: 2.0
```

For additional troubleshooting, see the main [README.md](../README.md) troubleshooting section.
