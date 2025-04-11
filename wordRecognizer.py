from google.cloud import speech, storage
import os

class wordRecognizer:

    def __init__(self, path):
        self.path = path
        self.words = None
        self.bucket = "my-audio-bucket-simongray"

    def getWords(self):
        return self.words

    def transcribe_file(self):
        client = speech.SpeechClient()
        gcs_uri = self.upload_to_gcs()
        audio = speech.RecognitionAudio(uri=gcs_uri)
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=24000,
            language_code="en-US",
            enable_word_time_offsets=True
        )
        operation = client.long_running_recognize(config=config, audio=audio)
        response = operation.result(timeout=300)
        self.extract_word_timings(response)

    def extract_word_timings(self, response):
        word_timings = []
        for result in response.results:
            for alternative in result.alternatives:
                for word_info in alternative.words:
                    word = word_info.word
                    start_time = word_info.start_time.total_seconds()
                    end_time = word_info.end_time.total_seconds()
                    word_timings.append((word, start_time, end_time))
                    print((word, start_time, end_time))
        self.words = word_timings

    def upload_to_gcs(self):
        storage_client = storage.Client()
        bucket = storage_client.bucket(self.bucket)
        blob_name = os.path.basename(self.path)
        blob = bucket.blob(blob_name)
        if blob.exists():
            gcs_uri = f"gs://{self.bucket}/{blob_name}"
            print(f"File already exists: {gcs_uri}")
            return gcs_uri
        blob.upload_from_filename(self.path)
        gcs_uri = f"gs://{self.bucket}/{blob_name}"
        print(f"Uploaded to {gcs_uri}")
        return gcs_uri