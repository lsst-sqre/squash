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

# on GKE
WAIT_TIME=5
while [ "$HOST" == "" ] && [ "$WAIT_TIME" -le 20 ]; do
    echo "Waiting for the service to become available..."
    sleep $(( WAIT_TIME++ ))
    HOST=$(kubectl get service squash -o jsonpath --template='{.status.loadBalancer.ingress[0].ip}')
done

if [ "$HOST" == "" ]; then
    echo "Service is not ready..."
    exit 1
fi

PORT=443
echo "Service address: $HOST:$PORT"

NAMESPACE=$(kubectl config current-context)

SQUASH_HOST="squash-${NAMESPACE}.lsst.codes"

if [ "$NAMESPACE" == "squash-prod" ]; then
    SQUASH_HOST="squash.lsst.codes"
fi

SQUASH_GRAPHQL_URL="https://squash-graphql-${NAMESPACE}.lsst.codes"

if [ "$NAMESPACE" == "squash-prod" ]; then
    SQUASH_GRAPHQL_URL="https://squash-graphql.lsst.codes"
fi

SQUASH_API_URL="https://squash-restful-api-${NAMESPACE}.lsst.codes"

if [ "$NAMESPACE" == "squash-prod" ]; then
    SQUASH_API_URL="https://squash-api.lsst.codes"
fi

SQUASH_BOKEH_URL="https://squash-bokeh-${NAMESPACE}.lsst.codes"

if [ "$NAMESPACE" == "squash-prod" ]; then
    SQUASH_BOKEH_URL="https://squash-bokeh.lsst.codes"
fi

sed -e "
s/{{ TAG }}/${TAG}/
s/{{ SQUASH_HOST }}/${SQUASH_HOST}/
s|{{ SQUASH_API_URL }}|\"${SQUASH_API_URL}\"|
s|{{ SQUASH_GRAPHQL_URL }}|\"${SQUASH_GRAPHQL_URL}\"|
s|{{ SQUASH_BOKEH_URL }}|\"${SQUASH_BOKEH_URL}\"|
" $1 > $2
