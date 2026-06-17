1. Update env and add api key created from Google AI Studio 

2. To run the project- 
   i. In one terminal run- uvicorn api:app --reload --port 8000 
   ii. Open second terminal and run - ngrok http 8000 

3. In Postman 
   i. method - Post
   
   ii - copy endpoint which is till free.app from the second terminal and paste it in postman and add /disney_assistant to it 
        eg. https://b3f7-2409-40c2-1057-876b-b861-f412-3a7-1cf1.ngrok-free.app/disney_assistant
   
   iii. In Headers add key - Content-Type and value - application/json
   
   iv. In body: 
    sample 1st question - 
    {
      "user_id": "test_user",
      "session_id": "session_1",
      "message": "What resorts are near Magic Kingdom?"
    } 
    Hit the request. Check the output, also you can see logs in vs code in logs folder agent_trail.jsonl 
    
    Sample 2nd question- 
    {
      "user_id": "test_user",
      "session_id": "session_1",
      "message": "Which one is best for families?"
    }

    Sample 3rd question- 
    {
      "user_id": "test_user",
      "session_id": "session_1",
      "message": "How much more expensive is it?"
    }

5. Verify the logs which is a json structure.
