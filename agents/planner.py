from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data.prompts import PLANNER_PROMPT

PLANNER_AGENT = AssistantAgent(
    name='planner',
    model_client=OpenAIChatCompletionClient(
        model='gpt-4o',
    ),
    description='An agent that creates a step by step plan for other agents.',
    system_message=PLANNER_PROMPT
)