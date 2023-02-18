# Week 0 — Billing and Architecture

## Conceptual Diagram

![image](https://user-images.githubusercontent.com/96197101/219812850-a0025123-3fcc-4fbb-8591-33e1d5280c1b.png)


## Logical Diagram

![image](https://user-images.githubusercontent.com/96197101/219813239-d4b6d833-ada2-4f24-ac80-3e09f59f46f6.png)

## Create a Budget

### Monthly Cost Budget 

I created a budget that notifies me when my monthy spend will be over 85$ (template has default alarm treshold set to 85% of my budget) and over 100$. 

![image](https://user-images.githubusercontent.com/96197101/219852691-a4239606-7afd-47ee-aec9-9b0f2332c68a.png)

### Credits Spend Budget

I also created a custom budget that notifies me when my credit spend will be over 0.8$ and 1$.

I typed budget name and budget amount. Also I set charge type to "Credits".

![image](https://user-images.githubusercontent.com/96197101/219853007-b19d4018-c94d-40a1-8cbd-ab65123d65fd.png)

I configured alarm that notifies me when my credits spend will be at 80%.

![image](https://user-images.githubusercontent.com/96197101/219853078-6ddb9b51-b8f6-4f80-9aed-50f06cbfe002.png)


### Zero Spend Budget

I created zero spend budget from a template that notifies me when my spending exceeds 0.01$.

![image](https://user-images.githubusercontent.com/96197101/219853776-002a1e37-9720-4cc2-8234-1f5b13bf36d9.png)


All budgets that I've created.

![image](https://user-images.githubusercontent.com/96197101/219853880-8f1113f9-cab7-46a6-b14c-25e310081942.png)

## Setting up Root account and Admin user

I set up MFA for Root account

![image](https://user-images.githubusercontent.com/96197101/219855018-9ca8a4ca-15b0-4099-b8b8-7261a7b48ad5.png)

I created Admin user and set up MFA and Access key.

![image](https://user-images.githubusercontent.com/96197101/219856443-5e4db848-e470-4b4d-896f-be53576d1690.png)


## Use Cloud Shell

https://awscli.amazonaws.com/v2/documentation/api/latest/reference/sts/get-caller-identity.html

I used command <code>aws sts get-caller-identity</code> to return details about the IAM user or role whose credentials are used to call the operation. 

![image](https://user-images.githubusercontent.com/96197101/219856557-2805bfc6-0fc0-4b6e-bc9d-39e91b24aaa9.png)


## Gitpod configuration (AWS Credentials, AWS CLI)

https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

Commands that I used to install AWS CLI in gitpod.

<code>cd /workspace
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  sudo ./aws/install
</code>


After executing above commands, AWS CLI is now intalled in my gitpod environment.

![image](https://user-images.githubusercontent.com/96197101/219857307-ad015e4f-1565-4fc0-80f2-94bd63563a12.png)

I set up environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION. 

Command <code>aws sts get-caller-identity</code> shows info about my admin user.

![image](https://user-images.githubusercontent.com/96197101/219857638-7d0fb529-7f12-42e9-807f-83397329f410.png)

I edited .gitpod file to make sure that when I start gitpod environment AWS CLI will be always installed. 

https://www.gitpod.io/docs/introduction/learn-gitpod/gitpod-yaml

![image](https://user-images.githubusercontent.com/96197101/219858134-9b3c37e2-0b95-4bf8-ab18-a6f365aa57b7.png)

I've also create environment variables for Gitpod AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION to not assign the every time.

![image](https://user-images.githubusercontent.com/96197101/219863852-b03c0ffb-eaf5-4b08-ae99-4126316005ab.png)

There is two ways to create Gitpod environment varibles: 
  - using Gitpod portal
  - typing <code> gp env <VAR_NAME>="<VAR_VALUE>"</code>

  
 ## Enable Billing
  
  I enabled Billing Alerts to revice alerts.
  
  ![image](https://user-images.githubusercontent.com/96197101/219864585-003044b9-3061-46f6-8b0d-5842ae4b8f54.png)

 ## Create a Budget from CLI
  
  https://docs.aws.amazon.com/cli/latest/reference/budgets/create-budget.html#examples
  
  ![image](https://user-images.githubusercontent.com/96197101/219865265-fd1c646f-4f1a-4c54-ae45-b0b5d130304e.png)

  ![image](https://user-images.githubusercontent.com/96197101/219865302-62f17aad-1eef-4e6d-a38d-a32e6e868be9.png)

 ## Create a Billing Alarm
  
 ### Create SNS Topic
  
  <code>aws sns create-topic --name billing-alarm</code>
  
  ![image](https://user-images.githubusercontent.com/96197101/219865471-19d1600b-7897-44d3-b163-8c6aca056e6d.png)

  <code>aws sns subscribe \
    --topic-arn TopicARN \
    --protocol email \
    --notification-endpoint your@email.com</code>
  
  ![image](https://user-images.githubusercontent.com/96197101/219865500-c18c5ee6-b01d-4441-86f3-84fdab33a8ea.png)
  
  I confirmed subscription.
  
  ![image](https://user-images.githubusercontent.com/96197101/219865562-c50c2c29-1782-4c9d-9d96-acfdc2a09e26.png)
  
  ### Create Alarm
  
  I created alarm_config.json file and paste JSON that is on page https://aws.amazon.com/premiumsupport/knowledge-center/cloudwatch-estimatedcharges-alarm/ and change AlarmActions section to my arn number that I created in previous step. 
  
  ![image](https://user-images.githubusercontent.com/96197101/219865849-87e62f3c-6432-4ff6-9c82-2eae02eec519.png)

  And then I run this command.
  
  <code>aws cloudwatch put-metric-alarm --cli-input-json file://aws/json/alarm_config.json</code>
  
  ![image](https://user-images.githubusercontent.com/96197101/219866006-4788a286-3fac-4049-ae04-706c3ca7b11b.png)
  
 Created alarm in AWS Portal.
  
  ![image](https://user-images.githubusercontent.com/96197101/219866062-bcbf6514-f027-4c4f-b5e8-b2e2071bc627.png)

## Open a support ticket and request a service limit
  
  ![image](https://user-images.githubusercontent.com/96197101/219879084-b336f413-051e-4ac4-b0ac-5edc1e81c763.png)

  
  

