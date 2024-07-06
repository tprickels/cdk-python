from constructs import Construct
from aws_cdk import (
    Stack,
    CfnOutput,
    aws_ec2 as ec2
)


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 cidr = '10.10.0.0/16',
                 subnet_mask = 24,
                 nat_gateways = 1,
                 db_port = 5432,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs              = 6,
                           ip_addresses         = ec2.IpAddresses.cidr(cidr),
                           subnet_configuration = [ec2.SubnetConfiguration(
                               subnet_type      = ec2.SubnetType.PUBLIC,
                               name             = "Public",
                               cidr_mask        = subnet_mask
                           ), 
                            ec2.SubnetConfiguration(
                               subnet_type      = ec2.SubnetType.PRIVATE_WITH_EGRESS,
                               name             = "Private",
                               cidr_mask        = subnet_mask
                           ), 
                            ec2.SubnetConfiguration(
                               subnet_type      = ec2.SubnetType.PRIVATE_ISOLATED,
                               name             = "DB",
                               cidr_mask        = subnet_mask
                           )
                           ],
                           nat_gateways=nat_gateways
                           )
                           
        
        private_subnets = self.vpc.private_subnets
        isolated_subnets = self.vpc.isolated_subnets
        
        isolated_nacl = ec2.NetworkAcl(self, "DBNacl", 
                                        vpc              = self.vpc, 
                                        subnet_selection = ec2.SubnetSelection(subnets=isolated_subnets))

        for id, subnet in enumerate(private_subnets, start=1):
            isolated_nacl.add_entry("DbNACLIngress{}".format(id*100), 
                                        rule_number = id*100,
                                        cidr        = ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                        traffic     = ec2.AclTraffic.tcp_port(db_port),
                                        direction   = ec2.TrafficDirection.INGRESS,
                                        rule_action = ec2.Action.ALLOW)
                                    
        for id, subnet in enumerate(private_subnets, start=1):
            isolated_nacl.add_entry("DbNACLEgress{}".format(id*100), 
                                    rule_number = id*100,
                                    cidr        = ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                    traffic     = ec2.AclTraffic.tcp_port_range(1024,65535),
                                    direction   = ec2.TrafficDirection.EGRESS,
                                    rule_action = ec2.Action.ALLOW)

     
        CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
