import requests
from requests.auth import HTTPBasicAuth
import time
import json

# Replace with your Flowroute Access Key and Secret Key
ACCESS_KEY = '91df19f2'
SECRET_KEY = '8ed5405f9ea0427193c04d02e37f1c0f'

# The endpoint to create and check CDR exports
CDR_EXPORT_ENDPOINT = 'https://api.flowroute.com/v2/cdrs/exports'

# Function to create a new CDR export
def create_cdr_export(start_time, end_time):
    payload = {
        "data": {
            "type": "cdrexport",
            "attributes": {
                "filter_parameters": {
                    "start_call_start_time": start_time,
                    "start_call_end_time": end_time
                }
            }
        }
    }

    headers = {
        'Content-Type': 'application/vnd.api+json',
        'Accept': 'application/vnd.api+json'
    }

    response = requests.post(
        CDR_EXPORT_ENDPOINT,
        auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY),
        headers=headers,
        data=json.dumps(payload)  # Ensure payload is converted to JSON string
    )

    if response.status_code == 201:
        print("CDR Export request is successful.")
        return response.json()['data']['id']
    else:
        print(f"Failed to create CDR export: {response.status_code} {response.text}")
        return None

# Function to check the status of an export
def check_export_status(export_id):
    response = requests.get(
        f"{CDR_EXPORT_ENDPOINT}/{export_id}",
        auth=HTTPBasicAuth(ACCESS_KEY, SECRET_KEY)
    )
    if response.status_code == 200:
        return response.json()['data']['attributes']
    else:
        print(f"Failed to check CDR export status: {response.status_code} {response.text}")
        return None

# Main script execution
if __name__ == "__main__":
    # Adjust to your desired start and end date in the format "YYYY-MM-DD HH:MM:SS"
    start_date = '2023-10-01 00:00:00'  # Replace with the actual start date
    end_date = '2023-10-31 23:59:59'    # Replace with the actual end date

    # Step 1: Create a new CDR export
    export_id = create_cdr_export(start_date, end_date)

    if export_id:
        print(f"CDR export requested. Export ID: {export_id}")

        # Step 2: Poll for the export to be completed
        while True:
            export_status = check_export_status(export_id)
            if export_status and export_status['status'] == 'completed':
                print("CDR export is complete.")
                print(f"The total cost for the period is: {export_status['total_cost']}")
                break
            elif export_status and export_status['status'] == 'failed':
                print("CDR export failed.")
                break
            else:
                print("CDR export is still processing...")
                time.sleep(60)  # Poll every 60 seconds
