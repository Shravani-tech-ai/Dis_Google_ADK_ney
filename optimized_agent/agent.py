from google.adk.agents import SequentialAgent

from .sub_agents.context_agent import context_agent
from .sub_agents.answer_agent import answer_agent

root_agent = SequentialAgent(
    name="disney_workflow",
    sub_agents=[
        context_agent,
        answer_agent
    ]
)