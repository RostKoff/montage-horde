import os
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent

config_list = [{"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"]}]

from openai import OpenAI

client = OpenAI()

audio_file  = open("data/audio.mp3", "rb")

transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file,
    response_format="text"
)

print(transcription)
