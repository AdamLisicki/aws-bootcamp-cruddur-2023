# Week 6 — Deploying Containers

## Create script to test RDS Connection

This script checks if our container has connectivity to RDS instance.

![image](https://user-images.githubusercontent.com/96197101/229611215-ea21b40a-575d-4647-b931-ec6d39b092ae.png)


## Create Health Check For Flask App

Add this endpoint for flask app to return 'success': True with HTTP code 200.

![image](https://user-images.githubusercontent.com/96197101/229611747-13fce468-aef3-473b-a119-4213abbbfef8.png)

Then create a script that return 0 when flask app is healthy and 1 when it's not.

![image](https://user-images.githubusercontent.com/96197101/229612868-c12ce6a3-7253-4d9c-8b4e-12aedbedeb03.png)

## Create ECS Cluster

To create ECS cluster we need to type below command.
 ```
 aws ecs create-cluster \
--cluster-name cruddur \
--service-connect-defaults namespace=cruddur
```

And ECS Cluster has been created.

![image](https://user-images.githubusercontent.com/96197101/229613569-7a469b7a-639e-4a40-9f13-21901583cbc7.png)


## Create ECR repo and push image for backend-flask

To create ECR for backend-flask run below command.

```
aws ecr create-repository \
  --repository-name backend-flask \
  --image-tag-mutability MUTABLE
```

Created repo.

![image](https://user-images.githubusercontent.com/96197101/229620729-67358d59-fdea-42de-93ef-07076c786ccb.png)


We also need to create repo for python image.

```
aws ecr create-repository \
  --repository-name cruddur-python \
  --image-tag-mutability MUTABLE
 ```

Created repo.

![image](https://user-images.githubusercontent.com/96197101/229621501-d53d36f1-24f1-4b0a-9d22-c897ee0dca96.png)


Set ECR_PYTHON_URL environment variable.

```
export ECR_PYTHON_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/cruddur-python"
```

Pull Image 

```
docker pull python:3.10-slim-buster
```

Tag Image

```
docker tag python:3.10-slim-buster $ECR_PYTHON_URL:3.10-slim-buster
```

We need to login to ECR

```
aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin "$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com"
```

And push tagged image to ECR python repo.

```
docker push $ECR_PYTHON_URL:3.10-slim-buster
```

Pushed image.

![image](https://user-images.githubusercontent.com/96197101/229622290-ab969893-054e-40fb-a417-5605891ca77a.png)


Now we need to edit Dockerfile for backend-flask so it uses our ECR repo instead of publick Docker repo.

![image](https://user-images.githubusercontent.com/96197101/229622671-cc35d218-8345-4c01-b4ae-b63b8da0ff88.png)


Create environment variable for backend-flask ECR repo.


```
export ECR_BACKEND_FLASK_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/backend-flask"
```

In backend-flask directory run below command to build an image.

```
docker build -t backend-flask .
```
Then tag image.

```
docker tag backend-flask:latest $ECR_BACKEND_FLASK_URL:latest
```

And push it to backend-flask ECR repo.

```
docker push $ECR_BACKEND_FLASK_URL:latest
```

Pushed image.

![image](https://user-images.githubusercontent.com/96197101/229623136-c955c5e9-778b-4ae5-94b8-adb9d2840616.png)


## Deploy Backend Flask app as a service to Fargate

Create CloudWatch log group for our ECS cluster and set retention for 1 day.

```
aws logs create-log-group --log-group-name cruddur
aws logs put-retention-policy --log-group-name cruddur --retention-in-days 1
```

Created ClouWatch log group.

![image](https://user-images.githubusercontent.com/96197101/229624605-ba75483d-9686-4660-a314-f0afec5aaee0.png)


We need to set up parameters for secrets for backend-flask.

```
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_ACCESS_KEY_ID" --value $AWS_ACCESS_KEY_ID
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/AWS_SECRET_ACCESS_KEY" --value $AWS_SECRET_ACCESS_KEY
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/CONNECTION_URL" --value $PROD_CONNECTION_URL
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/ROLLBAR_ACCESS_TOKEN" --value $ROLLBAR_ACCESS_TOKEN
aws ssm put-parameter --type "SecureString" --name "/cruddur/backend-flask/OTEL_EXPORTER_OTLP_HEADERS" --value "x-honeycomb-team=$HONEYCOMB_API_KEY"
```
Created parameters.

![image](https://user-images.githubusercontent.com/96197101/229625375-0881b617-99c9-4f14-9484-8995506c4417.png)

Create Execution Role and Execution Policy.

![image](https://user-images.githubusercontent.com/96197101/229626907-075b60c1-4c1d-4a24-9555-c5a7193a1215.png)


Create Task Role and Task Policy.

![image](https://user-images.githubusercontent.com/96197101/229627043-d75ea5ed-0497-45fe-9894-92235658ca0d.png)


Create JSON file for task definition. This file defines roles for execution and task, size of containers, container definitions, health check, logs, environment variables and secrets. And I've already set up CORS to ony allow traffic from our domain. 

![image](https://user-images.githubusercontent.com/96197101/229623538-db21aca9-52ff-4ecf-9762-1aca46276b64.png)


Register task definition for backend-flask.

```
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/backend-flask.json
```

Create security group for our services.

```
export CRUD_SERVICE_SG=$(aws ec2 create-security-group \
  --group-name "crud-srv-sg" \
  --description "Security group for Cruddur services on ECS" \
  --vpc-id $DEFAULT_VPC_ID \
  --query "GroupId" --output text)
```

Allow ingress rule for port 4567 (backend-flask) and 3000 (frontend-react-js).

Created Security Group.

![image](https://user-images.githubusercontent.com/96197101/229628080-a95537e3-c4d3-49a4-9b48-dc5bf078bcf7.png)


Add for RDS security group rule that allow port 5432 from services securiy group.

![image](https://user-images.githubusercontent.com/96197101/229628518-fec03541-1d93-4478-b227-78468a4acd47.png)


Create definition of our service.

![image](https://user-images.githubusercontent.com/96197101/229629007-ac32c56d-1936-49f4-88ac-e03883236465.png)

Create service.

```
aws ecs create-service --cli-input-json file://aws/json/service-backend-flask.json
```

Created healthy service.

![image](https://user-images.githubusercontent.com/96197101/229630319-5bd668cd-2547-47dd-a757-0a7d9d6c3e4d.png)


## Create ECR repo and push image for fronted-react-js	

Command for create frondend repo.

```
aws ecr create-repository \
  --repository-name frontend-react-js \
  --image-tag-mutability MUTABLE
```

Created repo.

![image](https://user-images.githubusercontent.com/96197101/229631009-fba4e9b0-387e-48c0-9fee-6a8715ff9029.png)

Set environment variable for frontend repo.

```
export ECR_FRONTEND_REACT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/frontend-react-js"
```

Create new multi stage Dockerfile.prod.

![image](https://user-images.githubusercontent.com/96197101/229631330-02fcc097-efdc-4ff6-b0e7-c4270dd3e14c.png)

Build an image.

```
docker build \
--build-arg REACT_APP_BACKEND_URL="https://4567-$GITPOD_WORKSPACE_ID.$GITPOD_WORKSPACE_CLUSTER_HOST" \
--build-arg REACT_APP_AWS_PROJECT_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_COGNITO_REGION="$AWS_DEFAULT_REGION" \
--build-arg REACT_APP_AWS_USER_POOLS_ID="$REACT_APP_AWS_USER_POOLS_ID" \
--build-arg REACT_APP_CLIENT_ID="$REACT_APP_CLIENT_ID" \
-t frontend-react-js \
-f Dockerfile.prod \
.
```

Tag image.

```
docker tag frontend-react-js:latest $ECR_FRONTEND_REACT_URL:latest
```

And push it to ECR repo.

```
docker push $ECR_FRONTEND_REACT_URL:latest
```

Pushed image.

![image](https://user-images.githubusercontent.com/96197101/229631739-7c7cde26-de1a-49f6-9a34-7c47df61d8a2.png)


## 	Deploy Frontend React JS app as a service to Fargate

Create task definition JSON file.

![image](https://user-images.githubusercontent.com/96197101/229631978-fff130a4-22bb-48fb-b393-4187138dc26e.png)

Create service definition JSON file.

![image](https://user-images.githubusercontent.com/96197101/229632037-66a738a1-53b6-492a-9bf5-2a17dfb8b62f.png)

Register task definition for frontend.

```
aws ecs register-task-definition --cli-input-json file://aws/task-definitions/frontend-react-js.json
```

And create service.

```
aws ecs create-service --cli-input-json file://aws/json/service-frontend-react-js.json
```

Created healthy fronend-react-js service.

![image](https://user-images.githubusercontent.com/96197101/229632579-ba06dac7-ab2e-4bf9-b2a1-34a666082523.png)


## Provision and configure Application Load Balancer along with target groups

Created Load Balancer.

![image](https://user-images.githubusercontent.com/96197101/229633074-e59003f9-7cc1-4b22-ac42-f32e8be11400.png)

Created target group for backend-flask.

![image](https://user-images.githubusercontent.com/96197101/229633381-f465b384-eb49-4971-b895-a46f7e335f36.png)

Health check confgiured in target backend-flask.

![image](https://user-images.githubusercontent.com/96197101/229633483-d51c7e07-75f2-471f-b627-697a58bfc844.png)


Created target group for frontend-react-js.

![image](https://user-images.githubusercontent.com/96197101/229633569-d0be2990-05aa-43be-87bf-fb8fca26616e.png)

Health check for frontend-react-js target group.

![image](https://user-images.githubusercontent.com/96197101/229633679-07528a6e-3402-4503-bade-2f61b7968cf3.png)

## 	Manage your domain useing Route53 via hosted zone

Domain cruddur.pl added to Route53.

![image](https://user-images.githubusercontent.com/96197101/229634442-dc1958f9-8511-403b-8e15-841f84324769.png)

Created SSL certificate via ACM.

![image](https://user-images.githubusercontent.com/96197101/229634619-7d9cad2f-a195-4f08-9be5-92ffea392713.png)

Setup a record set for naked domain to point to frontend-react-js.

![image](https://user-images.githubusercontent.com/96197101/229634902-6a9fff3e-3103-4f6d-8449-1d50940334bd.png)

Setup a record set for api subdomain to point to the backend-flask

![image](https://user-images.githubusercontent.com/96197101/229635014-08d1d0f7-1545-4101-964f-35ff3c33e1fb.png)


In Load Balancer set rule that redirect port 80 to 443.

![image](https://user-images.githubusercontent.com/96197101/229635155-9f82455a-775a-42ad-b00c-5cdeced8d81c.png)


And set up rules that redirect api.cruddur.pl to backend-flask target group and cruddur.pl redirect to frontend-react-js target group.

![image](https://user-images.githubusercontent.com/96197101/229635316-9eb3960c-aabb-4c1d-abea-a9b821dfb9b9.png)

cruddur.pl rediects to frontend-react-js.

![image](https://user-images.githubusercontent.com/96197101/229635562-cd00d286-9e66-4732-a1f2-e7fafc93010d.png)

api.cruddur.pl redirects to backend-flask.

![image](https://user-images.githubusercontent.com/96197101/229635660-2d664b1d-77c4-4a37-88f2-9895857a79b3.png)

## Secure Flask by not running in debug mode

Add to CMD in Dockerfile.prod in backend-flask --no-debug --no-debugger --no-reload. 

--no-debug: Disables the debug mode of the Flask application. When debug mode is enabled, Flask will display detailed error messages with a traceback in case of an exception. However, this can also be a security risk, as it can expose sensitive information about the application.

--no-debugger: Disables the interactive debugger that is included in the development server. The debugger allows you to step through the code and inspect variables at runtime, which can be very useful for debugging. However, this can also be a security risk, as it allows attackers to execute arbitrary code on the server.

--no-reload: Disables automatic reloading of the Flask application when code changes are detected. By default, Flask will automatically reload the application when changes are made to the code. This can be useful during development, as it eliminates the need to manually restart the server after every change. However, it can also be a performance issue in some cases, as the reloading process can slow down the development server.

![image](https://user-images.githubusercontent.com/96197101/232250585-32322c1a-4cbb-4616-8aa9-9ed3faa275ea.png)


## Implement Refresh Token for Amazon Cognito

Function getAccessToken() retrieves the access token for the currently signed-in user and stores it in the browser's local storage using localStorage.setItem().

Function checkAuth()checks if the user is authenticated and retrieves the user's display name and handle (preferred username) by calling Auth.currentAuthenticatedUser(). If the user is authenticated, it then retrieves the user's session information (which includes the access token) using Auth.currentSession() and stores the access token in the browser's local storage using localStorage.setItem(). 

![image](https://user-images.githubusercontent.com/96197101/232250822-6bb6958c-a609-49f9-95f0-d58effa42e92.png)


## Refactor bin directory to be top level

![image](https://user-images.githubusercontent.com/96197101/232251223-c9e7320d-8e0a-4974-85fd-b4cd628d2e38.png)

Example of shell script that sets some variables based on the location of the current script and some directories relative to it.

![image](https://user-images.githubusercontent.com/96197101/232251285-bedf35e4-42ce-40c4-af2e-173f6f13406c.png)

## Configure task defintions to contain x-ray and turn on Container Insights

backend-flask.json

![image](https://user-images.githubusercontent.com/96197101/232251333-5d963f77-b35f-4841-8eca-e74771577d4e.png)

frontend-react-js.json

![image](https://user-images.githubusercontent.com/96197101/232251348-571c02ce-282e-4536-a1e9-443e54a5a12d.png)

This code is defining a container named "xray" in an ECS task definition. The container is using an image named "public.ecr.aws/xray/aws-xray-daemon". The "essential" field is set to true, which means that if this container fails, the entire task will fail. The "user" field is set to "1337", which specifies the user that the container process will run as.

The container also has a port mapping defined in the "portMappings" field. This is specifying that traffic received on port 2000 using the UDP protocol will be forwarded to the container. The name "xray" is given to the port mapping for easier identification.


Turn on Container Insights.

![image](https://user-images.githubusercontent.com/96197101/232251434-169e8663-4c3d-469b-add9-6534cb49e6a5.png)

## Change Docker Compose to explicitly use a user-defined network

This code defines a network named "cruddur-net" using the "bridge" driver.

The "bridge" driver is a built-in driver that allows containers to communicate with each other and with the host machine using the same network interface. This is the default network driver for Docker containers.

The "name" attribute is optional and provides a user-defined name for the network. If no name is provided, Docker will automatically generate a unique name for the network.

Defining a network in a Docker Compose file allows multiple containers to communicate with each other using the same network, which can be useful for creating microservices architectures or for isolating different parts of an application.

![image](https://user-images.githubusercontent.com/96197101/232251527-d2547f14-38d3-44c8-92f9-3deb28eb81b3.png)

The "networks" attribute specifies that the "db" container should be connected to the "cruddur-net" network that was defined in the Docker Compose file.

![image](https://user-images.githubusercontent.com/96197101/232251532-be686da0-f8f1-4752-a5b5-2981bfba699e.png)


## Using ruby generate out env dot files for docker using erb templates

generate-env for backend

![image](https://user-images.githubusercontent.com/96197101/232251583-91380540-5be6-4665-85ea-6533e9498155.png)

erb file for backend

![image](https://user-images.githubusercontent.com/96197101/232251616-788247a0-1e0a-404b-ad40-8f57c4f50cee.png)


generate-env for frontend

![image](https://user-images.githubusercontent.com/96197101/232251589-9698fee9-499b-46ec-95f7-c5afbfe09ce9.png)

erb file for frontend 

![image](https://user-images.githubusercontent.com/96197101/232251621-4ddada9a-7c31-4789-9434-a141c2d5751f.png)

This script reads the contents of a file named "erb/backend-flask.env.erb", which is an ERB template file. The script then evaluates the template using the Ruby ERB library, which replaces any embedded Ruby code within the template with the output of that code.

The resulting output is then written to a new .env file for backend and frontend.


