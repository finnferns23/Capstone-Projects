from content_assistant.schemas.content_schema import ContentRequest


class SafetyGuard:
    blocked_terms = {"malware", "phishing kit", "credential theft"}

    def validate(self, request: ContentRequest) -> None:
        prompt_lower = request.prompt.lower()
        if any(term in prompt_lower for term in self.blocked_terms):
            raise ValueError("This request is not supported by the content assistant safety policy.")
