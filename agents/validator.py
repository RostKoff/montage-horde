from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
# from data.prompts import VALIDATOR_PROMPT
import os
from moviepy.editor import VideoFileClip
from openai import OpenAI

VALIDATOR_PROMPT = (
    "### ROLE ###"
    "You are a VALIDATOR agent."
    "You are responsible for reviewing the work of your colleagues in a video editing system." 
    "### TASK ###"
    "Your task is to check the edited video to ensure it meets the user's requirements."
    "Decide whether to send the video back to the editors for further modifications or to approve the changes as correct."
    "You can not make any modiffications"
    "If you approve the changes, write <TERMINATE> to finish the process."
    "If you get information that task is impossible to do, also write <TERMINATE>"
    "### EXAMPLES ###"
    "Example 1:"
    "Task: Ensure that the video won't have any english curses, and will have timestamps"
    "Response: The video has curses in the second part of video. Please remove it. Returning for further edits"
    "Example 2:"
    "Task: Review this film and analyze the impact of the film on the community, determining if it is positive, negative, or neutral."
    "Response: The video meets all the requirements. It includes a review and sentiment analysis. <TERMINATE>"
)
VALIDATOR_AGENT = AssistantAgent(
    name="validator",
    model_client=OpenAIChatCompletionClient(
        model="gpt-4o"
    ),
    description="An agent that validates video edits.",
    system_message=VALIDATOR_PROMPT
)

TRANSCRIPTION_1 = """
"Are you freaking serious right now, Dave? We’ve been driving for six damn hours, and you still don’t know where the hell we’re going?"

"Relax, okay? I’ve got the GPS. It’s just... uh... recalculating. Sh*t happens, alright?"

"Guys, can we not? I’m stuck in the back seat with no damn leg room, and you two are arguing like kids. Jesus Christ, grow up!"

"Shut the hell up, Karen! You’re not the one trying to figure out this bullsh*t."

"Oh, fuck off! Like it’s my fault you can’t read a map."""

TRANSCRIPTION_2 = """
"Are you serious right now, Dave? We’ve been driving for six hours, and you still don’t know where we’re going?"

"Relax, okay? I’ve got the GPS. It’s just... uh... recalculating. Things happen, alright?"

"Guys, can we not? I’m stuck in the back seat with no leg room, and you two are arguing like kids. Please, grow up!"

"Be quiet, Karen! You’re not the one trying to figure out this mess."

"Oh, come on! Like it’s my fault you can’t read a map."
"""
TRANSCRIPTION_3 = """"""


def inputter(*file_names, description=None):
    client = OpenAI()
    transcription_dict = {}
    for file_name in file_names:
        if file_name.endswith(".mp4"):
            mp3_file = os.path.splitext(file_name)[0] + ".mp3"
            try:
                video = VideoFileClip(file_name)
                video.audio.write_audiofile(mp3_file)
                print(f"Conversion successful! {file_name} -> {mp3_file}")
            except Exception as e:
                print(f"Failed to convert {file_name}: {e}")
        
        audio_file  = open(f"data/{mp3_file}", "rb")
        
        transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            response_format="text"
        )
        transcription_dict[file_name] = transcription

        transcription_string = "\n".join(
            f"{file_name}: {transcription}" for file_name, transcription in transcription_dict.items()
        )

    return transcription_string, description
    

DESCRIPTION = "OPIS FILMU np timestampy, recenzja czy streszczenie"
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
import asyncio

# Define the invoker function for the validator agent
async def invoke_validator_agent(task_description: str):
    cancellation_token = CancellationToken()
    message = TextMessage(content=task_description, source="user")
    
    # Get the response from the agent
    response = await VALIDATOR_AGENT.on_messages([message], cancellation_token)
    return response

async def main():
    transcription, description = inputter("audio_4.mp3", pho, description=DESCRIPTION)
    task_description = (f"Translate this videos to the english without any curses. videos: {transcription} and decription: {description}")
    response = await invoke_validator_agent(task_description)
    print("Agent Response:", response.chat_message.content)


if __name__ == "__main__":
    asyncio.run(main())
    print("\n\n"+"succes")