%postun
#!/bin/bash

printf "\n* Container postrm...\n"

# Use image label to cleanup possible orphaned images.
oImgs=$(buildah images | grep -F '<none>' | awk '{print $3}')
for img in $oImgs ; do
    if buildah inspect $img | grep -q '"AUTOMATION_CONTAINER_IMAGE": "api-checkpoint"'; then
        buildah rmi --force $img
    fi
done

# $1 is the number of time that this package is present on the system. If this script is run from an upgrade and not
if [ "$1" -eq "0" ]; then
    if podman volume ls | awk '{print $2}' | grep -q ^api-checkpoint$; then
        printf "\n* Clean up api-checkpoint volume...\n"
        podman volume rm -f api-checkpoint
        podman volume rm -f api-checkpoint-db
        podman volume rm -f api-checkpoint-cacerts
    fi
fi

exit 0
