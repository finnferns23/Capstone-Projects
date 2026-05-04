from content_assistant.schemas.content_schema import ContentRequest


class ValidationService:
    supported_tasks = {"text", "blog", "social", "email", "audio", "video", "image", "campaign", "repurpose", "seo"}

    def normalize(self, request: ContentRequest) -> ContentRequest:
        task = request.task.lower().strip()
        if task not in self.supported_tasks:
            task = "text"
        request.task = task
        request.prompt = request.prompt.strip() or "Create a professional content plan."
        return request
