# Architecture Documentation

## System Overview

The Parking Availability Forecasting System is designed as a complete MLOps pipeline that automates the entire lifecycle of a machine learning model: from data collection to model training and artifact storage.

## Components

### 1. Data Extraction Layer

**Location**: `scripts/extract_data.py`

This component interfaces with the Donostia municipal API to fetch real-time parking availability data. The script:
- Makes HTTP requests to the city's parking API
- Normalizes JSON responses into tabular format
- Appends timestamped records to the historical dataset
- Handles errors gracefully with retry logic

**Execution**: Triggered hourly via GitHub Actions (see Automation Layer)

### 2. Data Storage

**Location**: `data/data.csv`

A simple CSV file serves as the data lake for this project. While not scalable for production systems, it's appropriate for this use case because:
- Data volume is low (~24 records per parking lot per day)
- GitHub provides version control for the dataset
- No complex query requirements
- Easy to inspect and debug

**Schema**:
- `properties.nombre`: Parking facility name
- `properties.libres`: Number of available spaces
- `timestamp`: Data collection timestamp

### 3. Model Training Pipeline

**Location**: `src/train.py`

The training pipeline follows these steps:

1. **Data Loading**: Reads historical CSV and filters for target parking lot
2. **Train-Test Split**: Creates time-based splits (last 48 hours for testing)
3. **Feature Engineering**: Uses autoregressive lags as features (previous 24-72 hours)
4. **Hyperparameter Tuning**: Grid search over:
   - Random Forest parameters (n_estimators, max_depth)
   - Lag configurations (how many historical hours to use)
5. **Model Training**: Trains best model on full training set
6. **Artifact Saving**: Serializes model and training metadata

**Key Design Decisions**:
- **ForecasterAutoreg**: Specialized for time series forecasting with lagged features
- **Random Forest**: Handles non-linear patterns and interactions between lag features
- **Grid Search**: Ensures optimal hyperparameters for each parking lot

### 4. Configuration Management

**Location**: `src/config.py`, `config/.env.example`

Centralized configuration provides:
- Easy hyperparameter tuning without code changes
- Environment-specific settings (dev/prod)
- Path management for data and models
- Default values with environment variable overrides

### 5. Automation Layer

**Location**: `.github/workflows/update_data.yml`

GitHub Actions orchestrates the data collection pipeline:
- **Schedule**: Runs every hour using cron syntax
- **Environment**: Ubuntu runner with Python 3.9
- **Authentication**: Uses GitHub token for repository write access
- **Error Handling**: Only commits if new data is different from previous

## Data Flow

```
1. GitHub Actions Trigger (hourly)
   ↓
2. Environment Setup (Python, dependencies)
   ↓
3. Execute extract_data.py
   ↓
4. Fetch API data → Append to data.csv
   ↓
5. Git commit & push (if changes detected)
   ↓
6. Repository updated with new data
```

```
7. Manual trigger of train.py (or could be automated)
   ↓
8. Load historical data.csv
   ↓
9. Grid search for optimal parameters
   ↓
10. Train final model
    ↓
11. Save model.pickle + metadata
```

## Scalability Considerations

**Current Limitations**:
- CSV storage won't scale beyond ~1M rows
- GitHub Actions has 2,000 minutes/month free tier limit
- No model deployment/serving infrastructure
- Manual model retraining

**Production Enhancements**:
- **Storage**: Migrate to TimescaleDB or InfluxDB for time series data
- **Orchestration**: Use Airflow or Prefect for complex DAGs
- **Model Registry**: MLflow or Neptune for versioning and experiment tracking
- **Deployment**: Containerize with Docker, serve via FastAPI + Kubernetes
- **Monitoring**: Track data drift and model performance degradation

## Technology Choices

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Data Extraction | Python + Requests | Simple, reliable HTTP client |
| Data Processing | Pandas | Industry standard for tabular data |
| Model Training | scikit-learn + skforecast | Proven algorithms, time series specialization |
| Orchestration | GitHub Actions | Free, integrated with Git, sufficient for hourly jobs |
| Serialization | Pickle | Native Python, preserves model state exactly |

## Future Enhancements

1. **Real-time Predictions**: Deploy model as REST API
2. **Multi-parking Support**: Train separate models for each facility
3. **Feature Engineering**: Add weather data, events calendar, holidays
4. **Model Comparison**: Test ARIMA, Prophet, LSTM models
5. **Monitoring Dashboard**: Visualize predictions vs actuals
6. **Alerting**: Notify when model performance degrades
