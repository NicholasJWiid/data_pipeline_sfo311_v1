

def sf_weatherdata_pull(endpoint, api_key_id, days_past=1):
    """ Pulls weather data from the Open Weather Map API using the One Call subscription.

    Note:
         Function built specifically for the subscription option: Each day is a single API call.

    Args:
        endpoint: Open Weather Map end point for the One Call subscription plan
        api_key_id: Open Weather Map API key
        days_past: Number of days of historical data desired.
            E.g. 365 for the last year of data to present day.
    Returns:
        DataFrame: Flattened DataFrame with weather data for historical period selected.
            Includes 4 days worth of forecast data.
    """
    # Import modules
    import requests
    import pandas as pd
    from datetime import datetime, timedelta

    # Outline parameters needed for API
    parameters = {
                "lat": 37.774929,
                "lon": -122.419415,
                "date": {},
                "appid": api_key_id,
            }

    # Setting up the days past argument operations, including 4 days for forecast data
    end_date = datetime.now() + timedelta(days=5)
    start_date = datetime.now() - timedelta(days=days_past)
    date_format = "%Y-%m-%d"
    all_weather_data = []
    current_date = start_date

    try:
        while current_date <= end_date:
            # Convert the current date to the required format
            formatted_date = current_date.strftime(date_format)
            parameters["date"] = formatted_date

            response = requests.get(url=endpoint, params=parameters)
            response.raise_for_status()
            single_day_data = response.json()
            all_weather_data.append(single_day_data)
            current_date += timedelta(days=1)

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        print(f"Response text: {response.text}")

    except requests.exceptions.RequestException as err:
        print(f"An unexpected error occurred: {err}")

    # Convert json weather data into a Pandas DataFrame and flatten
    all_weather_df = pd.json_normalize(all_weather_data)

    # Rename columns to meet BigQuery formatting requirements
    all_weather_df.columns = [col.replace('.', '_') for col in all_weather_df.columns]

    return all_weather_df
