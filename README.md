# squash

`squash` is the web frontend to embed the bokeh apps and navigate through them. You can learn more about SQuaSH at [SQR-009](https://sqr-009.lsst.io).

[![Build Status](https://travis-ci.org/lsst-sqre/squash.svg?branch=master)](https://travis-ci.org/lsst-sqre/squash)

## Requirements

The `squash` web frontend requires the [squash-restful-api](https://github.com/lsst-sqre/squash-restful-api) and [squash-bokeh](https://github.com/lsst-sqre/squash-bokeh) microservices, and the TLS certificats that are installed by the
[`squash-deployment`](https://github.com/lsst-sqre/squash-deployment).

## Kubernetes deployment

You can provision a Kubernetes cluster in GKE, clone this repo and deploy the `squash` microservice using:

```
cd squash
TAG=latest make service deployment
```

The variables `SQUASH_MONITOR_APP` and `SQUASH_BOKEH_APPS` can be used to control the bokeh apps allowed in this
deployment, for example:

```
export SQUASH_MONITOR_APP=code_changes
export SQUASH_BOKEH_APPS="code_changes AMx PAx"
```

their default values correspond to the production deployment.

### Debugging

Use the `kubectl logs` command to view the logs of the `nginx` and `dash` containers:

```
kubectl logs deployment/squash-api nginx
kubectl logs deployment/squash-api dash
```

Use the `kubectl exec` to run an interactive shell inside a container. Use tab completion or `kubectl get pods` command
to find the pod's name:


```
kubectl exec -it <squash pod> -c dash /bin/bash
```

### Rolling out updates

Check the update history with:

```
kubectl rollout history deployment squash
```

Modify the `squash` image and then apply the new configuration for the kubernetes deployment:

```
# we need to setup the env for django to collect static files
virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
TAG=latest make build push update
```

Check the deployment changes:
```
kubectl describe deployments squash
```

### Scaling up the squash microservice

Use the `kubectl get replicasets` command to view the current set of replicas, and then the `kubectl scale` command
to scale up the `squash` deployment:

```
kubectl scale deployments squash --replicas=3
```

or change the `kubernetes/deployment.yaml` configuration file and apply the new configuration:

```
kubectl apply -f kubernetes/deployment.yaml
```

Check the deployment changes:

```
kubectl describe deployments squash
kubectl get pods
kubectl get replicasets
```

## Development workflow

You can install the dependencies for developing

1. Install the software dependencies
```
git clone  https://github.com/lsst-sqre/squash.git

cd squash

virtualenv env -p python3
source env/bin/activate
pip install -r requirements.txt
```

2. Run `squash`

```
export SQUASH_DASH_DEBUG=True
export SQUASH_BOKEH_URL=<suqash-bokeh url> # e.g. the one from squash-bokeh deployment
export SQUASH_API_URL=<squash-restful-api url> # e.g. the one from squash-restful-api deployment
```
The variables `SQUASH_MONITOR_APP` and `SQUASH_BOKEH_APPS` can be used to control the bokeh apps allowed in this
deployment, for example:

```
export SQUASH_MONITOR_APP=code_changes
export SQUASH_BOKEH_APPS="code_changes AMx PAx"

python manage.py runserver
```

The `squash` will run at `http://localhost:8000`.
