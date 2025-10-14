import os
import edge_tts
import asyncio
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO

g_voice = "zh-CN-XiaoxiaoNeural"  # 中文女声

class TTS:
    def __init__(self, model_path="models/zh_CN-huayan-medium.onnx", engine="piper"):
        # engine: "piper" 或自定义
        self.engine = engine
        self.model_path = model_path
    
    def speak(self, text):
        asyncio.run(self.__inner_speak(text))

    async def __inner_speak(self, text):
        print(f"播放: {text}")
        communicate = edge_tts.Communicate(text, g_voice)
        audio_stream = BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_stream.write(chunk["data"])

        audio_stream.seek(0)
        sound = AudioSegment.from_file(audio_stream, format="mp3")
        play(sound)