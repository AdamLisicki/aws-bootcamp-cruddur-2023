# Week 10 — CloudFormation Part 1

## CFN For Networking Layer

The CloudFormation template template for networking layer creates:
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

