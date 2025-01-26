from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from pathlib import Path
import sys
sys.path.append(Path('./').absolute().name)

from data.prompts import OUTPUT_FORMATTER_PROMPT
from utils.io_helper import IOHelper


OUTPUT_FORMATTER_AGENT = AssistantAgent(
    name = "output_formatter",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o"
    ),
    description="That agent format informations to the user",
    system_message=OUTPUT_FORMATTER_PROMPT
)

