import requests
import pandas as pd
from pathlib import Path


# Delhi coordinates
LATITUDE = 28.6139
LONGITUDE = 77.2090

# Open-Meteo Air Quality API
URL = "https://air-quality-api.open-meteo.com/v1/air-quality"


def fetch_historical_air_quality(start_date, end_date):
    """
    Fetch historical hourly air-quality data for Delhi
    from Open-Meteo.
    """

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "pm2_5",
            "pm10",
            "carbon_monoxide",
            "nitrogen_dioxide",
            "sulphur_dioxide",
            "ozone"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(
        URL,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    air_quality = pd.DataFrame(data["hourly"])

    air_quality["time"] = pd.to_datetime(
        air_quality["time"]
    )

    return air_quality


def save_raw_data(df):
    """
    Save raw air-quality data to data/raw/.
    """

    output_path = Path(
        "data/raw/air_quality_delhi.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(f"Data saved to: {output_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":

    START_DATE = "2025-01-01"
    END_DATE = "2025-12-31"

    air_quality_data = fetch_historical_air_quality(
        START_DATE,
        END_DATE
    )

    print("\nDataset preview:")
    print(air_quality_data.head())

    print("\nDataset information:")
    print(air_quality_data.info())

    save_raw_data(air_quality_data)