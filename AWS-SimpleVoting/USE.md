# Upload format
![Upload Format JSON Example](/images/JSON_example.png "Upload Format JSON Example")
# Finished Format (after all the proposals have been terminated)
![Upload Format JSON Example](/images/JSON_example_2.png "Upload Format JSON Example")
# Requests

## Get current votes for a proposal:
> curl --insecure  -X GET http://127.0.0.1:5000/CurrentVotes/**proposal_ID**/**API_KEY**

returns an object with 3 fields: id, yes_votes, no_votes
> {"id": "775b91bb-5616-4893-9de2-086f7fc41112", "yes_votes": "0", "no_votes": "0"}

## Get current API server JSON file info
> curl --insecure  -X GET http://127.0.0.1:5000/JSONInfo/**API_KEY**

returns JSON info

## Get winner for all proposals:
> curl --insecure  -X GET http://127.0.0.1:5000/Winner/**API_KEY**

returns JSON info

# Post
> curl -H "Content-Type: application/json" --data @**NameOfJSONFile**.json http://127.0.0.1:5000/UploadProposals/**API_KEY**

returns JSON info from the overwritten JSON file within the API server. This info should be kept in a json file and gives the IDs of each proposal. You can write some script that preforms de CURL and then writes the info to a JSON file

# Testing:
curl -H "Content-Type: application/json" --data @proposals_to_upload.json http://127.0.0.1:5000/UploadProposals/**API_KEY** - Upload the info

curl --insecure  -X GET http://127.0.0.1:5000/CurrentVotes/**PROPOSAL_ID**/**API_KEY**

curl --insecure  -X GET http://127.0.0.1:5000/JSONInfo/**API_KEY**

curl --insecure  -X GET http://127.0.0.1:5000/Winner/**API_KEY**

curl --insecure  -X GET http://127.0.0.1:5000/Winner/**API_KEY**- To see if it recognizes that the winner has been calculated

curl --insecure  -X GET http://127.0.0.1:5000/JSONInfo/**API_KEY** - To see if it gets the info still gets the info

- See if votes are well counted
- See if the file is well written in the end
- See if the previous two points hold trhough for 2 proposals uploads, one after another
