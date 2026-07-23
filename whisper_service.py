import os
from pathlib import Path
from openai import OpenAI
from typing import Optional

class WhisperService:
    """
    Service to handle audio-to-text conversion using the OpenAI Whisper API.
    """
    def __init__(self, api_key: Optional[str] = None):
        # Use provided API key or fallback to environment variable
        self.api_key = api_key or os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required for WhisperService")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=os.getenv("AI_API_BASE_URL")
        )

    def transcribe_audio(self, audio_path: Path, language: Optional[str] = None) -> str:
        """
        Sends an audio file to the Whisper API and returns the transcribed text.
        
        Args:
            audio_path: Path to the audio file.
            language: Optional ISO-639-1 language code.
            
        Returns:
            The transcribed text.
        """
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model=os.getenv("MODEL_NAME", "whisper-1"), 
                    file=audio_file,
                    language=language if language else None
                )
            return transcript.text
        except Exception as e:
            print(f"Whisper API Error: {str(e)}")
            raise e
