MESSAGE="https://13.19.117.110/message.gif"

curl -X POST https://messages-sandbox.nexmo.com/v0.1/messages \
-u 'api_key:api_secret' \
-H 'Content-Type: application/json' \
-H 'Accept: application/json' \
-d '{
    "from": { "type": "whatsapp", "number": "11111186170" },
    "to": { "type": "whatsapp", "number": "11110111111" },
    "message": {
      "content": {
        "type": "text",
        "text": "'$MESSAGE'"
      }
    }
  }'
