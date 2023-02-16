#!/bin/bash


# POLAND:

# localGroupUid
#   globalGroup1Uid
#     globalGroup1Ui2
#       hostUid


authBearer='Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2NjM4OTAzLCJpYXQiOjE2NzY1NTI1MDMsImp0aSI6ImMyMWMwNTgxMTU0MjQ3MWZiZjVmN2U5ODQ1NTM5MDQ2IiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbkBhdXRvbWF0aW9uLmxvY2FsIiwidXVpZCI6IjEzZGU2NSIsImdyb3VwcyI6WyJhdXRvbWF0aW9uLmxvY2FsIl19.CdnzTKaLLRPwoi7L-UiQql7S0_yrdfZi71DwN-QpuLak2HfVtmjdW76aLdoHg_j57TshppFVTOQPFen12hwZ5oz5_b_EtMzK1WSLX_atWLiLrvjmHOSAa5YMEuxbS9ltAv5f3-dq5zdgtD9WOF9voYyM1VN8by0_wazu9wNaZi6jDveLfcr8x2KFCfgDE9fOx2XmaKrZuktwL5ayUHeINGrQGfJX8RBv2MwxZotXK45Ne0RDXxiJ_5StAh3NpSiMUEUl27vRjOwwQdW_Cy8mSftvlcVShO75B4-G0fHNEEI-W54DlYUR74X3vLhEDzv62K9r6Sjrf8GxaGPV1Uc_1A'

export authBearer


# Create global host
out=`curl --location --request POST 'http://10.0.111.26/api/v1/checkpoint/1/Global/hosts/' \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "10.213.216.61",
        "ipv4-address": "10.213.216.61"
    }
}'`
hostUid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`


# Create local group
out=`curl --location --request POST 'http://10.0.111.26/api/v1/checkpoint/1/POLAND/groups/' \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "localGroupC31",
        "color": "black"
    }
}'`
localGroupUid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`


# Create global groups
out=`curl --location --request POST 'http://10.0.111.26/api/v1/checkpoint/1/Global/groups/' \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "globalGroupC31",
        "color": "black"
    }
}'`
globalGroup1Uid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`

out=`curl --location --request POST 'http://10.0.111.26/api/v1/checkpoint/1/Global/groups/' \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "globalGroupC32",
        "color": "black"
    }
}'`
globalGroup2Uid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`


# Place globalGroup1 in localGroup
curl --location --request POST "http://10.0.111.26/api/v1/checkpoint/1/POLAND/group/${localGroupUid}/groups/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"data\": {
        \"groups\": [
            \"$globalGroup1Uid\"
        ]
    }
}"


# Place globalGroup2 in globalGroup1
curl --location --request POST "http://10.0.111.26/api/v1/checkpoint/1/Global/group/${globalGroup1Uid}/groups/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"data\": {
        \"groups\": [
            \"$globalGroup2Uid\"
        ]
    }
}"


# Place host in globalGroup2
curl --location --request POST "http://10.0.111.26/api/v1/checkpoint/1/Global/group/${globalGroup2Uid}/hosts/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"data\": {
        \"hosts\": [
            \"$hostUid\"
        ]
    }
}"


echo
echo "Groups in localGroup":
curl --location --request GET "http://10.0.111.26/api/v1/checkpoint/1/POLAND/group/${localGroupUid}/groups/" \
--header "$authBearer"

echo

echo "Groups in globalGroup1":
curl --location --request GET "http://10.0.111.26/api/v1/checkpoint/1/Global/group/${globalGroup1Uid}/groups/" \
--header "$authBearer"

echo

echo "Hosts in globalGroup2":
curl --location --request GET "http://10.0.111.26/api/v1/checkpoint/1/Global/group/${globalGroup2Uid}/hosts/" \
--header "$authBearer"

echo 
