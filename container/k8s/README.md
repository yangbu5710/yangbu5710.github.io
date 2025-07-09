- [简介](#简介)

# 简介
本文主要介绍k8s相关指令操作

1. 查询namespace下的全部configmap`kubectl get cm -n kube-system`
2. 获取namespace下的指定configmap详情`kubectl describe cm -n kube-system`
3. 编辑namespace下的指定configmap详情`kubectl edit cm -n kube-system`
4. 