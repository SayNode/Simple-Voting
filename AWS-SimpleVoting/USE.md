
# GET

## Get current votes for a proposal:
> curl --insecure  -X GET http://127.0.0.1:5000/CurrentVotes/**proposal_ID**/**API_KEY**

returns an object with 3 fields: id, yes_votes, no_votes
> {"id": "775b91bb-5616-4893-9de2-086f7fc41112", "yes_votes": "0", "no_votes": "0"}

## Get winner for all proposals:
> curl --insecure  -X GET http://127.0.0.1:5000/Winner/**API_KEY**

returns JSON info

# Post
> curl -H "Content-Type: application/json" --data @**NameOfJSONFile**.json http://127.0.0.1:5000/UploadProposals/**API_KEY**

returns JSON info from the overwritten JSON file within the API server. This info should be kept in a json file and gives the IDs of each proposal. You can write some script that preforms de CURL and then writes the info to a JSON file
