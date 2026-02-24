from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from nodes import (
    analysis_planning,
    evidence_gathering,
    evidence_scoring,
    evaluation_node,
    refinement_node,
    conflict_detection_node,   # IMPORTANT: import this
    synthesis_node
)

class AgentState(TypedDict):
    question: str
    domain: str
    strategy: str
    queries: List[str]
    raw_evidence: List[Dict[str, Any]]
    scored_evidence: List[Dict[str, Any]]
    report: str
    conflicts: str
    confidence_history: List[float]
    confidence: float
    iteration: int
    thinking_log: List[str]


def build_graph():
    graph = StateGraph(AgentState)

    # Nodes
    graph.add_node("analysis", analysis_planning)
    graph.add_node("evidence", evidence_gathering)
    graph.add_node("scoring", evidence_scoring)
    graph.add_node("evaluation", evaluation_node)
    graph.add_node("refinement", refinement_node)
    graph.add_node("conflict", conflict_detection_node)
    graph.add_node("synthesis", synthesis_node)

    # Entry point
    graph.set_entry_point("analysis")

    # Main flow
    graph.add_edge("analysis", "evidence")
    graph.add_edge("evidence", "scoring")
    graph.add_edge("scoring", "evaluation")

    # Refinement logic
    def should_refine(state):
        if state["confidence"] >= 0.80:
            state["thinking_log"].append("Confidence threshold reached.")
            return False

        if state["iteration"] >= 2:
            state["thinking_log"].append("Max iterations reached.")
            return False

        return True

    # Conditional branch
    graph.add_conditional_edges(
        "evaluation",
        should_refine,
        {
            True: "refinement",
            False: "conflict"   # IMPORTANT CHANGE
        }
    )

    # Loop back if refining
    graph.add_edge("refinement", "evidence")

    # After conflict → synthesis
    graph.add_edge("conflict", "synthesis")

    # Final end
    graph.add_edge("synthesis", END)

    return graph.compile()