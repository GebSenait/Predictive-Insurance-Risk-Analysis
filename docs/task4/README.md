# Task 4: Predictive Modeling for Risk-Based Pricing and Severity Estimation

## Overview

Task 4 implements predictive models to support ACIS's dynamic, risk-based pricing system. The analysis focuses on three key modeling tasks:

1. **Claim Severity Model**: Predicts claim amounts for policies where claims occurred
2. **Premium Optimization Model**: Predicts appropriate premium levels using machine learning
3. **Claim Probability Model**: Estimates the probability of claims occurring (supports risk-based premium formula)

## Objectives

- Build production-ready predictive models for insurance risk assessment
- Compare multiple machine learning algorithms (Linear, Decision Tree, Random Forest, Gradient Boosting, XGBoost)
- Evaluate models using appropriate metrics (RMSE, R² for regression; Accuracy, Precision, Recall, F1 for classification)
- Provide model interpretability using SHAP and LIME
- Generate comprehensive reports with business implications

## Models

### 1. Claim Severity Model (Regression)

**Objective**: Predict claim amounts for policies where claims occurred.

**Target Variable**: `TotalClaims` (filtered to policies with claims > 0)

**Metrics**:
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

**Algorithms**:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor

**Use Case**: Supports reserve setting and pricing strategies by estimating expected claim amounts.

### 2. Premium Optimization Model (Regression)

**Objective**: Predict appropriate premium levels based on policy characteristics.

**Target Variable**: `TotalPremium`

**Metrics**:
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

**Algorithms**:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor
- XGBoost Regressor

**Use Case**: Supports dynamic pricing by identifying appropriate premium levels for different risk segments.

### 3. Claim Probability Model (Classification)

**Objective**: Estimate the probability of claims occurring.

**Target Variable**: Binary indicator (1 if `TotalClaims` > 0, 0 otherwise)

**Metrics**:
- Accuracy
- Precision
- Recall
- F1 Score

**Algorithms**:
- Logistic Regression
- Decision Tree Classifier
- Random Forest Classifier
- Gradient Boosting Classifier
- XGBoost Classifier

**Use Case**: Supports risk-based premium formula:
```
Premium = P(Claim) × Predicted Severity + Expense Loading + Profit Margin
```

## Data Preparation

The data preparation pipeline includes:

1. **Missing Value Handling**: Uses median/mean for numeric, mode for categorical
2. **Feature Engineering**:
   - Claim indicator (HasClaim)
   - Loss ratio (TotalClaims / TotalPremium)
   - Claim severity (for policies with claims)
   - Profit margin (TotalPremium - TotalClaims)
   - Age groups (if Age column exists)
   - Postal code prefixes (if PostalCode exists)
3. **Categorical Encoding**: One-hot encoding or label encoding
4. **Train-Test Split**: 70:30 or 80:20 (configurable)
5. **Feature Scaling**: StandardScaler for numeric features (optional)

## Model Training

All models are trained with:
- Fixed random seed (42) for reproducibility
- Configurable hyperparameters via `config/config.yaml`
- Cross-validation ready (can be extended)

## Model Evaluation

### Regression Metrics

- **RMSE**: Lower is better, measures prediction error in target units
- **R²**: Higher is better (0-1), measures proportion of variance explained

### Classification Metrics

- **Accuracy**: Proportion of correct predictions
- **Precision**: Proportion of positive predictions that are correct
- **Recall**: Proportion of actual positives correctly identified
- **F1 Score**: Harmonic mean of precision and recall

## Model Interpretability

### SHAP (SHapley Additive exPlanations)

- Identifies feature importance using game theory
- Provides local and global explanations
- Works with tree-based and linear models

### LIME (Local Interpretable Model-agnostic Explanations)

- Explains individual predictions
- Model-agnostic approach
- Provides feature importance for specific instances

### Top Features Analysis

For each model, the analysis identifies:
- Top 5-10 most influential features
- Combined importance scores (SHAP + LIME)
- Business interpretations for each key feature

## Usage

### Running the Analysis

```bash
# Run complete Task 4 pipeline
python scripts/run_task4.py
```

### Configuration

Configuration is managed in `config/config.yaml`:

```yaml
analysis:
  task4:
    enabled: true
    random_state: 42
    test_size: 0.3
    n_estimators: 100
    max_depth: 10
    learning_rate: 0.1
```

### Programmatic Usage

```python
from src.analysis.task4.task4_runner import Task4Runner

# Initialize runner
runner = Task4Runner()

# Run all analyses
results = runner.run_all()

# Access results
severity_results = results["severity"]
premium_results = results["premium"]
claim_prob_results = results["claim_probability"]
interpretability = results["interpretability"]
```

## Output Files

### Results

- `results/task4/task4_results.json`: Complete model results with metrics
- `results/task4/task4_top_features.json`: Top features from interpretability analysis

### Reports

- `results/reports/task4_modeling_report.md`: Comprehensive markdown report with:
  - Executive summary
  - Model comparison tables
  - Best model identification
  - Top influential features
  - Business implications and recommendations

- `results/reports/task4_model_comparison.csv`: Model comparison table in CSV format

## Reproducibility

All analysis is fully reproducible:

1. **Random Seed**: Fixed random seed (42) for all random operations
2. **Version Control**: Code is version-controlled in Git
3. **Data Versioning**: Data is version-controlled with DVC
4. **Configuration**: All parameters are in config files
5. **Dependencies**: All dependencies are specified in `requirements/base.txt`

## Business Implications

### Key Insights

1. **Claim Severity Prediction**: Enables accurate reserve setting and pricing strategies
2. **Premium Optimization**: Supports dynamic, risk-based pricing
3. **Claim Probability**: Enables risk-based premium formula implementation

### Recommendations

1. Implement best-performing models in production
2. Monitor model performance regularly and retrain as new data becomes available
3. Use interpretability insights to understand key risk drivers
4. Ensure regulatory compliance when using demographic/geographic features

## Dependencies

Additional dependencies required for Task 4:

- `xgboost>=2.0.0`: Gradient boosting framework
- `shap>=0.42.0`: Model interpretability
- `lime>=0.2.0`: Local interpretability

Install with:
```bash
pip install -r requirements/base.txt
```

## Model Selection

The best model for each task is selected based on:
- **Severity/Premium Models**: Highest test R²
- **Claim Probability Model**: Highest test F1 score

Alternative metrics can be used by modifying the `get_best_model()` method in `src/analysis/task4/models.py`.

## Extending the Analysis

### Adding New Models

To add a new model algorithm:

1. Add training method to `ModelTrainer` class in `src/analysis/task4/models.py`
2. Include in `train_all_regression_models()` or `train_all_classification_models()`
3. Update configuration if needed

### Custom Feature Engineering

Modify `engineer_features()` method in `src/analysis/task4/data_preparation.py` to add domain-specific features.

### Custom Metrics

Add evaluation metrics in the model training methods in `src/analysis/task4/models.py`.

## Troubleshooting

### XGBoost Not Available

If XGBoost is not installed, the pipeline will skip XGBoost models and continue with other algorithms.

### SHAP/LIME Not Available

If SHAP or LIME are not installed, interpretability analysis will skip unavailable methods but continue with available ones.

### Memory Issues

For large datasets:
- Reduce `max_samples` in SHAP analysis
- Use smaller `n_estimators` for ensemble models
- Process data in batches

## References

- [Scikit-learn Documentation](https://scikit-learn.org/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [LIME Documentation](https://github.com/marcotcr/lime)

