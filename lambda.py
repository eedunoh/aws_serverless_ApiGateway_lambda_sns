import json
import boto3
import base64
import time
import os


# AWS Clients
sns = boto3.client('sns')
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


# AWS Resource Names
SNS_TOPIC_ARN = "arn:aws:sns:eu-north-1:337909745504:file-upload"
S3_BUCKET_NAME = 'api-static-upload'
TABLE_NAME = 'file_upload_db'


table = dynamodb.Table(TABLE_NAME)


def lambda_handler(event, context):
   print("Received event:", json.dumps(event, indent=2))


   try:
       # Check if the event is from S3 (Manual Upload)
       if "Records" in event and "s3" in event["Records"][0]:
           return handle_s3_upload(event)


       # Handle JSON Data Storage in DynamoDB
       if 'id' in event and 'data' in event:
           table.put_item(Item={"id": event["id"], "data": event["data"]})
           return response(200, "JSON data added to DynamoDB!")


       # Handle File Upload via API Gateway (Base64-encoded)
       if event.get("isBase64Encoded") and "body" in event:
           return handle_binary_file_upload(event)


       return response(400, "Invalid request: missing or malformed content.")


   except Exception as e:
       print(f"Error: {e}")
       return response(500, f"Internal server error: {e}")


def handle_binary_file_upload(event):
   """Handles binary file upload via API Gateway (base64-encoded) to S3 and sends SNS notification."""
  
   # Decode the file data from base64
   file_data = base64.b64decode(event["body"])


   # Extract MIME type from the headers in the event
   mime_type = event.get("headers", {}).get("Content-Type", "")
   print(f"MIME Type: {mime_type}")


   # Validate MIME Type (accept common static file types and exclude, e.g., application/json)
   if not mime_type.startswith(("text/", "image/", "audio/", "video/", "application/pdf", "application/zip")):
       return response(400, "Invalid file type.")


   # Get original filename from headers (directly from the headers of the event)
   original_filename = event.get("headers", {}).get("x-file-name", "unknown_file.png")  # Default to .jpeg if missing
   print(f"Original filename from headers: {original_filename}")


   # Extract the file name and extension using os.path.splitext
   file_base, file_ext = os.path.splitext(original_filename)


   # Log file name and extension for debugging purposes
   print(f"Extracted filename: {file_base}, Extension: {file_ext}")


   # Use timestamp to ensure a unique file name (rounded to 3 decimal places)
   timestamp = round(time.time(), 3)
   new_file_key = f"{file_base}_{timestamp}{file_ext}"


   # Upload to S3
   try:
       s3.put_object(Bucket=S3_BUCKET_NAME, Key=new_file_key, Body=file_data, ContentType=mime_type)
       print(f"File uploaded to S3: {new_file_key}")
      
       # Send SNS notification on successful file upload
       sns.publish(
           TopicArn=SNS_TOPIC_ARN,
           Message=f"File uploaded successfully: s3://{S3_BUCKET_NAME}/{new_file_key}",
           Subject="File Upload Notification"
       )


       return response(200, f"File uploaded to S3: {new_file_key}")


   except Exception as e:
       # Handle errors during file upload
       print(f"Error uploading file to S3: {e}")
       return response(500, f"Error uploading file to S3: {str(e)}")


def handle_s3_upload(event):
   """Handles manual file uploads to S3 and sends SNS notifications."""
   for record in event["Records"]:
       bucket_name = record["s3"]["bucket"]["name"]
       file_key = record["s3"]["object"]["key"]


       # Send SNS Email Notification for manual file upload to S3
       sns.publish(
           TopicArn=SNS_TOPIC_ARN,
           Message=f"New file uploaded: s3://{bucket_name}/{file_key}",
           Subject="Manual File Upload Notification"
       )


   return response(200, "SNS email sent for manual S3 upload.")


def response(status_code, message):
   """Returns an HTTP response in JSON format."""
   return {"statusCode": status_code, "body": json.dumps(message)}
