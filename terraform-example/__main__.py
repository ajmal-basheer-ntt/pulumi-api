import pulumi
import pulumi_aws as aws

config = pulumi.Config()
aws_region = config.get("awsRegion")
if aws_region is None:
    aws_region = "us-east-1"
aws_amis = config.get_object("awsAmis")
if aws_amis is None:
    aws_amis = {
        "us-east-1": "ami-0ff8a91507f77f867",
        "us-west-2": "ami-a0cfeed8",
    }
# Our default security group to access
# the instances over SSH and HTTP
default_security_group = aws.ec2.SecurityGroup("defaultSecurityGroup",
    description="Used in the terraform",
    egress=[aws.ec2.SecurityGroupEgressArgs(
        cidr_blocks=["0.0.0.0/0"],
        from_port=0,
        protocol="-1",
        to_port=0,
    )],
    ingress=[
        aws.ec2.SecurityGroupIngressArgs(
            cidr_blocks=["0.0.0.0/0"],
            from_port=22,
            protocol="tcp",
            to_port=22,
        ),
        aws.ec2.SecurityGroupIngressArgs(
            cidr_blocks=["0.0.0.0/0"],
            from_port=80,
            protocol="tcp",
            to_port=80,
        ),
    ],
    name="eip_example")
web = aws.ec2.Instance("web",
    ami=aws_amis[aws_region],
    instance_type="t2.micro",
    security_groups=[default_security_group.name],
    tags={
        "Name": "eip-example",
    },
    user_data=(lambda path: open(path).read())("userdata.sh"))
default_eip = aws.ec2.Eip("defaultEip",
    instance=web.id,
    vpc=True)
pulumi.export("address", web.private_ip)
pulumi.export("elastic ip", default_eip.public_ip)
