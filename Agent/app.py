import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
#The code will not run without this line because it will not be able to access the API key as it lives inside the end file

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    tokens_used_1 = 0
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
        #Without this line, the code wont save the user's input and send it back to the AI. The input tokens will increase by less each prompt

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
        input_tokens = response.usage.input_tokens
        output_tokens = response.usage.output_tokens
        tokens_used_1 = tokens_used_1 +output_tokens + input_tokens
        pricing = input_tokens / 1000000 * 0.25 + output_tokens / 1000000 * 1.25
        print(f"Tokens used | in: {input_tokens} out: {output_tokens}")
        print(f"Total tokens used: {tokens_used_1}")
        print(f"Total cost of tokens used: ${pricing}")
        if turn == 3:
            print('History:', history)  
            #Without this line nothing hmuch happens, its just helpful if I need to debug something or just to view whats happening in the history list      
        history.append({'role': 'assistant', 'content': reply})
        #If this line is removed, the turn number will not update automatically and the bot will not save it's own reply in the history. Token count will grow much less exonentially
        turn = len(history) // 2 + 1

run_chat()
#Lab 1 Reflection question 1: In life, a situation where we have to give the entire history for something to make sense is when describing a human being's actions. You cant truly understands someone's actions and life without understanding their upbringing and their full story.
#Lab 1 Reflection question 2: Underneath each of the lines is my answer
#Lab 1 Reflection question 3: One bug I faced today and yesterday was that my API key just wasn't working. I had to copy and paste it again and again until it actually worked.
#usage.input_tokens is meant to show the user how many tokens their question used up when getting processed
#usage.output_tokens is meant to show the user how much tokens the answer to their question used up to be generated
#When I chaneg the tokens to 50, the bot cannot process long questions as the input tokens would be more than 50
#Temperature acctually controlls randomness and creativity in the bot (the closer to 1, the more creative and random
#The API needs the full history because without it it would never have full context on what the conversation revolves around
#Lab 2 reflection question 1: Something that exponentially grows like the cost of a message on real life is the price of housing, especially in Jeruslame. Real estate always grows in value, and the more time you give it, the higher the price of it becomes
#Lab 2 reflection question 2: This will be under each of the corresponding lines
#Lab 2 reflection question 3: One bug that I faced is whe I tries to use .total for the sum of the tokens instead of just using an operation to add the input and output tokens
