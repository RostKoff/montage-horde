from agents.translator import translation_agent
from agents.supervisor import supervisor_agent
from agents.sentiment_analyst import sentiment_analyst_agent

import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console

transcription = """Bettie Sophie, I just closed the shop.  

I thought you were coming?  

I have to finish this.  I hope you enjoy.  

OK, I'm off.  

Let's go girls.  Wait up!  Isn't anything wrong with my dress, is it?  Check 
it out!  Howl's castle is there.  
          """
language = "Polish"


async def main() -> None:
    model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key="")
    team = MagenticOneGroupChat([supervisor_agent,translation_agent, sentiment_analyst_agent], model_client=model_client)
    await Console(team.run_stream(task=f"Analyse the sentiment of '{transcription}', then translate it to {language} and return both results."))


asyncio.run(main())