from constructs import Construct
from aws_cdk import (
    Stack,
    aws_ecs as ecs,
    aws_ecr_assets as ecs_assets,
    aws_ecs_patterns as ecs_patterns
)


class ECSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster = ecs.Cluster(self, 'Container-Cluster', vpc=vpc)

        image_asset = ecs_assets.DockerImageAsset(self, 'Container-App-Page', directory='./container-app')

        image = ecs.ContainerImage.from_docker_image_asset(image_asset)

        ecs_patterns.ApplicationLoadBalancedFargateService(self, 'Container-App-Fargate',
                                                           cluster = cluster,
                                                           cpu = 256,
                                                           memory_limit_mib= 512,
                                                           desired_count= 1,
                                                           listener_port= 80,
                                                           task_image_options= ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                                                               image = image,
                                                               container_name = 'Container-App-Page',
                                                               container_port = 80
                                                           ),
                                                           public_load_balancer= True)