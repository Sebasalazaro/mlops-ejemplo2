# Parking Availability Forecasting System

<div align="center">

An automated MLOps pipeline that predicts parking spot availability in Donostia, Spain using time series forecasting. The system continuously collects real-time parking data via GitHub Actions and trains machine learning models to predict availability up to 48 hours in advance.

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white) ![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white) ![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

</div>

## Overview

This project demonstrates a complete MLOps workflow for time series forecasting. It automatically extracts parking availability data from the Donostia municipal API every hour, stores historical records, and trains forecasting models using Random Forest regressors optimized through grid search.

The pipeline addresses a real-world problem: available parking spots aren't tracked historically by the city, making predictive modeling impossible without building a data collection system first.

**Key Features:**
- Automated data extraction with GitHub Actions (runs hourly)
- Time series forecasting using `skforecast` library
- Hyperparameter optimization via grid search
- Modular, production-ready code structure
- Comprehensive logging and error handling

## Architecture

```
┌─────────────────┐
│  Donostia API   │ ← Real-time parking data
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│  GitHub Actions     │ ← Runs every hour
│  (Data Extraction)  │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   data/data.csv     │ ← Historical dataset
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  Training Pipeline  │ ← Grid search + validation
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│  models/model.pkl   │ ← Trained forecaster
└─────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.9+
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/parking-forecasting-mlops.git
cd parking-forecasting-mlops

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config/.env.example .env
```

### Usage

**Extract Parking Data:**
```bash
python scripts/extract_data.py
```

**Train Forecasting Model:**
```bash
python src/train.py
```

**Automated Data Collection:**

The GitHub Actions workflow automatically runs `extract_data.py` every hour. To set up:

1. Create a GitHub Personal Access Token with `repo` permissions
2. Add it as a repository secret named `GH_TOKEN`
3. Update the repository URL in `.github/workflows/update_data.yml`

## Project Structure

```
parking-forecasting-mlops/
├── .github/
│   └── workflows/
│       └── update_data.yml      # Automated data extraction workflow
├── config/
│   └── .env.example             # Configuration template
├── data/
│   └── data.csv                 # Historical parking data
├── docs/
│   └── ARCHITECTURE.md          # Detailed architecture documentation
├── models/                      # Trained models directory
├── scripts/
│   ├── extract_data.py          # API data extraction script
│   └── update_data.sh           # Git push automation
├── src/
│   ├── __init__.py
│   ├── config.py                # Centralized configuration
│   └── train.py                 # Model training pipeline
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Configuration

Edit `.env` or set environment variables:

- `PARKING_NAME`: Target parking lot name (default: "Boulevard")
- `PREDICTION_STEPS`: Forecast horizon in hours (default: 48)

Model hyperparameters can be adjusted in [src/config.py](src/config.py).

## Model Details

- **Algorithm**: Random Forest Regressor with Autoregressive features
- **Framework**: skforecast (specialized for time series forecasting)
- **Optimization**: Grid search over lag configurations and RF hyperparameters
- **Validation**: Time-based train-test split with forward chaining

**Hyperparameters Tuned:**
- Number of estimators: [100, 500]
- Max depth: [3, 5, 10]
- Lag configurations: [24, 48, 72 hours]

## Data Source

Parking availability data is sourced from the Donostia City Council's open API:
- **Endpoint**: `https://www.donostia.eus/info/ciudadano/camaras_trafico.nsf/getParkings.xsp`
- **Update Frequency**: Real-time
- **Coverage**: All municipal parking facilities in Donostia/San Sebastián

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Sebastian Salazar**
- Email: ssalazaro1@eafit.edu.co
- GitHub: [@Sebasalazaro](https://github.com/Sebasalazaro)

---

*Developed as part of the Intensive Systems course at Universidad EAFIT (2025)*

- https://github.com/edwinm67/mlops-ejemplo2.git 

2.	Crear su propio repo ‘mlops-ejemplo2.git’ en su cuenta github y seguir trabajando en este para todos los cambios.

3.	Realizar los ajustes respectivos en su propio código, cada vez haga ‘git push’

4.	Revisar la ejecución de las acciones github

5.	Actualizar el repositorio local para verificar cambios en los datos y buen funcionamiento del crarler y automatización: 

    LOCAL: git pull

6.	documente todas las anteriores actividades

7.	entregar el lab



