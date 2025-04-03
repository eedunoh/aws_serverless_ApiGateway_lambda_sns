# aws_serverless_ApiGateway_lambda_sns
This repository contains Python and Bash scripts for an AWS project that implements a severless strategy. It utilizes Serverless API for Secure JSON Data and static file Storage, Event-Driven Processing, and Automated Notifications via email.

## Architecture Design

![image](https://github.com/user-attachments/assets/ea02febd-2259-4b36-a457-c11a52e1e460)

## Project Structure
  
- **lambda_function**: Create a lambda function that will do the following;
  - Accepts an input event.
  - Checks if the data is json;
    - If yes, data is stored in a Dynamodb table
    - If no, it checks if the file is a static file,
      - If yes, the data/file is stored in a s3 bucket.
    - Returns a success message in the terminal (when we use curl) for both types of event
  - If the file uploaded is a static file, the lambda function will be triggered to send an email via SNS. This should happen when we use curl on the terminal to upload files to S3 and when we upload files directly in the AWS S3 management console. 


- **upload.sh**: This contain scripts that will be used to upload static and json files
