# Week 8 — Serverless Image Processing

## Implement CDK Stack

Create a new directory.

![image](https://user-images.githubusercontent.com/96197101/232309067-d8341912-8842-415e-a224-618ec2756f51.png)


 Install AWS CDK. 
 
 ```
 npm install aws-cdk -g
```

Go to the newly created directory and run the command below to initialize a new CDK project.

```
cdk init app --language typescript
```

Create a method that import existing bucket.

The code defines a function that returns an Amazon S3 bucket instance created from the given bucket name and adds it to an AWS CloudFormation or AWS CDK stack.

![image](https://user-images.githubusercontent.com/96197101/232309343-eb06b746-3630-4551-9f3b-6ea028d02aef.png)


Create a method that create a new lambda function.

This code defines a function named createLambda that takes four string parameters: functionPath, bucketName, folderInput, and folderOutput.

The runtime parameter specifies that the Lambda function will run on Node.js version 18.x.

The handler parameter specifies the name of the file and function that will handle the Lambda function's events. In this case, the index.js file's handler function will handle the events.

The code parameter specifies the location of the code for the Lambda function.

The environment parameter defines the Lambda function's environment variables. These variables include the destination S3 bucket name (DEST_BUCKET_NAME), the input folder for processing (FOLDER_INPUT), the output folder for the processed images (FOLDER_OUTPUT), and the desired width and height of the processed images (PROCESS_WIDTH and PROCESS_HEIGHT).

The function returns the created lambdaFunction object, which can be used to further configure and deploy the Lambda function.

![image](https://user-images.githubusercontent.com/96197101/232309879-18521afb-4bb7-49ba-9a84-38be186bc565.png)

Create methods that create SNS Topic and SNS Subscription.

The first method createSnsTopic takes a string parameter topicName and creates an Amazon SNS topic using the AWS CDK's sns.Topic class. 

The second method createSnsSubscription takes two parameters: an snsTopic object and a webhookUrl string. It creates an SNS subscription to the specified snsTopic using the addSubscription method on the snsTopic object. The subscription type is set to UrlSubscription, which sends notifications to a webhook URL.

![image](https://user-images.githubusercontent.com/96197101/232310134-76fa14e2-f5cc-4d48-8563-ea2867c455a8.png)

Create two methods that create Event Notification for Lambda and SNS.

The createS3NotifyToLambda method takes three parameters: prefix as a string, an lambda object representing an AWS Lambda function, and a bucket object representing an Amazon S3 bucket.

The function adds an event notification configuration to the bucket object using the addEventNotification method. The configuration specifies that when an object is created and put in the S3 bucket with the given prefix, a notification event will be sent to the specified lambda object.

The createS3NotifyToSns method takes three parameters: prefix as a string, an snsTopic object representing an Amazon SNS topic, and a bucket object representing an Amazon S3 bucket.

The function adds an event notification configuration to the bucket object using the addEventNotification method. The configuration specifies that when an object is created and put in the S3 bucket with the given prefix, a notification event will be sent to the specified snsTopic object.

![image](https://user-images.githubusercontent.com/96197101/232311115-f746f3b1-d43b-4c5b-80e5-126ceefc068f.png)


Create a method that craete a policy for lambda so it can Get and Put objects.

The policy statement allows for the s3:GetObject and s3:PutObject actions to be performed on any object within the specified S3 bucket (represented by the bucketArn parameter).

![image](https://user-images.githubusercontent.com/96197101/232312370-a1313971-879f-4b7f-801d-d03bbbcb68db.png)

Now we can call each of the functions and add them to our CDK stack.

![image](https://user-images.githubusercontent.com/96197101/232312491-0293fd87-7c8f-4140-8668-5b368a3590c3.png)

Run command below to set up the necessary infrastructure to store and deploy your application assets 

The cdk bootstrap command is used to set up the AWS resources required to deploy your AWS CDK (Cloud Development Kit) application. When you run this command, the AWS CDK CLI (Command Line Interface) will create a new Amazon S3 bucket in your AWS account, and it will use this bucket to store your CDK application assets.

```
cdk bootstrap "aws://$AWS_ACCOUNT_ID/$AWS_DEFAULT_REGION"
```
Create a env vars file.

![image](https://user-images.githubusercontent.com/96197101/232312648-959ddeec-443a-42c1-81eb-703a8f8434d4.png)


All of imports that our code needs.

![image](https://user-images.githubusercontent.com/96197101/232312671-c25fd867-f84f-4c63-9454-c7ff69047e82.png)


Create a lambda code.

Create Node.js module that exports four functions.

1. getClient(): This function creates a new S3Client instance from the AWS SDK for JavaScript v3 and returns it. The S3Client is used to interact with an S3 bucket in the AWS account.
2. getOriginalImage(client, srcBucket, srcKey): This function takes in an S3Client instance, a source S3 bucket name, and a source S3 object key. It returns a buffer that contains the original image retrieved from the source S3 bucket and object key specified. The function uses the GetObjectCommand from the AWS SDK to get the S3 object, and then uses the response.Body property to read the S3 object stream.
3. processImage(image, width, height): This function takes in an image buffer, a width, and a height. It uses the sharp library to resize and compress the image. It then returns a new buffer that contains the processed image.
4. uploadProcessedImage(client, dstBucket, dstKey, image): This function takes in an S3Client instance, a destination S3 bucket name, a destination S3 object key, and a buffer containing the processed image. It uses the PutObjectCommand from the AWS SDK to upload the processed image buffer to the destination S3 bucket and object key specified.

![image](https://user-images.githubusercontent.com/96197101/232312737-9374fad6-7cf8-46f9-adac-967d84ad2463.png)

 This code defines an AWS Lambda function that performs image processing on S3 objects and uploads the processed images to another S3 bucket.

![image](https://user-images.githubusercontent.com/96197101/232312839-2b0fe395-c65a-4920-8ece-af13c26f05f2.png)


package.json file for lambda function.

![image](https://user-images.githubusercontent.com/96197101/232313404-d797f5ee-917f-4936-afc2-20d20608855c.png) 

Run "npm install" in the lambda directory.

Create a bash script that install all dependencies for the CDK project.

![image](https://user-images.githubusercontent.com/96197101/232313535-5271801c-e390-4af1-9ec8-1e842e073ed2.png)

In the our project folder we can run "cdk deploy" to deploy our CDK stack.

Create a bash script for uploading an image to our S3 bucket.

![image](https://user-images.githubusercontent.com/96197101/232313998-a0e7215d-0840-4580-889a-b7773dccaf1a.png)

Create a bash script for deleting an image to our S3 bucket.

![image](https://user-images.githubusercontent.com/96197101/232314008-111efd0a-2801-400d-a3a0-b01a3d7a5e42.png)

Upload file to our repo.

![image](https://user-images.githubusercontent.com/96197101/232314069-7e544f72-44c1-44b4-8576-017b66eddfe2.png)

And upload it to our S3 bucket using the bash script.

![image](https://user-images.githubusercontent.com/96197101/232314092-04015961-0e2a-41bb-9ecd-6ab74788e714.png)

An image has beed uploaded to avatars/original directory.

![image](https://user-images.githubusercontent.com/96197101/232314126-42ead005-c1a0-49c6-ac82-d9a57fe2bef8.png)

And then processed by lambda function and put into avatars/processed directory.

![image](https://user-images.githubusercontent.com/96197101/232314172-a1c10fd3-0c49-4a3b-ad15-6b6cc3946f9b.png)


## Serve Avatars via CloudFront

Created CloudFront for S3 assets.cruddur.pl

![image](https://user-images.githubusercontent.com/96197101/232782905-abcc8c23-21d2-4079-8de1-928f5a6feb41.png)

![image](https://user-images.githubusercontent.com/96197101/232783088-f64b6484-4e12-459a-a34b-f167480fe07e.png)

Add entry to Route53.

![image](https://user-images.githubusercontent.com/96197101/232783263-6ca1a2ab-5d99-464d-82a8-5917a70ab956.png)

Add plicy to S3 bucket.

![image](https://user-images.githubusercontent.com/96197101/232783454-36f4cdb8-7a7a-418a-9178-4d921fb77ac0.png)

And image is visible on https://assets.cruddur.pl/avatars/data.jpg

![image](https://user-images.githubusercontent.com/96197101/232783535-fe5008e0-2d59-4573-9a3a-5bc359da79e2.png)


## Implement Users Profile Page

Update UserFeedPage.js

![image](https://user-images.githubusercontent.com/96197101/232796526-e377759d-5c03-4cde-91c1-0307053ecfc0.png)

Create a new component ProfileHeading.js

![image](https://user-images.githubusercontent.com/96197101/232796909-2a49c897-eab5-4ff6-b83f-7fb37474b242.png)

Upload banner image to assets.cruddur.pl bucket.

![image](https://user-images.githubusercontent.com/96197101/232802095-019540fb-d0a1-4636-9f94-9ab61773345a.png)


Set up CSS for ProfileHeading.js

![image](https://user-images.githubusercontent.com/96197101/232797063-fe3b19b2-e154-4e3c-8a24-e7ae462cedae.png)

Create a new component EditProfileButton.js

![image](https://user-images.githubusercontent.com/96197101/232797251-16b59a7c-d498-41ce-ac0b-15300eb4bd92.png)

Set up CSS for EditProfileButton.js

![image](https://user-images.githubusercontent.com/96197101/232797333-be650480-8ca8-490d-8bdc-1db41c42fb21.png)

Modify ActivityFeed.js component.

![image](https://user-images.githubusercontent.com/96197101/232797666-9ea040fd-6752-48c1-9f98-ab8369553dc3.png)

Modify user_activities.py service.

![image](https://user-images.githubusercontent.com/96197101/232797891-b9169644-6e0b-4cf6-bceb-a46ba555e3c3.png)

Create sql query show.sql

![image](https://user-images.githubusercontent.com/96197101/232798299-14760d9e-21a2-4f7d-8a3b-f309f8c66fd3.png)

Go to the profile tab.

![image](https://user-images.githubusercontent.com/96197101/232801805-0c46932f-65fb-4304-82b7-6c03b611b257.png)

## Implement Users Profile Form


Write a ProfileForm.js component.

```js
import './ProfileForm.css';
import React from "react";
import process from 'process';
import {getAccessToken} from 'lib/CheckAuth';

export default function ProfileForm(props) {
  const [bio, setBio] = React.useState(0);
  const [displayName, setDisplayName] = React.useState(0);

  React.useEffect(()=>{
    console.log('useEffects',props)
    setBio(props.profile.bio);
    setDisplayName(props.profile.display_name);
  }, [props.profile])

  const onsubmit = async (event) => {
    event.preventDefault();
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/profile/update`
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      const res = await fetch(backend_url, {
        method: "POST",
        headers: {
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          bio: bio,
          display_name: displayName
        }),
      });
      let data = await res.json();
      if (res.status === 200) {
        setBio(null)
        setDisplayName(null)
        props.setPopped(false)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const bio_onchange = (event) => {
    setBio(event.target.value);
  }

  const display_name_onchange = (event) => {
    setDisplayName(event.target.value);
  }

  const close = (event)=> {
    console.log('close',event.target)
    if (event.target.classList.contains("profile_popup")) {
      props.setPopped(false)
    }
  }

  if (props.popped === true) {
    return (
      <div className="popup_form_wrap profile_popup" onClick={close}>
        <form 
          className='profile_form popup_form'
          onSubmit={onsubmit}
        >
          <div class="popup_heading">
            <div class="popup_title">Edit Profile</div>
            <div className='submit'>
              <button type='submit'>Save</button>
            </div>
          </div>
          <div className="popup_content">
            <div className="field display_name">
              <label>Display Name</label>
              <input
                type="text"
                placeholder="Display Name"
                value={displayName}
                onChange={display_name_onchange} 
              />
            </div>
            <div className="field bio">
              <label>Bio</label>
              <textarea
                placeholder="Bio"
                value={bio}
                onChange={bio_onchange} 
              />
            </div>
          </div>
        </form>
      </div>
    );
  }
}
```
This code defines a component named ProfileForm, which renders a form for editing a user profile. The form contains two input fields: a text input field for the display name and a textarea field for the bio. The component receives props as a parameter which contains the profile object that represents the current user's profile. When the component is mounted or the profile object changes, the useEffect hook is called to update the input fields with the values from the profile object. The component also has an onsubmit function that is called when the form is submitted. This function sends a POST request to a backend API endpoint using the fetch function to update the user's profile information. If the API request is successful, the input fields are reset to their initial state, and the setPopped function is called with false to close the popup window that contains the form. The close function is used to close the popup window when the user clicks outside of the form.

Write CSS for the ProfileForm.js

```css
form.profile_form input[type='text'],
form.profile_form textarea {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 16px;
  border-radius: 4px;
  border: none;
  outline: none;
  display: block;
  outline: none;
  resize: none;
  width: 100%;
  padding: 16px;
  border: solid 1px var(--field-border);
  background: var(--field-bg);
  color: #fff;
}

.profile_popup .popup_content {
  padding: 16px;
}

form.profile_form .field.display_name {
  margin-bottom: 24px;
}

form.profile_form label {
  color: rgba(255,255,255,0.8);
  padding-bottom: 4px;
  display: block;
}

form.profile_form textarea {
  height: 140px;
}

form.profile_form input[type='text']:hover,
form.profile_form textarea:focus {
  border: solid 1px var(--field-border-focus)
}

.profile_popup button[type='submit'] {
  font-weight: 800;
  outline: none;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
  font-size: 16px;
  background: rgba(149,0,255,1);
  color: #fff;
}
```

Add import to ProfileFeedPage.js

```js
import ProfileForm from 'components/ProfileForm';
```

Add ProfileForm to ProfileFeedPage.js

```js
   <ProfileForm 
          profile={profile}
          popped={poppedProfile} 
          setPopped={setPoppedProfile} 
        />
```

Write the Popup.css file and delete popup elements from ReplyForm.css.

```css
.popup_form_wrap {
    z-index: 100;
    position: fixed;
    height: 100%;
    width: 100%;
    top: 0;
    left: 0;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    padding-top: 48px;
    background: rgba(255,255,255,0.1)
  }

  .popup_form {
    background: #000;
    box-shadow: 0px 0px 6px rgba(190, 9, 190, 0.6);
    border-radius: 16px;
    width: 600px;
  }

  .popup_form .popup_heading {
    display: flex;
    flex-direction: row;
    border-bottom: solid 1px rgba(255,255,255,0.4);
    padding: 16px;
  }

  .popup_form .popup_heading .popup_title{
    flex-grow: 1;
    color: rgb(255,255,255);
    font-size: 18px;

  }
```

Import this CSS file to App.js.

```js
import './components/Popup.css';
```

Create service for updating a profile information in a database.

```python
from lib.db import db

class UpdateProfile:
  def run(cognito_user_id,bio,display_name):
    model = {
      'errors': None,
      'data': None
    }

    if display_name == None or len(display_name) < 1:
      model['errors'] = ['display_name_blank']

    if model['errors']:
      model['data'] = {
        'bio': bio,
        'display_name': display_name
      }
    else:
      handle = UpdateProfile.update_profile(bio,display_name,cognito_user_id)
      data = UpdateProfile.query_users_short(handle)
      model['data'] = data
    return model

  def update_profile(bio,display_name,cognito_user_id):
    if bio == None:    
      bio = ''

    sql = db.template('users','update')
    handle = db.query_commit(sql,{
      'cognito_user_id': cognito_user_id,
      'bio': bio,
      'display_name': display_name
    })
  def query_users_short(handle):
    sql = db.template('users','short')
    data = db.query_object_json(sql,{
      'handle': handle
    })
    return data
```

Import this service to app.py file.

```python
from services.update_profile import *
```

Write an endpoint for updating user profile.

```python
@app.route("/api/profile/update", methods=['POST','OPTIONS'])
@cross_origin()
def data_update_profile():
  bio          = request.json.get('bio',None)
  display_name = request.json.get('display_name',None)
  access_token = extract_access_token(request.headers)
  try:
    claims = cognito_jwt_token.verify(access_token)
    cognito_user_id = claims['sub']
    model = UpdateProfile.run(
      cognito_user_id=cognito_user_id,
      bio=bio,
      display_name=display_name
    )
    if model['errors'] is not None:
      return model['errors'], 422
    else:
      return model['data'], 200
  except TokenVerifyError as e:
    # unauthenicatied request
    app.logger.debug(e)
    return {}, 401
```

### Implement Backend Migrations

Write a file that generate a migration file.

```bash
#!/usr/bin/env python3
import time
import os
import sys

if len(sys.argv) == 2:
  name = sys.argv[1]
else:
  print("pass a filename: eg. ./bin/generate/migration add_bio_column")
  exit(0)

timestamp = str(time.time()).replace(".","")

filename = f"{timestamp}_{name}.py"

klass = name.replace('_', ' ').title().replace(' ','')

file_content = f"""
from lib.db import db
class {klass}Migration:
  def migrate_sql():
    data = \"\"\"
    \"\"\"
    return data
  def rollback_sql():
    data = \"\"\"
    \"\"\"
    return data
  def migrate():
    db.query_commit({klass}Migration.migrate_sql(),{{
    }})
    
  def rollback():
    db.query_commit({klass}Migration.rollback_sql(),{{
    }})
migration = AddBioColumnMigration
"""
file_content = file_content.lstrip('\n').rstrip('\n')

current_path = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations',filename))
print(file_path)

with open(file_path, 'w') as f:
  f.write(file_content)
```

After generating a migration file we need to add SQL queries that creates a table and delete this table to generated migration file.

```python
from lib.db import db

class AddBioColumnMigration:
  def migrate_sql():
    data = """
    ALTER TABLE public.users ADD COLUMN bio text;
    """
    return data
  def rollback_sql():
    data = """
    ALTER TABLE public.users DROP COLUMN bio;
    """
    return data
  def migrate():
    db.query_commit(AddBioColumnMigration.migrate_sql(),{
    })
  def rollback():
    db.query_commit(AddBioColumnMigration.rollback_sql(),{
    })

migration = AddBioColumnMigration
```

Write two bash scripts one for migration and one for rollback.

migrate bash script

```bash
#!/usr/bin/env python3

import os
import sys
import glob
import re
import time
import importlib

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask'))
sys.path.append(parent_path)
from lib.db import db

def get_last_successful_run():
  sql = """
      SELECT last_successful_run
      FROM public.schema_information
      LIMIT 1
  """
  return int(db.query_value(sql,{},verbose=False))

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_successful_run)s
  WHERE id = 1
  """
  db.query_commit(sql,{'last_successful_run': value},verbose=False)
  return value

last_successful_run = get_last_successful_run()

migrations_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations'))
sys.path.append(migrations_path)
migration_files = glob.glob(f"{migrations_path}/*")


for migration_file in migration_files:
  filename = os.path.basename(migration_file)
  module_name = os.path.splitext(filename)[0]
  match = re.match(r'^\d+', filename)
  if match:
    file_time = int(match.group())
    if last_successful_run <= file_time:
      mod = importlib.import_module(module_name)
      print('=== running migration: ',module_name)
      mod.migration.migrate()
      timestamp = str(time.time()).replace(".","")
      last_successful_run = set_last_successful_run(timestamp)
```


rollback bash script

```bash
#!/usr/bin/env python3

import os
import sys
import glob
import re
import time
import importlib

current_path = os.path.dirname(os.path.abspath(__file__))
parent_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask'))
sys.path.append(parent_path)
from lib.db import db

def get_last_successful_run():
  sql = """
      SELECT last_successful_run
      FROM public.schema_information
      LIMIT 1
  """
  return int(db.query_value(sql,{},verbose=False))

def set_last_successful_run(value):
  sql = """
  UPDATE schema_information
  SET last_successful_run = %(last_successful_run)s
  WHERE id = 1
  """
  db.query_commit(sql,{'last_successful_run': value})
  return value

last_successful_run = get_last_successful_run()

migrations_path = os.path.abspath(os.path.join(current_path, '..', '..','backend-flask','db','migrations'))
sys.path.append(migrations_path)
migration_files = glob.glob(f"{migrations_path}/*")


last_migration_file = None
for migration_file in migration_files:
  if last_migration_file == None:
    filename = os.path.basename(migration_file)
    module_name = os.path.splitext(filename)[0]
    match = re.match(r'^\d+', filename)
    if match:
      file_time = int(match.group())
      if last_successful_run > file_time:
        last_migration_file = module_name
        mod = importlib.import_module(module_name)
        print('=== rolling back: ',module_name)
        mod.migration.rollback()
        set_last_successful_run(file_time)
```

## Presigned URL generation via Ruby Lambda

Write a ruby lambda function that is generating a presigned URL.

```ruby
require 'aws-sdk-s3'
require 'json'
require 'jwt'

def handler(event:, context:)
    puts event
    if event['routeKey'] == "OPTIONS /{proxy+}"
        puts({step: 'preflight', message: 'preflight CORS check'}.to_json)
        { 
            headers: {
              "Access-Control-Allow-Headers": "*, Authorization",
              "Access-Control-Allow-Origin": "https://3000-adamlisicki-awsbootcamp-ojfyeksv3wy.ws-eu95.gitpod.io",
              "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
            },
            statusCode: 200
        }
    else
        token = event['headers']['authorization'].split(' ')[1]
        puts({step: 'presignedurl', access_token: token}.to_json)

        body_hash = JSON.parse(event["body"])
        extension = body_hash["extension"]

        decoded_token = JWT.decode token, nil, false
        puts "decoded_token"
        cognito_user_uuid = decoded_token[0]['sub']
    

        s3 = Aws::S3::Resource.new
        bucket_name = ENV["UPLOADS_BUCKET_NAME"]
        object_key = "#{cognito_user_uuid}.#{extension}"
    
        puts({object_key: object_key}.to_json)
    
        obj = s3.bucket(bucket_name).object(object_key)
        url = obj.presigned_url(:put, expires_in: 60 * 5)
        url # this is the data that will be returned
        body = {url: url}.to_json
        { 
          headers: {
            "Access-Control-Allow-Headers": "*, Authorization",
            "Access-Control-Allow-Origin": "https://3000-adamlisicki-awsbootcamp-ojfyeksv3wy.ws-eu95.gitpod.io",
            "Access-Control-Allow-Methods": "OPTIONS,GET,POST"
          },
          statusCode: 200, 
          body: body 
        }
    end
end 
```

## Create JWT Lambda Layer

We need to create lambda layer in order to get "jwt" package for our ruby lambda.

Write a bash script that creates a JWT lambda layer with "jwt" package.

```bash
#! /usr/bin/bash

gem i jwt -Ni /tmp/lambda-layers/ruby-jwt/ruby/gems/2.7.0
cd /tmp/lambda-layers/ruby-jwt

zip -r lambda-layers . -x ".*" -x "*/.*"
zipinfo -t lambda-layers

aws lambda publish-layer-version \
  --layer-name jwt \
  --description "Lambda Layer for JWT" \
  --license-info "MIT" \
  --zip-file fileb://lambda-layers.zip \
  --compatible-runtimes ruby2.7
```

And then add this layer to our ruby lambda.

![image](https://user-images.githubusercontent.com/96197101/233829967-aea1384d-7ff2-4dc0-aae3-132204286fb5.png)

## HTTP API Gateway with Lambda Authorizer

Upload our lamda authorizer.

This lambda function verifies cognito access token and if it returns isAuthorized: true the API Gateway can execute lambda for generating presigned URL.

![image](https://user-images.githubusercontent.com/96197101/233830037-c0ad12cd-fc3d-444d-af25-7c9c8866cec2.png)

We need to create two routes in API Gateway and both of them integrate with Lambda that generates a presigned URL.
Only to /key_uplod route we need to add Authorization Lambda.

![image](https://user-images.githubusercontent.com/96197101/233830187-8e0d1115-d8a7-4b6a-897c-2c6a7fb2217d.png)


Add to functions to ProfileForm.js.
s3uploadkey will call API Gateway and generate a presigned URL.
s3upload will use this URL to upload image to S3 bucket.

```js
  const s3uploadkey = async (extension)=> {
    try {
      const gateway_url = `${process.env.REACT_APP_API_GATEWAY_ENDPOINT_URL}/avatars/key_upload`
      await getAccessToken()
      const access_token = localStorage.getItem("access_token")
      const json = {
        extension: extension
      }
      const res = await fetch(gateway_url, {
        method: "POST",
        body: JSON.stringify(json),
        headers: {
          'Origin': process.env.REACT_APP_FRONTEND_URL,
          'Authorization': `Bearer ${access_token}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }})
      let data = await res.json();
      if (res.status === 200) {
        return data.url
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }

  const s3upload = async (event)=> {
    const file = event.target.files[0]
    const filename = file.name
    const size = file.size
    const type = file.type
    const preview_image_url = URL.createObjectURL(file)
    console.log('file', file, size, type)
    const fileparts = filename.split('.')
    const extension = fileparts[fileparts.length-1]
    const presignedurl = await s3uploadkey(extension)
    try {
      const res = await fetch(presignedurl, {
        method: "PUT",
        body: file,
        headers: {
          'Content-Type': type
        }})
      if (res.status === 200) {
        
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  }


```

Add button to select image from our local PC and upload it to s3 bucket.

```js
<input type="file" name="avatarupload" onChange={s3upload} />
```

## Render Avatars in App via CloudFront

Create new ClouFront distribution and point it to our S3 backet when we are storing processed avatars.

![image](https://user-images.githubusercontent.com/96197101/233830981-84660da5-1be3-4787-bdc4-fa6511b97d4e.png)

Create a component named ProfileAvatar.js that will get image from CloudFront and set it to user avatar.

```js
import './ProfileAvatar.css';

export default function ProfileAvatar(props) {
  const backgroundImage = `url("https://assets.cruddur.pl/avatars/${props.id}.jpg")`;
  const styles = {
    backgroundImage: backgroundImage,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
  };

  return (
    <div 
      className="profile-avatar"
      style={styles}
    ></div>
  );
}
```

To ProfileHeading.js and ProfileInfo.js import this component.

```js
import ProfileAvatar from '../components/ProfileAvatar';
```

And pass arguments to that component so correct avatars will be loaded for users.

ProfileHeading.js 

```js
<ProfileAvatar id={props.user.cognito_user_uuid} />
```

ProfileInfo.js

```js
<ProfileAvatar id={props.profile.cognito_user_uuid} />
```

In CheckAuth.js add cognito_user_id

![image](https://user-images.githubusercontent.com/96197101/233830833-e30dada0-d3f4-4c64-8daa-76f730cf1b14.png)

And in show.sql add to SELECT query that will return cognito_user_uuid from a database.

![image](https://user-images.githubusercontent.com/96197101/233830911-73e472dc-eab4-4d82-8d59-ba9232f8f06a.png)

We also need to set CORS in our S3 bucket where we uploading images.

![image](https://user-images.githubusercontent.com/96197101/233831956-f7623e53-6b8d-4754-91b0-4d8b0a83f707.png)


And when we upload an image it shows in our app.

![image](https://user-images.githubusercontent.com/96197101/233831918-b62b2a59-559d-4914-bb77-623e180649d5.png)


