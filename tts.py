import pyaudio
import azure.cognitiveservices.speech as speechsdk


def synthesize_to_speaker(text):
    speech_config = speechsdk.SpeechConfig(subscription="", region="")
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.start_speaking_text_async(text).get()
    
    # create a stream to output (OutputStream)
    output_streamer = pyaudio.PyAudio()
    output_stream = output_streamer.open(format=8,channels=1,rate=16000,output=True)
    
    # create speech audio stream (InputStream) and read chunk by chunk and send it to OutputStream
    audio_data_stream = speechsdk.AudioDataStream(result)
    audio_buffer = bytes(16000)
    filled_size = audio_data_stream.read_data(audio_buffer)
    while filled_size > 0:
        print(f"{filled_size} bytes received.")
        output_stream.write(audio_buffer)
        audio_buffer = bytes(16000)
        filled_size = audio_data_stream.read_data(audio_buffer)


text = """
There was once a baby show among the Animals in the forest. Jupiter provided the prize. 
"""
synthesize_to_speaker(text)