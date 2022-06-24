import sys
import json
import pulumi
from pulumi import automation as auto
import pulumi_kubernetes as kubernetes

project_name = "helm-example"
stack_name = "dev"

def pulumi_program():

    nginx_ingress = kubernetes.helm.v3.Chart(
        "nginx-ingress",
        kubernetes.helm.v3.ChartOpts(
            chart="nginx-ingress",
            version="1.24.4",
            fetch_opts=kubernetes.helm.v3.FetchOpts(
                repo="https://charts.helm.sh/stable",
            ),
        ),
    )


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