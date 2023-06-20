# Week 10 — CloudFormation Part 1

## Diagram

![cruddur_cfn](https://github.com/AdamLisicki/aws-bootcamp-cruddur-2023/assets/96197101/7bd0c5b1-1037-4e8c-ab25-314c9437942c)

## CFN For Networking Layer

The CloudFormation template for networking layer creates:
  - VPC
    - sets DNS hostnames for EC2 instances
    - Only IPV4, IPV6 is disabled
  - InternetGateway
  - Route Table
    - route to the IGW
    - route to Local
  - 6 Subnets Explicity Associated to Route Table
    - 3 Public Subnets numbered 1 to 3
    - 3 Private Subnets numbered 1 to 3

config.toml file.
```
[deploy]
bucket = 'cfn-artifacts-cruddur'
region = 'us-east-1'
stack_name = 'CrdNet'
```

Deployment script. This script uses cfn-toml to get properties and parameters from config.toml file and execute CloudFormation template.

```
#! /usr/bin/bash

set -e


CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/networking/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/networking/config.toml"

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix networking \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-networking \
  --capabilities CAPABILITY_NAMED_IAM
```

Describing input parameters for a CFN template.

```
Parameters:
  AvailabilityZones:
    Type: CommaDelimitedList
    Default: >
      us-east-1a,
      us-east-1b,
      us-east-1c
  SubnetCidrBlocks:
    Description: "Comma-delimited list of CIDR blocks for subnets"
    Type: CommaDelimitedList
    Default: > 
      10.0.0.0/22, 
      10.0.4.0/22, 
      10.0.8.0/22, 
      10.0.12.0/22, 
      10.0.16.0/22, 
      10.0.20.0/22
  VPCCidrBlock:
    Type: String
    Default: 10.0.0.0/16
```

 - AvailabilityZones: This parameter allows you to specify a list of Availability Zones (AZs) where your AWS resources will be deployed. 
                      The default value suggests three AZs: us-east-1a, us-east-1b, and us-east-1c.
                      
 - SubnetCidrBlocks: This parameter allows you to specify a list of CIDR blocks for your subnets.
                     The default value suggests six CIDR blocks: 10.0.0.0/22, 10.0.4.0/22, 10.0.8.0/22, 10.0.12.0/22, 10.0.16.0/22, and 10.0.20.0/22.
                     
 - VPCCidrBlock: This parameter allows you to specify the CIDR block for your VPC.
                 Default value is set to 10.0.0.0/16, which suggests a VPC with a CIDR block of 10.0.0.0/16. 


```
Resources:
  VPC: 
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: !Ref VPCCidrBlock
      EnableDnsHostnames: true
      EnableDnsSupport: true
      InstanceTenancy: default
      Tags:
        - Key: Name 
          Value: !Sub "${AWS::StackName}VPC"
```

- The resource of type AWS::EC2:VPC is defined with the logical name "VPC".
- The resource properties are specified under the "Properties" section.
- The "CidrBlock" property is set using the !Ref function with the parameter "VPCCidrBlock". This means that the CIDR block for the VPC is dynamically determined based on the value provided for the "VPCCidrBlock" parameter during the stack deployment.
- The "EnableDnsHostnames" property is set to true, enabling DNS hostnames for the VPC.
- The "EnableDnsSupport" property is set to true, enabling DNS resolution for the VPC.
- The "InstanceTenancy" property is set to "default", indicating that instances launched within this VPC will have the default tenancy, which means they run on shared hardware.
- The "Tags" property is used to specify tags for the VPC resource. In this case, a single tag is defined with the key "Name" and the value is dynamically generated using the !Sub function with the format "${AWS::StackName}VPC". The ${AWS::StackName} variable refers to the name of the CloudFormation stack in which the VPC resource is being created.


```
  IGW:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags: 
      - Key: Name
        Value: !Sub "${AWS::StackName}IGW"

  AttachIGW:    
    Type: AWS::EC2::VPCGatewayAttachment
    Properties: 
      VpcId: !Ref VPC
      InternetGatewayId: !Ref IGW
```

1. Internet Gateway (IGW):
     - This section defines a resource named IGW of type AWS::EC2::InternetGateway.
     - The Tags property is used to specify tags for the Internet Gateway. In this case, a single tag is defined with the key "Name" and the value is dynamically generated using the !Sub function with the format "${AWS::StackName}IGW". The ${AWS::StackName} variable refers to the name of the CloudFormation stack in        which the Internet Gateway resource is being created.
     
2. VPC Gateway Attachment (AttachIGW):
     - This section defines a resource named AttachIGW of type AWS::EC2::VPCGatewayAttachment. A VPC Gateway Attachment is used to attach an Internet Gateway to a VPC.
     - The VpcId property is set to the logical reference !Ref VPC, which means the attachment will be made to the VPC identified by the logical name "VPC".
     - The InternetGatewayId property is set to the logical reference !Ref IGW, which means the attachment will be made to the Internet Gateway identified by the logical name "IGW".



```
  RouteTable:
    Type: AWS::EC2::RouteTable
    Properties:
      VpcId: !Ref VPC
      Tags: 
        - Key: Name
          Value: !Sub "${AWS::StackName}RT"

  RouteToIGW:
    Type: AWS::EC2::Route
    DependsOn: AttachIGW
    Properties:
      RouteTableId: !Ref RouteTable
      GatewayId: !Ref IGW
      DestinationCidrBlock: 0.0.0.0/0
```

1. Route Table (RouteTable):
   -  This section defines a resource named RouteTable of type AWS::EC2::RouteTable.
   -  The VpcId property is set to the logical reference !Ref VPC, which means the route table will be associated with the VPC identified by the logical name "VPC".
   -  The Tags property is used to specify tags for the Route Table. In this case, a single tag is defined with the key "Name" and the value is dynamically generated using the !Sub function with the format "${AWS::StackName}RT". The ${AWS::StackName} variable refers to the name of the CloudFormation stack in which         the Route Table resource is being created.
   
2. Route to an Internet Gateway (RouteToIGW):
   -  This section defines a resource named RouteToIGW of type AWS::EC2::Route. This resource is used to add a route to the Route Table created in the previous section, directing traffic to an Internet Gateway.
   -  The DependsOn property specifies that this resource depends on the successful creation of the AttachIGW resource.
   -  The RouteTableId property is set to the logical reference !Ref RouteTable, which means the route will be added to the Route Table identified by the logical name "RouteTable".
   -  The GatewayId property is set to the logical reference !Ref IGW, which means the traffic will be routed to the Internet Gateway identified by the logical name "IGW".
   -  The DestinationCidrBlock property is set to 0.0.0.0/0, which represents the default route for all traffic (any IP address). This route directs all traffic to the specified Internet Gateway.


```
SubnetPub1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [0, !Ref SubnetCidrBlocks]
      AvailabilityZone: !Select [0, !Ref AvailabilityZones]
      EnableDns64: false
      MapPublicIpOnLaunch: true
      Tags:
      - Key: Name
        Value: !Sub "${AWS::StackName}SubnetPub1"

  SubnetPub2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [1, !Ref SubnetCidrBlocks]
      AvailabilityZone: !Select [1, !Ref AvailabilityZones]
      EnableDns64: false
      MapPublicIpOnLaunch: true
      Tags:
      - Key: Name
        Value: !Sub "${AWS::StackName}SubnetPub2"

  SubnetPub3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [2, !Ref SubnetCidrBlocks]
      AvailabilityZone: !Select [2, !Ref AvailabilityZones]
      EnableDns64: false
      MapPublicIpOnLaunch: true
      Tags:
      - Key: Name
        Value: !Sub "${AWS::StackName}SubnetPub3"

  SubnetPriv1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [3, !Ref SubnetCidrBlocks]
      AvailabilityZone: !Select [0, !Ref AvailabilityZones]
      EnableDns64: false
      MapPublicIpOnLaunch: false
      Tags:
      - Key: Name
        Value: !Sub "${AWS::StackName}SubnetPriv1"

  SubnetPriv2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [4, !Ref SubnetCidrBlocks]
      AvailabilityZone: !Select [1, !Ref AvailabilityZones]
      EnableDns64: false
      MapPublicIpOnLaunch: false
      Tags:
      - Key: Name
        Value: !Sub "${AWS::StackName}SubnetPriv2"

  SubnetPriv3:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: !Select [5, !Ref SubnetCidrBlocks]
      AvailabilityZone: !Select [2, !Ref AvailabilityZones]
      EnableDns64: false
      MapPublicIpOnLaunch: false
      Tags:
      - Key: Name
        Value: !Sub "${AWS::StackName}SubnetPriv3"
```

1. SubnetPub1, SubnetPub2, SubnetPub3 (Public Subnets):

   - These sections define three resources of type AWS::EC2::Subnet, representing public subnets within the VPC.
   - The VpcId property is set to the logical reference !Ref VPC, which means these subnets will be associated with the VPC identified by the logical name "VPC".
   - The CidrBlock property is set using the !Select function to retrieve specific CIDR blocks from the SubnetCidrBlocks parameter. For example, !Select [0, !Ref SubnetCidrBlocks] selects the first CIDR block in the list. Each subnet uses a different CIDR block.
   - The AvailabilityZone property is set using the !Select function to retrieve specific Availability Zones (AZs) from the AvailabilityZones parameter. For example, !Select [0, !Ref AvailabilityZones] selects the first AZ in the list. Each subnet is associated with a different AZ.
   - The EnableDns64 property is set to false, indicating that DNS IPv6 resolution is disabled for these subnets.
   - The MapPublicIpOnLaunch property is set to true, enabling instances launched in these subnets to automatically receive a public IP address.
   - The Tags property is used to specify tags for the subnets. Each subnet has a single tag with the key "Name" and the value is dynamically generated using the !Sub function with the format "${AWS::StackName}SubnetPubX", where X represents the number of the subnet.

2. SubnetPriv1, SubnetPriv2, SubnetPriv3 (Private Subnets):

   - These sections define three resources of type AWS::EC2::Subnet, representing private subnets within the VPC.
   - The properties of these subnets are similar to the public subnets, except for a few differences:
       - The MapPublicIpOnLaunch property is set to false, meaning instances launched in these subnets will not receive a public IP address by default.
       - The Tags property follows the same pattern as the public subnets, generating a name based on the stack name and the subnet number.


```
SubnetPub1RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPub1
      RouteTableId: !Ref RouteTable

  SubnetPub2RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPub2
      RouteTableId: !Ref RouteTable


  SubnetPub3RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPub3
      RouteTableId: !Ref RouteTable


  SubnetPriv1RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPriv1
      RouteTableId: !Ref RouteTable

  SubnetPriv2RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPriv2
      RouteTableId: !Ref RouteTable

  SubnetPriv3RTAssociation:
    Type: AWS::EC2::SubnetRouteTableAssociation
    Properties:
      SubnetId: !Ref SubnetPriv3
      RouteTableId: !Ref RouteTable

```

1. SubnetPub1RTAssociation, SubnetPub2RTAssociation, SubnetPub3RTAssociation (Associations for Public Subnets):

   - These sections define three resources of type AWS::EC2::SubnetRouteTableAssociation, representing the association between public subnets and a route table.
   - The SubnetId property is set to the logical reference !Ref SubnetPubX, where X represents the number of the public subnet. This refers to the corresponding public subnet resource created earlier in the CloudFormation template.
   - The RouteTableId property is set to the logical reference !Ref RouteTable, which means the association will be made with the route table identified by the logical name "RouteTable".

2. SubnetPriv1RTAssociation, SubnetPriv2RTAssociation, SubnetPriv3RTAssociation (Associations for Private Subnets):

   - These sections define three resources of type AWS::EC2::SubnetRouteTableAssociation, representing the association between private subnets and a route table.
   - The SubnetId property is set to the logical reference !Ref SubnetPrivX, where X represents the number of the private subnet. This refers to the corresponding private subnet resource created earlier in the CloudFormation template.
   - The RouteTableId property is set to the logical reference !Ref RouteTable, indicating the association will be made with the same route table used for the public subnets.


## CFN Cluster Layer

  The CloudFormation template for cluster layer creates:
  - ECS Fargate Cluster
  - Application Load Balanacer (ALB)
    - ipv4 only
    - internet facing
    - certificate attached from Amazon Certification Manager (ACM)
  - ALB Security Group
  - HTTPS Listerner
    - send naked domain to frontend Target Group
    - send api. subdomain to backend Target Group
  - HTTP Listerner
    - redirects to HTTPS Listerner
  - Backend Target Group
  - Frontend Target Group
  
config.toml file.
```
[deploy]
bucket = 'cfn-artifacts-cruddur'
region = 'us-east-1'
stack_name = 'CrdCluster'

[parameters]
CertificateArn = 'arn:aws:acm:us-east-1:928597128531:certificate/d18c0598-4110-445f-8da4-90cba4d0ca9c'
NetworkingStack = 'CrdNet'
```

Deployment script. This script uses cfn-toml to get properties and parameters from config.toml file and execute CloudFormation template.

```
#! /usr/bin/bash

set -e

CFN_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/template.yaml"
CONFIG_PATH="/workspace/aws-bootcamp-cruddur-2023/aws/cfn/cluster/config.toml"

cfn-lint $CFN_PATH

BUCKET=$(cfn-toml key deploy.bucket -t $CONFIG_PATH)
REGION=$(cfn-toml key deploy.region -t $CONFIG_PATH)
STACK_NAME=$(cfn-toml key deploy.stack_name -t $CONFIG_PATH)
PARAMETERS=$(cfn-toml params v2 -t $CONFIG_PATH)

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --s3-bucket $BUCKET \
  --s3-prefix cluster \
  --region $REGION \
  --template-file "$CFN_PATH" \
  --no-execute-changeset \
  --tags group=cruddur-cluster \
  --parameter-overrides $PARAMETERS \
  --capabilities CAPABILITY_NAMED_IAM
```
  
Parameters
  
  ```
  Parameters:
  NetworkingStack:
    Type: String
    Description: This is our base layer of networking components eg. VPC, Subnets
    Default: CrdNet
  CertificateArn:
    Type: String
  #Frontend ------
  FrontendPort:
    Type: Number
    Default: 3000
  FrontendHealthCheckIntervalSeconds:
    Type: Number
    Default: 15
  FrontendHealthCheckPath:
    Type: String
    Default: "/"
  FrontendHealthCheckPort:
    Type: String
    Default: 80
  FrontendHealthCheckProtocol:
    Type: String
    Default: HTTP
  FrontendHealthCheckTimeoutSeconds:
    Type: Number
    Default: 5
  FrontendHealthyThresholdCount:
    Type: Number
    Default: 2
  FrontendUnhealthyThresholdCount:
    Type: Number
    Default: 2
  #Backend ------
  BackendPort:
    Type: Number
    Default: 4567
  BackendHealthCheckIntervalSeconds:
    Type: String
    Default: 15
  BackendHealthCheckPath:
    Type: String
    Default: "/api/health-check"
  BackendHealthCheckPort:
    Type: String
    Default: 80
  BackendHealthCheckProtocol:
    Type: String
    Default: HTTP
  BackendHealthCheckTimeoutSeconds:
    Type: Number
    Default: 5
  BackendHealthyThresholdCount:
    Type: Number
    Default: 2
  BackendUnhealthyThresholdCount:
    Type: Number
    Default: 2
  ```

- NetworkingStack: Represents the base layer of networking components, such as a Virtual Private Cloud (VPC) and subnets.

- CertificateArn: Represents the Amazon Resource Name (ARN) of an SSL certificate to be used for secure communication.

- FrontendPort: Specifies the port number on which the frontend service listens.

- FrontendHealthCheckIntervalSeconds: Defines the interval (in seconds) between health checks for the frontend service.

- FrontendHealthCheckPath: Specifies the path that the health check request is sent to on the frontend service.

- FrontendHealthCheckPort: Specifies the port on which the frontend health check is performed.

- FrontendHealthCheckProtocol: Specifies the protocol used for the frontend health check.

- FrontendHealthCheckTimeoutSeconds: Sets the timeout (in seconds) for the frontend health check.

- FrontendHealthyThresholdCount: Defines the number of consecutive successful health checks required to consider the frontend service as healthy.

- FrontendUnhealthyThresholdCount: Sets the number of consecutive failed health checks required to consider the frontend service as unhealthy.

- BackendPort: Specifies the port number on which the backend service listens.

- BackendHealthCheckIntervalSeconds: Defines the interval (in seconds) between health checks for the backend service.

- BackendHealthCheckPath: Specifies the path that the health check request is sent to on the backend service.

- BackendHealthCheckPort: Specifies the port on which the backend health check is performed.

- BackendHealthCheckProtocol: Specifies the protocol used for the backend health check.

- BackendHealthCheckTimeoutSeconds: Sets the timeout (in seconds) for the backend health check.

- BackendHealthyThresholdCount: Defines the number of consecutive successful health checks required to consider the backend service as healthy.

- BackendUnhealthyThresholdCount: Sets the number of consecutive failed health checks required to consider the backend service as unhealthy.

```
Resources:
  FargateCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub "${AWS::StackName}FargateCluster"
      CapacityProviders:
        - FARGATE
      ClusterSettings:
        - Name: containerInsights
          Value: enabled
      Configuration:
        ExecuteCommandConfiguration:
          # KmsKeyId: !Ref KmsKeyId
          Logging: DEFAULT
      ServiceConnectDefaults:
        Namespace: cruddur
```

This CloudFormation code creates an ECS cluster with Fargate capacity providers and configures various settings and defaults. 

- The CFN code creates an ECS cluster using Fargate capacity providers.
- The cluster is named "FargateCluster" and its ClusterName property is set dynamically using the AWS::StackName.
- Container insights are enabled for the cluster.
- Default logging behavior is set to "DEFAULT".
- The default service discovery namespace is set to "cruddur".


```
 ALB:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub "${AWS::StackName}ALB"
      Type: application
      Scheme: internet-facing
      IpAddressType: ipv4
      Subnets:
        Fn::Split:
          - ","
          - Fn::ImportValue:
              !Sub "${NetworkingStack}PublicSubnetIds"
      SecurityGroups:
        - !GetAtt ALBSG.GroupId
      LoadBalancerAttributes:
        - Key: routing.http2.enabled
          Value: true
        - Key: routing.http.preserve_host_header.enabled
          Value: false
        - Key: deletion_protection.enabled
          Value: true
        - Key: load_balancing.cross_zone.enabled
          Value: true
        - Key: access_logs.s3.enabled
          Value: false
```
This CloudFormation (CFN) code creates an Application Load Balancer (ALB) resource with specific properties.

- "Name" is set using the !Sub function, which substitutes the "${AWS::StackName}ALB" expression with the name of the CloudFormation stack followed by "ALB".
- "Type" specifies that the ALB is of type "application".
- "Scheme" indicates that the ALB is internet-facing.
- "IpAddressType" is set to "ipv4" to use IPv4 addresses.
- "Subnets" is set using the Fn::Split function, which splits the comma-separated list of subnet IDs obtained from an imported value called "${NetworkingStack}PublicSubnetIds".
- "SecurityGroups" specifies the security group associated with the ALB, obtained from the ALBSG resource using !GetAtt ALBSG.GroupId.
- "LoadBalancerAttributes" is an array of key-value pairs representing different ALB attributes. The code sets attributes related to routing, deletion protection, cross-zone load balancing, and access logs. It enables HTTP/2 routing, disables preserving the host header, enables deletion protection, enables cross-zone load balancing, and disables S3 access logging.

```
HTTPSListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties: 
      Certificates:
        - CertificateArn: !Ref CertificateArn
      DefaultActions:
        - Type: forward
          TargetGroupArn:  !Ref FrontendTG
      LoadBalancerArn: !Ref ALB
      Port: 443
      Protocol: HTTPS

  HTTPListener:
    Type: AWS::ElasticLoadBalancingV2::Listener
    Properties:
      Port: 80
      Protocol: HTTP
      LoadBalancerArn: !Ref ALB
      DefaultActions:
        - Type: redirect
          RedirectConfig:
            Protocol: "HTTPS"
            Port: 443
            Host: "#{host}"
            Path: "/#{path}"
            Query: "#{query}"
            StatusCode: "HTTP_301"
```

This CloudFormation (CFN) code creates two listeners for an Application Load Balancer (ALB).

1. "HTTPSListener" creates an HTTPS listener for the ALB:
      - The listener is of type AWS::ElasticLoadBalancingV2::Listener.
      - It is associated with an SSL certificate specified by the CertificateArn parameter.
      - The default action is set to forward requests to the target group referenced by FrontendTG.
      - The listener is attached to the ALB referenced by ALB.
      - It listens on port 443 using the HTTPS protocol.
      
2. "HTTPListener" creates an HTTP listener for the ALB:
      - The listener is of type AWS::ElasticLoadBalancingV2::Listener.
      - It listens on port 80 using the HTTP protocol.
      - The listener is attached to the ALB referenced by ALB.
      - The default action is set to redirect requests:
        - The redirection is to HTTPS using the Protocol property.
        - The redirected requests will have the destination port set to 443.
        - The host, path, and query parameters of the original request are preserved in the redirection.
        - The redirection status code is set to "HTTP_301" for a permanent redirect.


```
ApiALBListernerRule:
    Type: AWS::ElasticLoadBalancingV2::ListenerRule
    Properties:
      Conditions: 
        - Field: host-header
          HostHeaderConfig: 
            Values: 
              - api.cruddur.pl
      Actions: 
        - Type: forward
          TargetGroupArn:  !Ref BackendTG
      ListenerArn: !Ref HTTPSListener
      Priority: 1

```

This CloudFormation (CFN) code creates a listener rule for an Application Load Balancer (ALB).

The properties of the listener rule are configured as follows:
  - "Conditions" specify the conditions that need to be met for the rule to apply. In this case, the condition is based on the host header value. The rule will apply if the host header matches "api.cruddur.pl".
  - "Actions" define the action to be taken when the rule matches. In this case, the action is set to forward the request to the target group referenced by BackendTG.
  - "ListenerArn" references the HTTPS listener (HTTPSListener) to which this rule should be associated.
  - "Priority" sets the priority of the rule. A lower number indicates a higher priority. In this case, the priority is set to 1.
  

```
ALBSG:
    Type: AWS::EC2::SecurityGroup
    Properties:
      GroupName: !Sub "${AWS::StackName}AlbSG"
      GroupDescription: Public facing SG for our Cruddur ALB
      VpcId:
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId
      SecurityGroupIngress:
        - IpProtocol: tcp
          FromPort: 443
          ToPort: 443
          CidrIp: '0.0.0.0/0'
          Description: INTERNET HTTPS
        - IpProtocol: tcp
          FromPort: 80
          ToPort: 80
          CidrIp: '0.0.0.0/0'
          Description: INTERNET HTTP
```

This CloudFormation (CFN) code creates a security group (SG) for an Application Load Balancer (ALB).

The properties of the security group are configured as follows:
  - "GroupName" is set using the !Sub function, which substitutes the "${AWS::StackName}AlbSG" expression with the name of the CloudFormation stack followed by "AlbSG".
  - "GroupDescription" provides a description for the security group, indicating that it is a public-facing SG for the Cruddur ALB.
  - "VpcId" references the VPC ID obtained from an imported value called "${NetworkingStack}VpcId".
  - "SecurityGroupIngress" specifies the inbound traffic rules for the security group. Two rules are defined:
  - The first rule allows inbound traffic on TCP port 443 (HTTPS) from any IP address (0.0.0.0/0).
  - The second rule allows inbound traffic on TCP port 80 (HTTP) from any IP address (0.0.0.0/0).
  
  
```
BackendTG:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}BackendTG"
      Port: !Ref BackendPort
      HealthCheckProtocol: !Ref BackendHealthCheckProtocol
      HealthCheckEnabled: true
      HealthCheckIntervalSeconds: !Ref BackendHealthCheckIntervalSeconds
      HealthCheckPath: !Ref BackendHealthCheckPath
      HealthCheckPort: !Ref BackendHealthCheckPort
      HealthCheckTimeoutSeconds: !Ref BackendHealthCheckTimeoutSeconds
      HealthyThresholdCount: !Ref BackendHealthyThresholdCount
      UnhealthyThresholdCount: !Ref BackendUnhealthyThresholdCount
      IpAddressType: ipv4
      Matcher: 
        HttpCode: 200
      Protocol: HTTP
      ProtocolVersion: HTTP2
      TargetGroupAttributes: 
        - Key: deregistration_delay.timeout_seconds
          Value: 0
      VpcId:
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId

  FrontendTG:
    Type: AWS::ElasticLoadBalancingV2::TargetGroup
    Properties:
      Name: !Sub "${AWS::StackName}FrontendTG"
      Port: !Ref FrontendPort
      HealthCheckProtocol: !Ref FrontendHealthCheckProtocol
      HealthCheckEnabled: true
      HealthCheckIntervalSeconds: !Ref FrontendHealthCheckIntervalSeconds
      HealthCheckPath: !Ref FrontendHealthCheckPath
      HealthCheckPort: !Ref FrontendHealthCheckPort
      HealthCheckTimeoutSeconds: !Ref FrontendHealthCheckTimeoutSeconds
      HealthyThresholdCount: !Ref FrontendHealthyThresholdCount
      UnhealthyThresholdCount: !Ref FrontendUnhealthyThresholdCount
      IpAddressType: ipv4
      Matcher:
        HttpCode: 200
      Protocol: HTTP
      ProtocolVersion: HTTP2
      TargetGroupAttributes:
        - Key: deregistration_delay.timeout_seconds
          Value: 0
      VpcId: 
        Fn::ImportValue:
          !Sub ${NetworkingStack}VpcId
```

This CloudFormation (CFN) code creates two target groups for an Application Load Balancer (ALB): "BackendTG" and "FrontendTG". 

1. "BackendTG" target group:
      - It defines a resource of type AWS::ElasticLoadBalancingV2::TargetGroup.
      - The properties of the target group are configured as follows:
      - "Name" is set using the !Sub function, which substitutes the "${AWS::StackName}BackendTG" expression with the name of the CloudFormation stack followed by "BackendTG".
      - "Port" specifies the port that the target group listens on, obtained from the BackendPort parameter.
      - "HealthCheckProtocol" specifies the protocol used for health checks, obtained from the BackendHealthCheckProtocol parameter.
      - "HealthCheckEnabled" is set to true, indicating that health checks are enabled for the target group.
      - Various health check properties such as interval, path, port, timeout, healthy threshold count, and unhealthy threshold count are obtained from respective parameters.
      - "IpAddressType" is set to "ipv4" to use IPv4 addresses.
      - "Matcher" is configured to match HTTP response code 200.
      - "Protocol" is set to HTTP and "ProtocolVersion" is set to HTTP2.
      - "TargetGroupAttributes" specify additional attributes for the target group. In this case, a deregistration delay timeout of 0 seconds is set.
      - "VpcId" references the VPC ID obtained from an imported value called "${NetworkingStack}VpcId".
 
2. "FrontendTG" target group:
      - It defines a resource of type AWS::ElasticLoadBalancingV2::TargetGroup similar to "BackendTG".
      - The properties are configured in a similar way, but with values obtained from respective Frontend prefixed parameters.
