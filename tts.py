import os
import edge_tts

g_voice = "zh-CN-XiaoxiaoNeural"  # 中文女声

class TTS:
    def __init__(self, model_path=None, engine="piper"):
        # engine: "piper" 或自定义
        self.engine = engine
        self.model_path = model_path
    
    async def speak(self, text):
        communicate = edge_tts.Communicate(text, g_voice)
        output_file = "output.mp3"
        await communicate.save(output_file)
        os.system(f"afplay {output_file}")