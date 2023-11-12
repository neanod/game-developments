import openai
from openai import OpenAI

client = OpenAI(api_key="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")


def speech_to_text(audio_file):
	audio_file = open(audio_file, "rb")
	transcript = client.audio.translations.create(
		model="whisper-1",
		file=audio_file
	)
	return transcript.text
