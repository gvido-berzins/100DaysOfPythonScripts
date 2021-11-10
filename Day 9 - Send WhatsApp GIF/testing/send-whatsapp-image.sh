MESSAGES_API_URL=https://messages-sandbox.nexmo.com/v0.1/messages
JWT=LONG-JWT
TO_NUMBER=41231241512
WHATSAPP_NUMBER=1121123123
IMAGE_URL=https://2cdf-13-11-111-121.ngrok.io/birb.jpg
IMAGE_CAPTION=birb

curl -X POST $MESSAGES_API_URL \
  -H 'Authorization: Bearer '$JWT \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d $'{
    "from": { "type": "whatsapp", "number": "'$WHATSAPP_NUMBER'" },
    "to": { "type": "whatsapp", "number": "'$TO_NUMBER'" },
    "message": {
      "content": {
        "type": "image",
        "image": {
          "url": "'$IMAGE_URL'",
          "caption": "'$IMAGE_CAPTION'"
        }
      }
    }
  }'
