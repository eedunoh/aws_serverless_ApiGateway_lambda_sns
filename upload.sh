
# Use this to upload json data
curl -X POST "https://hqekq91bxg.execute-api.eu-north-1.amazonaws.com/dev/items" \
     -H "Content-Type: application/json" \
     -d '{"id": "123098", "data": "hello, this is a new data for tesing gateway api and aws lambda"}'


# use this to upload static files
curl -X POST "https://2n6cnvj70f.execute-api.eu-north-1.amazonaws.com/dev/items" \
     -H "Content-Type: application/json" \
     -H "x-file-name: aws.jpeg" \
     -d '{"isBase64Encoded": true, "body": "'"$(base64 ./aws.jpeg)"'", "headers": {"Content-Type": "image/jpeg"}}'
