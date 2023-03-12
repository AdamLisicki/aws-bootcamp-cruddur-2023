# Week 4 — Postgres and RDS

## Provision RDS Instance

I used below command to create db.t3.micro RDS Instance that is listening on port 5432. 

````
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username root \
  --master-user-password *************** \
  --allocated-storage 20 \
  --availability-zone us-east-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --enable-performance-insights \
  --performance-insights-retention-period 7 \
  --no-deletion-protection
  ````
  
  After RDS Instance was created I stopped it temporarily for 7 days.
  
  ![image](https://user-images.githubusercontent.com/96197101/224542782-5203d344-a9c0-46fd-b0e0-e8aa8a55736d.png)

# Creating PostgreSQL container

In the docker compose file I have already wrote code that creates PostgrSQL containter.

![image](https://user-images.githubusercontent.com/96197101/224543082-e2db55b6-4af9-4df1-a41b-44a9414cfbde.png)

After docker compose up I am able to log into PostgresSQL instance and list databases.

![image](https://user-images.githubusercontent.com/96197101/224543684-67935d5c-4d70-4034-9768-6676e5a5499c.png)

## Creating files for schema and seed.

schema.sql file for defining a schema of database.

![image](https://user-images.githubusercontent.com/96197101/224545685-7fbb4606-bfa2-470e-8e29-5c28c7143379.png)

seed.sql file for insterting some data into database.

![image](https://user-images.githubusercontent.com/96197101/224545711-42409c5d-7159-444b-b56e-de94f138d5ac.png)



## Creating bash scripts that create, drop, load schema and seed.

Before creating bash scripts I created environment variables with connection string to development database (local PSQL instance) and production database (AWS RDS PSQL instance).  

After creating each of the scripts I used command <code> chmod +x [PATH_TO_SCCRIPT] </code> to give it permission to executing. 

I am using Gitpod so all scripts will be created in the path <code>/workspace/aws-bootcamp-cruddur-2023/backend-flask/bin</code>, so I added this path to environment variable named PATH to run this scripts as the commands.

![image](https://user-images.githubusercontent.com/96197101/224544301-007e8069-49a6-44df-b667-8449e69eedc1.png)

![image](https://user-images.githubusercontent.com/96197101/224545054-1378f959-81de-4a2e-a8ca-311ef08946c9.png)

And also I added this to <code>.gitpod.yml</code> file to added this path to var PATH everytime I run Gitpod.

![image](https://user-images.githubusercontent.com/96197101/224545099-abc6b799-3d37-444d-9f58-ed4d33056aaf.png)


### Script to Create DB.

Script is removing name of database from my env var and assings it to variable NO_DB_CONNECTION SQL. Then script is executing command for creating database inside PSQL instance that connection string is pointing to. 

![image](https://user-images.githubusercontent.com/96197101/224543846-950e18bc-d8be-4743-b4e4-2eaf41e9eb2a.png)

After execuiting <code>db-create</code> command database is created. 

![image](https://user-images.githubusercontent.com/96197101/224545136-5353c5fd-1e9b-4c9f-8860-905a91fe6ca7.png)

### Script to load a schema.

First script is assinging a path to my database schema which is located in backend/db/schema.sql.
Then if script will be called with parameter <code>prod</code> diffrent database connection string is assiging to variablee URL. <code>$1</code> means first parameter after command eg. <code> db-schema-load prod </code> prod is "$1" and "$0" is command. 
And then script is loading schema into database. 

![image](https://user-images.githubusercontent.com/96197101/224544594-0bfdb00d-716e-4a62-ae31-4c7d54877d44.png)

After execuiting <code>db-schema-load</code> command schema is loaded into database.

![image](https://user-images.githubusercontent.com/96197101/224545171-113d47d9-69af-4d2d-9802-3af027d41cbb.png)


### Script to load the seed data.

This script is the same as for loading schema, but only difference is variable that is pointing to <code>seed.sql</code>. 

![image](https://user-images.githubusercontent.com/96197101/224545225-e0c8039e-1700-4a3f-8575-251112e044e7.png)

After execuiting <code>db-seed</code> command database is poplulated with data.

![image](https://user-images.githubusercontent.com/96197101/224545254-7caa76f1-8e3c-4e90-9267-803f466dfe06.png)


###  Script to Connect to DB

Script is using the environment variable with the connection string and executing command that is connecting to the database.

![image](https://user-images.githubusercontent.com/96197101/224545277-cb7e17f8-f7dd-4120-aa04-e65a06f2c5f5.png)

After execuiting <code>db-connect</code> command I am able to connect to database.

![image](https://user-images.githubusercontent.com/96197101/224545391-cc911415-ff35-4c12-a816-45bbf68974f2.png)

And all tables are created and schemas are loaded.

![image](https://user-images.githubusercontent.com/96197101/224545454-3221a325-79fd-4854-a405-c19304176f19.png)

![image](https://user-images.githubusercontent.com/96197101/224564569-cb05f9b2-2298-46c9-9ecc-4c7c3e6d1d23.png)

### Script to see open connections to our database

![image](https://user-images.githubusercontent.com/96197101/224565038-77341e46-8c1e-497c-9217-e5886f35b56f.png)

And when we connect to our db through GUI and run db-session command we can see open connections to our database.

![image](https://user-images.githubusercontent.com/96197101/224564830-c22d6f68-4746-4db4-babd-6db0896b8c81.png)

![image](https://user-images.githubusercontent.com/96197101/224564843-c1770933-9e18-43ea-9306-de0f966e4e1f.png)

## Script to setup DB

![image](https://user-images.githubusercontent.com/96197101/224565993-26a23e93-b23a-48c8-9307-c98af682caef.png)

After running db-setup command.

![image](https://user-images.githubusercontent.com/96197101/224565738-4cd2b0a3-f201-4385-a5b3-7574510949c1.png)


### Script to Drop DB

This script is the same as for creating database, but only difference is that used command in psql is for droping database.


![image](https://user-images.githubusercontent.com/96197101/224545588-033fe3ae-3df8-44d5-8c66-48e0bd78243e.png)

After executing this command database is dropped.

![image](https://user-images.githubusercontent.com/96197101/224545606-f74784af-6867-4dc9-8db4-4e7f7c8f4399.png)

## Install driver for PostgreSQL

Add <code> psycopg </code> and <code> psycopg </code> drivers to the requirements.txt file.

![image](https://user-images.githubusercontent.com/96197101/224566511-5e935c7d-b8c2-4f04-b24e-9a9a337d764f.png)

And run <code> pip install -r requirements.txt </code>.

Then setup environemnt variable in docker compose file for backend-flask.

![image](https://user-images.githubusercontent.com/96197101/224574510-cb5ab647-72f1-498e-af21-f4f43164f3af.png)

Create file lib/db.py and put code into it that creating connection pool for database.
This two functions are here for converting data from SQL query to json format.

![image](https://user-images.githubusercontent.com/96197101/224574587-d9f6e726-20e2-41e1-9116-f09e0ba78fb0.png)


In the home_activities.py file modify a code to connect to database, run query, transform it to json and return. 

![image](https://user-images.githubusercontent.com/96197101/224574707-f4dd55bc-918e-473c-86b4-b16982c7dbec.png)

After compose up I could see that we are getting data from database.

![image](https://user-images.githubusercontent.com/96197101/224574840-859fb0b4-fd37-4e20-88ed-34b610ba1edf.png)

Then in the home_activities.py file modify query to get only data that we want.

![image](https://user-images.githubusercontent.com/96197101/224574995-a0be29d3-2764-478d-ab81-f94fd8e56f84.png)

And the result. Username and preffered username showed up. 

![image](https://user-images.githubusercontent.com/96197101/224575011-6d8c9a1c-b677-4699-a7b2-2b6fa7dbcb88.png)


## Connect to AWS SQL RDS from Gitpod

After starting RDS instance go to security group associated with it.

![image](https://user-images.githubusercontent.com/96197101/224575956-34861876-26f9-4a6e-bb41-f136caf19b56.png)

Go to Edit Inboud Rules.

![image](https://user-images.githubusercontent.com/96197101/224575982-26904468-4c05-44a3-8323-a7f91e970d6b.png)

To get Gitpod ip address run below command.

![image](https://user-images.githubusercontent.com/96197101/224576042-44aba393-0393-4456-b1b8-86355397250f.png)

And add it to inboud rules and save them.

![image](https://user-images.githubusercontent.com/96197101/224576086-5225e472-e49b-4a45-8e20-3bb9a98c4246.png)

Now I can connect to RDS instance.

![image](https://user-images.githubusercontent.com/96197101/224576111-4e3da619-af0c-428a-8435-80d075763512.png)

But Gitpod ip address will not be the same every time so I need to create script that updates inboud rules.

I set up the environment variables for securitu group ID and inboud rule ID.

Script for updating SG rule.

![image](https://user-images.githubusercontent.com/96197101/224576975-cc697109-fcd1-4745-9f93-93c1c0279818.png)

Add this commands to <code>.gitpod.yml</code> file to run it everytime the new Gitpod environment lunches up.

![image](https://user-images.githubusercontent.com/96197101/224577837-d6c7ce46-ce91-481c-b1c2-b99bb0c594b4.png)












