
# Use this to upload json data
curl -X POST "https://hqekq91bxg.execute-api.eu-north-1.amazonaws.com/dev/items" \
     -H "Content-Type: application/json" \
     -d '{"id": "123098", "data": "hello, this is a new data for tesing gateway api and aws lambda"}'




# use this to upload static files
curl -X POST "https://rag7osp53m.execute-api.eu-north-1.amazonaws.com/dev/items" \
     -H "Content-Type: application/json" \
     --data-binary "$(jq -n --arg file_name "boy_playing_ball.jpeg" \
     --arg body "$(base64 boy_playing_ball.jpeg)" \
     '{"isBase64Encoded": true, "body": $body, "headers": {"Content-Type": "image/jpeg", "x-file-name": $file_name}}')"

