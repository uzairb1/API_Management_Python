import pandas as pd
import requests
import time

def read_faker_api(quantity, max_retries=5):
    """
    Fetches data from the Faker API with a specified quantity and includes a retry mechanism.

    Parameters:
    - quantity: int - The number of persons to fetch from the Faker API.
    - max_retries: int - Maximum number of retries for API calls.

    Returns:
    - pd.DataFrame - DataFrame containing the fetched data.
    """
    url = f"https://fakerapi.it/api/v2/persons?_quantity={quantity}&_birthday_start=1900-01-01"
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            if response.status_code == 200 and response.json()['status'] == "OK" and response.json()['total'] == quantity:
                return pd.json_normalize(response.json()['data'])
            else:
                print(f"Error in fetching data from Faker API: Status code {response.status_code}, Status: {response.json().get('status')}, Count:{response.json()['total']}")
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed with error: {e} \n check api url")
        
        # Exponential backoff
        time.sleep(2 ** attempt)
    
    raise Exception(f"Failed to fetch data from Faker API after {max_retries} attempts.")