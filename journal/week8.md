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

