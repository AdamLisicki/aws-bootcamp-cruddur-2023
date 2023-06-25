# Week 11 — CloudFormation Part 2

## CFN Service Layer
This CloudFormation tamplate creates:

- Task Definition File
- Fargate Service
- Execution Role
- Task Role

config.toml
```
[deploy]
bucket = 'cfn-artifacts-cruddur'
region = 'us-east-1'
stack_name = 'CrdSrvBackendFlask'
```

Deployment script. This script uses cfn-toml to get properties and parameters from config.toml file and execute CloudFormation template.

```
#! /usr/bin/bash

set -e

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/service/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/service/config.toml"

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
# PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix service \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-backend-flask \
  --capabilities CAPABILITY_NAMED_IAM
#   --parameter-overrides $PARAMETERS \
  
```


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


## CFN RDS

 The primary Postgres RDS Database for the application
 - RDS Instance
 - Database Security Group
 - DBSubnetGroup

config.toml
```
[deploy]
bucket = 'cfn-artifacts-cruddur'
region = 'us-east-1'
stack_name = 'CrdDb'

[parameters]
NetworkingStack = 'CrdNet'
ClusterStack = 'CrdCluster'
MasterUsername = 'cruddurroot'
```

Deployment script. This script uses cfn-toml to get deploy properties and parameters from config.toml file and execute CloudFormation template.

```
#! /usr/bin/bash

set -e

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/db/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/db/config.toml"

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix db \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-db \
  --parameter-overrides $PARAMETERS MasterUserPassword=$DB_PASSWORD \
  --capabilities CAPABILITY_NAMED_IAM
```

Parameters

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
  BackupRetentionPeriod:
    Type: Number
    Default: 0
  DBInstanceClass:
    Type: String
    Default: db.t4g.micro
  DBInstanceIdentifier:
    Type: String
    Default: cruddur-instance
  DBName:
    Type: String
    Default: cruddur
  DeletionProtection:
    Type: String
    AllowedValues:
      - true
      - false
    Default: true
  EngineVersion:
    Type: String
    Default: '15.2'
  MasterUsername:
    Type: String
  MasterUserPassword:
    Type: String
    NoEcho: true
```


- NetworkingStack: This parameter is of type String and is used to specify the base layer of networking components, such as VPC (Virtual Private Cloud) and subnets. The default value is set to "CrdNet".

- ClusterStack: This parameter is of type String and is used to specify the cluster layer components, such as an ECS (Elastic Container Service) cluster and an ALB (Application Load Balancer). The default value is set to "CrdCluster".

- BackupRetentionPeriod: This parameter is of type Number and is used to specify the number of days to retain automated backups of the database. The default value is set to 0, which means no backups are retained.

- DBInstanceClass: This parameter is of type String and is used to specify the AWS RDS (Relational Database Service) instance class for the database. The default value is set to "db.t4g.micro", which represents a small, general-purpose instance.

- DBInstanceIdentifier: This parameter is of type String and is used to specify the identifier for the database instance. The default value is set to "cruddur-instance".

- DBName: This parameter is of type String and is used to specify the name of the database. The default value is set to "cruddur".

- DeletionProtection: This parameter is of type String and allows only two values: "true" or "false". It is used to enable or disable deletion protection for the database instance. The default value is set to "true", meaning deletion protection is enabled.

- EngineVersion: This parameter is of type String and is used to specify the version of the database engine. The default value is set to "15.2".

- MasterUsername: This parameter is of type String and is used to specify the username for the master user of the database. The value for this parameter is not set as a default, so it must be provided during stack deployment.

- MasterUserPassword: This parameter is of type String and is used to specify the password for the master user of the database. The value is marked as NoEcho: true, which means the password will be hidden during stack deployment.

```
Resources:
  RDSPostgresSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}RDSSG"
      GroupDescription: Public Facing SG for our Cruddur ALB
      VpcId:
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          SourceSecurityGroupId:
            Fn::ImportValue:
              !Sub ${ClusterStack}ServiceSecurityGroupId
          FromPort: 5432
          ToPort: 5432
          Description: ALB HTTP
```

This CloudFormation template code defines a resource named "RDSPostgresSG", which is an AWS EC2 security group.

- "GroupName": It sets the name of the security group using the !Sub function, which substitutes variables with their corresponding values. In this case, ${AWS::StackName} represents the name of the CloudFormation stack, and "RDSSG" is appended to it.

- "GroupDescription": It provides a description for the security group, stating that it is a public-facing security group for the "Cruddur" Application Load Balancer (ALB).

- "VpcId": It specifies the VPC ID for the security group. The !Sub function is used along with Fn::ImportValue to import the value of ${NetworkingStack}VpcId from another CloudFormation stack. This allows the security group to be associated with the VPC defined in the "NetworkingStack" stack.

- "SecurityGroupIngress": It defines the ingress rules for the security group, specifying the inbound traffic allowed. In this case, there is a single ingress rule defined:

- "IpProtocol": It sets the protocol to TCP.

- "SourceSecurityGroupId": It uses the Fn::ImportValue function along with !Sub to import the value of ${ClusterStack}ServiceSecurityGroupId from another CloudFormation stack. This means that the security group allows incoming traffic from the security group associated with the service defined in the "ClusterStack" stack.

- "FromPort" and "ToPort": They define the range of ports allowed for the inbound traffic. In this case, it is port 5432, which is commonly used for PostgreSQL database connections.

- "Description": It provides a description for the ingress rule, stating that it allows ALB HTTP traffic

```
  DBSubnetGroup:
    Type: AWS::RDS::DBSubnetGroup
    Properties:
      DBSubnetGroupName: !Sub "${AWS::StackName}DBSubnetGroup"
      DBSubnetGroupDescription: !Sub "${AWS::StackName}DBSubnetGroup"
      SubnetIds: { 'Fn::Split' : [ ','  , { "Fn::ImportValue": { "Fn::Sub": "${NetworkingStack}PublicSubnetIds" }}] }
```

This CloudFormation template code defines a resource named "DBSubnetGroup" of type "AWS::RDS::DBSubnetGroup".

The "DBSubnetGroup" resource is used to create a subnet group for an Amazon RDS database. A subnet group is a collection of subnets in a VPC (Virtual Private Cloud) that can be used for deploying a multi-AZ (Availability Zone) RDS database.

- "DBSubnetGroupName": It sets the name of the DB subnet group using the !Sub function. The ${AWS::StackName} represents the name of the CloudFormation stack, and "DBSubnetGroup" is appended to it. This ensures that the subnet group has a unique name based on the stack name.

- "DBSubnetGroupDescription": It provides a description for the DB subnet group using the !Sub function. The ${AWS::StackName} represents the name of the CloudFormation stack, and the same value is used as the description. Again, this ensures a unique description based on the stack name.

- "SubnetIds": It specifies the subnet IDs that should be included in the subnet group. The Fn::Split function is used along with Fn::ImportValue and Fn::Sub to split and import the subnet IDs from another CloudFormation stack. The ${NetworkingStack}PublicSubnetIds represents the exported value of subnet IDs from the "NetworkingStack" stack. The subnet IDs are split using the comma (',') delimiter.

```
  Database:
    Type: AWS::RDS::DBInstance
    DeletionPolicy: 'Snapshot'
    UpdateReplacePolicy: 'Snapshot'
    Properties:
      AllocatedStorage: '20'
      AllowMajorVersionUpgrade: true
      AutoMinorVersionUpgrade: true
      BackupRetentionPeriod: !Ref BackupRetentionPeriod
      DBInstanceClass: !Ref DBInstanceClass
      DBInstanceIdentifier: !Ref DBInstanceIdentifier
      DBName: !Ref  DBName
      DBSubnetGroupName: !Ref DBSubnetGroup
      DeletionProtection: !Ref DeletionProtection
      EnablePerformanceInsights: true
      Engine: postgres
      EngineVersion: !Ref EngineVersion
      MasterUsername: !Ref MasterUsername
      MasterUserPassword: !Ref MasterUserPassword
      PubliclyAccessible: true
      VPCSecurityGroups:
        - !GetAtt RDSPostgresSG.GroupId

```

This CloudFormation template code creates a resource named "Database" of type "AWS::RDS::DBInstance".

- "DeletionPolicy" and "UpdateReplacePolicy": These properties specify the deletion and update policies for the database instance. In this case, "Snapshot" is used for both, indicating that when the stack is deleted or updated, a final snapshot of the database instance should be created.

- "AllocatedStorage": It specifies the amount of storage allocated for the database instance. The value is set to '20', indicating 20 GB of storage.

- "AllowMajorVersionUpgrade" and "AutoMinorVersionUpgrade": These properties control whether major and minor version upgrades are allowed for the database instance. Both are set to true, allowing automatic upgrades to the latest available versions.

- "BackupRetentionPeriod": It references the value of the parameter "BackupRetentionPeriod" using the !Ref function. The value of this parameter specifies the number of days to retain automated backups for the database instance.

- "DBInstanceClass": It references the value of the parameter "DBInstanceClass" using the !Ref function. The value of this parameter specifies the instance class for the database instance, determining its computational and memory capacity.

- "DBInstanceIdentifier": It references the value of the parameter "DBInstanceIdentifier" using the !Ref function. The value of this parameter specifies the unique identifier for the database instance.

- "DBName": It references the value of the parameter "DBName" using the !Ref function. The value of this parameter specifies the name of the database.

- "DBSubnetGroupName": It references the value of the resource "DBSubnetGroup" using the !Ref function. The value of this parameter specifies the DB subnet group to associate with the database instance, ensuring it is deployed in the specified subnets.

- "DeletionProtection": It references the value of the parameter "DeletionProtection" using the !Ref function. The value of this parameter specifies whether deletion protection should be enabled for the database instance.

- "EnablePerformanceInsights": It enables the performance insights feature for the database instance, allowing monitoring and analysis of database performance.

- "Engine": It specifies the database engine to use. In this case, "postgres" is used, indicating PostgreSQL.

- "EngineVersion": It references the value of the parameter "EngineVersion" using the !Ref function. The value of this parameter specifies the version of the database engine to use.

- "MasterUsername" and "MasterUserPassword": These properties reference the values of the parameters "MasterUsername" and "MasterUserPassword" using the !Ref function. These parameters provide the username and password for the master user of the database instance.

- "PubliclyAccessible": It sets whether the database instance is publicly accessible. In this case, it is set to true, allowing access from the internet.

- "VPCSecurityGroups": It specifies the security groups to associate with the database instance. In this case, it uses the !GetAtt function to retrieve the GroupId attribute of the "RDSPostgresSG" resource, which represents the security group created earlier. This allows the database instance to be associated with the security group.


# SAM CFN DynamoDB, Lambda

This CloudFormation tempalte creates:
   - DynamoDB Table
  - DynamoDB Stream

config.toml

```
version=0.1
[default.build.parameters]
region = "us-east-1"

[default.package.parameters]
region = "us-east-1"

[default.deploy.parameters]
region = "us-east-1"
```

build scirpt:
  sam build \ ...: This command uses the SAM CLI to build the serverless application. It performs the following actions:
    --use-container: This flag instructs SAM to use a Docker container for building the application, ensuring consistent and isolated builds.
    --config-file $CONFIG_PATH: This flag specifies the path to the SAM configuration file.
    --template $TEMPLATE_PATH: This flag specifies the path to the SAM template file.
    --base-dir $FUNC_DIR: This flag specifies the base directory where the Lambda functions for the application are located.
    
The sam build command essentially compiles the code, resolves dependencies, and prepares the application for deployment.

```
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

FUNC_DIR="/workspace/aws-bootcamp-cruddur-2023/ddb/function"
TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/ddb/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/ddb/config.toml"

sam validate -t $TEMPLATE_PATH

echo "== build"

sam build \
--use-container \
--config-file $CONFIG_PATH \
--template $TEMPLATE_PATH \
--base-dir $FUNC_DIR
#--parameter-overrides
```

package script:

sam package \ ...: This command uses the SAM CLI to package the serverless application. It performs the following actions:
  --s3-bucket $ARTIFACT_BUCKET: This flag specifies the S3 bucket where the packaged artifacts will be stored.
  --config-file $CONFIG_PATH: This flag specifies the path to the SAM configuration file.
  --output-template-file $OUTPUT_TEMPLATE_PATH: This flag specifies the path where the packaged SAM template file will be generated.
  --template-file $TEMPLATE_PATH: This flag specifies the path to the built SAM template file.
  --s3-prefix "ddb": This flag specifies a prefix to be used when storing artifacts in the S3 bucket. In this case, the prefix is set to "ddb".
The sam package command takes the built SAM template, resolves dependencies, and generates a packaged template that is ready for deployment. It also uploads the packaged artifacts to the specified S3 bucket.

```
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

ARTIFACT_BUCKET="cfn-artifacts-cruddur"
TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/template.yaml"
OUTPUT_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/ddb/config.toml"

echo "== package"

sam package \
  --s3-bucket $ARTIFACT_BUCKET \
  --config-file $CONFIG_PATH \
  --output-template-file $OUTPUT_TEMPLATE_PATH \
  --template-file $TEMPLATE_PATH \
  --s3-prefix "ddb"
```

deploy script:

sam deploy \ ...: This command uses the SAM CLI to deploy the serverless application. It performs the following actions:
  --template-file $PACKAGED_TEMPLATE_PATH: This flag specifies the path to the packaged SAM template file.
  --config-file $CONFIG_PATH: This flag specifies the path to the SAM configuration file.
  --stack-name "CrdDdb": This flag specifies the name of the CloudFormation stack to create or update during the deployment. In this case, the stack name is set to "CrdDdb".
  --tags group=cruddur-ddb: This flag specifies tags to associate with the CloudFormation stack. In this case, a tag with the key "group" and the value "cruddur-ddb" is set.
  --no-execute-changeset: This flag indicates that the CloudFormation changeset should not be executed immediately. It allows for a manual review of the changes before proceeding with the deployment.
  --capabilities "CAPABILITY_NAMED_IAM": This flag specifies the capabilities required for the deployment. In this case, the "CAPABILITY_NAMED_IAM" capability is enabled, which allows the creation of named IAM resources during the deployment.
The sam deploy command uses the packaged SAM template and the provided configuration to create or update the CloudFormation stack associated with the serverless application.

```
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

PACKAGED_TEMPLATE_PATH="/workspace/aws-bootcamp-cruddur-2023/.aws-sam/build/packaged.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/ddb/config.toml"

echo "== deploy"

sam deploy \
  --template-file $PACKAGED_TEMPLATE_PATH  \
  --config-file $CONFIG_PATH \
  --stack-name "CrdDdb" \
  --tags group=cruddur-ddb \
  --no-execute-changeset \
  --capabilities "CAPABILITY_NAMED_IAM"
```

Parameters

```
Parameters:
  PythonRuntime:
    Type: String
    Default: python3.9
  MemorySize:
    Type: String
    Default: 128
  Timeout:
    Type: Number
    Default: 3
  DeletionProtectionEnabled:
    Type: String
    Default: false
```

- PythonRuntime: This parameter is of type String and specifies the Python runtime version to be used for the serverless application. The default value is set to "python3.9".

- MemorySize: This parameter is of type String and specifies the memory size allocated to the serverless function. The default value is set to "128".

- Timeout: This parameter is of type Number and specifies the timeout duration for the serverless function in seconds. The default value is set to "3".

- DeletionProtectionEnabled: This parameter is of type String and specifies whether deletion protection is enabled for the resources created by the CloudFormation stack. The default value is set to "false".

```
Resources:
  DynamoDBTable:
    Type: AWS::DynamoDB::Table
    Properties: 
      AttributeDefinitions: 
        - AttributeName: message_group_uuid
          AttributeType: S
        - AttributeName: pk
          AttributeType: S
        - AttributeName: sk
          AttributeType: S
      KeySchema: 
        - AttributeName: pk
          KeyType: HASH
        - AttributeName: sk
          KeyType: RANGE
      ProvisionedThroughput: 
        ReadCapacityUnits: 5
        WriteCapacityUnits: 5
      TableClass: STANDARD
      BillingMode: PROVISIONED
      DeletionProtectionEnabled: !Ref DeletionProtectionEnabled
      GlobalSecondaryIndexes:
        - IndexName: message-group-sk-index
          KeySchema:
            - AttributeName: message_group_uuid
              KeyType: HASH
            - AttributeName: sk
              KeyType: RANGE
          Projection: 
            ProjectionType: ALL
          ProvisionedThroughput:
            ReadCapacityUnits: 5
            WriteCapacityUnits: 5
      StreamSpecification:
        StreamViewType: NEW_IMAGE
```

This code defines a DynamoDB table resource.

- AttributeDefinitions: This property defines the attribute schema of the table. It specifies three attributes: "message_group_uuid", "pk", and "sk", along with their respective attribute types.

- KeySchema: This property defines the primary key schema of the table. It specifies that the "pk" attribute is the hash key (KeyType: HASH), and the "sk" attribute is the range key (KeyType: RANGE).

- ProvisionedThroughput: This property specifies the provisioned throughput capacity for the table. The ReadCapacityUnits and WriteCapacityUnits are both set to 5, indicating 5 units of read capacity and 5 units of write capacity.

- TableClass: This property sets the table class to "STANDARD", which means it uses the standard storage type.

- BillingMode: This property sets the billing mode for the table to "PROVISIONED", indicating that provisioned capacity is used.

- DeletionProtectionEnabled: This property is set to the value of the parameter "DeletionProtectionEnabled" using the intrinsic function !Ref. It determines whether deletion protection is enabled for the table.

- GlobalSecondaryIndexes: This property defines a global secondary index (GSI) for the table. It specifies the index name, key schema (with "message_group_uuid" as the hash key and "sk" as the range key), projection type (ALL), and provisioned throughput capacity.

- StreamSpecification: This property specifies that the table should have a stream enabled with a StreamViewType of "NEW_IMAGE", which means it captures the new item image when a change is made to the table.

```
  ProcessDynamoDBStream:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: .
      PackageType: Zip
      Handler: lambda_handler
      Runtime: !Ref PythonRuntime
      Role: !GetAtt ExecutionRole.Arn
      MemorySize: !Ref MemorySize
      Timeout: !Ref Timeout
      Events:
        Stream:
          Type: DynamoDB
          Properties:
            Stream: !GetAtt DynamoDBTable.StreamArn
            BatchSize: 1
            StartingPosition: LATEST
```

This code defines a serverless function resource named "ProcessDynamoDBStream".

- Type: AWS::Serverless::Function: This property sets the resource type to AWS Serverless Function, indicating that it represents a serverless function in AWS Lambda.

- CodeUri: This property specifies the location of the function code. In this case, it is set to "." indicating that the code is located in the same directory as the CloudFormation template.

- PackageType: This property specifies the package type of the function. Here, it is set to "Zip" indicating that the code is packaged as a ZIP file.

- Handler: This property specifies the entry point for the function code. In this case, it is set to "lambda_handler", which is the name of the function that will be invoked when the Lambda function is triggered.

- Runtime: This property is set to the value of the parameter "PythonRuntime" using the intrinsic function !Ref. It specifies the runtime for the function, which will be determined based on the value provided for the "PythonRuntime" parameter.

- Role: This property is set to the ARN (Amazon Resource Name) of the "ExecutionRole" resource using the intrinsic function !GetAtt. It specifies the IAM role that will be assumed by the function to access AWS resources.

- MemorySize: This property is set to the value of the parameter "MemorySize" using the intrinsic function !Ref. It specifies the memory size allocated to the function, which will be determined based on the value provided for the "MemorySize" parameter.

- Timeout: This property is set to the value of the parameter "Timeout" using the intrinsic function !Ref. It specifies the maximum execution time for the function in seconds, which will be determined based on the value provided for the "Timeout" parameter.

- Events: This property specifies the events that trigger the function. In this case, there is a single event named "Stream" of type "DynamoDB". It is configured with the properties "Stream" set to the ARN of the DynamoDB table stream using the intrinsic function !GetAtt, "BatchSize" set to 1 indicating processing one record at a time, and "StartingPosition" set to "LATEST" indicating that the function should process new events as they arrive.

```
  LambdaLogGroup:
    Type: "AWS::Logs::LogGroup"
    Properties:
      LogGroupName: "/aws/lambda/cruddur-messaging-stream00"
      RetentionInDays: 14
  LambdaLogStream:
    Type: "AWS::Logs::LogStream"
    Properties:
      LogGroupName: !Ref LambdaLogGroup
      LogStreamName: "LambdaExecution"
  ExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: CruddurDdbStreamExecRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal:
              Service: 'lambda.amazonaws.com'
            Action: 'sts:AssumeRole'
      Policies:
        - PolicyName: "LambdaExecutionPolicy"
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: "Allow"
                Action: "logs:CreateLogGroup"
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:*"
              - Effect: "Allow"
                Action:
                  - "logs:CreateLogStream"
                  - "logs:PutLogEvents"
                Resource: !Sub "arn:aws:logs:${AWS::Region}:${AWS::AccountId}:log-group:${LambdaLogGroup}:*"
              - Effect: "Allow"
                Action:
                  - "ec2:CreateNetworkInterface"
                  - "ec2:DeleteNetworkInterface"
                  - "ec2:DescribeNetworkInterfaces"
                Resource: "*"
              - Effect: "Allow"
                Action:
                  - "lambda:InvokeFunction"
                Resource: "*"
              - Effect: "Allow"
                Action:
                  - "dynamodb:DescribeStream"
                  - "dynamodb:GetRecords"
                  - "dynamodb:GetShardIterator"
                  - "dynamodb:ListStreams"
                Resource: "*"
```

LambdaLogGroup:

  - Type: "AWS::Logs::LogGroup": This resource defines an AWS CloudWatch Logs log group.
    Properties:
      - LogGroupName: Specifies the name of the log group as "/aws/lambda/cruddur-messaging-stream00".
      - RetentionInDays: Sets the retention period for log events in the log group to 14 days.
     
LambdaLogStream:

  - Type: "AWS::Logs::LogStream": This resource defines an AWS CloudWatch Logs log stream.
    Properties:
      - LogGroupName: Refers to the LogGroupName property of the LambdaLogGroup resource using the intrinsic function !Ref.
      - LogStreamName: Specifies the name of the log stream as "LambdaExecution".

ExecutionRole:

  - Type: AWS::IAM::Role: This resource defines an IAM role.
    Properties:
      - RoleName: Specifies the name of the role as "CruddurDdbStreamExecRole".
      - AssumeRolePolicyDocument: Defines the trust policy for the role, allowing the Lambda service to assume this role.
      - Policies: Specifies the policies associated with the role.
      - PolicyName: Sets the name of the policy as "LambdaExecutionPolicy".
      - PolicyDocument: Defines the permissions granted by the policy.
          - The policy allows actions such as creating log groups, creating log streams, putting log events, and accessing network interfaces.
          - It also allows invoking Lambda functions and performing operations on DynamoDB streams.

## CFN CICD

This CloudFormation template creates:
  - CodeStar Connection V2 Github
  - CodePipeline
  - CodeBuild

config.toml

```
[deploy]
bucket = 'cfn-artifacts-cruddur'
region = 'us-east-1'
stack_name = 'CrdCicd'

[parameters]
ServiceStack = 'CrdSrvBackendFlask'
ClusterStack = 'CrdCluster'
GitHubBranch = 'prod'
GithubRepo = 'AdamLisicki/aws-bootcamp-cruddur-2023'
ArtifactBucketName = "codepipline-artifacts-cruddur"
```

Deployment script:
- PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH): This line executes the cfn-toml command to extract the parameters from the configuration file specified by the $CONFIG_PATH variable. The parameters are then stored in the PARAMETERS variable.

- BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH): This line executes the cfn-toml command to extract the value of the deploy.bucket key from the configuration file specified by the $CONFIG_PATH variable. The value is then stored in the BUCKET variable.

- REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH): This line executes the cfn-toml command to extract the value of the deploy.region key from the configuration file. The value represents the AWS region where the deployment will take place, and it is stored in the REGION variable.

- STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH): This line executes the cfn-toml command to extract the value of the deploy.stack_name key from the configuration file. The value represents the name of the CloudFormation stack, and it is stored in the STACK_NAME variable.

- aws cloudformation package \ ...: This command uses the AWS CLI's cloudformation package command to package the CloudFormation template and upload it to an S3 bucket. It performs the following actions:
  --template-file $CFN_PATH: This flag specifies the path to the original CloudFormation template.
  --s3-bucket $BUCKET: This flag specifies the name of the S3 bucket where the packaged template will be stored.
  --s3-prefix cicd-package: This flag specifies a prefix to be used when storing the packaged template in the S3 bucket. In this case, the prefix is set to "cicd-package".
  --region $REGION: This flag specifies the AWS region for the S3 bucket and the deployment.
  --output-template-file "$PACKAGED_PATH": This flag specifies the path where the packaged CloudFormation template will be generated.

- aws cloudformation deploy \ ...: This command uses the AWS CLI's cloudformation deploy command to deploy the CloudFormation stack. It performs the following actions:
  --stack-name $STACK_NAME: This flag specifies the name of the CloudFormation stack.
  --s3-bucket $BUCKET: This flag specifies the name of the S3 bucket where the packaged template is located.
  --s3-prefix cicd: This flag specifies a prefix to be used when referencing artifacts in the S3 bucket. In this case, the prefix is set to "cicd".
  --region $REGION: This flag specifies the AWS region for the deployment.
  --template-file "$PACKAGED_PATH": This flag specifies the path to the packaged CloudFormation template.
  --no-execute-changeset: This flag indicates that the CloudFormation changeset should not be executed immediately.
  --tags group=cruddur-cicd: This flag specifies tags to associate with the CloudFormation stack. In this case, a tag with the key "group" and the value "cruddur-cicd" is set.
  --parameter-overrides $PARAMETERS: This flag provides the extracted parameters from the configuration file to override any default parameter values.
  --capabilities CAPABILITY_NAMED_IAM: This flag specifies the capabilities required for the deployment. In this case, the "CAPABILITY_NAMED_IAM" capability is enabled.


```
#! /usr/bin/env bash
#set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cicd/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cicd/config.toml"
PACKAGED_PATH="/workspace/aws-bootcamp-cruddur-2023/tmp/packaged-template.yaml"
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)

# package
# -----------------
echo "== packaging CFN to S3..."
aws cloudformation package \
  --template-file $CFN_PATH \
  --s3-bucket $BUCKET \
  --s3-prefix cicd-package \
  --region $REGION \
  --output-template-file "$PACKAGED_PATH"

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix cicd \
  --region $REGION \
  --template-file "$PACKAGED_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cicd \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```

Parameters

```
Parameters:
  GitHubBranch:
    Type: String
    Default: prod
  GithubRepo:
    Type: String
    Default: 'AdamLisicki/aws-bootcamp-cruddur-2023'
  ClusterStack:
    Type: String
  ServiceStack:
    Type: String
  ArtifactBucketName:
    Type: String
```

- GitHubBranch: This parameter is of type string and has a default value of "prod". It is used to specify the branch name of a GitHub repository. By default, it assumes the branch to be "prod".

- GithubRepo: This parameter is of type string and has a default value of 'AdamLisicki/aws-bootcamp-cruddur-2023'. It represents the name of the GitHub repository that contains the source code for the application or infrastructure being deployed. The default value indicates the repository "aws-bootcamp-cruddur-2023" owned by the user "AdamLisicki".

- ClusterStack: This parameter is of type string. It is used to specify the name or identifier of an existing AWS CloudFormation stack that represents an ECS cluster. The ECS cluster is a logical group of EC2 instances running Docker containers.

- ServiceStack: This parameter is of type string. It is used to specify the name or identifier of an existing AWS CloudFormation stack that represents an ECS service. The ECS service manages and deploys the Docker containers on the ECS cluster.

- ArtifactBucketName: This parameter is of type string. It is used to specify the name of an S3 bucket where deployment artifacts or files are stored. The artifacts could include compiled code, configuration files, or any other files required for the deployment.

```
Resources:
  CodeBuildBakeImageStack:
    Type: AWS::CloudFormation::Stack
    Properties:
      TemplateURL: nested/codebuild.yaml
  CodeStarConnection:
    Type: AWS::CodeStarConnections::Connection
    Properties:
      ConnectionName: !Sub ${AWS::StackName}-connection
      ProviderType: GitHub
```

This CloudFormation (CFN) template creates two AWS resources:

- CodeBuildBakeImageStack: This resource creates an AWS CloudFormation stack using the AWS::CloudFormation::Stack resource type. It deploys a nested CloudFormation stack using the template specified by the TemplateURL property, which is set to "nested/codebuild.yaml". The "nested/codebuild.yaml" template likely contains the configuration for an AWS CodeBuild project that builds an image or artifact for your application.

- CodeStarConnection: This resource creates an AWS CodeStar Connections connection using the AWS::CodeStarConnections::Connection resource type. It establishes a connection between AWS CodeStar and a version control system, in this case, GitHub. The ConnectionName property uses the !Sub intrinsic function to substitute ${AWS::StackName}-connection, where ${AWS::StackName} represents the name of the current CloudFormation stack. This ensures that each connection created will have a unique name based on the stack name. The ProviderType property is set to "GitHub" to specify that the connection is for a GitHub repository.


```
  Pipeline:
    Type: AWS::CodePipeline::Pipeline
    Properties:
      ArtifactStore:
        Location: !Ref ArtifactBucketName
        Type: S3
      RoleArn: !GetAtt CodePipelineRole.Arn
      Stages:
        - Name: Source
          Actions:
            - Name: ApplicationSource
              RunOrder: 1
              ActionTypeId:
                Category: Source
                Provider: CodeStarSourceConnection
                Owner: AWS
                Version: '1'
              OutputArtifacts:
                - Name: Source
              Configuration:
                ConnectionArn: !Ref CodeStarConnection
                FullRepositoryId: !Ref GithubRepo
                BranchName: !Ref GitHubBranch
                OutputArtifactFormat: "CODE_ZIP"
        - Name: Build
          Actions:
            - Name: BuildContainerImage
              RunOrder: 1
              ActionTypeId:
                Category: Build
                Owner: AWS
                Provider: CodeBuild
                Version: '1'
              InputArtifacts:
                - Name: Source
              OutputArtifacts:
                - Name: ImageDefinition
              Configuration:
                ProjectName: !GetAtt CodeBuildBakeImageStack.Outputs.CodeBuildProjectName
                BatchEnabled: false
        - Name: Deploy
          Actions:
            - Name: Deploy
              RunOrder: 1
              ActionTypeId:
                Category: Deploy
                Provider: ECS
                Owner: AWS
                Version: '1'
              InputArtifacts:
                - Name: ImageDefinition
              Configuration:
                # In Minutes
                DeploymentTimeout: "10"
                ClusterName:
                  Fn::ImportValue:
                    !Sub ${ClusterStack}ClusterName
                ServiceName:
                  Fn::ImportValue:
                    !Sub ${ServiceStack}ServiceName
```

This CloudFormation (CFN) code creates an AWS CodePipeline pipeline.

- ArtifactStore: This section defines the artifact store for the pipeline. It specifies that the artifacts will be stored in an S3 bucket, and the bucket name is referenced by the ArtifactBucketName parameter.

- RoleArn: This property specifies the Amazon Resource Name (ARN) of the IAM role that CodePipeline will assume to perform pipeline actions. It uses the !GetAtt intrinsic function to get the ARN of the CodePipelineRole.

- Stages: This section defines the stages of the pipeline. A pipeline typically consists of one or more stages, and each stage contains one or more actions.
    - Source stage: This stage is responsible for retrieving the source code from a version control system, in this case, GitHub. The ApplicationSource action is configured to connect to the GitHub repository specified by GithubRepo parameter. The ConnectionArn property references the CodeStar connection created           earlier. The source code is stored as a Source output artifact.

    - Build stage: This stage is responsible for building the application or creating a container image. The BuildContainerImage action uses AWS CodeBuild to build the project. The ProjectName property references the CodeBuildBakeImageStack.Outputs.CodeBuildProjectName output from the CodeBuildBakeImageStack stack         created earlier. The source artifact from the previous stage is used as the input artifact, and the output artifact is named ImageDefinition.

    - Deploy stage: This stage is responsible for deploying the application or the container image. The Deploy action deploys the image to an ECS cluster. The cluster name and service name are obtained from the ClusterStack and ServiceStack stacks respectively using the Fn::ImportValue function.


```
  CodePipelineRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Statement:
        - Action: ['sts:AssumeRole']
          Effect: Allow
          Principal:
            Service: [codepipeline.amazonaws.com]
        Version: '2012-10-17'
      Path: /
      Policies:
        - PolicyName: !Sub ${AWS::StackName}EcsDeployPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - ecs:DescribeServices
                - ecs:DescribeTaskDefinition
                - ecs:DescribeTasks
                - ecs:ListTasks
                - ecs:RegisterTaskDefinition
                - ecs:UpdateService
                Effect: Allow
                Resource: "*"
        - PolicyName: !Sub ${AWS::StackName}CodeStarPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - codestar-connections:UseConnection
                Effect: Allow
                Resource:
                  !Ref CodeStarConnection
        - PolicyName: !Sub ${AWS::StackName}CodePipelinePolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - s3:*
                - logs:CreateLogGroup
                - logs:CreateLogStream
                - logs:PutLogEvents
                - cloudformation:*
                - iam:PassRole
                - iam:CreateRole
                - iam:DetachRolePolicy
                - iam:DeleteRolePolicy
                - iam:PutRolePolicy
                - iam:DeleteRole
                - iam:AttachRolePolicy
                - iam:GetRole
                - iam:PassRole
                Effect: Allow
                Resource: '*'
        - PolicyName: !Sub ${AWS::StackName}CodePipelineBuildPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Action:
                - codebuild:StartBuild
                - codebuild:StopBuild
                - codebuild:RetryBuild
                - codebuild:BatchGetBuilds
                Effect: Allow
                Resource: !Join
                  - ''
                  - - 'arn:aws:codebuild:'
                    - !Ref AWS::Region
                    - ':'
                    - !Ref AWS::AccountId
                    - ':project/'
                    - !GetAtt CodeBuildBakeImageStack.Outputs.CodeBuildProjectName
```

This CloudFormation (CFN) code creates an IAM role named CodePipelineRole. The role is used by AWS CodePipeline to perform various actions within the pipeline.

- AssumeRolePolicyDocument: This section defines the policy that specifies who can assume this IAM role. In this case, the codepipeline.amazonaws.com service is allowed to assume the role. This means that CodePipeline is granted permission to assume this role and perform actions on behalf of this role.

- Path: This property sets the path for the IAM role to "/". The path is a way to organize and manage IAM resources.

- Policies: This section defines the policies attached to the IAM role. The role has multiple policies with different sets of permissions:

    - EcsDeployPolicy: This policy allows permissions for ECS-related actions such as describing services, task definitions, tasks, listing tasks, registering task definitions, and updating services. The Resource: "*" statement allows these actions on all ECS resources.

    - CodeStarPolicy: This policy allows permission to use the CodeStar Connections connection. The Resource property references the CodeStar connection created earlier.

    - CodePipelinePolicy: This policy grants various permissions related to CodePipeline, CloudFormation, IAM, S3, and CloudWatch Logs. It allows actions such as managing S3 buckets (s3:*), creating and managing CloudFormation stacks (cloudformation:*), managing IAM roles (iam:*), and creating and managing                 CloudWatch Logs (logs:*). The Resource: '*' statement allows these actions on all resources.

    - CodePipelineBuildPolicy: This policy grants permission for CodeBuild-related actions. It allows starting, stopping, retrying builds, and getting information about builds in CodeBuild. The Resource property references the specific CodeBuild project using the CodeBuildBakeImageStack.Outputs.CodeBuildProjectName       output.

## CFN Static Website Hosting Frontend

This CloudFormation template creates:
  - CloudFront Distribution
  - S3 bucket for www.
  - S3 bucket for naked domain
  - Bucket Policy

config.toml

```
[deploy]
bucket = 'cfn-artifacts-cruddur'
region = 'us-east-1'
stack_name = 'CrdFrontend'

[parameters]
CertificateArn = 'arn:aws:acm:us-east-1:928597128531:certificate/d18c0598-4110-445f-8da4-90cba4d0ca9c'
WwwBucketName = 'www.cruddur.pl'
RootBucketName = 'cruddur.pl'
```

Deployment script. This script uses cfn-toml to get properties and parameters from config.toml file and execute CloudFormation template.

```
#! /usr/bin/env bash
set -e # stop the execution of the script if it fails

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/frontend/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/frontend/config.toml"
echo $CFN_PATH

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix frontend \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-frontend \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```

Parameters

```
Parameters:
  CertificateArn:
    Type: String
  WwwBucketName:
    Type: String
  RootBucketName:
    Type: String
```

- CertificateArn: This parameter is of type string. It is used to specify the Amazon Resource Name (ARN) of an SSL/TLS certificate. The certificate is typically associated with a domain or subdomain and is used for securing HTTPS connections. The certificate ARN can be obtained from AWS Certificate Manager (ACM) or AWS Identity and Access Management (IAM) Certificate Store.

- WwwBucketName: This parameter is of type string. It is used to specify the name of an S3 bucket that will be used for hosting the content of the "www" subdomain. The "www" subdomain is often used as a canonical version of a website's domain name. For example, if the domain name is "example.com", the "www.example.com" subdomain can be associated with this bucket to serve the website content.

- RootBucketName: This parameter is of type string. It is used to specify the name of an S3 bucket that will be used for hosting the content of the root domain. The root domain refers to the main domain without any subdomains. For example, if the domain name is "example.com", this bucket can be associated with it to serve the website content directly from the root domain.

```
Resources:
  RootBucketPolicy:
    Type: AWS::S3::BucketPolicy
    Properties:
      Bucket: !Ref RootBucket
      PolicyDocument:
        Statement:
          - Action:
              - 's3:GetObject'
            Effect: Allow
            Resource: !Sub 'arn:aws:s3:::${RootBucket}/*'
            Principal: '*'
```

This CloudFormation (CFN) code creates an S3 bucket policy resource named RootBucketPolicy. The bucket policy is attached to the S3 bucket specified by the RootBucket parameter. 

- Type: This specifies the resource type as AWS::S3::BucketPolicy, indicating that it is an S3 bucket policy resource.

- Properties: This section defines the properties of the RootBucketPolicy resource.

    - Bucket: The Bucket property references the S3 bucket specified by the RootBucket parameter using the !Ref intrinsic function. This links the bucket policy to the specified S3 bucket.

    - PolicyDocument: This property specifies the policy document that defines the permissions for the bucket. The policy document is a JSON-based document.

- Statement: The Statement section within the PolicyDocument specifies the permissions to be allowed for the S3 bucket.

    - Action: The Action property defines the action to be allowed. In this case, it allows the 's3:GetObject' action, which allows fetching (GET) objects from the S3 bucket.

    - Effect: The Effect property specifies whether the action is allowed or denied. In this case, it is set to 'Allow', indicating that the 's3:GetObject' action is allowed.

    - Resource: The Resource property specifies the Amazon Resource Name (ARN) of the S3 bucket and its objects. The !Sub intrinsic function is used to substitute the value of the RootBucket parameter into the ARN string.

    - Principal: The Principal property specifies the entity to which the policy applies. In this case, it is set to '*' (wildcard), indicating that the policy applies to all principals (users, roles, or accounts).
    
  
  ```
    WWWBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Ref WwwBucketName
      WebsiteConfiguration:
        RedirectAllRequestsTo:
          HostName: !Ref RootBucketName

  RootBucketDomain:
    Type: AWS::Route53::RecordSet
    Properties:
      HostedZoneName: !Sub ${RootBucketName}.
      Name: !Sub ${RootBucketName}.
      Type: A
      AliasTarget:
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-hostedzoneid
        # Specify Z2FDTNDATAQYW2. This is always the hosted zone ID when you create an alias record that routes traffic to a CloudFront distribution.
        DNSName: !GetAtt Distribution.DomainName
        HostedZoneId: Z2FDTNDATAQYW2

  WwwBucketDomain:
    Type: AWS::Route53::RecordSet
    Properties:
      HostedZoneName: !Sub ${RootBucketName}.
      Name: !Sub ${WwwBucketName}.
      Type: A
      AliasTarget:
        DNSName: !GetAtt Distribution.DomainName
        # https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-hostedzoneid
        # Specify Z2FDTNDATAQYW2. This is always the hosted zone ID when you create an alias record that routes traffic to a CloudFront distribution.
        HostedZoneId: Z2FDTNDATAQYW2

  RootBucket:
    Type: AWS::S3::Bucket
    # DeletionPolicy: Retain
    Properties:
      BucketName: !Ref RootBucketName
      PublicAccessBlockConfiguration:
        BlockPublicPolicy: false
      WebsiteConfiguration:
        IndexDocument: index.html
        ErrorDocument: error.html
  ```
  
  This CloudFormation (CFN) code sets up an AWS S3 bucket for website hosting and configures DNS records in AWS Route 53 to associate the bucket with the specified domain names.
  
  
- WWWBucket: This section creates an S3 bucket for hosting the content of the "www" subdomain. The BucketName property references the WwwBucketName parameter, which specifies the name of the S3 bucket. The WebsiteConfiguration property is set to redirect all requests to the RootBucketName.

- RootBucketDomain: This section creates a Route 53 record set for the root domain. The HostedZoneName property specifies the hosted zone name for the root domain, which is obtained by substituting the RootBucketName parameter. The Name property specifies the DNS record name for the root domain. The Type property is set to 'A' to create an A record. The AliasTarget property specifies the target as an alias to a CloudFront distribution.

- WwwBucketDomain: This section creates a Route 53 record set for the "www" subdomain. The HostedZoneName property specifies the hosted zone name for the root domain, which is obtained by substituting the RootBucketName parameter. The Name property specifies the DNS record name for the "www" subdomain. The Type property is set to 'A' to create an A record. The AliasTarget property specifies the target as an alias to a CloudFront distribution.

- RootBucket: This section creates an S3 bucket for hosting the content of the root domain. The BucketName property references the RootBucketName parameter, which specifies the name of the S3 bucket. The PublicAccessBlockConfiguration property is set to allow public access. The WebsiteConfiguration property specifies the index and error documents for the website.

```
  Distribution:
    Type: AWS::CloudFront::Distribution
    Properties:
      DistributionConfig:
        Aliases:
          - cruddur.pl
          - www.cruddur.pl
        Comment: Frontend React Js for Cruddur
        Enabled: true
        HttpVersion: http2and3 
        DefaultRootObject: index.html
        Origins:
          - DomainName: !GetAtt RootBucket.DomainName
            Id: RootBucketOrigin
            S3OriginConfig: {}
        DefaultCacheBehavior:
          TargetOriginId: RootBucketOrigin
          ForwardedValues:
            QueryString: false
            Cookies:
              Forward: none
          ViewerProtocolPolicy: redirect-to-https
        ViewerCertificate:
          AcmCertificateArn: !Ref CertificateArn
          SslSupportMethod: sni-only
```

This CloudFormation (CFN) code creates an Amazon CloudFront distribution.

- DistributionConfig: This property defines the configuration settings for the CloudFront distribution.

- Aliases: The Aliases property specifies the domain names (cruddur.pl and www.cruddur.pl) that will be associated with the CloudFront distribution. These domain names will be used to access the content served by the distribution.

- Comment: The Comment property allows you to provide a description or comment about the CloudFront distribution.

- Enabled: The Enabled property is set to true, indicating that the distribution is enabled and ready to serve content.

- HttpVersion: The HttpVersion property is set to http2and3, which enables HTTP/2 and HTTP/3 support for the CloudFront distribution.

- DefaultRootObject: The DefaultRootObject property specifies the default object to serve when a request is made to the root URL of the CloudFront distribution. In this case, it is set to index.html.

- Origins: The Origins property specifies the origin server for the CloudFront distribution. In this case, it refers to the S3 bucket specified by RootBucket using the !GetAtt intrinsic function.

- DefaultCacheBehavior: This property defines the default behavior for caching and forwarding requests to the origin. It specifies the TargetOriginId as RootBucketOrigin, which refers to the origin server defined earlier. The ForwardedValues property controls how CloudFront handles query strings and cookies. In this case, query strings are not forwarded, and cookies are not used.

- ViewerProtocolPolicy: The ViewerProtocolPolicy property is set to redirect-to-https, which redirects HTTP requests to HTTPS.

- ViewerCertificate: This property specifies the SSL certificate to use for HTTPS connections. The AcmCertificateArn property references the CertificateArn parameter, which specifies the ARN of the SSL certificate. The SslSupportMethod property is set to sni-only, which enables Server Name Indication (SNI) for SSL/TLS encryption.
 
 
