from content_assistant.tools.media_tools import image_prompt, shot_list
from content_assistant.tools.seo_tools import keyword_pack, meta_description
from content_assistant.tools.text_tools import call_to_action, headline


class ContentToolkit:
    def headline(self, prompt: str, audience: str) -> str:
        return headline(prompt, audience)

    def cta(self, task: str) -> str:
        return call_to_action(task)

    def keywords(self, prompt: str) -> list[str]:
        return keyword_pack(prompt)

    def meta(self, prompt: str) -> str:
        return meta_description(prompt)

    def shots(self, prompt: str) -> list[str]:
        return shot_list(prompt)

    def image_prompt(self, prompt: str, tone: str) -> str:
        return image_prompt(prompt, tone)
