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

