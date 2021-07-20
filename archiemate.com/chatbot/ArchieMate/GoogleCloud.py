import html
from google.cloud import texttospeech

from ArchieMate import Logger

logger = Logger.get_logger(__name__)

def ssml_to_audio(ssml_text: str) -> bytes:
  client = texttospeech.TextToSpeechClient()
  synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
  voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", name="en-US-Wavenet-J"
  )
  audio_config = texttospeech.AudioConfig(
    audio_config = texttospeech.AudioEncoding.MP3
  )
  response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config)
  return response.audio_content

def text_to_ssml(text: str) -> str:
  logger.debug(f"text_to_ssml(text: '{text}')")
  escaped_text = html.escape(text)
  logger.debug(f"Escaped text: '{escaped_text}'")
  ssml = f"<speak>{escaped_text.replace('\n', '\n<break time=\"1s\"/>')}</speak>"
  logger.debug(f"Result: '{ssml}'")
  return ssml
