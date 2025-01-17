from autogen_agentchat.agents import UserProxyAgent

system_message="You are the supervisor managing a workflow. Your role is to assign tasks to other agents (translation_agent and sentiment_analyst_agent) to fulfill user's requests. Your role is to assign tasks to other agents (translation_agent and sentiment_analyst_agent) step-by-step to fulfill the user's requests. Whenever the agent gives you back their results, decide what to do with them next based on user's prompt. Make sure that you are the last agent to speak and that you print out the results of both tasks: sentiment analysis and translation."

supervisor_agent = UserProxyAgent(
    name="supervisor_agent"
    
)