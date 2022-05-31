# Upload format
![Upload Format JSON Example](/images/JSON_example.png "Upload Format JSON Example")
# Finished Format (after all the proposals have been terminated)
![Upload Format JSON Example](/images/JSON_example_2.png "Upload Format JSON Example")

# JSON files
- **proposals-example.json**: has an example of how the proposals json should be. This can be copied and adapted, but should remain unaltered;
- **proposals-to-upload.json**: the proposal that will be POSTed to the API server;
- **proposals.json**: to simulate the json file that will be o the API server

# Rules
- After the "GET winner" is called, the votes are sealed and can't be recounted. Every vote after this is not accounted for. This includes the "GET currentvotes" which will give out the established votes after "GET winner" was called. 

# Requests

# Post
> curl -H "Content-Type: application/json" --data @**NameOfJSONFile**.json http://127.0.0.1:5000/UploadProposals/**API_KEY**

returns JSON info from the overwritten JSON file within the API server. This info should be kept in a json file and gives the IDs of each proposal. You can write some script that preforms de CURL and then writes the info to a JSON file

## Get current votes for a proposal:
> curl --insecure  -X GET http://127.0.0.1:5000/CurrentVotes/**proposal_ID**/**API_KEY**

Returns an object with 3 fields (id, yes_votes, no_votes):
> {"id": "775b91bb-5616-4893-9de2-086f7fc41112", "yes_votes": "0", "no_votes": "0"}

## Get current API server JSON file info
> curl --insecure  -X GET http://127.0.0.1:5000/JSONInfo/**API_KEY**

Returns JSON info of the current state of the JSON file in the API server, without calculating a winner:
> {"proposals": {"1": {"desc": "New website", "id": "8a9ffea9-9f9c-49b2-9cb7-36a961ff7a82", "yes_wallet": "0x26b199b73c913886b3aaed37cfa6d2b4c7fede38", "no_wallet": "0xba3ae2cdc6ba21b3e9238aac41a30ca4804a9b90", "status": "on-going", "winner": "", "final_yes_votes": "", "final_no_votes": ""}, "2": {"desc": "New Voting System", "id": "0a5df539-343d-4d23-ae50-e2a90fcfc712", "yes_wallet": "0x5de6a2cfbc288979bcb97cb4ade335e171c0c47a", "no_wallet": "0x10ee72ce38449be4be6c1a355170217c40f80e0e", "status": "on-going", "winner": "", "final_yes_votes": "", "final_no_votes": ""}, "3": {"desc": "World cup Sponsorship", "id": "37e4c51b-b42f-415d-bfe7-45858e041984", "yes_wallet": "0x162f8a348cef8bf4e562d349d04282bc996f2475", "no_wallet": "0x5f8dfb44323f45fc8a618da957c5191b41fa7453", "status": "on-going", "winner": "", "final_yes_votes": "", "final_no_votes": ""}}}  

## Get winner for all proposals:
> curl --insecure  -X GET http://127.0.0.1:5000/Winner/**API_KEY**

Returns JSON info of the current state of the JSON file in the API server after calculating a winner:
> {"proposals": {"1": {"desc": "New website", "id": "8a9ffea9-9f9c-49b2-9cb7-36a961ff7a82", "yes_wallet": "0x26b199b73c913886b3aaed37cfa6d2b4c7fede38", "no_wallet": "0xba3ae2cdc6ba21b3e9238aac41a30ca4804a9b90", "status": "finished", "winner": "tie", "final_yes_votes": 0, "final_no_votes": 0}, "2": {"desc": "New Voting System", "id": "0a5df539-343d-4d23-ae50-e2a90fcfc712", "yes_wallet": "0x5de6a2cfbc288979bcb97cb4ade335e171c0c47a", "no_wallet": "0x10ee72ce38449be4be6c1a355170217c40f80e0e", "status": "finished", "winner": "tie", "final_yes_votes": 0, "final_no_votes": 0}, "3": {"desc": "World cup Sponsorship", "id": "37e4c51b-b42f-415d-bfe7-45858e041984", "yes_wallet": "0x162f8a348cef8bf4e562d349d04282bc996f2475", "no_wallet": "0x5f8dfb44323f45fc8a618da957c5191b41fa7453", "status": "finished", "winner": "tie", "final_yes_votes": 0, "final_no_votes": 0}}}  

# Testing:
- See if JSON info is posted and overwritten correctly;
- Vote
- GET current votes for 3 proposals
- GET info (contents of JSON file in API server)
- GET winners and verify that the voting is written in the JSON file and can't be overwritten
- Vote again
- Try GET winners again to see that it is not possible and that the votes remain the same
- GET info again to verify the previous point
- 
# Testing code:
curl -H "Content-Type: application/json" --data @proposals_to_upload.json http://127.0.0.1:5000/UploadProposals/**API_KEY** - Upload the info (WORKS)

curl --insecure  -X GET http://127.0.0.1:5000/CurrentVotes/**PROPOSAL_ID**/**API_KEY**

curl --insecure  -X GET http://127.0.0.1:5000/JSONInfo/**API_KEY**

curl --insecure  -X GET http://127.0.0.1:5000/Winner/**API_KEY**

curl --insecure  -X GET http://127.0.0.1:5000/Winner/**API_KEY**- To see if it recognizes that the winner has been calculated

curl --insecure  -X GET http://127.0.0.1:5000/JSONInfo/**API_KEY** - To see if it gets the info still gets the info

- See if votes are well counted
- See if the file is well written in the end
- See if the previous two points hold trhough for 2 proposals uploads, one after another
