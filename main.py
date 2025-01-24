import asyncio
import os
from typing import Sequence
from dotenv import load_dotenv
from agents.translator import TRANSLATOR_AGENT
from agents.supervisor import SUPERVISOR_AGENT
from agents.sentiment_analyst import SENTIMENT_ANALYST_AGENT
from agents.planner import PLANNER_AGENT
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient

load_dotenv()

transcription = """Bettie Sophie, I just closed the shop.  

I thought you were coming?  

I have to finish this.  I hope you enjoy.  

OK, I'm off.  

Let's go girls.  Wait up!  Isn't anything wrong with my dress, is it?  Check 
it out!  Howl's castle is there.  
          """
language = "Polish"

text_mention_termination = TextMentionTermination("<TERMINATE>")
max_messages_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_messages_termination

def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
    if messages[-1].source != SUPERVISOR_AGENT.name:
        return SUPERVISOR_AGENT.name
    return None

async def main() -> None:
    team = SelectorGroupChat(
    [SUPERVISOR_AGENT,TRANSLATOR_AGENT,SENTIMENT_ANALYST_AGENT, PLANNER_AGENT],
    model_client=OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    termination_condition=termination,
    selector_func=selector_func
    )
    await Console(team.run_stream(task=f"Analyse the sentiment of {transcription}, translate it to {language} and return both result."))

asyncio.run(main())