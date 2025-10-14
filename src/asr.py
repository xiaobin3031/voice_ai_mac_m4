import whisper
import warnings
import queue
import threading
import sounddevice as sd
import numpy as np
import concurrent.futures
from collections import deque

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

SAMPLERATE = 16000
CHANNELS = 1
WAKE_WORD = "皮皮"
SILENCE_THRESHOLD = 0.01  # RMS 阈值，可调
SILENCE_SECONDS = 2       # 静音超过 2 秒停止
CHUNK = 1024              # 每次读取的帧数

class ASR:
    def __init__(self, model_size="small"):
        # 会自动下载模型到 ~/.cache
        self.model = whisper.load_model(model_size)
        self.audio_queue = queue.Queue()
        self.listening = False
        self.on_wakeup = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status)
        if np.max(np.abs(indata)) < 1e-3:
            return
        self.audio_queue.put(indata.copy())

    def start(self, on_wakeup):
        """ 启动监听 监测到唤醒词后调用回调 """
        self.on_wakeup = on_wakeup
        self.listening = True
        threading.Thread(target=self._recognize_stream, daemon=True).start()
        sd.InputStream(callback=self.audio_callback, channels=CHANNELS, samplerate=SAMPLERATE).start()
        print("🎙️ 开始监听唤醒词...")

    def safe_transcribe(self, float_data):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: self.model.transcribe(
                float_data,
                fp16=False,
                language="zh",
                condition_on_previous_text=False,
                no_speech_threshold=0.5,
                logprob_threshold=-1.0
            ))
            try:
                return future.result(timeout=5)
            except concurrent.futures.TimeoutError:
                print("⏱️ Whisper 推理超时，跳过该片段")
                return {"text": ""}

    def _recognize_stream(self):
        buffer = np.zeros((0, CHANNELS), dtype=np.int16)
        while self.listening:
            try:
                data = self.audio_queue.get()
                buffer = np.concatenate((buffer, data))
                if len(buffer) >= SAMPLERATE:
                    segment = buffer[:SAMPLERATE]
                    buffer = buffer[SAMPLERATE:]
                    float_data = segment.astype(np.float32) / 32768.0
                    if np.max(np.abs(float_data)) < 1e-3 or np.sum(np.abs(float_data)) < 50:
                        continue
                    result = self.safe_transcribe(float_data)
                    print('result', result)
                    text = result.get("text", "").strip()
                    print('text', text)
                    if text:
                        if WAKE_WORD in text:
                            print("✅ 检测到唤醒词：", WAKE_WORD)
                            if self.on_wakeup:
                                self.on_wakeup()
            except Exception as e:
                print("识别错误：", e)

    def record_phrase(self):
        """ 录制一段话"""
        # 这里也不固定长度，而改成判断2秒静音就结束
        print("🎧 开始录音...")
        buffer = []

        # 用 deque 保存最近静音状态，用于检测连续 2 秒静音
        silence_window = deque(maxlen=int(SAMPLERATE / CHUNK * SILENCE_SECONDS))

        with sd.InputStream(samplerate=SAMPLERATE, channels=CHANNELS, dtype='int16', blocksize=CHUNK) as stream:
            while True:
                data, _ = stream.read(CHUNK)
                float_data = data.astype(np.float32) / 32768.0
                buffer.append(float_data)

                # 计算 RMS
                rms = np.sqrt(np.mean(float_data**2))
                silence_window.append(rms < SILENCE_THRESHOLD)

                # 如果最近连续静音超过 SILENCE_SECONDS
                if len(silence_window) == silence_window.maxlen and all(silence_window):
                    print("⏹ 静音检测到，停止录音")
                    break

        # 拼接所有片段
        audio = np.concatenate(buffer)
        # 转写
        result = self.model.transcribe(audio, fp16=False, language="zh")
        return result["text"].strip()

    def transcribe_file(self, wav_path: str) -> str:
        result = self.model.transcribe(wav_path)
        return result.get("text", "")

    def transcribe_audio_bytes(self, autio_path: str) -> str:
        return self.transcribe_file(autio_path)