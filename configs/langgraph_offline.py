# Offline LangGraph check: state graph + checkpointing + human-approval interrupt, no LLM.
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command

class S(TypedDict):
    findings: list
    approved: bool

def scan(s): return {"findings": ["lab-sqli-string-format"]}
def gate(s): return {"approved": interrupt({"review": s["findings"]})}
def report(s): return {"findings": s["findings"] + (["APPROVED"] if s["approved"] else ["REJECTED"])}

g = StateGraph(S)
for n, f in [("scan", scan), ("gate", gate), ("report", report)]: g.add_node(n, f)
g.add_edge(START, "scan"); g.add_edge("scan", "gate"); g.add_edge("gate", "report"); g.add_edge("report", END)
app = g.compile(checkpointer=InMemorySaver())
cfg = {"configurable": {"thread_id": "t1"}}
out = app.invoke({"findings": [], "approved": False}, cfg)
assert "__interrupt__" in out, out
out = app.invoke(Command(resume=True), cfg)
assert out["findings"] == ["lab-sqli-string-format", "APPROVED"], out
print("langgraph offline OK:", out)
