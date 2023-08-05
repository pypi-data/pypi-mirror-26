import boto3
from tornado import gen
from jupyterhub.spawner import Spawner
from traitlets import (
    Dict,
    Unicode,
    List,
    Bool,
    Int,
)



class ECSSpawner(Spawner):
    ecs_client = boto3.client("ecs")
    ec2_client = boto3.client('ec2')
    cluster_name = Unicode("notebook-cluster",
                           help="Name of the cluster setup").tag(config=True)
    task_definition = Unicode("ql_notebook_spawner_task:3",
                              help="The task definition in <defn>:<revision> format").tag(config=True)

    task_arn = Unicode()
    container_instance_arn = Unicode()
    container_ip = Unicode()
    container_port = Int(0)

    def load_state(self, state):
        super().load_state(state)
        self.task_arn = state.get('task_arn', '')
        self.container_instance_arn = state.get('container_instance_arn', '')

    def get_state(self):
        state = super().get_state()
        if self.task_arn:
            state['task_arn'] = self.task_arn
        if self.container_instance_arn:
            state['container_instance_arn'] = self.container_instance_arn

        return state

    @gen.coroutine
    def poll(self):
        if self.task_arn:
            res = self.ecs_client.describe_tasks(
                cluster=self.cluster_name,
                tasks = [self.task_arn]
            )
            if res['tasks'][0]['lastStatus'].lower() in ('pending', 'running'):
                return None
            else:
                return 1
        else:
            return 0


    @gen.coroutine
    def start(self):
        client = self.ecs_client
        if not self.container_port or not self.container_ip:
            resp1 = client.run_task(cluster=self.cluster_name, taskDefinition=self.task_definition,
                                    count=1, startedBy="ecsspawner")
            self.task_arn = resp1['tasks'][0]['containers'][0]['taskArn']
            container_instance_arn = resp1['tasks'][0]['containerInstanceArn']
            self.log.info("Spawned notebook container ")
            self.log.info("Fetching container info")
            resp2 = client.describe_tasks(cluster=self.cluster_name, tasks=[self.task_arn])
            ctr = 0
            last_status = resp2['tasks'][0]['containers'][0]['lastStatus']
            while last_status != 'RUNNING' and ctr<100:
                self.log.info("Waiting for container instance status to move from %s to RUNNING" % last_status)
                yield gen.sleep(1)
                ctr += 1
                resp2 = client.describe_tasks(cluster=self.cluster_name, tasks=[self.task_arn])
                last_status = resp2['tasks'][0]['containers'][0]['lastStatus']
            port = resp2['tasks'][0]['containers'][0]['networkBindings'][0]['hostPort']
            self.container_port = port
            self.log.info("Container running on port %d" % int(port))
            resp3 = client.describe_container_instances(cluster=self.cluster_name,
                                                        containerInstances=[container_instance_arn])
            ec2_instance_id = resp3['containerInstances'][0]['ec2InstanceId']

            self.log.info("Fetching ec2 container instance IP addresses")
            resp4 = self.ec2_client.describe_instances(InstanceIds=[ec2_instance_id])

            ip = resp4['Reservations'][0]['Instances'][0]['PublicIpAddress']
            self.container_ip = ip
            private_ip = resp4['Reservations'][0]['Instances'][0]['PrivateIpAddress']
            self.log.info("Finished with the start method")
        else:
            ip = self.container_ip
            port = self.container_port

        return (ip, port)

    def stop(self, now=False):
        self.log.info("Stopping task %s" % self.task_arn)
        self.ecs_client.stop_task(
            cluster=self.cluster_name,
            task=self.task_arn,
            reason="Shutdown by the hub"
        )
        self.log.info("The requested task has been stopped")
        self.clear_state()
