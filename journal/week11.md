# Week 11 — CloudFormation Part 2

## CFN Service Layer

Parameters:

```
Parameters:
  NetworkingStack:
    Type: String
    Description: This is our base layer of networking components eg. VPC, Subnets
    Default: CrdNet
  ClusterStack:
    Type: String
    Description: This is our cluster layer eg. ECS Cluster, ALB
    Default: CrdCluster
  ContainerPort:
    Type: Number
    Default: 4567
  ServiceCpu:
    Type: String
    Default: '256'
  ServiceMemory:
    Type: String
    Default: '512'
  EcrImage:
    Type: String
    Default: '928597128531.dkr.ecr.us-east-1.amazonaws.com/backend-flask'
  ContainerName:
    Type: String
    Default: backend-flask
  TaskFamily:
    Type: String
    Default: backend-flask
  ServiceName:
    Type: String
    Default: backend-flask
  EnvOtelServiceName:
    Type: String
    Default: backend-flask
  EnvOtelExporterOtlpEndpoint:
    Type: String
    Default: https://api.honeycomb.io
  EnvAwsCognitoUserPoolId:
    Type: String
    Default: us-east-1_5SN7XhsT0
  EnvAwsCognitoUserPoolClientId:
    Type: String
    Default: 4em6p32irpbr10ujcn3svhsdm4
  EnvFrontendUrl:
    Type: String
    Default: https://cruddur.pl
  EnvBackendUrl:
    Type: String
    Default: https://api.cruddur.pl
  SecretsAWSAccessKeyId:
    Type: String
    Default: 'arn:aws:ssm:us-east-1:928597128531:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID'
  SecretsSecretAccessKey:
    Type: String
    Default: 'arn:aws:ssm:us-east-1:928597128531:parameter/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY'
  SecretsConnectionUrl:
    Type: String
    Default: 'arn:aws:ssm:us-east-1:928597128531:parameter/cruddur/backend-flask/CONNECTION_URL'
  SecretsRollbarAccessToken:
    Type: String
    Default: 'arn:aws:ssm:us-east-1:928597128531:parameter/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN'
  SecretsOtelExporterOltpHeaders:
    Type: String
    Default: 'arn:aws:ssm:us-east-1:928597128531:parameter/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS'
```

- NetworkingStack: Represents the name of the base layer networking stack. It is a string parameter with a default value of "CrdNet".

- ClusterStack: Represents the name of the cluster layer stack. It includes components like ECS Cluster and ALB (Application Load Balancer). It is a string parameter with a default value of "CrdCluster".

- ContainerPort: Represents the number of the container port to be used. It is a numeric parameter with a default value of 4567.

- ServiceCpu: Represents the CPU units allocated to the service. It is a string parameter with a default value of '256'.

- ServiceMemory: Represents the memory allocated to the service. It is a string parameter with a default value of '512'.

- EcrImage: Represents the ECR (Elastic Container Registry) image used for the backend-flask container. It is a string parameter with a default value of '928597128531.dkr.ecr.us-east-1.amazonaws.com/backend-flask'.

- ContainerName: Represents the name of the container. It is a string parameter with a default value of "backend-flask".

- TaskFamily: Represents the family name of the task. It is a string parameter with a default value of "backend-flask".

- ServiceName: Represents the name of the service. It is a string parameter with a default value of "backend-flask".

- EnvOtelServiceName: Represents the environment variable for the OpenTelemetry service name. It is a string parameter with a default value of "backend-flask".

- EnvOtelExporterOtlpEndpoint: Represents the environment variable for the OpenTelemetry exporter OTLP (OpenTelemetry Protocol) endpoint. It is a string parameter with a default value of "https://api.honeycomb.io".

- EnvAwsCognitoUserPoolId: Represents the environment variable for the AWS Cognito user pool ID. It is a string parameter with a default value of "us-east-1_5SN7XhsT0".

- EnvAwsCognitoUserPoolClientId: Represents the environment variable for the AWS Cognito user pool client ID. It is a string parameter with a default value of "4em6p32irpbr10ujcn3svhsdm4".

- EnvFrontendUrl: Represents the environment variable for the frontend URL. It is a string parameter with a default value of "https://cruddur.pl".

- EnvBackendUrl: Represents the environment variable for the backend URL. It is a string parameter with a default value of "https://api.cruddur.pl".

- SecretsAWSAccessKeyId: Represents the AWS SSM (Systems Manager) parameter ARN for the backend-flask AWS access key ID. It is a string parameter with a default value of "'arn:aws:ssm:us-east-1:928597128531:parameter/cruddur/backend-flask/AWS_ACCESS_KEY_ID'".

- SecretsSecretAccessKey: Represents the AWS SSM parameter ARN for the backend-flask AWS secret access key


```
Resources:
  FargateService:
    Type: AWS::ECS::Service
    Properties:
      Cluster: 
        Fn::ImportValue:
          !Sub "${ClusterStack}ClusterName"
      DeploymentController:
       Type: ECS
      DesiredCount: 1
      EnableECSManagedTags: true
      EnableExecuteCommand: true
      HealthCheckGracePeriodSeconds: 0
      LaunchType: FARGATE
      LoadBalancers:
        - TargetGroupArn:
            Fn::ImportValue:
              !Sub "${ClusterStack}BackendTGArn"
          ContainerName: 'backend-flask'
          ContainerPort: !Ref ContainerPort
      NetworkConfiguration:
        AwsvpcConfiguration:
          AssignPublicIp: 'ENABLED'
          SecurityGroups:
            - Fn::ImportValue:
                !Sub "${ClusterStack}ServiceSecurityGroupId"
          Subnets:
            Fn::Split:
              - ","
              - Fn::ImportValue:
                  !Sub "${NetworkingStack}PublicSubnetIds"
      PlatformVersion: LATEST
      PropagateTags: SERVICE
      ServiceConnectConfiguration:
        Enabled: true
        Namespace: "cruddur"
        Services:
          - DiscoveryName: backend-flask
            PortName: backend-flask
            ClientAliases:
              - Port: !Ref ContainerPort
      ServiceName: !Ref ServiceName
      TaskDefinition: !Ref TaskDefinition
```

 This code defines a resource of type AWS::ECS::Service called FargateService. This resource creates and configures an ECS (Elastic Container Service) service to run on AWS Fargate.
 
- Cluster: Specifies the ECS cluster where the service will be deployed. The value is obtained by importing the output value of the ${ClusterStack}ClusterName CloudFormation export.

- DeploymentController: Specifies the deployment controller type for the service. In this case, it is set to ECS, indicating the default ECS deployment controller.

- DesiredCount: Sets the desired number of tasks (containers) to run for the service. In this case, it is set to 1.

- EnableECSManagedTags: Enables ECS to manage tags for the service.

- EnableExecuteCommand: Enables the ECS ExecuteCommand feature, allowing running commands in the running containers of the service.

- HealthCheckGracePeriodSeconds: Sets the grace period in seconds before performing health checks on new container instances. In this case, it is set to 0, indicating immediate health checks.

- LaunchType: Specifies the launch type for the tasks. In this case, it is set to FARGATE, indicating that the tasks will run on AWS Fargate.

- LoadBalancers: Configures the load balancer settings for the service. It specifies the target group ARN to associate with the service, the container name to forward traffic to (backend-flask), and the container port to use, which is obtained from the ContainerPort parameter.

- NetworkConfiguration: Configures the network settings for the service. It uses the AWS VPC (Virtual Private Cloud) configuration with an assigned public IP. It specifies the security group ID obtained from the CrdClusterServiceSecurityGroupId export and the subnet IDs obtained from the CrdNetworkPublicSubnetIds export.

- PlatformVersion: Specifies the platform version to use for Fargate tasks. In this case, it is set to LATEST.

- PropagateTags: Specifies how tags are propagated to the resources created by the service. In this case, it is set to SERVICE, indicating that tags are propagated to the ECS service.

- ServiceConnectConfiguration: Enables service discovery and sets the configuration for connecting to the service. It specifies the service discovery namespace, service name, and port name. It also configures client aliases for the service, which includes the port obtained from the ContainerPort parameter.

- ServiceName: Specifies the name of the ECS service. The value is obtained from the ServiceName parameter.

- TaskDefinition: Specifies the task definition to use for the service. The value is obtained from the TaskDefinition parameter, which is a reference to a separate task definition resource defined in the CloudFormation template.


```
 TaskDefinition:
    Type: AWS::ECS::TaskDefinition
    Properties:
      Family: !Ref TaskFamily
      ExecutionRoleArn: !GetAtt ExecutionRole.Arn
      TaskRoleArn: !GetAtt TaskRole.Arn
      NetworkMode: awsvpc
      Cpu: !Ref ServiceCpu
      Memory: !Ref ServiceMemory
      RequiresCompatibilities:
        - FARGATE
      ContainerDefinitions:
        - Name: xray
          Image: public.ecr.aws/xray/aws-xray-daemon
          Essential: true
          User: '1337'
          PortMappings:
            - Name: xray
              ContainerPort: 2000
              Protocol: udp
        - Name: !Ref ContainerName
          Image: !Ref EcrImage
          Essential: true
          HealthCheck:
            Command:
              - CMD-SHELL
              - python /backend-flask/bin/health-check
            Interval: 30
            Timeout: 5
            Retries: 3
            StartPeriod: 60
          PortMappings:
            - Name: backend-flask
              ContainerPort: !Ref ContainerPort
              Protocol: tcp
              AppProtocol: http
          LogConfiguration:
            LogDriver: awslogs
            Options:
              awslogs-group: cruddur
              awslogs-region: !Ref AWS::Region
              awslogs-stream-prefix: !Ref ServiceName
          Environment:
            - Name: OTEL_SERVICE_NAME
              Value: !Ref EnvOtelServiceName
            - Name: OTEL_EXPORTER_OTLP_ENDPOINT
              Value: !Ref EnvOtelExporterOtlpEndpoint
            - Name: AWS_COGNITO_USER_POOL_ID
              Value: !Ref EnvAwsCognitoUserPoolId
            - Name: AWS_COGNITO_USER_POOL_CLIENT_ID
              Value: !Ref EnvAwsCognitoUserPoolClientId
            - Name: FRONTEND_URL
              Value: !Ref EnvFrontendUrl
            - Name: BACKEND_URL
              Value: !Ref EnvBackendUrl
            - Name: AWS_DEFAULT_REGION
              Value: !Ref AWS::Region
          Secrets:
            - Name: AWS_ACCESS_KEY_ID
              ValueFrom: !Ref SecretsAWSAccessKeyId
            - Name: AWS_SECRET_ACCESS_KEY
              ValueFrom: !Ref SecretsSecretAccessKey
            - Name: CONNECTION_URL
              ValueFrom: !Ref SecretsConnectionUrl
            - Name: ROLLBAR_ACCESS_TOKEN
              ValueFrom: !Ref SecretsRollbarAccessToken
            - Name: OTEL_EXPORTER_OTLP_HEADERS
              ValueFrom: !Ref SecretsOtelExporterOltpHeaders
```

This section defines a resource of type AWS::ECS::TaskDefinition called TaskDefinition. This resource defines the configuration for an ECS task definition, which describes how a Docker container should be launched and run within an ECS service.

- Family: Specifies the family name of the task definition. The value is obtained from the TaskFamily parameter.

- ExecutionRoleArn: Specifies the Amazon Resource Name (ARN) of the IAM role used for executing the task. The !GetAtt function retrieves the ARN of the ExecutionRole resource.

- TaskRoleArn: Specifies the ARN of the IAM role that the task assumes when it runs. The !GetAtt function retrieves the ARN of the TaskRole resource.

- NetworkMode: Specifies the networking mode for the task. In this case, it is set to awsvpc, which allows the task to use the AWS VPC networking mode.

- Cpu: Specifies the CPU units to allocate to the task. The value is obtained from the ServiceCpu parameter.

- Memory: Specifies the memory to allocate to the task. The value is obtained from the ServiceMemory parameter.

- RequiresCompatibilities: Specifies the launch types that the task is compatible with. In this case, it is set to FARGATE, indicating compatibility with AWS Fargate.

- ContainerDefinitions: Defines the list of containers within the task.

      a. xray container:

        - Name: Specifies the name of the container as xray.
        - Image: Specifies the Docker image to use for the container, which is the AWS X-Ray daemon.
        - Essential: Specifies whether the container is essential for the task. It is set to true.
        - User: Specifies the user inside the container as '1337'.
        - PortMappings: Specifies the port mappings for the container, specifically port 2000 using UDP protocol.
 
      b. backend-flask container:

        - Name: Specifies the name of the container, which is obtained from the ContainerName parameter.
        - Image: Specifies the Docker image to use for the container, which is obtained from the EcrImage parameter.
        - Essential: Specifies whether the container is essential for the task. It is set to true.
        - HealthCheck: Specifies the health check configuration for the container. It runs a command (python /backend-flask/bin/health-check) and checks the response.
        - PortMappings: Specifies the port mappings for the container, using the value of the ContainerPort parameter as the container port and setting the protocol to TCP.
        - AppProtocol: Specifies the application protocol as HTTP.
        - LogConfiguration: Configures the logging for the container, using AWS CloudWatch Logs as the log driver. It specifies the log group name, AWS region, and stream prefix based on the ServiceName parameter.
        - Environment: Specifies the environment variables for the container. It sets various environment variables using the values obtained from the corresponding parameters.
        - Secrets: Specifies the secrets to be injected into the container. It retrieves the values from the respective AWS SSM (Systems Manager) parameters using the ValueFrom property.


```
  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: 'CruddurServiceExecutionRole'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal: 
              Service: 'ecs-tasks.amazonaws.com'
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: cruddur-execution-policy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Sid: VisualEditor0
                Effect: Allow
                Action:
                  - ecr:GetAuthorizationToken
                  - ecr:BatchCheckLayerAvailability
                  - ecr:GetDownloadUrlForLayer
                  - ecr:BatchGetImage
                  - logs:CreateLogStream
                  - logs:PutLogEvents
                Resource: "*"
              - Sid: VisualEditor1
                Effect: Allow
                Action:
                  - ssm:GetParameters
                  - ssm:GetParameter
                Resource: !Sub 'arn:${AWS::Partition}:ssm:${AWS::Region}:${AWS::AccountId}:parameter/cruddur/${ServiceName}/*'
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/CloudWatchLogsFullAccess

  
  TaskRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: 'CruddurServiceTaskRole'
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal: 
              Service: 'ecs-tasks.amazonaws.com'
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: cruddur-task-policy
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Sid: VisualEditor0
                Effect: Allow
                Action:
                  - ssmmessages:CreateControlChannel
                  - ssmmessages:CreateDataChannel
                  - ssmmessages:OpenControlChannel
                  - ssmmessages:OpenDataChannel
                Resource: "*"
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/CloudWatchLogsFullAccess
        - arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess

```

ExecutionRole and TaskRole. These roles are used by ECS tasks to grant necessary permissions and access within the AWS environment.

ExecutionRole:

  - Type: Specifies the resource type as AWS::IAM::Role.
  - RoleName: Specifies the name of the role as 'CruddurServiceExecutionRole'.
  - AssumeRolePolicyDocument: Defines the IAM policy that allows the ECS service to assume this role. It permits the 'ecs-tasks.amazonaws.com' service to assume the role.
  - Policies: Specifies the policies attached to the role.
  - PolicyName: Specifies the name of the policy as 'cruddur-execution-policy'.
  - PolicyDocument: Defines the IAM policy document that specifies the permissions for the execution role. It allows various actions related to Amazon ECR (Elastic Container Registry) and AWS CloudWatch Logs.
  - ManagedPolicyArns: Specifies the ARNs of managed policies to be attached to the role. In this case, it includes the CloudWatchLogsFullAccess policy.
  
TaskRole:

  - Type: Specifies the resource type as AWS::IAM::Role.
  - RoleName: Specifies the name of the role as 'CruddurServiceTaskRole'.
  - AssumeRolePolicyDocument: Defines the IAM policy that allows the ECS service to assume this role. It permits the 'ecs-tasks.amazonaws.com' service to assume the role.
  - Policies: Specifies the policies attached to the role.
  - PolicyName: Specifies the name of the policy as 'cruddur-task-policy'.
  - PolicyDocument: Defines the IAM policy document that specifies the permissions for the task role. It allows actions related to AWS Systems Manager (SSM) to manage message channels.
  - ManagedPolicyArns: Specifies the ARNs of managed policies to be attached to the role. In this case, it includes the CloudWatchLogsFullAccess and AWSXRayDaemonWriteAccess policies.

```
Outputs:
  ServiceName:
    Value: !GetAtt  FargateService.Name
    Export:
      Name: !Sub "${AWS::StackName}ServiceName"
```
The code defines an output named ServiceName.

- Value: Specifies the value of the output. In this case, it uses the !GetAtt function to retrieve the Name attribute of the FargateService.
- Export: Specifies that the output should be exported, making it available for other CFn stacks or resources to reference.
- Name: Specifies the name of the export. It uses the !Sub function to substitute ${AWS::StackName} with the actual name of the stack. The AWS::StackName pseudo parameter represents the name of the current stack.
