# Kitaabi_Keeda
Messenger chatbot to help students browse through books and also find the exact location of books in the IIT Kharagpur Central Library

The chatbot is hosted on a Flask server (using Python). API.AI is used for figuring out the intents of the inputs given by the user and mapping them to the corresponding actions.
'ngrok' was used to host the webhook (linked to the Facebook app) locally as we needed to scrape data from IIT Kharagpur Central Library website.
The user can search using various types of inputs like book title, author, subject, publisher, ISBN value etc. and we used API.AI's slot-filling features at several places to improve the conversation flow.

To run the bot, one would need to run the Flask server, set the appropriate webhook in the Facebook app and link the API.AI agent with the Flask server.
