##################################################################
# Christmas Cookie example with OpenAI Swarm Agents 🎄🎄🧑‍🎄🧑‍🎄
# Author: Mark Hagebaum 
# Date: 11.11.2024 
# Status: Experimental prototype - no warranty
#
#
# Further reading: https://github.com/openai/swarm
# Pre-requisite  Ollama 3.2



from swarm import Swarm, Agent
from duckduckgo_search import DDGS
import os

#############################################################################################################
# Here are the handover definitions between the different Agents

def handoff_to_chef():
    """ Call this to bring the internet agent back to the chef """
    print("The Bakery chef took over ...")
    return chef_baker

def handoff_to_chocolate():
    """ Call this to provide chocolate Christmas cookies recipe """
    print("The chocolate baker took over...\n")
    return chocolate_baker

def handoff_to_vanillia():
    """ Call this to provide a vanillia Christmas cookies recipe"""
    print("The vanillia baker took over...\n")
    return vanillia_baker

#def handoff_to_internet():
#    """ Call this to search a cookies recipe int the internet"""
#    print("The Internet expert from cookie recipes took over...\n")
#    return internet_baker

def handoff_to_internet():
    """ Call this to search a cookies recipe int the internet"""
    print("The Internet expert from cookie recipes took over...\n")
    print("Searching the Internet for top Christmas cookie recipes.....\n")
    # DuckDuckGo cookie search
    
    ddg_api = DDGS()
    results = ddg_api.text("best christmas cookie recipes", max_results=3)
    if results:
       cookie_result = "\n\n".join([f"Title: {result['title']}\nURL: {result['href']}\nDescription: {result['body']}" for result in results])
       print(cookie_result + "\n")
    else:
       print("Could not find recipes")

    return internet_baker


def handoff_to_other():
    """ Call this to explain what the agents do"""
    print("Ups.. no cookie request. The bakery assistant took over to help you...\n")
    return other 


#############################################################################################################
# Here are our five "Swarm" baker Agents and their briefing

chef_baker = Agent(
    name="Kitchen chef baker",
    instructions="You handle no cookie recipes.",
    functions=[handoff_to_chocolate, handoff_to_vanillia, handoff_to_internet, handoff_to_other],
    model="llama3.2"
)

chocolate_baker = Agent(
    name="Chocolate cookie baker",
    instructions=" You handle only chocolate Christmas cookie recipes. ", 
    functions=[handoff_to_vanillia],
    model="llama3.2"
    )

vanillia_baker = Agent(
    name="Vanillia cookie baker",
    instructions=" You handle only vanillia Christmas cookie recipes", 
    functions=[handoff_to_internet],
    model="llama3.2"
    )
 
internet_baker = Agent(
    name= "Internet cookie baker",
    instructions= "You explain how to search in the internet",
    functions=[handoff_to_other],
    model="llama3.2"
    )

other = Agent(
    name= "All other requests",
    instructions= "You are a friendly agent to handle all other requests.",
    functions=[handoff_to_chef],
    model="llama3.2"
    )

#############################################################################################################
# Initialize the Swarm client and clear the screen

client = Swarm()
os.system('clear')


#############################################################################################################
# User in- and output in a loop 


print("🍪 🍪 🍪\n\nHi, welcome at our 🎄 Christmas Cookie Bakery! We are a team of 3 baker experts:\nOne for Chocolate cookie recipes, one for Vanillia cookie recipes and one who knows the best recipes in the Internet. \nPlease let us know what Christmas cookies you like (CTRL-C to end):\n")
while True: 
   user_input = input("> ")
    
   messages = [{"role": "user", "content": user_input}]
   handoff_response = client.run(agent=chef_baker, messages=messages)
   print(handoff_response.messages[-1]["content"]+"\n")
   print ("Anything else I can help you with?\n")


