import speech_recognition as sr


def speech_to_text(audio_file_path):
	r = sr.Recognizer()
	with sr.AudioFile(audio_file_path) as source:
		# r.adjust_for_ambient_noise(source)
		audio = r.record(source)
		return r.recognize_google(audio, language='ru')
	
	