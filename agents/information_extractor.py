from autogen_agentchat.agents import AssistantAgent
from utils.transcription_extractor import TranscriptionExtractor
from data.prompts import INFORMATION_EXTRACTOR_PROMPT
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.tools import FunctionTool


def init_information_extractor_agent(transcription_extractor: TranscriptionExtractor):
    transcription_tool = FunctionTool(
        transcription_extractor.get_transcription, 
        description="Get transcription from provided video or audio file. Defaults timestamps to segment precision. Word precision or speaker diarization can be added.",
        name='get_transcription')
    return AssistantAgent(
        name="information_extractor",
        model_client=OpenAIChatCompletionClient(
            model='gpt-4o'
        ),
        description="An agent that extracts information from videos.",
        system_message=INFORMATION_EXTRACTOR_PROMPT,
        tools=[transcription_tool]
    )


