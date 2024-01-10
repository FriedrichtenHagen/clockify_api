import requests
from dotenv import load_dotenv
import os
from pprint import pprint

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

params = {
    "page": 1,
    "pageSize": 200,
    "sharedReportsFilter": "CREATED_BY_ME",
}

try:
    response = requests.get(url, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Request successful")
        pprint(response.json())  # Assuming the response is in JSON format
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(response.text)  # Print the response content for debugging
except Exception as e:
    print(f"An error occurred: {e}")