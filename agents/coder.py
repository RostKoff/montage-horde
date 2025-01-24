from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data.prompts import CODER_PROMPT

CODER_AGENT = AssistantAgent(
    name='coder',
    model_client=OpenAIChatCompletionClient(
        model='gpt-4o',
    ),
    description='An agent that writes a code to modify videos.',
    system_message=CODER_PROMPT
)

