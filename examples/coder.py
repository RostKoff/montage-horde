from pathlib import Path
# Append project to python search path in order to resolve local packages.
import sys
sys.path.append(Path('./').absolute().name)

from autogen_core import CancellationToken
from agents.executor import EXECUTOR_AGENT
from agents.coder import CODER_AGENT
from utils.docker_helper import DockerHelper
from utils.io_helper import IOHelper
import asyncio
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console


output_dir = Path('app/work_dir/output')
output_dir.mkdir(exist_ok=True)

test_file = Path('user_input_test.txt')
test_file.touch(exist_ok=True)

io_helper = IOHelper(output_dir=output_dir)
docker_executor = DockerHelper(io_helper, timeout=180)

async def coder_test(prompt):
    code_executor = await docker_executor.initialize([test_file.absolute().name])
    executor_agent = EXECUTOR_AGENT
    executor_agent.set_code_executor(code_executor)
    
    termination_condition = MaxMessageTermination(3)
    team=RoundRobinGroupChat([CODER_AGENT, executor_agent], termination_condition=termination_condition)
    
    await Console(team.run_stream(task=prompt, cancellation_token=CancellationToken()))
    
    zipped_file = docker_executor.get_zipped_output('generate_test.zip') 
    print(f'Zipped output created under path: {zipped_file}')
    
    await docker_executor.finish()
    
asyncio.run(coder_test(
    (
        "Write a script to read text file from the input and transfer it's content to the output text file.\n" 
        "If there is nothing in the input file, write NO DATA in the output file.\n" 
        "### INPUT FILES ###\n"
        "`user_input_test.txt``\n"
    )
))
        
    