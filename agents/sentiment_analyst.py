import openai
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from transformers import pipeline
from data.prompts import SENTIMENT_ANALYSIS_PROMPT

def analyze_sentiment(prompt: str) -> str:
    try:
        pipe = pipeline("text-classification", model="tabularisai/multilingual-sentiment-analysis")
        return f"Sentiment: {pipe(prompt)}"
    except Exception as e:
        return f"Error analyzing sentiment: {str(e)}"

SENTIMENT_ANALYST_AGENT = AssistantAgent(
    name="sentiment_analyst",
    model_client=OpenAIChatCompletionClient(
    model="gpt-4o"),
    tools=[analyze_sentiment],
    system_message=SENTIMENT_ANALYSIS_PROMPT,
)