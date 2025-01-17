import openai
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

openai.api_key = ""

def analyze_sentiment(prompt: str) -> str:
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": SENTIMENT_ANALYSIS_PROMPT},
                      {"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.0
        )
        sentiment = response.choices[0].message.content
        return f"Sentiment: {sentiment}"
    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"

SENTIMENT_ANALYSIS_PROMPT = """
You are a sentiment analysis agent. Your task is to analyze the sentiment of the given transcription and return to your supervisor whether it's positive, negative, or neutral.
"""

model_client = OpenAIChatCompletionClient(
    model="gpt-4o",
    api_key="",
)
sentiment_analyst_agent = AssistantAgent(
    name="sentiment_analyst_agent",
    model_client=model_client,
    tools=[analyze_sentiment],
    system_message=SENTIMENT_ANALYSIS_PROMPT,
)