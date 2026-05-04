"""Main async orchestration layer for the Advanced Content AI Assistant."""
from __future__ import annotations

from content_assistant.core.grounding import GroundingGuard
from content_assistant.core.safety import SafetyGuard
from content_assistant.graph.workflow import ContentWorkflow
from content_assistant.schemas.content_schema import ContentRequest, ContentResponse
from content_assistant.services.content_service import ContentService
from content_assistant.services.capstone_service import CapstoneIntelligenceService
from content_assistant.services.export_service import ExportService
from content_assistant.services.memory_service import MemoryService
from content_assistant.services.rag_service import RagService
from content_assistant.services.validation_service import ValidationService
from content_assistant.utils.logging_config import get_logger

logger = get_logger(__name__)


class ContentAssistantOrchestrator:
    """Coordinates validation, safety, memory, RAG, agent routing, and exporting."""

    def __init__(self) -> None:
        self.validator = ValidationService()
        self.safety = SafetyGuard()
        self.grounding = GroundingGuard()
        self.memory = MemoryService()
        self.rag = RagService()
        self.content = ContentService()
        self.exporter = ExportService()
        self.capstone = CapstoneIntelligenceService()
        self.workflow = ContentWorkflow()

    async def run(self, request: ContentRequest) -> ContentResponse:
        """Run the complete assistant workflow with production-safe error handling."""
        try:
            request = self.validator.normalize(request)
            self.safety.validate(request)
            logger.info("Running content workflow for task=%s", request.task)

            category = self.capstone.classify(request.prompt)
            request.metadata["predicted_category"] = category
            request.metadata["category_confidence"] = self.capstone.confidence(request.prompt)

            memory_context = await self.memory.recall(request.prompt)
            rag_context = await self.rag.context_for(request.prompt)
            response = await self.content.generate(request, context=rag_context, memory=memory_context)

            grounding = self.grounding.build(rag_context, self.capstone.dataset_summary)

            optimized_content, optimization_metadata = self.capstone.optimize(
                response.content,
                category=category,
                audience=request.audience,
                tone=request.tone,
            )
            response.content = self.grounding.append_note(optimized_content, grounding)
            response.metadata.update(optimization_metadata)
            response.metadata["predicted_category"] = category
            response.metadata["grounding_sources"] = grounding.sources
            if grounding.warning:
                response.metadata["grounding_warning"] = grounding.warning
            response.metadata["category_confidence"] = self.capstone.confidence(request.prompt)

            try:
                await self.memory.remember(request.prompt, response.content, request.task)
            except Exception:
                logger.exception("Memory write failed; continuing without breaking the response.")
                response.metadata["memory_warning"] = "Memory write failed."

            try:
                saved_path = self.exporter.save(response.content)
                response.metadata["saved_path"] = str(saved_path)
            except Exception:
                logger.exception("Export failed; returning unsaved response.")
                response.metadata["export_warning"] = "Export failed."

            response.metadata["workflow"] = self.workflow.describe()
            self.capstone.track({
                "task": request.task,
                "predicted_category": category,
                "prompt_length": len(request.prompt),
                "output_length": len(response.content),
                "quality_score": response.metadata.get("quality_score"),
            })
            return response
        except Exception as exc:
            logger.exception("Content assistant workflow failed.")
            return ContentResponse(
                content=(
                    "The assistant encountered a recoverable workflow issue. "
                    "Please check your input and configuration, then try again.\n\n"
                    f"Details: {exc}"
                ),
                agent_name="orchestrator_fallback",
                mode="safe_error_fallback",
                metadata={"error": str(exc)},
            )
