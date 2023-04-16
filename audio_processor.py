#from https://github.com/Uberi/speech_recognition

import argparse
import io
import os
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep
from sys import platform

class AudioProcessor:
    def __init__(self, source = None, phrases = None, model: str = "tiny", non_english: bool = False, record_timeout: float = 2, phrase_timeout: float = 1, energy_threshold: int = 1000, default_microphone: str = "default", ):
        # The last time a recording was retreived from the queue.
        self.phrase_time = None
        # Current raw audio bytes.
        self.last_sample = bytes()
        # Thread safe Queue for passing data from the threaded recording callback.
        self.data_queue = Queue()
        # We use SpeechRecognizer to record our audio because it has a nice feauture where it can detect when speech ends.
        self.recorder = sr.Recognizer()
        self.recorder.energy_threshold = energy_threshold
        # Definitely do this, dynamic energy compensation lowers the energy threshold dramtically to a point where the SpeechRecognizer never stops recording.
        self.recorder.dynamic_energy_threshold = False

        self.phrases = phrases

        if source == None:
            # Important for linux users. 
            # Prevents permanent application hang and crash by using the wrong Microphone
            if 'linux' in platform:
                mic_name = default_microphone
                if not mic_name or mic_name == 'list':
                    print("Available microphone devices are: ")
                    for index, name in enumerate(sr.Microphone.list_microphone_names()):
                        print(f"Microphone with name \"{name}\" found")   
                    return
                else:
                    for index, name in enumerate(sr.Microphone.list_microphone_names()):
                        if mic_name in name:
                            self.source = sr.Microphone(sample_rate=16000, device_index=index)
                            break
            else:
                self.source = sr.Microphone(sample_rate=16000)
        else:
            self.source = source

        # Load / Download model
        if model != "large" and not non_english:
            model = model + ".en"
        self.audio_model = whisper.load_model(model)

        self.record_timeout = record_timeout
        self.phrase_timeout = phrase_timeout

        self.temp_file = NamedTemporaryFile().name
        self.transcription = ['']

        with self.source as source:
            if (source.device_index != 17):
                self.recorder.adjust_for_ambient_noise(source)

        def record_callback(_, audio:sr.AudioData) -> None:
            """
            Threaded callback function to recieve audio data when recordings finish.
            audio: An AudioData containing the recorded bytes.
            """
            # Grab the raw bytes and push it into the thread safe queue.
            data = audio.get_raw_data()
            self.data_queue.put(data)

        # Create a background thread that will pass us raw audio bytes.
        # We could do this manually but SpeechRecognizer provides a nice helper.
        self.recorder.listen_in_background(self.source, record_callback, phrase_time_limit=self.record_timeout)

        # Cue the user that we're ready to go.
        print("Model loaded.\n")

    def update_transcript(self) -> None:
        now = datetime.utcnow()
        # Pull raw recorded audio from the queue.
        if not self.data_queue.empty():
            phrase_complete = False
            # If enough time has passed between recordings, consider the phrase complete.
            # Clear the current working audio buffer to start over with the new data.
            if self.phrase_time and now - self.phrase_time > timedelta(seconds=self.phrase_timeout):
                self.last_sample = bytes()
                phrase_complete = True
            # This is the last time we received new audio data from the queue.
            self.phrase_time = now

            # Concatenate our current audio data with the latest audio data.
            while not self.data_queue.empty():
                data = self.data_queue.get()
                self.last_sample += data

            # Use AudioData to convert the raw data to wav data.
            audio_data = sr.AudioData(self.last_sample, self.source.SAMPLE_RATE, self.source.SAMPLE_WIDTH)
            wav_data = io.BytesIO(audio_data.get_wav_data())

            # Write wav data to the temporary file as bytes.
            with open(self.temp_file, 'w+b') as f:
                f.write(wav_data.read())

            # Read the transcription.
            result = self.audio_model.transcribe(self.temp_file, fp16=torch.cuda.is_available(), initial_prompt=self.phrases)
            text = result['text'].strip()

            # If we detected a pause between recordings, add a new item to our transcripion.
            # Otherwise edit the existing one.
            if phrase_complete:
                self.transcription.append(text)
            else:
                self.transcription[-1] = text

            # Clear the console to reprint the updated transcription.
            os.system('cls' if os.name=='nt' else 'clear')
            #for line in self.transcription:
            #    print(line)
            # Flush stdout.
            print('', end='', flush=True)




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="medium", help="Model to use",
                        choices=["tiny", "base", "small", "medium", "large"])
    parser.add_argument("--non_english", action='store_true',
                        help="Don't use the english model.")
    parser.add_argument("--energy_threshold", default=1000,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=2,
                        help="How real time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=3,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)  
    if 'linux' in platform:
        parser.add_argument("--default_microphone", default='pulse',
                            help="Default microphone name for SpeechRecognition. "
                                 "Run this with 'list' to view available Microphones.", type=str)
    args = parser.parse_args()

    ap = AudioProcessor()

    while True:
        try:
            ap.update_transcript()
            sleep(0.25)
        except Exception as e:
            print(e)
            break

    # print("\n\nTranscription:")
    # for line in ap.transcription:
    #     print(line)


if __name__ == "__main__":
    main()