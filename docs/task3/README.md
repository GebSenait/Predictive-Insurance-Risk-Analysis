# Task 3: Statistical Validation of Risk Drivers through A/B Hypothesis Testing

## Overview

Task 3 implements statistical hypothesis testing to validate or reject key assumptions about insurance risk drivers. This analysis supports ACIS's segmentation strategy by quantifying risk across geographic, demographic, and profitability dimensions.

## Objectives

- Perform statistical hypothesis testing on four null hypotheses related to insurance risk drivers
- Compute key performance indicators (KPIs): Claim Frequency, Claim Severity, and Margin
- Create proper A/B test groups for each hypothesis
- Generate comprehensive reports with business interpretations

## Null Hypotheses Tested

1. **H₀: No risk differences across provinces**
   - Tests: Claim Frequency, Claim Severity

2. **H₀: No risk differences between zip codes**
   - Tests: Claim Frequency, Claim Severity

3. **H₀: No significant margin (profit) difference between zip codes**
   - Tests: Margin (TotalPremium - TotalClaims)

4. **H₀: No significant risk difference between women and men**
   - Tests: Claim Frequency, Claim Severity

## Metrics Computed

### Claim Frequency
- **Definition**: Number of claims per policy (binary: 0 or 1+)
- **Group-level**: Total claims / Total policies
- **Use**: Measures how often claims occur

### Claim Severity
- **Definition**: Average claim amount when claims occur
- **Group-level**: Total claims amount / Number of policies with claims
- **Use**: Measures the size of claims when they happen

### Margin
- **Definition**: TotalPremium - TotalClaims
- **Group-level**: Sum of premiums - Sum of claims
- **Use**: Measures profitability per group

### Loss Ratio
- **Definition**: TotalClaims / TotalPremium
- **Use**: Measures claims relative to premiums collected

## Statistical Tests

The analysis uses appropriate statistical tests based on data characteristics:

- **Chi-square test**: For categorical frequency differences (claim frequency)
- **t-test**: For continuous mean differences (when data is normally distributed)
- **Mann-Whitney U test**: Non-parametric alternative for continuous data (when data is not normal)

### Significance Level
- **α = 0.05**: Standard significance level
- **p < 0.05**: Reject null hypothesis (significant difference)
- **p ≥ 0.05**: Fail to reject null hypothesis (no significant difference)

## Project Structure

```
src/analysis/task3/
├── __init__.py              # Module exports
├── metrics.py               # Metric computation (Claim Frequency, Severity, Margin)
├── segmentation.py         # A/B group creation
├── statistical_tests.py     # Hypothesis testing functions
├── hypothesis_testing.py    # Main testing runner
├── visualizations.py        # Visualization generation
└── reporting.py            # Report generation
```

## Usage

### Running the Analysis

```bash
# From project root
python scripts/run_task3.py
```

### Programmatic Usage

```python
from src.analysis.task3 import HypothesisTestingRunner

# Initialize runner
runner = HypothesisTestingRunner()

# Run all tests
results = runner.run_all_tests()

# Save results
runner.save_results(results)
```

### Individual Components

```python
from src.analysis.task3 import (
    MetricCalculator,
    DataSegmentation,
    StatisticalTester,
)

# Calculate metrics
calculator = MetricCalculator()
claim_freq = calculator.calculate_claim_frequency(df)

# Create groups
segmentation = DataSegmentation()
group_a, group_b, info = segmentation.create_province_groups(df)

# Perform tests
tester = StatisticalTester()
result = tester.test_difference(group_a, group_b, metric_type="continuous")
```

## Output Files

After running the analysis, the following files are generated:

### Results
- `results/task3_results.json`: Complete test results in JSON format
- `results/reports/task3_results_table.csv`: Summary table in CSV format

### Reports
- `results/reports/task3_statistical_report.md`: Comprehensive markdown report with:
  - Executive summary
  - Detailed test results for each hypothesis
  - P-values and statistical conclusions
  - Business interpretations

### Visualizations
- `results/figures/hypothesis_test_summary.png`: Summary visualization of all p-values

## Configuration

Configuration is managed in `config/config.yaml`:

```yaml
analysis:
  task3:
    enabled: true
    alpha: 0.05  # Significance level
    min_samples_province: 1000
    min_samples_zipcode: 500
    min_samples_gender: 1000
```

## Data Requirements

The analysis requires the following columns in the dataset:

- `Province`: Province name
- `PostalCode`: Zip/Postal code
- `Gender`: Gender (Male, Female, etc.)
- `TotalPremium`: Total premium amount
- `TotalClaims`: Total claims amount

## Reproducibility

All analysis is fully reproducible:

1. **Random Seed**: Fixed random seed (42) for sampling operations
2. **Version Control**: Code is version-controlled in Git
3. **Data Versioning**: Data is version-controlled with DVC
4. **Configuration**: All parameters are in config files

## Business Interpretations

When a null hypothesis is rejected (p < 0.05), the report includes business interpretations such as:

- **Geographic Segmentation**: Recommendations for province or zip code-based pricing adjustments
- **Risk Assessment**: Implications for risk segmentation strategies
- **Profitability**: Insights on margin differences and pricing strategies
- **Regulatory Compliance**: Notes on gender-based pricing restrictions

## Example Interpretation

> "We reject H₀ for claim frequency across provinces (p < 0.01). Gauteng shows 15% higher loss ratio than Western Cape → consider regional premium adjustments."

## Dependencies

Additional dependencies required for Task 3:

- `scipy>=1.10.0`: Statistical testing functions
- `matplotlib>=3.7.0`: Visualization
- `seaborn>=0.12.0`: Enhanced visualizations

## Testing

To verify the implementation:

```bash
# Run unit tests (if available)
pytest tests/unit/test_task3.py

# Run the analysis
python scripts/run_task3.py

# Check output files
ls results/reports/
ls results/figures/
```

## Troubleshooting

### Insufficient Sample Size

If you see warnings about insufficient sample sizes:

1. Reduce `min_samples_*` parameters in config
2. Check data quality and filtering
3. Consider combining categories if appropriate

### Memory Issues

For large datasets:

1. Process data in chunks
2. Use data sampling for initial exploration
3. Consider using processed/intermediate data files

## Next Steps

After completing Task 3:

1. Review the statistical report
2. Validate business interpretations with domain experts
3. Consider additional hypotheses based on findings
4. Integrate results into pricing and segmentation models

## References

- Statistical Testing: [SciPy Documentation](https://docs.scipy.org/doc/scipy/reference/stats.html)
- Hypothesis Testing: [Wikipedia - Statistical Hypothesis Testing](https://en.wikipedia.org/wiki/Statistical_hypothesis_testing)
- A/B Testing: [Wikipedia - A/B Testing](https://en.wikipedia.org/wiki/A/B_testing)

