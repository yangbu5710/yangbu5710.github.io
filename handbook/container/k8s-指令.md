# Kubernetes 指令

本文主要记录 Kubernetes 常用指令操作。

## ConfigMap

1. 查询 namespace 下的全部 ConfigMap：`kubectl get cm -n kube-system`
2. 获取 namespace 下的指定 ConfigMap 详情：`kubectl describe cm -n kube-system <configmap-name>`
3. 编辑 namespace 下的指定 ConfigMap：`kubectl edit cm -n kube-system <configmap-name>`

