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
    audio_encoding = texttospeech.AudioEncoding.MP3
  )
  response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config)
  return response.audio_content

def text_to_ssml(text: str) -> str:
  logger.debug(f"text_to_ssml(text: '{text}')")
  escaped_text = html.escape(text)
  logger.debug(f"Escaped text: '{escaped_text}'")
  lined_text = escaped_text.replace('\n', '\n<break time="1s"/>')
  logger.debug(f"Lined text: {lined_text}")
  ssml = f"<speak>{lined_text}</speak>"
  logger.debug(f"Result: '{ssml}'")
  return ssml

def user_text_to_ssml(display_name: str, text: str) -> str:
  logger.debug(f"user_text_to_ssml(display_name: '{display_name}', text: '{text}')")
  escaped_text = html.escape(text)
  logger.debug(f"Escaped text: '{escaped_text}'")
  lined_text = escaped_text.replace('\n', '\n<break time="1s"/>')
  logger.debug(f"Lined text: {lined_text}")
  joined_text = f"<emphasis level=\"strong\">{display_name}</emphasis> said:<break time=\"500\"/>{text}"
  logger.debug(f"Joined text: {joined_text}")
  ssml = f"<speak>{joined_text}</speak>"
  logger.debug(f"Result: '{ssml}'")
  return ssml
