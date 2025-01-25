import deepl
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from data.prompts import TRANSLATOR_PROMPT

from dotenv import load_dotenv
import os

load_dotenv()

def deepL_translate(transcription: str, language: str) -> str:
    auth_key = os.getenv("DEEPL_API_KEY")  
    translator = deepl.Translator(auth_key)
    try:
        result = translator.translate_text(transcription, target_lang=language)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {str(e)}"

TRANSLATOR_AGENT = AssistantAgent(
    name="translator",
    model_client=OpenAIChatCompletionClient(
    model="gpt-4o"),
    tools=[deepL_translate],
    system_message=TRANSLATOR_PROMPT,
)