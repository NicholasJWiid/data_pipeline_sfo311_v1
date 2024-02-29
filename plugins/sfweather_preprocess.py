# Preprocess weather data


def raw_weather_preprocess(df):
    import os

    raw_weather_data = df

    kelvin_to_fahrenheit = lambda K: (K - 273.15) * 9 / 5 + 32
    for column in raw_weather_data.columns:
        if 'temperature' in column:
            raw_weather_data[column] = round(kelvin_to_fahrenheit(raw_weather_data[column]), 0)

    return raw_weather_data




