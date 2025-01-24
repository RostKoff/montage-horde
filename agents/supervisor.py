# from autogen_agentchat.agents import UserProxyAgent
from data.prompts import SUPERVISOR_PROMPT

# system_message=SUPERVISOR_PROMPT

# SUPERVISOR_AGENT = UserProxyAgent(
#     name="supervisor"
# )

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

SUPERVISOR_AGENT = AssistantAgent(
    name="supervisor",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o"
    ),
    description="An agent that manages tasks based on a plan provided by the PLANNER.",
    system_message=SUPERVISOR_PROMPT
)