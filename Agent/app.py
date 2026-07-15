import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
#The code will not run without this line because it will not be able to access the API key as it lives inside the end file

client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

def run_chat():
    history = []
    tokens_used_1 = 0
    scores = []
    turn  = len(history) + 1
    goal = input("What is your goal in football? ")
    system_message = f"""
    You are MessiGPT, an agent meant to help give students advice on their football skills.

    Your job is to provide helpful and meaningful feedback for the student, along with a curated training plan.

    Rules:
    - Always ask the user for their current skill level and position before giving advice
    - Always ask the user for their goals and what they want to achieve in football
    - Never give advice that is unsafe or could lead to injury

    Response format:
    - Start with a one-sentence summary of what the user said.
    - Then give your response.
    - End with one follow-up question.
    The user's goal is {goal}

    Score every response the user gives on a scale of 1-10 with 10 being the best. Add it in this fasion exactly: "Score: 7" at the end of your response. Do not include any other text in the score line. The score should be based on how well the user is progressing towards their goal and how well they are following your advice. Do this for every response unless its a command like 'exit', 'reset', 'summary' or 'average score'
    """
    #If I remove the response formatting from the system message the AI will start answering in very different ways to what I think fits the users the best
    print("Hello! I am MessiGPT, your personal football coach. I am here to help you improve your football skills and achieve your goals. Insert 'exit' to quit or 'reset' to delete chat history or 'summary' to get a summary of the conversation or 'average score' to see your average performance. Please tell me about your current skill level and position.")

    while True:
        user_input = input(f"Turn {turn} You: ")

        if user_input.lower() == 'exit':
            break
        #If the break wasn't here the code would just continue to run even when the user types exit
        if user_input.lower() == 'reset':
            history = []
            print("Your conversation history is now clean!!.")
            turn = 1
            continue
        if user_input.lower() == 'summary':
            response = client.messages.create(
                model='claude-haiku-4-5-20251001',
                max_tokens=300,
                #If max tokens becomes 50 or lower, the reply will be extremely short or will cut off
                temperature=1,
                system=system_message,
                #Without this line the code will run but it will have no personality. It will just be like any other chatbot
                messages=history + [{'role': 'user', 'content': 'Please summarize the conversation so far.'}]
            )
            print(response.content[0].text)
            continue
        if user_input.lower() == "average score":
            if scores != []:
                average_score = sum(scores) / len(scores)
                print(f"Average score so far: {average_score:.2f}")
                continue
            else:
                print("No scores available yet.")
                continue 
        history.append({'role': 'user', 'content': user_input})
            #Without this line, the code wont save the user's input and send it back to the AI. The input tokens will increase by less each prompt

        response = client.messages.create(
            model='claude-haiku-4-5-20251001',
            max_tokens=300,
            temperature=1,
            #Without this line, the code will still run, but the personality of the bot will be of, because it doesn't know how random or strict it should be
            system=system_message,
            messages=history
            )

        reply = response.content[0].text
        lines = reply.split('\n')
        for line in lines:
            if line.startswith('Score:'):
                score = int(line.split(':')[1].strip())
                scores.append(score)
                #without this line the whole avarage score function will basically become useless
                print(f"Score for this turn: {score}")
                break

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
#Lab 3 reflection question 1: It's like the roots of a tree. We can't see them but they determine how the tree looks and acts
#Lab 3 reflection question 2: This will be under each of the corresponding lines
#Lab 3 reflection question 3: One bug I faced was that the bot would give me scores for the prompt messages like exit or summary
#Lab 3 bonus reflection question: I think my analogy still makes sense. To understand a perrson's actions, you need their entire history.