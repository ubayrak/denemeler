import requests
import json


def get_Autentication_Token() :
    max_retries = 3
    retries = 0
    url = f"{domain_url}/oauth/token"
    data = {
        'id': id,
        'password': password,
        'domainId': 'BOUYGUES',
        'grant_type': 'password'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    while retries < max_retries:
        try:
            response = requests.post(url, data=data, headers=headers)
            response.raise_for_status()  # Error handling
            token_data = response.json()
            access_token = token_data.get('access_token', None)
            if access_token:
                auth_token = access_token  # Store the access token in the "auth_token" variable
                return auth_token
            else:
                print("Access token could not be obtained.")
                return None
        except requests.exceptions.RequestException as e:
                retries += 1
                print(f"An error occurred: {e}")
                if retries < max_retries:
                    print(f"Retrying... (Attempt {retries}/{max_retries})")
    # If all retries fail, return None
    print(f"Unable to obtain authentication token after {max_retries} attempts.")
    return None


def get_Stations(serial_no) :
    serial_no = serial_no.replace('"', '')
    auth_token = get_Autentication_Token()
 
    url = f'{domain_url}/acapi/v3/stats/homes/{serial_no}/stations'
 
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }
 
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        formatted_json = json.dumps(response.json(), indent=4, ensure_ascii=False)
        print(f"------------------\n---Response Data---\nurl:{url}\n------------------\n{formatted_json}\n------------------\n")
        return response.json()
    else:
        # İstek başarısız oldu
        print('Error:', response.status_code, response.text)
 
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()  # Error handling
        token_data = response.json()
        if response.status_code == 200:
            return token_data
        else:
            print("Access token could not be obtained.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
    
    
# Example usage
domain_url = "https://secapi-uc-stg.bouygues.airtiescloud.eu"
id = "52b81fd9-51f3-4697-889a-50a0d932735d"
password = "d6C9mZSGmeqgwqwEX1d1OHM4OVRJGvOU"
serial_no = "172201450101197"

print(get_Autentication_Token())
# get_Stations(serial_no)

