# Week 3 — Decentralized Authentication

## Setup Cognito User Pool

Choose the attributes that will be used to sing in to application.

![image](https://user-images.githubusercontent.com/96197101/224513746-6cb40383-1681-4252-85c9-3b37a4d57a30.png)

Configure password policy, MFA and account recovery settings.

![image](https://user-images.githubusercontent.com/96197101/224513785-e02ac96e-be7c-4675-8519-9f67552e388b.png)

On the next page choose he atributes that are required.

![image](https://user-images.githubusercontent.com/96197101/224513873-bb53a4cb-9223-4e69-b1f6-759a2b757d1e.png)

Then choose "Send email with Cognito"

![image](https://user-images.githubusercontent.com/96197101/224513892-1ab9a866-75ca-4cfc-84da-279171174a7d.png)

Next name user pool and app client. Choose "Generate a client secret".

![image](https://user-images.githubusercontent.com/96197101/224514068-f05f9f04-30da-4fd0-890c-f462e0232e86.png)

Created Cognito User Pool

![image](https://user-images.githubusercontent.com/96197101/224513653-dfdb8686-b5da-43e4-b6a3-308984377448.png)

## Conditionally show compoennts based on logged or logged out

Run <code> npm i aws-amplify --save</code> in the fronted directory. <code>--save</code> will add aws-amplify to package.json file so next time we can run only <code>npm install</code>.

![image](https://user-images.githubusercontent.com/96197101/224514340-70b5d040-6723-41fc-a837-ebaa82852738.png)

Set up varaibles for Amplify.

![image](https://user-images.githubusercontent.com/96197101/224515770-a3913954-9ffe-48ca-b7d3-f6d77db744ff.png)

Add environment variables to docker compose file for backend and frontend.

![image](https://user-images.githubusercontent.com/96197101/224517323-54a6835f-b19d-49bb-a2ea-44f77c2c71f5.png)

![image](https://user-images.githubusercontent.com/96197101/224517350-83c400d8-1f58-42ea-8b80-fe5420d76858.png)

To the HomeFeedPage.js add below code.

![image](https://user-images.githubusercontent.com/96197101/224517516-7cd88645-3968-4300-8d7b-6cfcce9dabbf.png)

![image](https://user-images.githubusercontent.com/96197101/224517687-6c1de6f0-422a-4686-b504-2eed69656b5e.png)

Then we rewrite the DeskotopNavigation.js file. 

![image](https://user-images.githubusercontent.com/96197101/224517777-64710703-92e8-49d3-becb-f82e97f8ef11.png)

When the user is not logged in he sees only Home and more.

![image](https://user-images.githubusercontent.com/96197101/224517820-c40d75b3-ed6c-45cb-a0b6-bac482741fa2.png)

But when he is logged in he can sees more links.

![image](https://user-images.githubusercontent.com/96197101/224517910-f8b7454e-bf1f-407e-8d8b-7c4ad0c6ee19.png)

To the ProfileInfo.js file add this code to remove access token when user sing out.

![image](https://user-images.githubusercontent.com/96197101/224517958-ef129d28-6347-49a2-b7bc-7bce003bb6d7.png)

Rewrite the DesktopSidebar.js file to shows componenest depening on user is logged in or not.

![image](https://user-images.githubusercontent.com/96197101/224518023-7cb3c46e-151e-4fdf-bb27-ee2b46dbd847.png)

When user is sing out he can sees this.

![image](https://user-images.githubusercontent.com/96197101/224518046-d5f65739-ab1f-4b8a-9250-a0eb2ef501be.png)

And when he is logged in he can sees this.

![image](https://user-images.githubusercontent.com/96197101/224518061-d327b07b-da05-4359-96d5-006ebbdee7c6.png)


## Implement Custom Signin Page

To SinginPage.js add this code to integrate it with Congnito. 

![image](https://user-images.githubusercontent.com/96197101/224518248-2b5c61c2-1b30-489b-88b2-d1672683129c.png)

## Implement Custom Signup Page

To SingupPage.js add this piece of code to integrate it with Cognito.

![image](https://user-images.githubusercontent.com/96197101/224518359-6911087c-7e48-46bb-9725-bf36a98595fb.png)


## Implement Custom Confirmation Page

To ConfirmatrioPage.js add this lines of code to Cognito be able to send confirmation email agter we sing up.

![image](https://user-images.githubusercontent.com/96197101/224518428-188eb1ef-4be8-4726-ac85-116b1c27eced.png)

## Implement Custom Recovery Page

In the RecoveryPage.js add following lines of code to be able to change our possword when we forgot it.

![image](https://user-images.githubusercontent.com/96197101/224518530-e8f4bde9-6bcc-4d17-8a20-f552a11a7cd5.png)


## Transfer accesss token to backend

And in HomeFeedPage.js add header with access token.

![image](https://user-images.githubusercontent.com/96197101/224518613-460719a5-c7a6-429c-962c-9eaba79613c4.png)

To transger our access token to the backend we need to update CORS.

![image](https://user-images.githubusercontent.com/96197101/224518761-50b0b27c-0980-4e0d-becd-018e53d31c1b.png)

And now we can code what user can sees when he is logged in or not when hitting an endpoint.

For example for /api/activities/home endpoint add this code in app.py file.

![image](https://user-images.githubusercontent.com/96197101/224518805-e943bfbc-74e5-4127-b74b-bfae1bc7a22e.png)

And add this code to home_activities.py so when user is logged he can sees additional entry.

![image](https://user-images.githubusercontent.com/96197101/224518842-2abea171-7277-4399-ad09-c1a3cf185778.png)

User is not logged in.

![image](https://user-images.githubusercontent.com/96197101/224519000-e107d519-15a3-413e-a7e2-90d152164165.png)

User is logged in.

![image](https://user-images.githubusercontent.com/96197101/224519016-9ffac2b3-ca84-4a02-80fd-b3c8f8a1e91c.png)


