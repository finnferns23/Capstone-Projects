from content_assistant.voice.elevenlabs_tts import ElevenLabsTTS


class VoiceInterface:
    def __init__(self) -> None:
        self.tts = ElevenLabsTTS()

    async def speak(self, text: str) -> str:
        return await self.tts.synthesize(text)
