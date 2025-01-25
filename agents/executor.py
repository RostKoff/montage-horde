from autogen_core.code_executor import CodeExecutor
from autogen_agentchat.agents import CodeExecutorAgent

class ExecutorAgent(CodeExecutorAgent):
    """CodeExecutorAgent class wrapper with explicit code_executor setter."""
    
    def __init__(self, name, description: str = "A computer terminal that perform"):
        super().__init__(name=name, description=description, code_executor=None)
    
    def set_code_executor(self, code_executor: CodeExecutor):
        self._code_executor = code_executor

EXECUTOR_AGENT = ExecutorAgent(
    name='code_executor',
    description='An agent that runs code to modify videos.',
 )

        
