# Week 5 — DynamoDB and Serverless Caching

 ## Implement Schema Load Script
 
 I wrote schema-load python script that create table named "cruddur-messages" in my local dynamodb instance.
 
 ![image](https://user-images.githubusercontent.com/96197101/227774661-89f065b9-2a0d-418c-ae50-6804d92c1f7d.png)
 
 After execution of this script table has been created.
 
 ![image](https://user-images.githubusercontent.com/96197101/227774870-a6f06604-7094-4e25-af8b-b591916aa0d8.png)

## Implemet List Tables Script

Script that list all tables in dynamodb database.

![image](https://user-images.githubusercontent.com/96197101/227777494-07d8ba29-7476-4b75-bc20-04c86e794d70.png)

Result of executing this script.

![image](https://user-images.githubusercontent.com/96197101/227777542-6f716920-1fb3-46a1-b480-c9462212e692.png)

## Implement Drop Table Script

This script drops table that name is provided as first argument while executing this script.

![image](https://user-images.githubusercontent.com/96197101/227777565-5cb4392c-9cfd-4c30-829c-ee64ab9d427b.png)


## Implement Seed Script

First part of script sets variable attrs. If a first argument is "prod" attrs is empty. 

![image](https://user-images.githubusercontent.com/96197101/227774978-086a790e-0896-4a90-bccd-8aec8deeaecc.png)

This function:
  1) Assigns the SQL request to variable "sql"
  2) To variable "users" is assigned return of function query_array_jason located in lib/db file. This function takes SQL request and arguments that are assigned to %(my_handle)s and (other_handle)s in SQL request and returns a JSON formatted user.uuid, display_name and handle.
  3) Then this function finds users with handle 'andrewbrown' and 'bayko' and assigns this handles to dictionary variable results.
  4) Function returns variable results. 

![image](https://user-images.githubusercontent.com/96197101/227776323-738c394b-d7be-4e4e-b837-47a355898585.png)


Next two functions are responisble for creating message and message_group in dynamodb table.

![image](https://user-images.githubusercontent.com/96197101/227775776-5c60c2a8-713d-4f6c-865b-674d41fcd104.png)

Then script calls function that creates message group for my_user and for other_user.

![image](https://user-images.githubusercontent.com/96197101/227775897-bd09d783-82d6-4dea-86ed-ba08668c0096.png)

To varaible "conversation" script assigns sample conversation between two persons.

![image](https://user-images.githubusercontent.com/96197101/227775946-18c2be61-d98d-486e-b14c-43d5bac36a46.png)

In the end script is taking each line from variable "conversation" and using function create_message creates a message. If "Person 1" is on the beginnig of line the uuid, display name and hande is provided in function create_message if "Person 2" is on the beginning of line values of other_user is assignet to arguments of crate_message function.

![image](https://user-images.githubusercontent.com/96197101/227776069-5088866d-b801-471e-98f5-1bfe3d59f899.png)

After executing scritp data is loaded into table.

![image](https://user-images.githubusercontent.com/96197101/227777290-da3bdb96-e460-487e-9a01-1675bf1e8daa.png)

## Implement Scan Script

Script that is printing all records in table "cruddur-messages".

![image](https://user-images.githubusercontent.com/96197101/227777319-ae5d5ad7-2df2-4063-bda4-744df0f19965.png)

After executing this script the conversation is printed in console.

![image](https://user-images.githubusercontent.com/96197101/227777399-658bf7b4-3856-41e3-8841-46a4ae0cb3bb.png)

## Implement Pattern Scripts for Read and List Conversations

Script that query table by pk that is equal to MSG#{message_group_id} and sk begins with 2023. So this scirpt will gave 20 messages (becouse limit in query is set to 20) that pk is equal to MSG#5ae290ed-55d1-47a0-bc6d-fe2bc2700399 and messages are from 2023 year.
Then script prints messages. 

![image](https://user-images.githubusercontent.com/96197101/227783206-35b54ac0-eb81-4962-a482-76c5ea436ed2.png)


After execution of that script 20 messages from conversation are listed.

![image](https://user-images.githubusercontent.com/96197101/227783833-c8c18519-c6c9-4ec6-8c11-476eb44c214b.png)

Script that gets user uuid and then query all groups messages of this user. 

![image](https://user-images.githubusercontent.com/96197101/227783938-1d3886fa-65b1-4852-a1ae-18076d988b9f.png)

After execution of this script response from dynamodb is printed.

![image](https://user-images.githubusercontent.com/96197101/227784082-398b02ab-1e58-4288-8a9d-e07580147646.png)

## Implement Update Cognito ID Script for Postgres Database

Script that updates cognito user ID in PSQL.

Funtion get_cognito_user_ids gets a Cognito user ID from user pool.
Function update_users_with_cognito_user_id takes users handle and Cognito user ID and updates a Cognito user ID in PSQL database for user with specified handle. 

![image](https://user-images.githubusercontent.com/96197101/228157123-7ee8a849-fafb-467a-b81f-040ef24d3766.png)

## Implement (Pattern B) Listing Messages Group into Application

Create a script that connects to DynamoDB and queries for message groups.

![image](https://user-images.githubusercontent.com/96197101/228183919-f534b30e-4d23-454e-b9c9-21c445e91f38.png)

SQL query that gets user UUID for specified Cognito user ID.

![image](https://user-images.githubusercontent.com/96197101/228168002-d2c478e0-5fa3-476f-b5f1-f36b9addd3be.png)

In message_groups.py add code that uses list_message_groups from Ddb.py file and returns message groups.

![image](https://user-images.githubusercontent.com/96197101/228184536-d4866a8a-5dcc-42bc-94b1-d2a879c9ed77.png)

In MessageGroupsPage.js we need to add headers to send acces_token to backend.

![image](https://user-images.githubusercontent.com/96197101/228185502-6f3464d4-2ea5-4950-a447-abb5f7139c21.png)

Then in app.py in /api/messages_group add code that uses message_group.py service and returns errors or data with message groups.

![image](https://user-images.githubusercontent.com/96197101/228184957-025f9191-2819-4c51-8bf3-b2b0e56d27b0.png)

When I sing in and click messages I can see that message group appears.

![image](https://user-images.githubusercontent.com/96197101/228193299-f43a3e26-d5d5-46a0-ba04-d2bd7ba0fdf0.png)


## Implement (Pattern A) Listing Messages in Message Group into Application

Function list_messages in lib/ddb.py file.
This function queries DynamoDB database for 20 messages from message group that ID is equal to value of message_group_id and messages are from current year.

![image](https://user-images.githubusercontent.com/96197101/228164591-4d327378-0a87-44b2-8e53-aad3d1ee0d5c.png)

services/messages.py 
This code calls function list_messages and returns messages for specified message_group_uuid.

![image](https://user-images.githubusercontent.com/96197101/228168355-01b60f9d-8451-4553-88d4-be699a7dd260.png)

In MessageGroupPage.js file we need to add headers to send access_token to backend.

![image](https://user-images.githubusercontent.com/96197101/228176317-621b6dbb-bddc-4dc4-8ab8-2a72a22912b2.png)

In app.py for endpoint /api/messages/message_group_uuid added code that takes Cognito user ID and message_group_uuid and returns 20 messages from specified message group. 

![image](https://user-images.githubusercontent.com/96197101/228174897-c6cc6baf-3e59-40ea-bcbe-5f392f3ea0d8.png)

When I click on message group I can see messages.

![image](https://user-images.githubusercontent.com/96197101/228193549-7bdad350-3ca8-4929-a689-4ab8968d1577.png)

## Implement (Pattern C) Creating a Message for an existing Message Group into Application/Implement (Pattern D) Creating a Message for a new Message Group into Application

In MessageForm.js condition that when new message_group is creating it takes "param.handle" and when we are updating existing one it takes "param.message_group_uuid". 

![image](https://user-images.githubusercontent.com/96197101/229279502-b83690b3-e987-4518-875d-b9b923d81c08.png)

In lib/ddb.py file create the method that creates a message. This method takes: message_group_uuid, message, my_user_uuid, my_user_display_name, my_user_handle. Then inserts it to the dynamodb database.  

![image](https://user-images.githubusercontent.com/96197101/229278573-26b7b681-43db-4eb9-8182-e72efc996a9a.png)

Create SQL query that returns user UUID, display name, handle and kind. It also recognizes if user is sender or reciver and assing it to column named "kind".

![image](https://user-images.githubusercontent.com/96197101/229280166-e654bc1e-f80c-4e0b-852e-866b5b117e0d.png)

In services/create_meesage.py the method create_mesage first validates some variables.

![image](https://user-images.githubusercontent.com/96197101/229280785-80a3bd62-65f8-437a-936a-27fdf291c59f.png)

Then this function executes SQL query that was created before and assigns value to my_user and other_user based on colum "kind".
Then depends on what value of variable mode it needs to craete new message_group or update exsiting one.

![image](https://user-images.githubusercontent.com/96197101/229280843-68242113-43d1-4104-bbb4-1ff13d52b98e.png)

In app.py function takes values from MessageForm.js response and if message_group_id is None new messsage group is created and otherwise exisiting message group is updated.

![image](https://user-images.githubusercontent.com/96197101/229281091-6099913d-87e1-4bcd-8c6f-d0840e8215fa.png)

Create new page for creation of new conversation. 

![image](https://user-images.githubusercontent.com/96197101/229284559-c0e4fa01-88cb-42cb-b3a5-261e968c4679.png)

In this new page we need to load data about user and message group.

![image](https://user-images.githubusercontent.com/96197101/229285017-93fe2783-ad5a-4b16-a91b-74c7d06331b7.png)

![image](https://user-images.githubusercontent.com/96197101/229285054-02980fcc-9221-42c1-b158-51a76fdfd142.png)

In order to load user data create a SQL query that return taht data.

![image](https://user-images.githubusercontent.com/96197101/229285140-0d55ec52-98b8-4767-abee-0b2fff8a6f3b.png)

Create services/user_short.py that executes this query and return user data.

![image](https://user-images.githubusercontent.com/96197101/229285178-44a848f5-f063-41e6-b862-9377a6689655.png)

In app.py add enpoint for user short to return user data.

![image](https://user-images.githubusercontent.com/96197101/229285218-afa0011a-32d7-4383-9278-159855d18640.png)

To create a item that we can click and enter the message group we need to create new file components/MessageGroupNewItem.js

![image](https://user-images.githubusercontent.com/96197101/229285394-13514c72-600b-4d9e-b58d-eea3d0be493a.png)

In MessageGroupFeed.js we need to add this new item.

![image](https://user-images.githubusercontent.com/96197101/229285465-4f2cf8b9-cb74-4605-9d48-8b21bde8edda.png)

To redirect to proper page after creation of new message group we need to add rhis if else statement.

![image](https://user-images.githubusercontent.com/96197101/229285657-f9646631-5a0d-4313-9fb4-cbd2bb2ffea7.png)

In ddb.py create new method that creates a message group in in table "cruddur-messages" of dynamodb database.

![image](https://user-images.githubusercontent.com/96197101/229285753-eebdd367-7960-40db-83b9-f26bd1393cbf.png)
![image](https://user-images.githubusercontent.com/96197101/229285757-de149684-491f-497b-b66b-d9e1d5cc4272.png)

And when I go to /messages/new/adamlisicki page as Andrew Brown is logged in the message group is created and it is redirected to correct page with message_group_uuid.

![image](https://user-images.githubusercontent.com/96197101/229285927-ff660529-73f9-46db-a9d6-1058faa7fa76.png)


When I log in as Adam Lisicki I can see new message group and message from Andrew Brown.

![image](https://user-images.githubusercontent.com/96197101/229285991-be9176e4-855f-457f-950b-cc666df65d75.png)













