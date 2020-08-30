from __future__ import division

import re
import sys

from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import pyaudio
from six.moves import queue

import config as cfg

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
#                               Microfono

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self,rate=cfg.RATE,chunk=cfg.CHUNK):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# --------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------
#                               Transcriber
"""
class Transcriber(MicrophoneStream):
    def  __init__(self,rate=cfg.RATE,chunk=cfg.CHUNK):
        # llamo a la super clase MicrophoneStream y la parametrizo
        MicrophoneStream.__init__(self,rate, chunk)
        self.transcriber_data = "nada"
"""

class Transcriber():
    def __init__(self,name_asistant):
         self.transcriber_data = ""
         self.name_asistant = name_asistant
    
    def go_transcriber(self,my_mic):
        # cofiguracion para la api de google Specch Recognition
        client,streaming_config = self.config_speech()
        # realizo request a la api con un fragmento de audio
        with my_mic as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator)
            responses = client.streaming_recognize(streaming_config, requests)
            # inciar un bucle 
            self.get_results(responses)

    def get_results(self,responses):
        # la variable response sigue creciendo mientras siga en el streaming por lo que se quedara en este loop
        for response in responses:
            if not response.results:
                continue
            result = response.results[0]
            if not result.alternatives:
                continue
            # Display the transcription of the top alternative.
            self.transcriber_data  = result.alternatives[0].transcript
            if re.search(r'\b(adiós|salir)\b', self.transcriber_data, re.I):
                print('Exiting..')
                break

    def config_speech(self,language_code=cfg.language_code,path_json=cfg.path_json):
        client = speech.SpeechClient.from_service_account_json(path_json)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=language_code)
        streaming_config = types.StreamingRecognitionConfig(
            config=config,
            interim_results=True)
        return client,streaming_config


    