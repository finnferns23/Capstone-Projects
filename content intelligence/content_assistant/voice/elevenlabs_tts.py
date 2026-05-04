from pathlib import Path
from content_assistant.config import settings


class ElevenLabsTTS:
    async def synthesize(self, text: str, output_path: Path | None = None) -> str:
        if not settings.elevenlabs_api_key:
            return "ElevenLabs fallback: add ELEVENLABS_API_KEY to enable voice file generation."
        try:
            from elevenlabs.client import ElevenLabs
            client = ElevenLabs(api_key=settings.elevenlabs_api_key)
            audio = client.text_to_speech.convert(voice_id="21m00Tcm4TlvDq8ikWAM", text=text, model_id="eleven_multilingual_v2")
            target = output_path or settings.output_dir / "voice_output.mp3"
            target.parent.mkdir(parents=True, exist_ok=True)
            with target.open("wb") as file:
                for chunk in audio:
                    file.write(chunk)
            return str(target)
        except Exception as exc:
            return f"ElevenLabs generation failed safely: {exc}"
