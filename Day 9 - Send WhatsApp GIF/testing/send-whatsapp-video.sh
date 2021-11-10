MESSAGES_API_URL=https://messages-sandbox.nexmo.com/v0.1/messages
JWT=JWT_TOKEN
TO_NUMBER=12410293213
WHATSAPP_NUMBER=1082391231203
IMAGE_URL=https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4
IMAGE_CAPTION=video_here
MESSAGE_TYPE=video

curl -X POST $MESSAGES_API_URL \
  -H 'Authorization: Bearer '$JWT \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d $'{
    "from": { "type": "whatsapp", "number": "'$WHATSAPP_NUMBER'" },
    "to": { "type": "whatsapp", "number": "'$TO_NUMBER'" },
    "message": {
      "content": {
        "type": "'$MESSAGE_TYPE'",
        "'$MESSAGE_TYPE'": {
          "url": "'$IMAGE_URL'",
          "caption": "'$IMAGE_CAPTION'"
        }
      }
    }
  }'
