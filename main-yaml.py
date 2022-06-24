import sys
import json
import pulumi
from pulumi import automation as auto
import pulumi_kubernetes as kubernetes

project_name = "yaml-example"
stack_name = "dev"

def pulumi_program():
    example = kubernetes.yaml.ConfigFile(
        "example",
        file="example-file.yaml",
    )

stack = auto.create_or_select_stack(stack_name=stack_name,
                                    project_name=project_name,
                                    program=pulumi_program)

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
