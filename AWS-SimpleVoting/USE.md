curl --insecure  -X GET BASE/winner/Block_ini/Block_end/API_KEY

curl -X POST -H 'Accept: application/json' -H 'Accept-Encoding: gzip, deflate' -H 'Connection: keep-alive' -H 'Content-Length: 248' -H 'Content-Type: application/json' -H 'User-Agent: python-requests/2.27.1' -d 'JSON FILE CONTENTS' http://127.0.0.1:5000/UploadProposals/API_KEY

# Post
curl -H "Content-Type: application/json" --data @**NameOfJSONFile**.json http://127.0.0.1:5000/UploadProposal/**API_KEY**