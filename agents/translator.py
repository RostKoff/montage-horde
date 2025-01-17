import deepl
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

def deepL_translate(transcription: str, language: str) -> str:
    auth_key = ""  
    translator = deepl.Translator(auth_key)
    try:
        result = translator.translate_text(transcription, target_lang=language)
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {str(e)}"

TRANSLATION_PROMPT = """
You are a translator that analyses contextually a video transcription from your supervisor and translates it into a given language.
For translation, only use the functions provided to you. Check the functions output, compare it to the original text and make improvements to match the context better if necessary. Then, return the translation result to your supervisor.
Constraints:
- Understand the context of the text and use it in your translation.
- Be accurate and precise.
- Do not translate names.
- Reflect on your answer, and if you think you are hallucinating, reformulate the answer.
- Do not repeat yourself.
"""

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key="",
)
translation_agent = AssistantAgent(
    name="translation_agent",
    model_client=model_client,
    tools=[deepL_translate],
    system_message=TRANSLATION_PROMPT,
)