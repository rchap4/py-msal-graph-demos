#!/bin/bash
python msgraph-confidential-client-example.py \
    --config config.json \
    --secretsdb ../GraphSecrets.kdbx \
    --secretdbkey ../GraphSecrets.keyx 
