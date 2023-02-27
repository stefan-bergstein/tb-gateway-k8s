# tb-gateway-k8s

## Intro

This repository shows how to deploy the Thingsboard Gateway on Red Hat MicroShift. In this playground, the Thingsboard Gateway sends data to a Thingsboard deployment that runs on Red Hat OpenShift. The Thingsboard deployment on OpenShift exposes the MQTT service via a secure route (similar to K8S Ingress) on port 443. The Thingsboard Gateway is configured to receive REST message. Please feel free to fork and add further protocols (OPC-UA, Modbus, etc) that the Thingsboard Gateway offers. The repo includes a few virtual demo sensors to test and showcase the solution.


## Build gateway container image
```
podman build . -t tb-gateway:latest -f containerfile
```

## Run container with connection to demo.thingsboard.io
```
podman run --rm -it --name tb-gateway -e host=demo.thingsboard.io -e port=1883 -e accessToken=YOUR_GW_ACCESS_TOKEN -p 5000:5000  tb-gateway
```

## Test the gateway
```
curl  -H "Content-Type: application/json" -X POST -d '{"sensorName": "Sensor T1", "sensorModel": "example", "temp": "20.5"}' http://127.0.0.1:5000/my_devices
```

## Run and Cconnect to Thingsboards on your OpenShift cluster 
```
podman run --rm -it --name tb-gateway -v tb-gateway-k8s/certs-nogit:/app/thingsboard-gateway/certs:Z   -e host=hostname-of-your-route -e port=443 -e accessToken=YOUR_GW_ACCESS_TOKEN -e caCert=../../certs/server.pem -p 5000:5000  tb-gateway
```


# Deploy to MicroShift
This assumes you have a MicroShift and Thingsboards on your OpenShift cluster already installed.

```
export KUBECONFIG=$HOME/.kube/ushift3-config
```

## Create cconfig map with cert
User the cerfifate of the Thingsboard MQTT over TLS configuration, of your Thingsboards on OpenShift

```
kubectl create configmap tb-gateway-cert --from-file=cert/server.pem=server.pem  --dry-run=client
```
Replace it with k8s/tb-gateway-cert.yaml, if needed.

## Deploy the gatewate
```
oc apply -k k8s/
```

## Deploy two sensor simulator

```
oc apply -k sensor-sim/k8s/overlays/
```

