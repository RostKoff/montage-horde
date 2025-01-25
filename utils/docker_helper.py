from autogen_ext.code_executors.docker import DockerCommandLineCodeExecutor
from utils.io_helper import IOHelper

class DockerHelper():
    def __init__(self, io_helper: IOHelper, timeout: int):
        self.io_helper = io_helper
        self.timeout = timeout
        self.code_executor = None
        
    async def initialize(self, gradio_files):
        self.io_helper.init_work_dir(gradio_files)
        
        self.code_executor = DockerCommandLineCodeExecutor( 
            work_dir=self.io_helper.work_dir.name,
            timeout=self.timeout,
            auto_remove=True,
            stop_container=True
        )
        await self.code_executor.start()
        return self.code_executor
    
    def get_zipped_output(self, output_name):
        return self.io_helper.create_zipped_output(output_name)
    
    async def finish(self):
        self.io_helper.cleanup()
        if self.code_executor:
            await self.code_executor.stop()