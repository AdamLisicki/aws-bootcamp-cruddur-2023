# Week 10 — CloudFormation Part 1

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

- The resource is defined with the logical name "VPC".
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
     -
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


