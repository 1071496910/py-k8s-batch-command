#!/bin/bash
regs="reg.local:5000 registry.meizu.com"
for reg in $regs
do
    docker build -t $reg/common/k8s-batch-command .
    docker push $reg/common/k8s-batch-command
done
