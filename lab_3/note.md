# Check clusters created
kind get clusters

# Change cluster
kubectl config use-context <cluster-name>

# Check cluster context (* marks the current one)
kubectl config get-contexts

# 1. Create a 1-node cluster
kind create cluster --name etcd

# 2. Create namespace etcd
kubectl create namespace etcd

# 3. Install Local Path Provisioner (for dynamic storage provisioning)
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml

# 4. Apply the Etcd YAML file
kubectl apply -f ./etcd.yml

# 5. Port forwarding (expose etcd client API on localhost:2379)
kubectl port-forward etcd-0 2379:2379 -n etcd