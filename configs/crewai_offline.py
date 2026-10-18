# Offline CrewAI check: construct agent/task/crew objects without kicking off (no LLM call).
import os
os.environ.setdefault("OPENAI_API_KEY", "sk-fake-offline")  # fake; kickoff() is never called
from crewai import Agent, Task, Crew, Process
a = Agent(role="Triage", goal="Review findings", backstory="lab", allow_delegation=False)
t = Task(description="Review lab findings", expected_output="summary", agent=a)
c = Crew(agents=[a], tasks=[t], process=Process.sequential)
assert len(c.tasks) == 1
print("crewai offline OK: crew constructed, process =", c.process)
