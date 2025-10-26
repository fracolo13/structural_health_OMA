# Quick Start Guide

## 5-Minute Setup

This guide will get you running the structural health monitoring workflow in 5 minutes using synthetic data.

### Step 1: Clone and Setup (1 minute)

```bash
# Clone repository  
git clone https://github.com/your-username/structural-health-monitoring-workflow.git
cd structural-health-monitoring-workflow

# Install minimal dependencies
pip install numpy pandas scipy matplotlib scikit-learn PyYAML pyoma2
```

### Step 2: Generate Sample Data (1 minute)

```bash
# Generate 5 sample data segments for testing
python examples/generate_sample_data.py \
    --config config/config.yaml \
    --n-segments 5 \
    --case-name quickstart
```

This creates synthetic acceleration data in `data/raw/` with:
- 5 data segments (25 minutes each)
- 6 sensors with realistic modal behavior
- Some artificial outliers and noise

### Step 3: Run Complete Workflow (3 minutes)

```bash
# Step 1: Data filtering and quality control
python src/processing/step1_data_filtering_qc.py \
    --config config/config.yaml \
    --segment-start 1 \
    --segment-end 5

# Step 2: Operational Modal Analysis  
python src/processing/step2_data_processing_oma.py \
    --config config/config.yaml \
    --case-name quickstart \
    --filter-type bandpass

# Step 3: Modal analysis and outlier detection
python src/processing/step3_modal_analysis.py \
    --config config/config.yaml \
    --mode 6 \
    --outlier-method all
```

### Step 4: View Results

Check the generated outputs:

```bash
# View processing summary
ls data/filtered/    # Quality-controlled data
ls data/processed/   # OMA analysis results  
ls results/          # Final analysis outputs

# View analysis plots
open results/mode_6_analysis/mode_6_comprehensive_analysis.png
open results/mode_6_analysis/mode_6_outliers.csv
```

## Expected Results

After running the workflow, you should see:

### Console Output
```
Processing complete. Total files processed: 5
MODE 6 ANALYSIS COMPLETE
Total data points: 15
Outliers detected: 2
Outlier percentage: 13.3%
```

### Generated Files
```
data/
├── raw/           # 5 synthetic pickle files
├── filtered/      # 5 quality-controlled files  
└── processed/     # 5 OMA result files

results/
└── mode_6_analysis/
    ├── mode_6_outliers.csv
    ├── mode_6_comprehensive_analysis.png
    ├── mode_6_outlier_methods_comparison.png
    └── mode_6_raw_data_summary.csv
```

### Key Metrics
- **Data Quality**: 95-100% of windows pass quality control
- **Modal Analysis**: 3-6 modes identified per segment
- **Outlier Detection**: 1-3 outliers detected using combined methods
- **Processing Time**: ~2-3 minutes for 5 segments

## Next Steps

1. **Customize Configuration**: Edit `config/config.yaml` for your structure
2. **Add Real Data**: Replace synthetic data with your acceleration measurements
3. **Tune Parameters**: Adjust quality control and outlier detection thresholds
4. **Analyze More Modes**: Run analysis for modes 1-5 using `--mode` parameter

## Common Issues

### ImportError: pyoma2
```bash
pip install pyoma2
```

### No files processed
Check that data files are in the correct location:
```bash
ls data/raw/*.pickle
```

### Configuration errors
Verify YAML syntax:
```bash
python -c "import yaml; yaml.safe_load(open('config/config.yaml'))"
```

## Full Documentation

For complete documentation, see [README.md](README.md) which includes:
- Detailed configuration options
- Advanced analysis features  
- Custom data format guidelines
- Troubleshooting guide
