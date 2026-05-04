"""Workflow definition for the Advanced Content Intelligence system.

The runtime orchestrator is intentionally explicit for readability and reliable
local execution. This module provides a LangGraph-compatible workflow blueprint
so the same pipeline can be promoted into a graph execution layer when needed.
"""
from __future__ import annotations

from typing import Any, Dict, List, TypedDict


class ContentWorkflowState(TypedDict, total=False):
    """State shape used by the optional LangGraph workflow."""

    request: Dict[str, Any]
    validation_status: str
    safety_status: str
    memory_context: str
    rag_context: str
    selected_agent: str
    draft_content: str
    optimized_content: str
    export_path: str
    metadata: Dict[str, Any]


class ContentWorkflow:
    """Describes and optionally builds the advanced content workflow."""

    def __init__(self) -> None:
        self.steps: List[str] = [
            "validate_request",
            "apply_safety_guard",
            "classify_content_intent",
            "recall_memory_context",
            "retrieve_rag_context",
            "route_to_specialist_agent",
            "generate_channel_ready_content",
            "optimize_with_capstone_intelligence",
            "ground_response_with_sources",
            "persist_memory_and_export",
        ]

    def describe(self) -> Dict[str, Any]:
        return {
            "workflow": "advanced_content_intelligence_graph",
            "execution_mode": "explicit_async_orchestrator_with_langgraph_blueprint",
            "steps": self.steps,
            "capabilities": [
                "multi-agent routing",
                "RAG grounding",
                "persistent memory",
                "dataset-backed classification",
                "content optimization",
                "safe local fallback generation",
                "optional LangGraph promotion",
            ],
        }

    def build_langgraph(self):
        """Build a lightweight LangGraph blueprint when langgraph is installed.

        The nodes are pass-through markers so imports and tests remain safe
        without binding runtime services directly into the graph definition.
        """
        try:
            from langgraph.graph import END, StateGraph
        except Exception:
            return None

        def mark(step_name: str):
            def _node(state: ContentWorkflowState) -> ContentWorkflowState:
                metadata = dict(state.get("metadata", {}))
                completed = list(metadata.get("completed_steps", []))
                completed.append(step_name)
                metadata["completed_steps"] = completed
                state["metadata"] = metadata
                return state

            return _node

        graph = StateGraph(ContentWorkflowState)
        for step in self.steps:
            graph.add_node(step, mark(step))

        graph.set_entry_point(self.steps[0])
        for current_step, next_step in zip(self.steps, self.steps[1:]):
            graph.add_edge(current_step, next_step)
        graph.add_edge(self.steps[-1], END)
        return graph.compile()
