import io
from openai import OpenAI
from pydub import AudioSegment
from pydub.playback import play

client = OpenAI(api_key="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")


def stream_and_play(text: str, voice="alloy"):
	response = client.audio.speech.create(
		model="tts-1",
		voice=voice,
		input=text,
	)
	
	# Convert the binary response content to a byte stream
	byte_stream = io.BytesIO(response.content)
	
	# Read the audio data from the byte stream
	audio = AudioSegment.from_file(byte_stream, format="mp3")
	
	# Play the audio
	play(audio)


if __name__ == "__main__":
	stream_and_play(input("Enter text: "))
