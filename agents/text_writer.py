from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data.prompts import TEXT_WRITER_PROMPT


TEXT_WRITER_AGENT = AssistantAgent(
    name="text_writer",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o"),
        description="An agent that write summarizes, review etc.",
        system_message=TEXT_WRITER_PROMPT
)

