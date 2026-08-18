import requests
import pandas as pd
from pathlib import Path


# Delhi coordinates
LATITUDE = 28.6139
LONGITUDE = 77.2090

# Open-Meteo historical weather API
URL = "https://archive-api.open-meteo.com/v1/archive"


def fetch_historical_weather(start_date, end_date):
    """
    Fetch historical hourly weather data for Delhi
    from Open-Meteo.
    """

    params = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "cloud_cover",
            "wind_speed_10m",
            "wind_gusts_10m"
        ],
        "timezone": "Asia/Kolkata"
    }

    response = requests.get(URL, params=params, timeout=30)

    response.raise_for_status()

    data = response.json()

    weather = pd.DataFrame(data["hourly"])

    weather["time"] = pd.to_datetime(weather["time"])

    return weather


def save_raw_data(df):
    """
    Save raw weather data to data/raw/.
    """

    output_path = Path("data/raw/weather_delhi.csv")

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_path, index=False)

    print(f"Data saved to: {output_path}")
    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")


if __name__ == "__main__":

    START_DATE = "2025-01-01"
    END_DATE = "2025-12-31"

    weather_data = fetch_historical_weather(
        START_DATE,
        END_DATE
    )

    print("\nDataset preview:")
    print(weather_data.head())

    print("\nDataset information:")
    print(weather_data.info())

    save_raw_data(weather_data)