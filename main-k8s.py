# https://www.pulumi.com/registry/packages/kubernetes/api-docs/core/


import sys
import json
import pulumi
from pulumi import automation as auto
import pulumi_kubernetes as kubernetes

project_name = "nginx-pod"
stack_name = "dev"

def pulumi_program():
    nginx_pod = kubernetes.core.v1.Pod(
        "nginxPod",
        metadata=kubernetes.meta.v1.ObjectMetaArgs(
            name="nginx",
        ),
        spec=kubernetes.core.v1.PodSpecArgs(
            containers=[kubernetes.core.v1.ContainerArgs(
                name="nginx",
                image="nginx:1.14.2",
                ports=[kubernetes.core.v1.ContainerPortArgs(
                    container_port=80,
                )],
            )],
        ))

stack = auto.create_or_select_stack(stack_name=stack_name,
                                    project_name=project_name,
                                    program=pulumi_program)


# up_res = stack.up(on_output=print)

# to destroy:
# venv/bin/python main-k8s.py destroy

destroy = False
args = sys.argv[1:]
if len(args) > 0:
    if args[0] == "destroy":
        destroy = True

if destroy:
    print("destroying stack...")
    stack.destroy(on_output=print)
    print("stack destroy complete")
    sys.exit()
else:
    print("creating stack...")
    stack.up(on_output=print)
    print("stack creation complete")
    sys.exit()
