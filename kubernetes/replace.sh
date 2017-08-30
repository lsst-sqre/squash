#!/bin/bash

usage(){
	echo "Usage: $0 <template configuration> <configuration>"
	exit 1
}

if [ "$1" == "" ] || [ "$2" == "" ]; then
    usage
fi

# values returned if the service is not ready
HOST=""
PORT=""

# on minikube we don't have an external IP
# configure the `minikube ip` to point to squash-local.lsst.codes in your /etc/hosts

if [ "$MINIKUBE" == "true" ]; then
    HOST=squash-local.lsst.codes
    PORT=$(kubectl get services squash-dash -o jsonpath --template='{.spec.ports[0].nodePort}')
else
    # on GKE
    WAIT_TIME=5
    while [ "$HOST" == "" ] && [ "$WAIT_TIME" -le 10 ]; do
        echo "Waiting for the service to become available..."
        sleep $(( WAIT_TIME++ ))
        # TODO: we'll need the hostname once DNS is configured
        HOST=$(kubectl get service squash-dash -o jsonpath --template='{.status.loadBalancer.ingress[0].ip}')
    done
    PORT=443
fi

if [ "$HOST" == "" ]; then
    echo "Service is not ready..."
    echo "If you are deploying to a minikube local cluster, make sure you set MINIKUBE=true."
    exit 1
fi

echo "Service address: $HOST:$PORT"


sed -e "
s/{{ TAG }}/${TAG}/
s/{{ SQUASH_DASH_HOST }}/${HOST}/
s/{{ SQUASH_DASH_PORT }}/${PORT}/
" $1 > $2
