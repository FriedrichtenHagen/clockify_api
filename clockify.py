import requests
from dotenv import load_dotenv
import os
from pprint import pprint
import pandas as pd
import json

# https://docs.clockify.me/#tag/Task

load_dotenv()
API_KEY = os.getenv('API_KEY')
USER_ID = os.getenv('USER_ID')
WORKSPACE_ID = os.getenv('WORKSPACE_ID')
# the shared report ID can be found in the url. https://app.clockify.me/shared/654g45283f84759g98rf93847
SHARED_REPORT_ID = os.getenv('SHARED_REPORT_ID')

url = f"https://reports.api.clockify.me/v1/shared-reports/{SHARED_REPORT_ID}"

headers = {
    "x-api-key": API_KEY,
    "Content-Type": "application/json", 
}
page_size = 200
start_params = {
    "page": 1,
    "pageSize": page_size,
}

def make_request(params, result_df):
    try:
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful")
            json_data = response.json()

            # extract page count needed for pagination
            entries_count = json_data.get("totals", [])[0].get("entriesCount")
            print(f'pages: {entries_count}')

            # Extracting values from each object in timeentries
            entries_data = []
            for entry in json_data.get("timeentries", []):
                entry_data = {
                    "created_at_local": (entry.get("timeInterval").get("start"))[:10],
                    "project_name": entry.get("projectName"),
                    "user_name": entry.get("userName"),
                    "duration_minutes": (entry.get("timeInterval").get("duration"))/60,
                    "billing_amount_euro": entry.get("amount"),
                }
                entries_data.append(entry_data)

            df = pd.DataFrame(entries_data)
            # add page results of this request to result df
            result_df = pd.concat([result_df, df], ignore_index=True)
            return result_df

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)  # Print the response content for debugging
    except Exception as e:
        print(f"An error occurred: {e}")


def paginate():
    # make initial request to get page count
    try:
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Request successful")
            json_data = response.json()

            # extract page count needed for pagination
            entries_count = json_data.get("totals", [])[0].get("entriesCount")
            print(f'pages: {entries_count}')

        else:
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)  # Print the response content for debugging
    except Exception as e:
        print(f"An error occurred: {e}")

    # result data frame
    result_df = pd.DataFrame()
    
    number_of_necessary_requests = (entries_count // page_size)+1
    # make request for all pages
    for page_index in range(number_of_necessary_requests):
        request_params = {
            "page": page_index,
            "pageSize": 200,
        }
        result_df = make_request(request_params, result_df)
    print(result_df.index)







# paginate()
# need to use more than 1 day
    # pagination
    # incremental import
        
# for testing
result_df = pd.DataFrame()
print(make_request(start_params, result_df))