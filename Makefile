all:
DASH = lsstsqre/squash-dash
NGINX = lsstsqre/squash-dash-nginx
NGINX_CONFIG = kubernetes/nginx/nginx.conf
DEPLOYMENT_TEMPLATE = kubernetes/deployment-template.yaml
DEPLOYMENT_CONFIG = kubernetes/deployment.yaml
SERVICE_CONFIG = kubernetes/service.yaml
STATIC = kubernetes/nginx/static
REPLACE = ./kubernetes/replace.sh

$(STATIC):
	cd squash; python manage.py collectstatic

build: check-tag $(STATIC)
	docker build -t $(DASH):${TAG} .
	docker build -t $(NGINX):${TAG} kubernetes/nginx

push: check-tag
	docker push $(DASH):${TAG}
	docker push $(NGINX):${TAG}

service:
	@echo "Creating service..."
	kubectl delete --ignore-not-found=true services squash-dash
	kubectl create -f $(SERVICE_CONFIG)

configmap:
	@echo "Creating config map for the nginx configuration..."
	kubectl delete --ignore-not-found=true configmap squash-dash-nginx-conf
	kubectl create configmap squash-dash-nginx-conf --from-file=$(NGINX_CONFIG)

deployment: check-tag configmap
	@echo "Creating deployment..."
	@$(REPLACE) $(DEPLOYMENT_TEMPLATE) $(DEPLOYMENT_CONFIG)
	kubectl delete --ignore-not-found=true deployment squash-dash
	kubectl create -f $(DEPLOYMENT_CONFIG)

update: check-tag
	@echo "Updating squash-dash deployment..."
	@$(REPLACE) $(DEPLOYMENT_TEMPLATE) $(DEPLOYMENT_CONFIG)
	kubectl apply -f $(DEPLOYMENT_CONFIG) --record
	kubectl rollout history deployment squash-dash

clean:
	rm $(DEPLOYMENT_CONFIG)
	rm -r $(STATIC)

check-tag:
	@if test -z ${TAG}; then echo "Error: TAG is undefined."; exit 1; fi

