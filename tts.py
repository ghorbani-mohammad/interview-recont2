import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig

def synthesize_to_speaker(text):
    speech_config = speechsdk.SpeechConfig(subscription="", region="")
    file_name = "outputaudio.mp3"
    # audio_config = AudioOutputConfig(use_default_speaker=True, filename=file_name)
    audio_config = AudioOutputConfig(use_default_speaker=True)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    result = synthesizer.speak_text_async(text).get()
    first_byte_latency = int(result.properties.get_property(speechsdk.PropertyId.SpeechServiceResponse_SynthesisFirstByteLatencyMs))
    finished_latency = int(result.properties.get_property(speechsdk.PropertyId.SpeechServiceResponse_SynthesisFinishLatencyMs))
    # you can also get the result id, and send to us when you need help for diagnosis
    result_id = result.result_id
    print(f"result-id: {result_id}")
    print(f"first-byte-latency: {first_byte_latency}")
    print(f"finished-latency: {finished_latency}")
    audio_data_stream = speechsdk.AudioDataStream(result)
    audio_buffer = bytes(16000)
    filled_size = audio_data_stream.read_data(audio_buffer)
    counter = 0
    while filled_size > 0:
        print(f"{filled_size} bytes received.")
        # audio_data_stream.save_to_wav_file(f"outputaudio-{counter}.wav")
        filled_size = audio_data_stream.read_data(audio_buffer)
    # if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    #     print(f"Speech synthesized for text [{text}], and the audio was saved to [{file_name}]")
    # elif result.reason == speechsdk.ResultReason.Canceled:
    #     cancellation_details = result.cancellation_details
    #     print(f"Speech synthesis canceled: {cancellation_details.reason}")
    #     if cancellation_details.reason == speechsdk.CancellationReason.Error:
    #         print(f"Error details: {cancellation_details.error_details}")


text = """
There was once a baby show among the Animals in the forest. Jupiter provided the prize. 
Of course all the proud mammas from far and near brought their babies.
But none got there earlier than Mother Monkey. Proudly she presented her baby among the other contestants.
As you can imagine, there was quite a laugh when the Animals saw the ugly flat-nosed, hairless, pop-eyed little creature.
"Laugh if you will," said the Mother Monkey. "Though Jupiter may not give him the prize, I know that he is the prettiest, the sweetest, the dearest darling in the world."
"""
synthesize_to_speaker(text)