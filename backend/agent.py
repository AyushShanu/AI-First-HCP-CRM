"""
LangGraph AI Agent for HCP CRM.
Role: Understands natural language from field reps, extracts structured
interaction data via the Groq LLM, and routes intent to the correct tool.
"""
import os, json
from typing import Annotated, TypedDict
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver

from database import SessionLocal
from models import Interaction, HCP, FollowUp

# Stores the most recently extracted interaction for the current request
LAST_EXTRACTED = {}
load_dotenv()

MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
llm = ChatGroq(model=MODEL, temperature=0)
# Extraction LLM (used inside tools for summarization/entity extraction)
extractor_llm = ChatGroq(model=MODEL, temperature=0)


# ---------------------------------------------------------------------------
# TOOL 1: Log Interaction  (MANDATORY)
# Uses the LLM internally for entity extraction + summarization
# ---------------------------------------------------------------------------

@tool
def log_interaction(raw_text: str) -> str:
    """Log a new HCP interaction from a free-text description."""

    prompt = f"""Extract structured CRM data from this pharma field-rep note.
Return ONLY valid JSON with keys:
hcp_name, interaction_type (Meeting/Call/Email/Conference),
date (YYYY-MM-DD or ""), time (HH:MM or ""), attendees,
topics_discussed, materials_shared, samples_distributed,
sentiment (Positive/Neutral/Negative), outcomes, follow_up_actions,
summary (1-2 sentence professional summary).

Note: \"\"\"{raw_text}\"\"\""""

    resp = extractor_llm.invoke([HumanMessage(content=prompt)]).content
    resp = (
        resp.strip()
        .removeprefix("```json")
        .removeprefix("```")
        .removesuffix("```")
        .strip()
    )

    try:
        data = json.loads(resp)
    except json.JSONDecodeError:
        return "ERROR: Could not extract structured data."

    db = SessionLocal()

    try:
        hcp = (
            db.query(HCP)
            .filter(HCP.name.ilike(f"%{data.get('hcp_name', '')}%"))
            .first()
        )

        rec = Interaction(
            hcp_id=hcp.id if hcp else None,
            hcp_name=data.get("hcp_name", "Unknown"),
            interaction_type=data.get("interaction_type", "Meeting"),
            date=data.get("date", ""),
            time=data.get("time", ""),
            attendees=data.get("attendees", ""),
            topics_discussed=data.get("topics_discussed", ""),
            materials_shared=data.get("materials_shared", ""),
            samples_distributed=data.get("samples_distributed", ""),
            sentiment=data.get("sentiment", "Neutral"),
            outcomes=data.get("outcomes", ""),
            follow_up_actions=data.get("follow_up_actions", ""),
            ai_summary=data.get("summary", ""),
        )

        db.add(rec)
        db.commit()
        db.refresh(rec)

        # Update shared dictionary
        LAST_EXTRACTED.clear()
        LAST_EXTRACTED["interaction_id"] = rec.id
        LAST_EXTRACTED["form"] = data

        print("AGENT:", LAST_EXTRACTED)

        return json.dumps({
            "status": "logged",
            "interaction_id": rec.id,
            "extracted": data,
        })

    finally:
        db.close()


# ---------------------------------------------------------------------------
# TOOL 2: Edit Interaction  (MANDATORY)
# ---------------------------------------------------------------------------
@tool
def edit_interaction(
    interaction_id: str,
    field: str,
    new_value: str
) -> str:
    """
    Edit a logged interaction.

    Allowed fields:
    hcp_name,
    interaction_type,
    date,
    time,
    attendees,
    topics_discussed,
    materials_shared,
    samples_distributed,
    sentiment,
    outcomes,
    follow_up_actions
    """

    # Convert interaction_id to integer
    try:
        interaction_id = int(interaction_id)
    except (ValueError, TypeError):
        return "ERROR: Interaction ID must be a valid integer."

    allowed = {
        "hcp_name",
        "interaction_type",
        "date",
        "time",
        "attendees",
        "topics_discussed",
        "materials_shared",
        "samples_distributed",
        "sentiment",
        "outcomes",
        "follow_up_actions",
    }

    if field not in allowed:
        return (
            f"ERROR: Invalid field '{field}'. "
            f"Allowed fields: {', '.join(sorted(allowed))}"
        )

    db = SessionLocal()

    try:
        # Modern SQLAlchemy way
        rec = db.get(Interaction, interaction_id)

        if rec is None:
            return f"ERROR: Interaction {interaction_id} not found."

        old_value = getattr(rec, field)

        setattr(rec, field, new_value)

        db.commit()
        db.refresh(rec)

        return json.dumps({
            "status": "updated",
            "interaction_id": interaction_id,
            "field": field,
            "old_value": old_value,
            "new_value": new_value
        })

    finally:
        db.close()


# ---------------------------------------------------------------------------
# TOOL 3: Get HCP Profile / Interaction History
# ---------------------------------------------------------------------------
@tool
def get_hcp_history(hcp_name: str) -> str:
    """Retrieve an HCP's profile and recent interaction history
    so the rep can prepare before a visit."""
    db = SessionLocal()
    try:
        hcp = db.query(HCP).filter(HCP.name.ilike(f"%{hcp_name}%")).first()
        recs = (db.query(Interaction)
                .filter(Interaction.hcp_name.ilike(f"%{hcp_name}%"))
                .order_by(Interaction.created_at.desc()).limit(5).all())
        return json.dumps({
            "profile": {"name": hcp.name, "specialty": hcp.specialty,
                        "hospital": hcp.hospital} if hcp else "Not in database",
            "recent_interactions": [
                {"id": r.id, "date": r.date, "type": r.interaction_type,
                 "topics": r.topics_discussed, "sentiment": r.sentiment,
                 "summary": r.ai_summary} for r in recs],
        })
    finally:
        db.close()


# ---------------------------------------------------------------------------
# TOOL 4: Schedule Follow-up
# ---------------------------------------------------------------------------
@tool
def schedule_follow_up(hcp_name: str, task: str, due_date: str = "") -> str:
    """Create a follow-up task for an HCP (e.g. 'send Phase III PDF',
    'schedule meeting in 2 weeks'). due_date format YYYY-MM-DD."""
    db = SessionLocal()
    try:
        fu = FollowUp(hcp_name=hcp_name, task=task, due_date=due_date)
        db.add(fu); db.commit(); db.refresh(fu)
        return json.dumps({"status": "scheduled", "follow_up_id": fu.id,
                           "hcp": hcp_name, "task": task, "due": due_date})
    finally:
        db.close()


# ---------------------------------------------------------------------------
# TOOL 5: Compliance / Sample Limit Check
# ---------------------------------------------------------------------------
@tool
def check_sample_compliance(hcp_name: str) -> str:
    """Check how many samples were distributed to an HCP recently and
    flag if the compliance limit (3 per quarter) is exceeded."""
    db = SessionLocal()
    try:
        recs = (db.query(Interaction)
                .filter(Interaction.hcp_name.ilike(f"%{hcp_name}%"),
                        Interaction.samples_distributed != "").all())
        count = len(recs)
        LIMIT = 3
        return json.dumps({
            "hcp": hcp_name, "sample_events_this_quarter": count,
            "limit": LIMIT,
            "compliant": count < LIMIT,
            "message": "OK to distribute samples." if count < LIMIT
                       else "⚠️ LIMIT REACHED – do NOT distribute more samples."})
    finally:
        db.close()


# ---------------------------------------------------------------------------
# Build the LangGraph agent
# ---------------------------------------------------------------------------
TOOLS = [log_interaction, edit_interaction, get_hcp_history,
         schedule_follow_up, check_sample_compliance]

SYSTEM_PROMPT = """You are an AI assistant inside a pharma CRM helping field
representatives manage interactions with Healthcare Professionals (HCPs).

Decide the user's intent and call the correct tool:
- Describing a meeting/call/visit → log_interaction (pass the full text)
- Correcting logged data → edit_interaction
- Asking about an HCP or past visits → get_hcp_history
- Reminders / next steps → schedule_follow_up
- Sample limits / compliance → check_sample_compliance

After a tool runs, confirm briefly and clearly what was done, including the
interaction ID. Never invent medical claims. Be concise and professional."""

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

llm_with_tools = llm.bind_tools(TOOLS)

def agent_node(state: AgentState):
    msgs = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
    return {"messages": [llm_with_tools.invoke(msgs)]}

graph_builder = StateGraph(AgentState)
graph_builder.add_node("agent", agent_node)
graph_builder.add_node("tools", ToolNode(TOOLS))
graph_builder.add_edge(START, "agent")
graph_builder.add_conditional_edges("agent", tools_condition)
graph_builder.add_edge("tools", "agent")

memory = MemorySaver()
agent_graph = graph_builder.compile(checkpointer=memory)


def run_agent(message: str, session_id: str = "default") -> str:
    config = {"configurable": {"thread_id": session_id}}
    result = agent_graph.invoke(
        {"messages": [HumanMessage(content=message)]}, config=config)
    return result["messages"][-1].content
