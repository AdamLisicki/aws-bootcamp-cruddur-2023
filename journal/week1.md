# Week 1 — App Containerization

## Containerize Application (Dockerfiles, Docker Compose)

I wrote two Dockerfiles. One for backend and second for frontend.

### Dockerfile for backend

This Dockerfile is using python:3.10-slim-buster image.

```
FROM python:3.10-slim-buster

WORKDIR /backend-flask

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

EXPOSE ${PORT}

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]
```
<code> WORKDIR /backend-flask </code> - create /backend-flask direcotry in container and set it to default work directory.

<code> COPY requirements.txt requirements.txt </code> - copy requirements.txt file from location of Dockerfile and put it into container in work directory.

<code> RUN pip3 install -r requirements.txt </code> - run this command to install all required dependencies in container.

<code> COPY . . </code> - copy whole content of directory where Dockerfile is located and put in into a container.

<code> ENV FLASK_ENV=development </code> - set environment variable.

<code> EXPOSE ${PORT} </code> - this opens port for our backend in container.

<code> CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"] </code> - run command that starts backend.


### Dockerfile for frontend

This Dockerfile is using node:16.18 image.

```
FROM node:16.18

ENV PORT=3000

COPY . /frontend-react-js

WORKDIR /frontend-react-js

RUN npm install

EXPOSE ${PORT}

CMD ["npm", "start"]
```

<code> ENV PORT=3000 </code> - set environment variable.

<code> COPY . /frontend-react-js  </code> - copy all content from directory where Dockerfile is located.

<code> WORKDIR /frontend-react-js </code> - set work directory.

<code> RUN npm install </code> - run npm install in container.

<code> EXPOSE ${PORT} </code> - open port 

<code> CMD ["npm", "start"] </code> - run npm start

## docker compose file


```
version: "3.8"
services:
  backend-flask:
    environment:
      FRONTEND_URL: "https://3000-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
      BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./backend-flask
    ports:
      - "4567:4567"
    volumes:
      - ./backend-flask:/backend-flask
  frontend-react-js:
    environment:
      REACT_APP_BACKEND_URL: "https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
    build: ./frontend-react-js
    ports:
      - "3000:3000"
    volumes:
      - ./frontend-react-js:/frontend-react-js

# the name flag is a hack to change the default prepend folder
# name when outputting the image names
networks: 
  internal-network:
    driver: bridge
    name: cruddur
    
```

In Gitpod right click on docker compose file and select "Compose Up"

![image](https://user-images.githubusercontent.com/96197101/221364863-8529390f-1587-43ec-b078-a220aff4f0f5.png)

Frontend and backend are running.

![image](https://user-images.githubusercontent.com/96197101/221364920-c4d4d99b-c11d-4f5d-ba2b-a2ffd201bc68.png)

![image](https://user-images.githubusercontent.com/96197101/221364946-0370cb79-69f5-49c2-82e5-b702f467ad12.png)

![image](https://user-images.githubusercontent.com/96197101/221364993-c9ad268e-c840-4b23-9abc-4cd16afc9479.png)


## Document the Notification Endpoint for the OpenAI Document

Added entry to openapi-3.0.yml file.

![image](https://user-images.githubusercontent.com/96197101/221408142-7f33ef4f-cad7-4d0a-82bf-c0b1a21c85e4.png)


## Write a Flask Backend Endpoint for Notifications

Added notifications_activities import to app.py file.

![image](https://user-images.githubusercontent.com/96197101/221411384-3bc5733c-91c3-4e5b-ae97-408f1b61e99c.png)

Added endpoint to app.py file.

![image](https://user-images.githubusercontent.com/96197101/221411348-edc5f4d9-0164-4198-9af2-f30898b48b73.png)

Write some data to notifications_activities.py file. 

![image](https://user-images.githubusercontent.com/96197101/221411366-ef02b79c-9af9-4be7-b0a5-e11319d069a2.png)

Called /api/activities/noftifications api shows data that was added to notifications_activities.py file.

![image](https://user-images.githubusercontent.com/96197101/221425703-ab2c155e-1621-4463-9434-d2542f9bb9fb.png)



## Write a React Page for Notifications


![image](https://user-images.githubusercontent.com/96197101/221411466-86ca9de9-ce9b-4902-a3c4-3215fd824d56.png)


```
import './NotificationsFeedPage.css';
import React from "react";

import DesktopNavigation  from '../components/DesktopNavigation';
import DesktopSidebar     from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';

// [TODO] Authenication
import Cookies from 'js-cookie'

export default function NotificationsFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/notifications`
      const res = await fetch(backend_url, {
        method: "GET"
      });
      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson)
      } else {
        console.log(res)
      }
    } catch (err) {
      console.log(err);
    }
  };

  const checkAuth = async () => {
    console.log('checkAuth')
    // [TODO] Authenication
    if (Cookies.get('user.logged_in')) {
      setUser({
        display_name: Cookies.get('user.name'),
        handle: Cookies.get('user.username')
      })
    }
  };

  React.useEffect(()=>{
    //prevents double call
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth();
  }, [])

  return (
    <article>
      <DesktopNavigation user={user} active={'notifications'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm  
          popped={popped}
          setPopped={setPopped} 
          setActivities={setActivities} 
        />
        <ReplyForm 
          activity={replyActivity} 
          popped={poppedReply} 
          setPopped={setPoppedReply} 
          setActivities={setActivities} 
          activities={activities} 
        />
        <ActivityFeed 
          title="Notifications" 
          setReplyActivity={setReplyActivity} 
          setPopped={setPoppedReply} 
          activities={activities} 
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}

```



