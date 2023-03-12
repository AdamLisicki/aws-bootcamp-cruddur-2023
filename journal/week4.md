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

![image](https://user-images.githubusercontent.com/96197101/224565884-4a0a1398-b638-4978-8e3d-58d401088d1f.png)

After running db-setup command.

![image](https://user-images.githubusercontent.com/96197101/224565738-4cd2b0a3-f201-4385-a5b3-7574510949c1.png)


### Script to Drop DB

This script is the same as for creating database, but only difference is that used command in psql is for droping database.


![image](https://user-images.githubusercontent.com/96197101/224545588-033fe3ae-3df8-44d5-8c66-48e0bd78243e.png)

After executing this command database is dropped.

![image](https://user-images.githubusercontent.com/96197101/224545606-f74784af-6867-4dc9-8db4-4e7f7c8f4399.png)

