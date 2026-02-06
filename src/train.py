"""Train a forecasting model to predict parking availability."""

import pandas as pd
import pickle
from pathlib import Path
from skforecast.ForecasterAutoreg import ForecasterAutoreg
from sklearn.ensemble import RandomForestRegressor
from skforecast.model_selection import grid_search_forecaster

from config import (
    DATA_PATH, MODEL_PATH, LAST_TRAINING_DATE_PATH,
    PARKING_NAME, PREDICTION_STEPS, LAGS, 
    PARAM_GRID, LAGS_GRID, GRID_SEARCH_STEPS,
    METRIC, INITIAL_TRAIN_SIZE_RATIO, RANDOM_STATE
)


def load_and_prepare_data(data_path: Path, parking_name: str) -> pd.DataFrame:
    """
    Load parking data and filter for specific parking lot.
    
    Args:
        data_path: Path to the CSV data file
        parking_name: Name of the parking lot to filter
        
    Returns:
        DataFrame with timestamp and available spaces columns
    """
    data = pd.read_csv(data_path)
    data = data.loc[
        data['properties.nombre'] == parking_name,
        ['properties.libres', 'timestamp']
    ]
    return data.reset_index(drop=True)


def split_train_test(data: pd.DataFrame, n_steps: int) -> tuple:
    """
    Split data into training and test sets.
    
    Args:
        data: Input DataFrame with parking availability data
        n_steps: Number of steps to use for test set
        
    Returns:
        Tuple of (train_series, test_series)
    """
    data_train = data[:-n_steps]['properties.libres']
    data_test = data[-n_steps:]['properties.libres']
    return data_train, data_test


def train_forecaster(data_train: pd.Series) -> ForecasterAutoreg:
    """
    Train forecasting model with grid search optimization.
    
    Args:
        data_train: Training time series data
        
    Returns:
        Trained ForecasterAutoreg model with optimal parameters
    """
    forecaster = ForecasterAutoreg(
        regressor=RandomForestRegressor(random_state=RANDOM_STATE),
        lags=LAGS
    )
    
    initial_train_size = int(len(data_train) * INITIAL_TRAIN_SIZE_RATIO)
    
    grid_search_forecaster(
        forecaster=forecaster,
        y=data_train,
        param_grid=PARAM_GRID,
        lags_grid=LAGS_GRID,
        steps=GRID_SEARCH_STEPS,
        metric=METRIC,
        initial_train_size=initial_train_size,
        return_best=True,
        verbose=False
    )
    
    return forecaster


def save_model_artifacts(
    forecaster: ForecasterAutoreg,
    last_training_timestamp: str,
    model_path: Path,
    timestamp_path: Path
) -> None:
    """
    Save trained model and metadata to disk.
    
    Args:
        forecaster: Trained forecasting model
        last_training_timestamp: Timestamp of last training data point
        model_path: Path to save the model
        timestamp_path: Path to save the training timestamp
    """
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(timestamp_path, 'wb') as f:
        pickle.dump(last_training_timestamp, f)
    
    with open(model_path, 'wb') as f:
        pickle.dump(forecaster, f)


def main():
    """Main training pipeline execution."""
    print(f"Loading data from {DATA_PATH}...")
    data = load_and_prepare_data(DATA_PATH, PARKING_NAME)
    
    print(f"Splitting data (test size: {PREDICTION_STEPS} steps)...")
    data_train, data_test = split_train_test(data, PREDICTION_STEPS)
    
    print("Training forecaster with grid search...")
    forecaster = train_forecaster(data_train)
    
    last_training_date = data[:-PREDICTION_STEPS]['timestamp'].values[-1]
    
    print(f"Saving model to {MODEL_PATH}...")
    save_model_artifacts(
        forecaster,
        last_training_date,
        MODEL_PATH,
        LAST_TRAINING_DATE_PATH
    )
    
    print("Training completed successfully!")


if __name__ == "__main__":
    main()
