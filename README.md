# Microsoft Graph Confidential Client Example
Creates a MS Graph Confidential Client and reads out some users as JSON.

## Create Configuration File
Setup the below and save as config.json

```
{
    "authority": "https://login.microsoftonline.com/{tenant-id}",
    "client_id": "app-client-id",
    "scope": ["https://graph.microsoft.com/.default"],
}

```

## Setup Secret

This example uses KeePass, change the function **get_client_secret** to do something differnt.

* Create KeePass DB and Secret Key
* Add Secret to KeePass, with title, GraphApiSecret