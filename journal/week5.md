# Week 5 — DynamoDB and Serverless Caching

 ## Implement Schema Load Script
 
 I wrote schema-load python script that create table named "cruddur-messages" in my local dynamodb instances.
 
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

