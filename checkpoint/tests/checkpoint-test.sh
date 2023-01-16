#!/bin/bash


# POLAND:

# localGroupUid
#   globalGroup1Uid
#     globalGroup1Ui2
#       hostUid


authBearer='Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjczOTUwMjEyLCJpYXQiOjE2NzM4NjM4MTIsImp0aSI6IjI2NWFiMGVmNjU1MTQ3OTQ5M2YzOGFkZTk3YWU3YmJjIiwidXNlcl9pZCI6MSwidXNlcm5hbWUiOiJhZG1pbkBhdXRvbWF0aW9uLmxvY2FsIiwidXVpZCI6IjE2Y2Y3ZiIsImdyb3VwcyI6WyJhdXRvbWF0aW9uLmxvY2FsIl19.pmG6LF7qWBHpdN01v5XJ3R1QJ0XvZ-x4_GQPaG82UCRPz3MGOUe0kR-6HOOAeS-o4iCdXzPEjNq1UgZE3i4J-UEMzh1ty4c99gctlMT7_cWE3W1zEOfrQNbea76eihnPa3zJU1k4CUjbu-dvrC6T4pAAA4Q6gnAyzWf5Rbcd3ld7svpCKUvBZZdvUtIYZPxDQ3-V30UQetkyip7rn_LOSCZyf5QDdlRScaVMiMQAyAE5GtWmoa8UBuZi-V6q8RutTe_hPbNNzhHLrmGIA_Q5MCg1ukZTLFDZVkI8oCJuHtRjD-UXT6oWcXe6ACOnHAb8i7tCQomL5EVs82d3IUB-Og'

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
        "name": "localGroupC21",
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
        "name": "globalGroupC21",
        "color": "black"
    }
}'`
globalGroup1Uid=`echo $out | jq '.data.uid' | sed -r -e 's/^"//' -e's/"$//'`

out=`curl --location --request POST 'http://10.0.111.26/api/v1/checkpoint/1/Global/groups/' \
--header "$authBearer" \
--header 'Content-Type: application/json' \
--data-raw '{
    "data": {
        "name": "globalGroupC22",
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
