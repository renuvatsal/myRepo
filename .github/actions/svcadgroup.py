import sys
import os
import yaml
import requests
import json
import argparse
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

COLOR_RED = "\u001b[31m"
COLOR_GREEN = "\u001b[32m"

# Fetchs env vars
def fetch_env(name):
    value = os.getenv(name)
    
    if value is None or value.strip() == '':
        raise EnvironmentError(f'Environment variable not found')
    else:
        return value

# Single template build urls with given env
def build_environment(env):
    env_suffix = f'{env}'
    auth_suffix = '' if env == 'prod' else f'-uat'
    auth_server_url = f'https://auth{auth_suffix}.domain/as/token.oauth2'
    
    environment_payload = {
        'serviceaccount_url': f'https://api-gtwy-{env_suffix}.domain/serviceAccount',
        'adgroup_url': f'https://api-gtwy-{env_suffix}.domain/adGroup',
        'groupassignment_url': f'https://api-gtwy-{env_suffix}.domain/assignADGroup',
        'auth_server_url': auth_server_url,
        'headers': {
            'Content-Type': 'application/json',
            'ESB-OAUTH': 'Bearer {}'.format(get_token(auth_server_url)),
            'PASSWORD': fetch_env('KEY'),
            'USERNAME': 'svc_custom_openshift',
            'Authorization': fetch_env('TOKEN'),
        }
    }
    logging.info(f'{COLOR_GREEN}Environment payload generated successfully')
    return environment_payload

# Fetches token only using auth server
def get_token(auth_server_url):
    token_req_payload = {'grant_type': 'client_credentials'}
    token_response = requests.post(auth_server_url,
                                   data=token_req_payload, verify=False, allow_redirects=False,
                                   auth=(fetch_env('CLIENT_ID'), fetch_env('CLIENT_SECRET')))
    if token_response.status_code == 200:
        logging.info(f'{COLOR_GREEN}Fetched token successfully, Status code: {token_response.status_code}')
        tokens = json.loads(token_response.text)
    else:
        raise ConnectionError(token_response.reason)
    return tokens['access_token']

# API call
def api_call(name, url, payload_list, headers):
    for item in payload_list:
        payload = json.dumps(item)

        # Trigger
        max_retries = 3
        retry_count = 0
        """
        request_details = f\"\"\"
        === {name.upper()} API Request (Attempt {retry_count + 1}/{max_retries}) ===
        URL: {url}
        Payload: {payload}
        Headers: {headers}
        \"\"\"
        print(request_details) # Use print for immediate output
        """
        try:
            request_details = f\"\"\"
            === {name.upper()} API Request (Attempt {retry_count + 1}/{max_retries}) ===
            URL: {url}
            Payload: {payload}
            Headers: {headers}
            \"\"\"
            print(request_details) # Use print for immediate output

            while retry_count < max_retries:
                response = requests.post(url, data=payload, headers=headers, timeout=60)
                logging.info(f"{name.upper()} Response (Attempt {retry_count + 1}/{max_retries}):")
                output = json.loads(response.text)

                error_code = error_msg = ''

                if 'errorList' and 'errorMessage' in response.text:
                    error_code = output["errorList"][0]["errorCode"]
                    error_msg = output["errorList"][0]["errorMessage"]
                    
                if response.status_code == 200 and output["status"] == 'SUCCESS':
                    logging.info(f'{COLOR_GREEN}Response: {output["message"]}')
                    break # Exit the retry loop on success
                else:
                    # For any non-200 status code, including 404, retry
                    if output["status"] == 'FAILED':
                        if error_code != '' and error_msg != '' and 'already exist' not in error_msg:
                            logging.warning(f'{COLOR_RED}Read API call response below')
                            logging.error(f'{COLOR_RED}ERROR CODE: {error_code}')
                            logging.error(f'{COLOR_RED}ERROR MESSAGE: {error_msg}\n')
                            retry_count += 1
                        elif 'already exist' in error_msg:
                            logging.info(f'{COLOR_GREEN}{error_msg}\n')
                            break
                        else:
                            logging.error(f'{COLOR_RED}Response: {output}\n')

            if retry_count < max_retries:
                logging.info(f"Waiting 60 seconds before retry {retry_count + 1}...")
                time.sleep(60) # Wait 1 minute before retry
            else:
                logging.error(f'{COLOR_RED}Max retries reached after all attempts for {name.upper()}')
                sys.exit(1)
        except requests.RequestException as e:
            raise requests.ConnectionError(f"{COLOR_RED}{name.upper()} error: {str(e)}")

# Prepare template for api call
def prepare_payload(adgroup_value, svc_value, appid_value, environment_payload, trigger, primary_owner, secondary_owner, users_list, env):
    
    group_domain = "CS" if env == 'prod' else "ZQ"
    serviceaccount_payload = [{
        "primaryOwner": primary_owner,
        "backupOwner": secondary_owner,
        "domain": group_domain,
        "serviceName": svc_value,
        "applicationId": appid_value,
        "description": "Prod SA for customerole1",
        "environment": "Prd" if env == 'prod' else f"NPrd",
        "rotationFrequency": "NoManage",
        "rotatePassword": "No"
    }]
    
    adgroup_payload = [{
        "applicationId": appid_value,
        "groupName": adgroup_value,
        "groupOwner": primary_owner,
        "groupDomain": group_domain,
        "approvalNeededByPO": "true",
        "backupOwner": secondary_owner,
        "requestable": "true",
        "containsNuids": "false",
        "elevated": "false",
        "risk": "LOW_RISK",
        "groupDescription": "An Active Directory group simplifies administration by allowing permissions to be assigned to the group rather than individual users"
    }]
    
    groupassignment_payload = [{
        "groupName": adgroup_value,
        "groupDomain": group_domain,
        "nuids": user
        }
        for user in users_list
    ]
    
    payloads = {
        "serviceaccount": serviceaccount_payload,
        "adgroup": adgroup_payload,
        "groupassignment": groupassignment_payload
    }

    
    headers = environment_payload['headers']
    
    links = dict(list(environment_payload.items())[:3])
    
    items = list(links.items())
    total = len(items)

    if trigger == 'all':
        
        for index, (name, link) in enumerate(links.items()):
            payload = name.split('_')[0]
            logging.info(f'Processing {payload.upper()} payload')
            payload_data = payloads.get(f'{payload}')
            api_call(payload.upper(), link, payload_data, headers)

            if index < total - 1:
                next_item = items[index + 1][0].split('_')[0]
                logging.info(f'Waiting 60 seconds before proceeding to next {next_item.upper()}')
                time.sleep(60)
            else:
                logging.info('All payloads processed.')
    else:
        if '&' in trigger:
            
            optional_trigger = trigger.split('&')

            for index, (name, link) in enumerate(links.items()):
                payload = name.split('_')[0]
                if payload in optional_trigger:
                    logging.info(f'Processing {payload.upper()} payload')
                    payload_data = payloads.get(f'{payload}')
                    api_call(payload.upper(), link, payload_data, headers)

                    if index < total - 1:
                        next_item = items[index + 1][0].split('_')[0]
                        if next_item in optional_trigger:
                            logging.info(f'Waiting 60 seconds before proceeding to next {next_item.upper()}')
                            time.sleep(60)
                    else:
                        logging.info('All payloads processed.')
        else:
            logging.info(f'Preparing payload for {trigger.upper()}')
            link = links.get(f'{trigger}_url')
            payload_data = payloads.get(f'{trigger}')
            api_call(trigger, link, payload_data, headers)
            
def process_yaml_file(filename, base_path):
    try:
        file_path = os.path.join(base_path, filename)
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        adgroup_value = data["accounts"]["adGroupDevNonProd"]
        svc_value = data["accounts"]["jenkinsSAnonprod"]
        primaryOwner = data["users"]["primaryOwner"]
        secondaryOwner = data["users"]["secondaryOwner"]
        userList = data["users"]["list"]

        # Input validation
        if userList != None:
            users_list = [item.strip() for item in userList.split(',') if item.strip()]
        else:
            users_list = userList

        if svc_value.upper().startswith('SVC'):
            svc_value = svc_value[3:]
        appid_value = data["application"]["atlasAppid"]

        adgroup_words = adgroup_value.split("_")
        if adgroup_words[0] != "Openshift":
            raise Exception("The first word of the AD group should be 'Openshift'")
        return adgroup_value, svc_value, appid_value, primaryOwner, secondaryOwner, users_list
    except FileNotFoundError:
        print("Values FileNotFoundError")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+', help='The namespace files')
    parser.add_argument('--environment', choices=['dev', 'QA', 'UAT', 'PROD'], required=True, help='The environment to use')
    parser.add_argument('--trigger', choices=['serviceaccount', 'adgroup', 'groupassignment', 'adgroup&groupassignment', 'all'], required=True, help='Specify which APIs to trigger')
    args = parser.parse_args()

    workspace = os.environ.get('GITHUB_WORKSPACE', os.getcwd())
    base_path = os.path.join(workspace, 'sampledetails')

    for values_file in args.files:
        adgroup_value, svc_value, appid_value, primary_owner, secondary_owner, users_list = process_yaml_file(values_file, base_path)

        if args.trigger in ['serviceaccount', 'adgroup', 'adgroup&groupassignment', 'all']:
            if primary_owner is None or secondary_owner is None:
                raise ValueError("Primary and Secondary Owner are required for selected trigger")

        if args.trigger in ['adgroup&groupassignment', 'all']:
            if users_list is None:
                raise ValueError("User list is required for selected trigger")

        environment_payload = build_environment(args.environment)
        prepare_payload(adgroup_value, svc_value, appid_value, environment_payload, args.trigger, primary_owner, secondary_owner, users_list, args.environment)

if __name__ == "__main__":
    main()
