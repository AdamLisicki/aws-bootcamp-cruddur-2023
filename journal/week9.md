# Week 9 — CI/CD with CodePipeline, CodeBuild and CodeDeploy

## Configuring CodeBuild and CodePipeline

In order to configure CodeBuild we need to write buildspec.yml file that instructs CodeBuild how to build our application.
When build is completed CodeBuild return artifact imagedefinitions.json that CodeDeploy will use to deploy our application to ECS cluster.

![image](https://user-images.githubusercontent.com/96197101/233832089-fb7a1ea0-7a8b-4387-ab71-d6b1c099d0fd.png)


First we need to create a CodePipline and integrate it with our GitHub repo.

![image](https://user-images.githubusercontent.com/96197101/233832297-3e069bd1-e4ff-4d06-ba79-bfa6dc0590ae.png)

Next we need to create a CodeDeploy stage that will trigger when we do PULL_REQUEST_MERGED on prod branch in our repo.

![image](https://user-images.githubusercontent.com/96197101/233832359-d6a4a320-7562-4064-b94c-1823ab9bf845.png)

Specify where buildspec.yml is located in our repo.

![image](https://user-images.githubusercontent.com/96197101/233832413-1c225a29-be86-4e8b-9c57-41a2b2d2b7b5.png)

Add CodeBuild stage to our pipeline and set output artifact.

![image](https://user-images.githubusercontent.com/96197101/233832511-6c749a7c-53b9-42e4-9381-beb601203504.png)

In CodeDeploy stage setup on input artifact the artifact that was on otput in build stage.

![image](https://user-images.githubusercontent.com/96197101/233832581-74c75104-e007-45f4-8ee1-2d137c2d7a7d.png)

We also need to set up permisions for CodeBuild so it can perform some operations in ECR.

![image](https://user-images.githubusercontent.com/96197101/233832641-c3b6abea-f87a-44e9-ae2a-edff38bf7894.png)

And now wen we trigger this pipeline by pull request from main to prod branch it will run and deploy our app.
