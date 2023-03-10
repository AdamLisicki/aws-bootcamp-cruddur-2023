# Week 2 — Distributed Tracing

## Instrument Honeycomb with OTEL

I set up environment varaible with API key for a shell and a Gitpod.

![image](https://user-images.githubusercontent.com/96197101/223701553-35df6495-a1ca-4ce6-b84f-6fcc2c641511.png)

I set up the environment variables for backend in the docker-compose file.

![image](https://user-images.githubusercontent.com/96197101/223700285-0a0cdd55-9f90-4284-80be-acf1b932b692.png)

I added python libraries to requirements.txt file.

![image](https://user-images.githubusercontent.com/96197101/223721899-48c72d69-d4c0-45a1-938a-0c77d00876f8.png)

And then run below command.

````
pip install -r requirements.txt
````
![image](https://user-images.githubusercontent.com/96197101/223723494-ac6e14c6-61a3-4ac3-a0e7-5741ff06e43c.png)

I imported required libries to app.py file.

![image](https://user-images.githubusercontent.com/96197101/223723783-e1ac680f-fb88-47e3-bd53-9f7f75896168.png)

I added code to the app.py file that initialize tracing and an exporter that can send data to Honycomb.

![image](https://user-images.githubusercontent.com/96197101/223725619-07d333a0-24ac-4051-a8cc-50051bcc8fd0.png)

I wrote to the app.py file code that initializes automatic instrumentation with Flask.

![image](https://user-images.githubusercontent.com/96197101/223725999-e1228242-c228-46b4-9f15-2156f1e5ee27.png)

I run custom query that shows latency for selected user id.

![image](https://user-images.githubusercontent.com/96197101/223766810-13b6b62f-0a95-44fb-b5ee-234a9ca0c0c7.png)

I saved this query in a board. 

![image](https://user-images.githubusercontent.com/96197101/223767188-5bab4226-70d6-4594-bc5c-697d26f94bdf.png)




And now when i hit an enpoint data is send to Honeycomb.

![image](https://user-images.githubusercontent.com/96197101/223733098-01f1a607-6406-4df0-9bba-14371814a672.png)

I created custom span for home activities endpoint. 

![image](https://user-images.githubusercontent.com/96197101/223753697-b913a110-b93f-4564-8181-568bd1fb4e84.png)

In Honeycomb I can see created span.

![image](https://user-images.githubusercontent.com/96197101/223754838-5512832a-939f-478b-9f7d-6358cb32a894.png)

I added custom attribute to span user.id with hard coded value of User ID.

![image](https://user-images.githubusercontent.com/96197101/223761530-6ee4ed15-5be3-4aae-962a-7602a30e2cc5.png)

After implementation of Amazon Cognito from Week 3 of the bootcamp I change hard coded value to ID of logged in user.

![image](https://user-images.githubusercontent.com/96197101/223764183-9136c91b-917b-4c29-8134-b19864c25ed9.png)

When I hit now this enpoint I can see in Honeycomb ID of user who call this endpoint.

![image](https://user-images.githubusercontent.com/96197101/223764481-3b888dc3-61c8-4684-b438-9b9b1eb34026.png)

I created query that shows latencies of specified UserId.

![image](https://user-images.githubusercontent.com/96197101/223767636-5de8344b-171a-41d4-9d63-176d7e2593b6.png)

I saved this query in the board.

![image](https://user-images.githubusercontent.com/96197101/223767759-1ef0e0d9-24f0-46c2-8b2b-f5c404f52ca4.png)

## Instrument AWS X-Ray

Firstly I added <code>aws-xray-sdk</code> to the requirements.txt file and then run <code> pip install -r requirements.txt </code> to install AWS X-RAY SDK.

![image](https://user-images.githubusercontent.com/96197101/223838244-4f5c49df-ee32-4f96-aafc-0e9d9a713126.png)

![image](https://user-images.githubusercontent.com/96197101/223838332-a5f85cb6-e04b-43ca-b851-a13c212afd36.png)

I created a xray group.

![image](https://user-images.githubusercontent.com/96197101/223842085-4388aa2a-9f72-4bda-aba8-95dc2166229b.png)

I created a sampling rule.

![image](https://user-images.githubusercontent.com/96197101/223843997-fb76c569-a167-4863-a136-1e5a75a29237.png)

Added to the docker compose file lines that create a container with a X-Ray deamon.

![image](https://user-images.githubusercontent.com/96197101/223860608-91f92f3d-0ff4-4326-a2b4-19cea1e54dc6.png)

Added two environment variables for X-ray.

![image](https://user-images.githubusercontent.com/96197101/223863868-ee4a3701-3a17-4b3b-983f-852580830da4.png)

Added code for X-ray in the app.py file.

![image](https://user-images.githubusercontent.com/96197101/223866920-f6eb4d17-2be6-406f-9768-c131502c4064.png)

I run docker compose up.

![image](https://user-images.githubusercontent.com/96197101/223867099-2b74dbfb-9e44-4a78-9dfc-8793b71823cd.png)

I hit an endpoint few times. 

![image](https://user-images.githubusercontent.com/96197101/223867163-27a0a13c-0b9c-4778-a036-b2a94ab817e0.png)

In the x-ray contaier logs I see that data is send to AWS X-ray.

![image](https://user-images.githubusercontent.com/96197101/223867229-7169575a-e36f-42c5-877d-c1eca3612600.png)

In AWS Portal I can see that data showed up.

![image](https://user-images.githubusercontent.com/96197101/223867479-811690b8-a726-435c-b927-7baa0e12b65d.png)

## Instrument AWS X-Ray Subsegments

Create a segment for /api/activities/home and /api/activities/@user endpoints.

![image](https://user-images.githubusercontent.com/96197101/224176741-e0063a2d-a733-4da8-8738-098df19ce5e3.png)

And when I hit an /api/activities/home endpoint In the X-Ray I can see created segment.

![image](https://user-images.githubusercontent.com/96197101/224176926-0bb98e93-137e-4da7-8200-403a94c2ea2c.png)

Create subsegment for the user activities endpoint.

![image](https://user-images.githubusercontent.com/96197101/224177345-1611338a-de9b-4eec-b678-19867d8d414b.png)

After hitting an /api/activities/@andrewbrown endpoint X-Ray is showing created subsegment named "mock-data".

![image](https://user-images.githubusercontent.com/96197101/224177780-488b95db-6642-4f0f-ae13-418ac4213680.png)


## Configure custom logger to send to CloudWatch Logs

Added <code>watchtower</code> to requirements.txt and then run <code>pip install -r requirements.txt</code>

In the app.py file add this piece of code to configure logger to use CloudWatch.

![image](https://user-images.githubusercontent.com/96197101/224444860-def275a6-f15a-49a3-a38c-8e3e750276cd.png)

In the home_activities.py file add this piece of code to add custom loggin to HomeActivities.

![image](https://user-images.githubusercontent.com/96197101/224445006-8b0c137f-2b43-43b1-b644-567705b2eaaf.png)


And in the /api/activities/home endpoind add value to the argument logger of <code>run</code> method. 

![image](https://user-images.githubusercontent.com/96197101/224445104-25286e24-daa3-466d-b032-a6a474731e7b.png)

And when I run the app I can see the logs in CloudWatch.

![image](https://user-images.githubusercontent.com/96197101/224445325-30073b91-398e-4b77-b6c4-1a974395cbef.png)

![image](https://user-images.githubusercontent.com/96197101/224445355-63454ead-a9c8-4366-a0df-1ed544b7bacd.png)


## Integrate Rollbar and capture and error

Added <code>blinker</code> and <code>rollback</code> to requirements.txt and then run <code>pip install -r requirements.txt</code>

Then set environment variable for rollback access token and add it to the docker-compose file.

Add this lines of code to the app.py file.

![image](https://user-images.githubusercontent.com/96197101/224446851-91d0cdb9-bdfb-416b-ac60-abfe846c62cc.png)

![image](https://user-images.githubusercontent.com/96197101/224446888-21b1a863-f15f-4971-864d-ee04ee099c63.png)

After docker compose up and hitting /rollbar/test endpoint in rollbar I can see items.

![image](https://user-images.githubusercontent.com/96197101/224447249-cc9e6d9d-8d1d-4bee-85db-2875f96ac97e.png)

![image](https://user-images.githubusercontent.com/96197101/224447285-1aae45ac-7caa-494c-9b7f-ce77d03c123b.png)

![image](https://user-images.githubusercontent.com/96197101/224447311-e381ca47-c55b-46ea-a036-7e57cce31619.png)








