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


