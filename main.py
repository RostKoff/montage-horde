import os
from typing import Sequence
from dotenv import load_dotenv
from agents.translator import TRANSLATOR_AGENT
from agents.supervisor import SUPERVISOR_AGENT
from agents.sentiment_analyst import SENTIMENT_ANALYST_AGENT
from agents.planner import PLANNER_AGENT
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_ext.models.openai import OpenAIChatCompletionClient
from pathlib import Path
import sys
sys.path.append(Path('./').absolute().name)
from agents.executor import EXECUTOR_AGENT
from agents.coder import CODER_AGENT
from utils.docker_helper import DockerHelper
from utils.io_helper import IOHelper

import docker
print(docker.__file__)

load_dotenv()

output_dir = Path('app/work_dir')
output_dir.mkdir(exist_ok=True)
output_dir = Path('app/work_dir/output')
output_dir.mkdir(exist_ok=True)

io_helper = IOHelper(output_dir=output_dir)
docker_executor = DockerHelper(io_helper, timeout=180)

text_mention_termination = TextMentionTermination("<TERMINATE>")
max_messages_termination = MaxMessageTermination(max_messages=25)
termination = text_mention_termination | max_messages_termination

def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
    if messages[-1].source != SUPERVISOR_AGENT.name:
        return SUPERVISOR_AGENT.name
    return None

async def process_request(files, prompt):
    if not files or not prompt:
        return "Please provide both files and a prompt.", None
    for uploaded_file in files:
        file_path = os.path.abspath(uploaded_file.name)
        print(f"Uploaded file path: {file_path}")
    
    code_executor = await docker_executor.initialize([files[0].name])
    executor_agent = EXECUTOR_AGENT
    executor_agent.set_code_executor(code_executor)
    team = SelectorGroupChat(
    [SUPERVISOR_AGENT, TRANSLATOR_AGENT, SENTIMENT_ANALYST_AGENT, PLANNER_AGENT, EXECUTOR_AGENT, CODER_AGENT],
    model_client=OpenAIChatCompletionClient(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY")),
    termination_condition=termination,
    selector_func=selector_func
    ) 
    results = await Console(team.run_stream(task=f"Process files and respond to: {prompt}"))

    zipped_file = docker_executor.get_zipped_output('generate_test.zip') 
    print(f'Zipped output created under path: {zipped_file}')

    await docker_executor.finish()

    return results, zipped_file