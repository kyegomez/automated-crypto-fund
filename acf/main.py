import os

from cryptoagent.main import CryptoAgent
from cryptoagent.prompts import CRYPTO_AGENT_SYS_PROMPT
from dotenv import load_dotenv
from news_swarm.main import NewsAgent
from swarm_models import OpenAIChat
from swarms import Agent, AgentRearrange

load_dotenv()

# Get the OpenAI API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Create an instance of the OpenAIChat class
model = OpenAIChat(
    openai_api_key=api_key, model_name="gpt-4o-mini", temperature=0.1
)

# Initialize the agent
base_agent = Agent(
    agent_name="News-Agent-V1",
    # system_prompt=FINANCIAL_AGENT_SYS_PROMPT,
    llm=model,
    max_loops=1,
    autosave=True,
    dashboard=False,
    verbose=True,
    dynamic_temperature_enabled=True,
    saved_state_path="news_agent.json",
    user_name="swarms_corp",
    retry_attempts=1,
    context_length=200000,
    return_step_meta=False,
    # output_type="json",
)

# Agent
news_agent = NewsAgent(
    agent_name="news-agent-v1",
    agent=base_agent,
    newsapi_api_key=os.getenv("NEWSAPI_API_KEY"),
    system_prompt=None,
    return_json=True,
    # start_date="2024-08-01",
    # end_date="2024-08-10"
)


# Run the agent
# print(agent.run("multi-agent collaboration"))
# print(agent.run_concurrently(["OpenAI", "Anthropic"]))

# # Create an instance of the OpenAIChat class for LLM integration
# api_key = os.getenv("OPENAI_API_KEY")
# model = OpenAIChat(
#     openai_api_key=api_key, model_name="gpt-4o-mini", temperature=0.1
# )

# Create the input agent
crypto_data_agent = Agent(
    agent_name="Crypto-Analysis-Agent",
    system_prompt=CRYPTO_AGENT_SYS_PROMPT,
    llm=model,
    max_loops=1,
    autosave=True,
    dashboard=False,
    verbose=True,
    dynamic_temperature_enabled=True,
    saved_state_path="crypto_agent.json",
    user_name="swarms_corp",
    retry_attempts=1,
    context_length=10000,
)

# Create CryptoAgent instance and pass the input agent
crypto_analyzer = CryptoAgent(agent=crypto_data_agent, autosave=True)

# Example coin IDs to summarize multiple coins
coin_ids = ["bitcoin", "ethereum"]

# Fetch and summarize crypto data for multiple coins in parallel
summaries = crypto_analyzer.run(
    coin_ids,
    "Conduct a thorough analysis of the following coins:",
    # real_time=True,
)



analyst_swarm = AgentRearrange(
    name = "analyst-team-01",
    description="First fetch coins, then fetch news, then write a detailed report on whether it's a buy and sell.",
    agents = [crypto_data_agent, news_agent],
    flow=f"{crypto_data_agent.name} -> {news_agent.name}"
)


