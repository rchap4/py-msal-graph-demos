# Microsoft Graph Client Demos
Creates an MS Graph Confidential Client and reads users as JSON.

## Create an AppRegistration in AzureAD
Create the needed AppRegistration in your AzureAD tenant, the specific steps are left as an exercise for the reader. 

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

This example uses KeePass, change the function **get_client_secret** to do something different.

* Create KeePass DB and Secret Key
* Add Secret to KeePass, with title, GraphApiSecret

## Run Example
Shell script also for convenience.
```
python msgraph-confidential-client-example.py \
    --config config.json \
    --secretsdb ../GraphSecrets.kdbx \
    --secretdbkey ../GraphSecrets.keyx 

```

## TODO
* Add some exception handling