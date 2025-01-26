import os
from typing import Sequence
from dotenv import load_dotenv
from agents.information_extractor import init_information_extractor_agent
from agents.translator import TRANSLATOR_AGENT
from agents.supervisor import SUPERVISOR_AGENT
from agents.sentiment_analyst import SENTIMENT_ANALYST_AGENT
from agents.planner import PLANNER_AGENT
from agents.text_writer import TEXT_WRITER_AGENT
from agents.validator import VALIDATOR_AGENT
from agents.output_formatter import OUTPUT_FORMATTER_AGENT
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from pathlib import Path
import sys
import torch
from utils import transcription_extractor
sys.path.append(Path('./').absolute().name)
from agents.executor import EXECUTOR_AGENT
from agents.coder import CODER_AGENT
from utils.docker_helper import DockerHelper
from utils.io_helper import IOHelper
import logging
import docker

print(docker.__file__)

load_dotenv()

logger = logging.getLogger('autogen_core')
logger.setLevel(logging.ERROR)
logger = logging.getLogger('httpx')
logger.setLevel(logging.ERROR)

device = torch.device("gpu" if torch.cuda.is_available() else "cpu")

output_dir = Path('app/work_dir')
output_dir.mkdir(exist_ok=True)
output_dir = Path('app/work_dir/output')
output_dir.mkdir(exist_ok=True)

io_helper = IOHelper(output_dir=output_dir)
docker_executor = DockerHelper(io_helper, timeout=180, docker_image="tburrows13/moviepy")

text_mention_termination = TextMentionTermination("<TERMINATE>")
max_messages_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_messages_termination

transcription_extractor = transcription_extractor.TranscriptionExtractor(
    whisper_arch='small', 
    device=device.type, 
    hf_auth_token=os.getenv('HF_AUTH_TOKEN'),
)

information_extractor = init_information_extractor_agent(transcription_extractor)

def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
    if messages[-1].source == CODER_AGENT.name:
        return EXECUTOR_AGENT.name
    
    if messages[-1].source != SUPERVISOR_AGENT.name:
        return SUPERVISOR_AGENT.name
    return None

async def process_request(files, prompt):
    if not files or not prompt:
        return "Please provide both files and a prompt.", None
    file_pathes = []
    for uploaded_file in files:
        file_path = os.path.abspath(uploaded_file.name)
        file_pathes.append(file_path)
        print(f"Uploaded file path: {file_path}")
    
    code_executor = await docker_executor.initialize(file_pathes)

    file_names = []
    for uploaded_file in files:
        file_tmp_path = Path(docker_executor.io_helper.work_dir.name) / docker_executor.io_helper.user_input_dir_name / uploaded_file.name.split('/')[-1]
        file_names.append(str(file_tmp_path))
        
    executor_agent = EXECUTOR_AGENT
    executor_agent.set_code_executor(code_executor)
    team = SelectorGroupChat(
    [SUPERVISOR_AGENT,
     TRANSLATOR_AGENT,
     SENTIMENT_ANALYST_AGENT, 
     PLANNER_AGENT, 
     TEXT_WRITER_AGENT, 
     VALIDATOR_AGENT, 
     executor_agent, 
     CODER_AGENT, 
     information_extractor,
     OUTPUT_FORMATTER_AGENT],
    
    model_client=OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    termination_condition=termination,
    selector_func=selector_func
    ) 
    results = await Console(team.run_stream(task=f"Process files and respond to: {prompt}\n### INPUT FILES ###\n{' '.join(file_names)}"))

    zipped_file = docker_executor.get_zipped_output('generate_test.zip') 
    print(f'Zipped output created under path: {zipped_file}')

    await docker_executor.finish()

    return results, zipped_file