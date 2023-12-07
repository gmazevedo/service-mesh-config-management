# Service Mesh for Configuration Managemen
This work presents the setup of a local environment using Minikube to establish a Kubernetes cluster and the installation of Istio as a Service Mesh. It details the environment, including the installation of kubectl and Istio, with an emphasis on installation profiles. It explores the implementation of the BookInfo application, from namespace labeling to ingress configuration, highlighting the functioning of the Service Mesh in communication between services. Additionally, it illustrates the use of Istio's traffic shifting for controlled migration of microservices versions. This practical discussion of the configuration is relevant for real-world scenarios and integrates a debate on network configuration management.

## Requirements
* You need to have Docker or VirtualBox or some other VM manager installed. Docker, QEMU, Hyperkit, Hyper-V, KVM, Parallels, Podman, VirtualBox, or VMware Fusion/Workstation.
* kubectl
* Minikube

# Instructions

```
$ minikube start --driver=docker --cpus 6 --memory 3795
$ istioctl install --set profile=demo
```

## Book Info

```
$ minikube kubectl label namespace default istio-injection=enabled
$ kubectl apply -f samples/bookinfo/platform/kube/bookinfo.yaml
$ kubectl apply -f samples/bookinfo/networking/bookinfo-gateway.yaml
```

## Determining the ingress IP and ports
[Istio tutorial - Ingress Control](https://istio.io/latest/docs/tasks/traffic-management/ingress/ingress-control/#determining-the-ingress-ip-and-ports)

**Open another terminal**
```
$ minikube tunnel
```

**Return to tutorial terminal**
```
$ export INGRESS_NAME=istio-ingressgateway
$ export INGRESS_NS=istio-system
$ export INGRESS_HOST=$(kubectl -n "$INGRESS_NS" get service "$INGRESS_NAME" -o jsonpath='{.status.loadBalancer.ingress[0].ip}')
$ export INGRESS_PORT=$(kubectl -n "$INGRESS_NS" get service "$INGRESS_NAME" -o jsonpath='{.spec.ports[?(@.name=="http2")].port}')
$ export SECURE_INGRESS_PORT=$(kubectl -n "$INGRESS_NS" get service "$INGRESS_NAME" -o jsonpath='{.spec.ports[?(@.name=="https")].port}')
$ export TCP_INGRESS_PORT=$(kubectl -n "$INGRESS_NS" get service "$INGRESS_NAME" -o jsonpath='{.spec.ports[?(@.name=="tcp")].port}')
```

## Book Info

```
$ export GATEWAY_URL=$INGRESS_HOST:$INGRESS_PORT
$ kubectl apply -f samples/bookinfo/networking/destination-rule-all.yaml
```

You should be able to access using via web browser:

```http://$GATEWAY_URL/productpage```

## Request Routing

[Istio tutorial - Request Routing](https://istio.io/latest/docs/tasks/traffic-management/request-routing/)

```
$ kubectl apply -f samples/bookinfo/networking/virtual-service-all-v1.yaml
$ kubectl apply -f samples/bookinfo/networking/virtual-service-reviews-test-v2.yaml
```

## Traffic Shifting
```
$ kubectl apply -f samples/bookinfo/networking/virtual-service-reviews-50-v3.yaml
```



