#!/bin/bash

# POLAND:

# localGroupUid
#   globalGroup1Uid
#     globalGroup1Ui2
#       hostUid

apiCheckPointIp=10.0.111.26
ssoIp=10.0.111.100

domain=POLAND
hostIp=10.213.216.61

if ! which jq > /dev/null; then
    echo "jq not found: install jq package."
    exit 1
fi

export hostIp ssoIp apiCheckPointIp
# SSO login
token=`curl --no-progress-meter --location "http://${ssoIp}/api/v1/token/" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"username\": \"admin@automation.local\",
    \"password\": \"password\"
}" | jq '.access' | sed -e 's/^"//' -e 's/"$//'`

authBearer="Authorization: Bearer $token"
export authBearer


# Get the uid of the first access layer in $domain (and check if it exists).
out=`curl --no-progress-meter --location "http://${apiCheckPointIp}/api/v1/checkpoint/1/${domain}/access-layers/?local=null" \
--header "$authBearer"`
layerUid=`echo $out | jq '.data.items[0].uid' | sed -r -e 's/^"//' -e's/"$//'`
if [ -z "$layerUid" ]; then
    echo "Cannot find an access layer in domain, create an access layer first."
    exit 1
fi
echo "layerUid: $layerUid"
export layerUid

###################
# Create global host
out=`curl --no-progress-meter --location --request POST "http://${apiCheckPointIp}/api/v1/checkpoint/1/Global/hosts/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"data\": {
        \"name\": \"$hostIp\",
        \"ipv4-address\": \"$hostIp\"
    }
}"`
hostUid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`
echo "hostUid: $hostUid"
export hostUid


# Create local group
out=`curl --no-progress-meter --location --request POST "http://${apiCheckPointIp}/api/v1/checkpoint/1/${domain}/groups/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "localGroupC31",
        "color": "black"
    }
}'`
localGroupUid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`
echo "localGroupUid: $localGroupUid"
export localGroupUid


# Create global groups
out=`curl --no-progress-meter --location --request POST "http://${apiCheckPointIp}/api/v1/checkpoint/1/Global/groups/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "globalGroupC31",
        "color": "black"
    }
}'`
globalGroup1Uid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`
echo "globalGroup1Uid: $globalGroup1Uid"
export globalGroup1Uid

out=`curl --no-progress-meter --location --request POST "http://${apiCheckPointIp}/api/v1/checkpoint/1/Global/groups/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "globalGroupC32",
        "color": "black"
    }
}'`
globalGroup2Uid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`
echo "globalGroup2Uid: $globalGroup2Uid"
export globalGroup2Uid


# Create an access rule in $layerUid with $hostUid as source. Without destination param, the destination is "any".
out=`curl --no-progress-meter --location "http://${apiCheckPointIp}/api/v1/checkpoint/1/${domain}/access-layer/${layerUid}/rules/" \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw "{
    \"data\": {
        \"name\": \"Pasa su tous cos\",
        \"position\": 1,
        \"service\": [
            \"HTTP\",
            \"SMTP\"
        ],
        \"source\": \"${hostUid}\"

    }
}"`
ruleUid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`
echo "ruleUid: $ruleUid"
export ruleUid


# Place globalGroup1 in localGroup
curl --no-progress-meter --location --request POST "http://${apiCheckPointIp}/api/v1/checkpoint/1/${domain}/group/${localGroupUid}/groups/" \
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
curl --no-progress-meter --location --request POST "http://${apiCheckPointIp}/api/v1/checkpoint/1/Global/group/${globalGroup1Uid}/groups/" \
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
curl --no-progress-meter --location --request POST "http://${apiCheckPointIp}/api/v1/checkpoint/1/Global/group/${globalGroup2Uid}/hosts/" \
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
curl --no-progress-meter --location --request GET "http://${apiCheckPointIp}/api/v1/checkpoint/1/${domain}/group/${localGroupUid}/groups/" \
--header "$authBearer" | jq '.data.items[] | "{uid: \(.uid), name: \(.name)}"'


echo

echo "Groups in globalGroup1":
curl --no-progress-meter --location --request GET "http://${apiCheckPointIp}/api/v1/checkpoint/1/Global/group/${globalGroup1Uid}/groups/" \
--header "$authBearer" | jq '.data.items[] | "{uid: \(.uid), name: \(.name)}"'

echo

echo "Hosts in globalGroup2":
curl --no-progress-meter --location --request GET "http://${apiCheckPointIp}/api/v1/checkpoint/1/Global/group/${globalGroup2Uid}/hosts/" \
--header "$authBearer" | jq '.data.items[] | "{uid: \(.uid), name: \(.name)}"'

echo 
