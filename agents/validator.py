from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data.prompts import VALIDATOR_PROMPT

VALIDATOR_AGENT = AssistantAgent(
    name="validator",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o"
    ),
    description="An agent that validates video edits.",
    system_message=VALIDATOR_PROMPT
)
