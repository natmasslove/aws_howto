import os
from dotenv import load_dotenv
from strands.models.openai import OpenAIModel

load_dotenv()

model = OpenAIModel(
    client_args={
        "api_key": os.environ["OPENROUTER_API_KEY"],
        "base_url": "https://openrouter.ai/api/v1",
    },
    model_id="minimax/minimax-m2.5:free",
)

from strands import Agent

agent = Agent(
    model=model,  # Works the same whether BedrockModel or OpenAIModel
    system_prompt="You are a personal AI assistant.",
    # tools=my_tools,
)

agent("What is the biggest country in the world (territory)? Name top10")
