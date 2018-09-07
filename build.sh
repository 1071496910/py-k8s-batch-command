#!/bin/bash
docker build -t reg.local:5000/common/k8s-batch-command .
docker push reg.local:5000/common/k8s-batch-command
