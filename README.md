# GiveMeJuice

This repository contains bot.py file used for the GiveMeJuice
The code is written in Python
BotHub.Studio is used to host chatbot
Interaction with the chatbot takes place on Telegram

To see what GiveMeJuice does:

  1. go to bothub.studio to sign up

  2. type the following on your shell command window:
  
      pip install bothub-cli
      
  3. connect the account by typing the following:
  
      bothub configure
      
  4. create a new project with the following commands:
  
      mkdir GiveMeJuiceBot
      cd GiveMeJuiceBot
      bothub init
      
  5. connect the telegram messenger to the project:
  
      bothub channel add telegram --api-key=<api-key>
  
      (replace <api-key> with the api key provided on bothub.studio)
  
  6. replace bothub/bot.py with the bot.py in this repository
  
  7. deploy with the following command:
  
      bothub deploy
   
  8. navigate to the root folder of your project in your shell window and enter:
  
      bothub property set menu "{\"Watermelon_Juice\": {\"description\": \"blending watermelons.\", \"price\": 5 }, \"Melon_Juice\": {\"description\": \"blending melons.\", \"price\": 4.5 }, \"Strawberry_Juice\": {\"description\": \"blending strawberries.\", \"price\": 3.5 }, \"Orange_Juice\": {\"description\": \"blending oranges.\", \"price\": 3}, \"Kiwi_Juice\": {\"description\": \"blending kiwis.\", \"price\": 3.75}}"
  
  9. Once you find the chatbot on telegram, type /start to get the conversation started!
  
  
  
  Things left undone:
  - need to put a space in the name of the juice
    e.g. Watermelon_Juice needs to be "Watermelon Juice"
        (do this by implementing unique id?)
  - need to implement natural language processing
