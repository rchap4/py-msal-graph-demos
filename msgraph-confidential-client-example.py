##
## Copyright RChapman 2021
## This file is part of python-graph-client.
## python-graph-client is free software: you can redistribute it and/or modify
## it under the terms of the Affero GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version
## python-graph-client is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## Affero GNU General Public License for more details
## You should have received a copy of the Affero GNU General Public License
## along with python-graph-client.  If not, see <https://www.gnu.org/licenses/>.
##

import json
import logging
import requests
from requests.models import Response
import msal
import argparse
from typing import Dict, List
from pykeepass import PyKeePass

# Stolen from Microsoft Python msal examples
def setup_graph_confidential_client(client_id: str,
                                    secret: str,
                                    authority: str,
                                    scope: str) ->Dict[str, str]:

    # Create a preferably long-lived app instance which maintains a token cache.
    app = msal.ConfidentialClientApplication(
        client_id= client_id, authority=authority,
        client_credential=secret,
        # token_cache=...  # Default cache is in memory only.
                        # You can learn how to use SerializableTokenCache from
                        # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
        )

    # The pattern to acquire a token looks like this.
    result: str = None

    # Firstly, looks up a token from cache
    # Since we are looking for token for the current app, NOT for an end user,
    # notice we give account parameter as None.
    result = app.acquire_token_silent(scope, account=None)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
        result = app.acquire_token_for_client(scope)

    return result

# Get all users in Default  Directory
def query_user_endpoint(token: str):
    endpoint: str = "https://graph.microsoft.com/v1.0/users"

    graph_data: Response = requests.get(  # Use token to call downstream service
        endpoint,
        headers={'Authorization': 'Bearer ' + token}, ).json()
    print("Graph API call result: ")
    print(json.dumps(graph_data, indent=2))

# This won't work in a personal tenent as there are no mail enabled accounts
def send_message(token: str):
    message_json = """{
        "message": {
            "subject": "Test message",
            "body": {
            "contentType": "Text",
            "content": "Hello from Python"
            },
            "toRecipients": [
            {
                "emailAddress": {
                "address": ""
                }
            }
            ],
            "ccRecipients": [
            {
                "emailAddress": {
                "address": ""
                }
            }
            ]
        },
        "saveToSentItems": "false"
        }"""
    user_id: str = None
    endpoint: str = 'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail'.format(user_id)
    
    headers: Dict[str, str] = {'Authorization': 'Bearer ' + token,
                'Content-type': 'application/json'}
    mail_results: Response = requests.post(endpoint,
                                headers= headers,
                                data= message_json)

    print("Send resutls {}".format(mail_results.status_code))
    print(mail_results.text)

# Setup CLI args and return the object
def setup_arg_parser() -> argparse.ArgumentParser:
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument('--config', type= str, required= True)
    parser.add_argument('--logging', type= bool, required= False)
    parser.add_argument('--secretsdb', type= str, required= True)
    parser.add_argument('--secretdbkey', type= str, required= True)
    return parser.parse_args();

# This could be used with any secret engine, KeePass demostrated
def get_client_secret(path_to_db: str, path_to_key: str, secret_name: str) -> str:
    kee_pass: PyKeePass = PyKeePass(path_to_db, keyfile= path_to_key)
    entry: List[str] = kee_pass.find_entries(title= secret_name, first= True)
    return entry.password


def main() -> int:
    
    parsed_args: argparse.ArgumentParser = setup_arg_parser()
    if parsed_args.logging:
        logging.basicConfig(level=logging.DEBUG)

    config: Dict[str, str] = json.load(open(parsed_args.config))
    secret: str = get_client_secret(parsed_args.secretsdb, parsed_args.secretdbkey, 'GraphApiSecret')

    if not config:
        exit("Invalid config {}".format(parsed_args.config))
    
    client_results = setup_graph_confidential_client(config["client_id"],
                                                    secret,
                                                    config["authority"],
                                                    config["scope"])
    if "access_token" in client_results:
        # Calling graph using the access token, gets all users
        query_user_endpoint(client_results["access_token"])
        
        # This call will fail in a personal tenant with no mail
        # enabled accounts.
        ## send_message(client_results["access_token"])
    else:
        print(client_results.get("error"))
        print(client_results.get("error_description"))
        print(client_results.get("correlation_id"))  # You may need this when reporting a bug

    return 0


if __name__ == "__main__":
    main()