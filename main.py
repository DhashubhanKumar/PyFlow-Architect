import os
import sys
import io
import operator
from typing import Annotated, TypedDict, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

# 1. Setup Environment
load_dotenv()
llm = ChatGroq(model="llama-3.3-70b-versatile")

# 2. Define the State
class AgentState(TypedDict):
    messages: Annotated[List[str], operator.add]
    current_code: str
    is_fixed: bool
    attempts: int

# 3. Scout Agent: Strategic Planning
def scout_agent(state: AgentState):
    user_input = state['messages'][-1]
    system_prompt = (
        "You are a Senior Python Architect. Analyze the user's request and provide "
        "a detailed logic plan. Specify which Python libraries to use (e.g., math, itertools). "
        "Instruct the developer to include sample test data within the code."
    )
    response = llm.invoke([{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}])
    return {"messages": [response.content]}

# 4. Mechanic Agent: Python Specialist
def mechanic_agent(state: AgentState):
    # Check for error feedback from the Inspector
    last_message = state['messages'][-1]
    error_feedback = ""
    if "FAIL" in last_message:
        error_feedback = f"\n\nCRITICAL: Your last code failed. Fix this error: {last_message}"

    system_prompt = (
        "You are an Expert Python Developer. Write ONLY raw Python code. "
        "Do not use markdown backticks or explanations. Include all imports. "
        "Ensure the code includes its own test cases so it can be verified immediately."
        f"{error_feedback}"
    )
    
    # Use the most recent long message (the plan) as context
    plan = [msg for msg in state['messages'] if len(msg) > 100][-1]
    response = llm.invoke([{"role": "system", "content": system_prompt}, {"role": "user", "content": plan}])
    return {"current_code": response.content, "messages": ["Mechanic generated Python code."]}

# 5. Inspector Agent: Internal Python Execution
def inspector_agent(state: AgentState):
    code = state['current_code']
    # Clean code of accidental markdown
    clean_code = code.replace("```python", "").replace("```", "").strip()
    
    # Capture stdout
    output_capture = io.StringIO()
    old_stdout = sys.stdout
    sys.stdout = output_capture
    
    try:
        # Execute the code in a clean global scope
        exec(clean_code, {"__name__": "__main__"}) 
        sys.stdout = old_stdout
        result = f"PASS\nOutput:\n{output_capture.getvalue()}"
        is_fixed = True
    except Exception as e:
        sys.stdout = old_stdout
        result = f"FAIL: {type(e).__name__}: {str(e)}"
        is_fixed = False
    
    return {
        "messages": [f"Inspector Result: {result}"], 
        "is_fixed": is_fixed, 
        "attempts": state.get('attempts', 0) + 1
    }

# 6. Graph Construction
workflow = StateGraph(AgentState)
workflow.add_node("scout", scout_agent)
workflow.add_node("mechanic", mechanic_agent)
workflow.add_node("inspector", inspector_agent)

workflow.set_entry_point("scout")
workflow.add_edge("scout", "mechanic")
workflow.add_edge("mechanic", "inspector")

def decide_to_finish(state):
    if state["is_fixed"] or state.get("attempts", 0) >= 3:
        return "end"
    return "mechanic"

workflow.add_conditional_edges("inspector", decide_to_finish, {"mechanic": "mechanic", "end": END})

app = workflow.compile(checkpointer=MemorySaver())