"""
Sample Data Generator for Testing the Workflow

This script generates synthetic acceleration data that follows the expected format
for the structural health monitoring workflow. Useful for testing and demonstration.

Usage:
    python generate_sample_data.py --config ../config/config.yaml --n-segments 10
"""

import os
import sys
import pickle
import argparse
import numpy as np
import pandas as pd
import yaml
from pathlib import Path
from datetime import datetime, timedelta

# Add utils to path for config loading
sys.path.append(str(Path(__file__).parent.parent / 'src' / 'utils'))

try:
    from data_processing_utilities import load_config
except ImportError:
    def load_config(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)


def generate_synthetic_acceleration_data(sensor_names, duration_minutes=25, fs=250, 
                                       base_frequencies=[5, 12, 18, 25, 35], 
                                       noise_level=0.05, trend_amplitude=0.02):
    """
    Generate synthetic acceleration data with modal characteristics.
    
    Parameters:
    - sensor_names: list of sensor channel names
    - duration_minutes: duration of signal in minutes
    - fs: sampling frequency in Hz
    - base_frequencies: fundamental frequencies to simulate
    - noise_level: amplitude of random noise
    - trend_amplitude: amplitude of low-frequency trends
    
    Returns:
    - pandas DataFrame with synthetic acceleration data
    """
    # Calculate number of samples
    n_samples = int(duration_minutes * 60 * fs)
    
    # Create time vector
    t = np.linspace(0, duration_minutes * 60, n_samples)
    
    # Create datetime index
    start_time = datetime.now().replace(second=0, microsecond=0)
    time_index = pd.date_range(start=start_time, periods=n_samples, freq=f'{1000/fs}ms')
    
    # Initialize data dictionary
    data = {}
    
    for i, sensor in enumerate(sensor_names):
        # Start with base signal
        signal = np.zeros(n_samples)
        
        # Add modal contributions
        for j, freq in enumerate(base_frequencies):
            # Mode shape factor (varies by sensor position)
            mode_factor = np.sin(np.pi * (i + 1) / (len(sensor_names) + 1))
            
            # Add modal response with some frequency variation
            freq_var = freq * (1 + 0.02 * np.random.randn())  # 2% frequency variation
            amplitude = 0.1 * mode_factor * (1 / (j + 1))  # Decreasing amplitude with mode number
            phase = np.random.uniform(0, 2*np.pi)  # Random phase
            
            signal += amplitude * np.sin(2 * np.pi * freq_var * t + phase)
        
        # Add low-frequency trend (simulate environmental effects)
        trend_freq = 0.001 + 0.001 * np.random.randn()  # Very low frequency
        trend = trend_amplitude * np.sin(2 * np.pi * trend_freq * t + np.random.uniform(0, 2*np.pi))
        signal += trend
        
        # Add random noise
        noise = noise_level * np.random.randn(n_samples)
        signal += noise
        
        # Add some occasional "outliers" - sudden shifts
        if np.random.rand() < 0.1:  # 10% chance of outlier region
            outlier_start = np.random.randint(int(0.1 * n_samples), int(0.8 * n_samples))
            outlier_duration = np.random.randint(int(0.01 * n_samples), int(0.05 * n_samples))
            outlier_end = min(outlier_start + outlier_duration, n_samples)
            
            # Add systematic shift
            shift_amplitude = 0.3 * np.random.randn()
            signal[outlier_start:outlier_end] += shift_amplitude
        
        # Simulate sensor attachment/detachment artifacts at edges
        if np.random.rand() < 0.2:  # 20% chance of edge artifact
            edge_samples = int(0.02 * n_samples)  # 2% of signal at each edge
            
            # Start edge artifact
            if np.random.rand() < 0.5:
                ramp = np.linspace(2.0, 0, edge_samples)
                signal[:edge_samples] += ramp * np.random.randn()
            
            # End edge artifact  
            if np.random.rand() < 0.5:
                ramp = np.linspace(0, -1.5, edge_samples)
                signal[-edge_samples:] += ramp * np.random.randn()
        
        # Scale to typical acceleration range (adjust mean to be within QC bounds)
        target_mean = np.random.uniform(-1.05, -0.95)  # Within typical QC bounds
        signal = signal - np.mean(signal) + target_mean
        
        data[sensor] = signal
    
    # Create DataFrame
    df = pd.DataFrame(data, index=time_index)
    
    return df


def create_sample_pickle_file(output_path, acceleration_data, metadata=None):
    """
    Create a pickle file in the expected format.
    
    Parameters:
    - output_path: path for output file
    - acceleration_data: pandas DataFrame with acceleration data
    - metadata: optional metadata dictionary
    """
    if metadata is None:
        metadata = {
            'tag_columns': [],  # No tag columns in synthetic data
            'sampling_frequency': 250,
            'generation_timestamp': datetime.now().isoformat(),
            'synthetic': True
        }
    
    data_dict = {
        'accelerations': acceleration_data,
        'metadata': metadata
    }
    
    with open(output_path, 'wb') as f:
        pickle.dump(data_dict, f)


def generate_sample_dataset(config, output_dir, n_segments=10, case_name='sample'):
    """
    Generate a complete sample dataset with multiple segments.
    
    Parameters:
    - config: configuration dictionary
    - output_dir: output directory for sample files
    - n_segments: number of segments to generate
    - case_name: name prefix for files
    """
    # Get sensor names from config
    oma_config = config.get('oma', {})
    geometry = oma_config.get('geometry', {})
    sensor_names = geometry.get('sensor_names', ['sensor_1', 'sensor_2', 'sensor_3', 'sensor_4'])
    
    # Get sampling frequency
    signal_config = config.get('signal_processing', {})
    fs = signal_config.get('sampling_frequency', 250)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {n_segments} sample segments...")
    print(f"Sensors: {sensor_names}")
    print(f"Sampling frequency: {fs} Hz")
    print(f"Output directory: {output_path}")
    
    for segment in range(1, n_segments + 1):
        # Generate time stamps for this segment (25-minute segments with 5-minute gaps)
        base_time = datetime(2024, 1, 1, 9, 0, 0) + timedelta(minutes=(segment-1) * 30)
        start_time = base_time
        end_time = base_time + timedelta(minutes=25)
        
        # Format timestamps for filename
        start_str = start_time.strftime('%Y%m%d%H%M%S')
        end_str = end_time.strftime('%Y%m%d%H%M%S')
        
        # Generate acceleration data
        acceleration_data = generate_synthetic_acceleration_data(
            sensor_names=sensor_names,
            duration_minutes=25,
            fs=fs,
            base_frequencies=[4 + segment*0.1, 12 + segment*0.05, 18 + segment*0.02, 25, 35],  # Slight frequency drift
            noise_level=0.05 + 0.01 * np.random.randn(),  # Variable noise
            trend_amplitude=0.02 + 0.005 * np.random.randn()  # Variable trends
        )
        
        # Set the time index to match the segment times
        new_index = pd.date_range(start=start_time, end=end_time, periods=len(acceleration_data))
        acceleration_data.index = new_index
        
        # Create metadata
        metadata = {
            'tag_columns': [],
            'sampling_frequency': fs,
            'segment_number': segment,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'generation_timestamp': datetime.now().isoformat(),
            'synthetic': True,
            'data_quality': np.random.choice(['good', 'fair', 'excellent'], p=[0.6, 0.3, 0.1])
        }
        
        # Create filename
        filename = f"{case_name}_segment{segment}_{start_str}_{end_str}.pickle"
        file_path = output_path / filename
        
        # Save file
        create_sample_pickle_file(file_path, acceleration_data, metadata)
        
        if segment <= 5 or segment % 10 == 0:  # Print progress for first 5 and every 10th
            print(f"Generated segment {segment}: {filename}")
    
    print(f"\nGenerated {n_segments} sample files in {output_path}")
    
    # Create a summary file
    summary = {
        'dataset_info': {
            'n_segments': n_segments,
            'case_name': case_name,
            'sensors': sensor_names,
            'sampling_frequency': fs,
            'segment_duration_minutes': 25,
            'generation_date': datetime.now().isoformat()
        },
        'file_pattern': f"{case_name}_segment{{N}}_{{start}}_{{end}}.pickle",
        'expected_workflow_steps': [
            f"step1_data_filtering_qc.py --config config.yaml",
            f"step2_data_processing_oma.py --config config.yaml --case-name {case_name}",
            f"step3_modal_analysis.py --config config.yaml --mode 6"
        ]
    }
    
    summary_path = output_path / 'dataset_summary.yaml'
    with open(summary_path, 'w') as f:
        yaml.dump(summary, f, default_flow_style=False, sort_keys=False)
    
    print(f"Dataset summary saved to: {summary_path}")
    
    return output_path


def main():
    """Main function for sample data generation."""
    parser = argparse.ArgumentParser(description='Generate Sample Data for SHM Workflow')
    parser.add_argument('--config', required=True, help='Path to configuration file')
    parser.add_argument('--output-dir', help='Output directory (default: from config)')
    parser.add_argument('--n-segments', type=int, default=10, help='Number of segments to generate')
    parser.add_argument('--case-name', default='sample', help='Case name prefix for files')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    else:
        # Use the input_data_dir from config
        paths = config.get('paths', {})
        if paths.get('use_relative_paths', True):
            project_root = Path.cwd()
            output_dir = project_root / paths.get('input_data_dir', 'data/raw')
        else:
            output_dir = Path(paths.get('input_data_dir', 'data/raw'))
    
    print("Sample Data Generator for SHM Workflow")
    print("=" * 50)
    print(f"Configuration: {args.config}")
    print(f"Output directory: {output_dir}")
    print(f"Number of segments: {args.n_segments}")
    print(f"Case name: {args.case_name}")
    print("=" * 50)
    
    try:
        result_path = generate_sample_dataset(
            config=config,
            output_dir=output_dir,
            n_segments=args.n_segments,
            case_name=args.case_name
        )
        
        print("\n" + "=" * 50)
        print("SAMPLE DATA GENERATION COMPLETE")
        print("=" * 50)
        print(f"Files created in: {result_path}")
        print(f"Total segments: {args.n_segments}")
        
        print("\nNext steps:")
        print("1. Review the generated configuration and data")
        print("2. Run the workflow steps:")
        print(f"   python src/processing/step1_data_filtering_qc.py --config {args.config}")
        print(f"   python src/processing/step2_data_processing_oma.py --config {args.config} --case-name {args.case_name}")
        print(f"   python src/processing/step3_modal_analysis.py --config {args.config} --mode 6")
        
        return 0
        
    except Exception as e:
        print(f"\nError generating sample data: {e}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
