#!/bin/bash


case $1 in
    "start" )
        docker pull registry.meizu.com/common/k8s-batch-command
        docker run --name k8s-batch-command  -d  --net host -v /etc/kubernetes/ssl:/etc/kubernetes/ssl:ro -v /root/.kube:/root/.kube:ro registry.meizu.com/common/k8s-batch-command
            ;;
    "stop" )
        docker rm -f k8s-batch-command
            ;;
    "restart" )
        docker pull registry.meizu.com/common/k8s-batch-command
        docker rm -f k8s-batch-command
        docker run --name k8s-batch-command  -d  --net host -v /etc/kubernetes/ssl:/etc/kubernetes/ssl:ro -v /root/.kube:/root/.kube:ro registry.meizu.com/common/k8s-batch-command
            ;;
esac
