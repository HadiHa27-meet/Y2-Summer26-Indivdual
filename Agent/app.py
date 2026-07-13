import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
#The code will not run without this line because it will not be able to access the API key as it lives inside the end file

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    print('You: (type exit to quit)')
    personality = input("Choose the personality you would like your AI assistant to be, for example humorous, professional, goofy, etc. ")
    system_message = f"You are a {personality} AI assistant. Answer the users requests in a way that fits this personality."
    history = []
    turn  = len(history) + 1
    while True:
        user_input = input(f"Turn {turn} You: ")

        if user_input.lower() == 'exit':
            break
        #If the break wasn't here the code would just continue to run even when the user types exit
        if user_input.lower() == 'reset':
            history = []
            turn = 1
            print("Your conversation history is now clean!!.")
            continue

        history.append({'role': 'user', 'content': user_input})

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=0.7,
            #Without this line, the code will still run, but the personality of the bot will be of, because it doesn't know how random or strict it should be
            system=system_message,
            messages=history
        )

        reply = response.content[0].text
        print(f'Claude: {reply}')
        if turn == 3:
            print('History:', history)        
        history.append({'role': 'assistant', 'content': reply})
        #If this line is removed, the turn number will not update automatically and the bot will not save it's own reply in the history
        turn = len(history) // 2 + 1

run_chat()
#Reflection question 1: In life, a situation where we have to give the entire history for something to make sense is when describing a human being's actions. You cant truly understands someone's actions and life without understanding their upbringing and their full story.
#Reflection question 2: Underneath each of the lines is my answer
#Reflection question 3: One bug I faced today and yesterday was that my API key just wasn't working. I had to copy and paste it again and again until it actually worked.
#usage.input_tokens is meant to show the user how many tokens their question used up when getting processed
#usage.output_tokens is meant to show the user how much tokens the answer to their question used up to be generated
#When I chaneg the tokens to 50, the bot cannot process long questions as the input tokens would be more than 50
#Temperature acctually controlls randomness and creativity in the bot (the closer to 1, the more creative and random
#The API needs the full history because without it it would never have full context on what the conversation revolves around