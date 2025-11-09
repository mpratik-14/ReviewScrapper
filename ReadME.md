When deploying application manually
 it can be error prone
 time consuming
 frustrating

What is AWS?
Elastic Beanstalk is a platform-as-a-service (Paas) offered by AWS that makes it incredibly easy to deploy, manage and scale web applications and services.

With Elastic Beanstalk, you dont have to worry about the underlying infrastructure

It automatically handles the deployment, from capacity provisioning, load balancing, and auto-scaling to application health monitoring

Plus it supports a wide range of programming languages and frameworks, including Python, Java, .NET, Node.js, PHPm Ruby and Go.

//to create docker image

     touch Dokcerfile

//paste below code in Dockerfile
     FROM python:3.13.2-slim
     
     WORKDIR /app
     
     COPY requirements.txt .
     
     RUN pip install --no-cache-dir -r requirements.txt
     
     COPY . .
     
     EXPOSE 3000
     
     CMD ["python", "app.py"]

//build docker image
     docker build -t review-scrapper . 

//run docker image
     docker run -p 3000:3000 review-scrapper:latest

//how to deploy on elastic beanstalk (automation)

select elastic beanstalk -> create application -> web server environment ->
App name - review-scrapper-gh-app
Platform - Docker
Application code - sample application
Presets - single instance -> next -> next -> skip to default -> create



First establish connection
Click on pipeline -> Settings -> connections -> Create connection -> Select github
Connection name -> review-scrapper-gh-conn -> connect to github -> add app installation
Click on connect

Now go back to code pipeline -> click on pipelines under Pipeline ->
Click on create pipeline -> Build custom pipeline ->
Pipeline Name - review-scrapper-gh-app
Execution mode - Superseded
Service role - new service role -> next
Source - GitHub (via GitHub App) 
Connection - the one which we created above
select repo
select branch
select no filter
Skip build and test stage
Select aws beanstalk in deploy stage
choose the previously created environment and click create

yt link = https://www.youtube.com/watch?v=bP7KpRnvysI&t=979s





