import speech_recognition as sr

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    
    try:
        # Convert the audio file to AudioFile object
        with sr.AudioFile(audio_file) as source:
            # Record the audio data
            audio_data = recognizer.record(source)
            # Convert speech to text
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Speech recognition could not understand the audio"
    except sr.RequestError:
        return "Could not request results from speech recognition service"