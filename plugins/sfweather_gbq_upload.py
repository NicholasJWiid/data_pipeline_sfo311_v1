# Upload DataFrame to Google BigQuery


def upload_weather_gbq(df):
    import pandas_gbq
    import os
    
    GBQ_credentials = os.environ.get("GBQ_CREDENTIALS")
    
    sf_weather_data = df
    pandas_gbq.to_gbq(
        sf_weather_data,
        'SF_311_project_data.sf_weather_data_test',
        project_id='portfolio-projects-2023-405100',
        if_exists='replace',
        credentials=GBQ_credentials
    )


