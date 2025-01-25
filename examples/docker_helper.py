from pathlib import Path
# Append project to python search path in order to resolve local packages.
import sys
sys.path.append(Path('./').absolute().name)

import asyncio
from autogen_core import CancellationToken
from autogen_core.code_executor import CodeBlock
from utils.docker_helper import DockerHelper
from utils.io_helper import IOHelper

output_dir = Path('app/work_dir/output')
output_dir.mkdir(exist_ok=True)

test_file = Path('user_input_test.txt')
test_file.touch()

io_helper = IOHelper(output_dir=output_dir)
docker_executor = DockerHelper(io_helper, timeout=180)


async def test():
    global zipped_file
    await docker_executor.initialize([test_file.absolute().name])
    await docker_executor.code_executor.execute_code_blocks(code_blocks=[CodeBlock("ls user_input/ > test.txt", 'sh')], cancellation_token=CancellationToken())
    
    zipped_file = docker_executor.get_zipped_output('docker_test.zip') 
    print(zipped_file)
    
    await docker_executor.finish()
    
asyncio.run(test())
    

