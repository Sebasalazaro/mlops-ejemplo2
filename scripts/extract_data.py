"""Extract parking availability data from Donostia API and store locally."""

import os
import pandas as pd
import requests
from datetime import datetime
from pathlib import Path


# Configuration
API_URL = 'https://www.donostia.eus/info/ciudadano/camaras_trafico.nsf/getParkings.xsp'
OUTPUT_DIR = 'data'
OUTPUT_FILENAME = 'data.csv'
IMPORTANT_COLUMNS = ['properties.nombre', 'properties.libres']


def fetch_parking_data(api_url: str) -> pd.DataFrame:
    """
    Fetch current parking availability from Donostia API.
    
    Args:
        api_url: URL of the parking data API endpoint
        
    Returns:
        DataFrame containing parking names and available spaces
        
    Raises:
        requests.RequestException: If API request fails
    """
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        
        data = pd.json_normalize(response.json()['features'])
        data = data.loc[:, IMPORTANT_COLUMNS]
        data['timestamp'] = pd.Timestamp.now()
        
        return data
    
    except requests.RequestException as e:
        print(f"Error fetching parking data: {e}")
        raise


def save_parking_data(data: pd.DataFrame, output_dir: str, filename: str) -> None:
    """
    Save parking data to CSV, appending to existing file if present.
    
    Args:
        data: DataFrame with parking availability data
        output_dir: Directory to save the CSV file
        filename: Name of the output CSV file
    """
    # Ensure we're in the project root directory
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    file_path = output_path / filename
    
    if file_path.exists():
        existing_data = pd.read_csv(file_path)
        final_data = pd.concat([existing_data, data], ignore_index=True)
    else:
        final_data = data.copy()
    
    final_data.to_csv(file_path, index=False)
    print(f"Data saved successfully: {len(data)} new records added")


def main():
    """Main execution: fetch and store parking data."""
    print(f"Fetching parking data from API... ({datetime.now()})")
    parking_data = fetch_parking_data(API_URL)
    
    print(f"Saving data to {OUTPUT_DIR}/{OUTPUT_FILENAME}...")
    save_parking_data(parking_data, OUTPUT_DIR, OUTPUT_FILENAME)
    
    print("Extraction completed successfully!")


if __name__ == "__main__":
    main()
