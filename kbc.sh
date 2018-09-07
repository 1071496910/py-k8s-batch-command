#!/bin/bash


case $1 in
    "start" )
        docker pull reg.local:5000/common/k8s-batch-command
        docker run --name k8s-batch-command  -d  --net host -v /root/.kube:/root/.kube:ro reg.local:5000/common/k8s-batch-command
            ;;
    "stop" )
        docker rm -f k8s-batch-command
            ;;
    "restart" )
        docker pull reg.local:5000/common/k8s-batch-command
        docker rm -f k8s-batch-command
        docker run --name k8s-batch-command  -d  --net host -v /root/.kube:/root/.kube:ro reg.local:5000/common/k8s-batch-command
            ;;
esac
