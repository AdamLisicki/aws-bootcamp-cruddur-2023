# Week 10 — CloudFormation Part 1

## CFN For Networking Layer

```yaml
AWSTemplateFormatVersion: 2010-09-09

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
    
# VPC
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
# IGW
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


Outputs:
  VpcId:
    Value: !Ref VPC
    Export:
      Name: !Sub "${AWS::StackName}VpcId"
  VpcCidrBlock:
    Value: !GetAtt VPC.CidrBlock
    Export:
      Name: !Sub "${AWS::StackName}VpcCidrBlock"
  SubnetCidrBlocks:
    Value: !Join [",", !Ref SubnetCidrBlocks]
    Export:
      Name: !Sub "${AWS::StackName}SubnetCidrBlocks"
  PublicSubnetIds:
    Value: !Join 
      - ","
      - - !Ref SubnetPub1
        - !Ref SubnetPub2
        - !Ref SubnetPub3
    Export:
      Name: !Sub "${AWS::StackName}PublicSubnetIds"
  PrivateSubnetIds:
    Value: !Join 
      - ","
      - - !Ref SubnetPriv1
        - !Ref SubnetPriv2
        - !Ref SubnetPriv3
    Export:
      Name: !Sub "${AWS::StackName}PrivateSubnetIds"
  AvailabilityZones:
    Value: !Join [",", !Ref AvailabilityZones]
    Export:
      Name: !Sub "${AWS::StackName}AvailabilityZones"
```

This CloudFormation yaml template creates:
  - VPC
  - Internet Gateway
  - Route Table
  - Subnets
