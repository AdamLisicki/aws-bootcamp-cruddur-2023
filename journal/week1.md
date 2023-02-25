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

