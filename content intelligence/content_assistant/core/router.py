from content_assistant.agents.audio_agent import AudioAgent
from content_assistant.agents.blog_agent import BlogAgent
from content_assistant.agents.campaign_agent import CampaignAgent
from content_assistant.agents.email_agent import EmailAgent
from content_assistant.agents.image_agent import ImageAgent
from content_assistant.agents.repurpose_agent import RepurposeAgent
from content_assistant.agents.seo_agent import SeoAgent
from content_assistant.agents.social_agent import SocialAgent
from content_assistant.agents.text_agent import TextAgent
from content_assistant.agents.video_agent import VideoAgent


class AgentRouter:
    def __init__(self) -> None:
        self.agents = {
            "text": TextAgent(),
            "blog": BlogAgent(),
            "social": SocialAgent(),
            "email": EmailAgent(),
            "audio": AudioAgent(),
            "video": VideoAgent(),
            "image": ImageAgent(),
            "campaign": CampaignAgent(),
            "repurpose": RepurposeAgent(),
            "seo": SeoAgent(),
        }

    def route(self, task: str):
        return self.agents.get(task, self.agents["text"])
