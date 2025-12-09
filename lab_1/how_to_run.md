# Kafka Cluster Setup on Kind (WSL2 + Docker Desktop)

## 1. Open Docker Desktop
Make sure Docker Desktop is running before starting.

## 2. Create the Kubernetes Cluster
```bash
kind create cluster --name wslkindmultinodes --config ./kind-3nodes.yaml
```
## 3. Install Local Path Provisioner
Provides dynamic storage provisioning for your cluster:
```bash
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```
## 4. Create Namespace
```bash
kubectl create namespace kafka
```
## 5. Deploy Kafka
Apply your Kafka configuration:
```bash
kubectl apply -f ./kafka.yml
```
## 6. Create a Kafka Topic
Run inside the Kafka Pod:
```bash
kubectl exec -it kafka-0 -n kafka -- \
  /opt/kafka/bin/kafka-topics.sh \
  --create \
  --bootstrap-server localhost:9092 \
  --topic dblab
```
## 7. Expose Kafka Port Outside the Cluster
Forward the Kafka service port to your local machine:
```bash
kubectl port-forward svc/kafka-service 9094:9094 -n kafka
```
## 8. Run Producer and Consumer
Use Kafka console tools or your Python client to confirm message flow.


## Delete command
# delete kafka completely
kubectl delete configmap <CONFIGMAP_NAME> -n <NAMESPACE>
kubectl delete service <SERVICE_NAME> -n <NAMESPACE>
kubectl delete statefulset <STATEFULSET_NAME> -n <NAMESPACE>
kubectl delete pvc -l app=<STATEFULSET_NAME> -n <NAMESPACE>


kubectl delete configmap kafka-config -n kafka
kubectl delete service kafka-service -n kafka
kubectl delete statefulset kafka -n kafka
kubectl delete pvc -l app=kafka -n kafka
## Check kafka pods
kubectl get pods -n kafka -o wide

## Activate virtual env
source $HOME/dissys/bin/activate

## Check pod start
kubectl logs <pod-name> -n kafka | grep STARTED
No log: problems

## Restart pod
kubectl delete pod <pod name> -n kafka
