# kube-ai-sre-agent
Kubernetes AI for self-healing with policy controls

# Kind
- WHY?
    - Lightweight and fast
    - local k8s running inside docker for testing

to see the desc
    `kubectl describe pod memory-hog -n demo`


# fresh start
kubectl delete namespace demo
kubectl get ns
kubectl create namespace demo

kubectl apply -n demo -f slow-memory-hog.yml
kubectl get pods -n demo -w

kubectl apply -n demo -f memory-hog.yml
kubectl get pods -n demo -w


# Optional improvements
- Watch API instead of polling → detect OOMs immediately.
- Event-based logging → record every container OOM event.
- Automatic remediation → scale memory limits or restart pods.
- Alert de-duplication → avoid reporting the same pod repeatedly.
- For all types of events.
