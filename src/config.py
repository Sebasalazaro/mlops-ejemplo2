"""Configuration settings for the parking availability prediction model."""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "models"

# Data settings
DATA_PATH = DATA_DIR / "data.csv"
PARKING_NAME = os.getenv("PARKING_NAME", "Boulevard")

# Model settings
MODEL_PATH = MODELS_DIR / "model.pickle"
LAST_TRAINING_DATE_PATH = MODELS_DIR / "last_training_date.pickle"
PREDICTION_STEPS = int(os.getenv("PREDICTION_STEPS", "48"))

# Training parameters
LAGS = 12
TRAIN_TEST_SPLIT_STEPS = PREDICTION_STEPS
INITIAL_TRAIN_SIZE_RATIO = 0.9

# Model hyperparameters
PARAM_GRID = {
    'n_estimators': [100, 500],
    'max_depth': [3, 5, 10]
}

LAGS_GRID = [24, 48, 72]
GRID_SEARCH_STEPS = 10
METRIC = 'mean_squared_error'
RANDOM_STATE = 123
