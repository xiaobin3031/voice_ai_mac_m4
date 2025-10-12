import whisper
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class ASR:
    def __init__(self, model_size="small"):
        # 会自动下载模型到 ~/.cache
        self.model = whisper.load_model(model_size)

    def transcribe_file(self, wav_path: str) -> str:
        result = self.model.transcribe(wav_path)
        return result.get("text", "")

    def transcribe_audio_bytes(self, autio_path: str) -> str:
        return self.transcribe_file(autio_path)