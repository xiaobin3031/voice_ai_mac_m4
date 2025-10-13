import wavio
import sounddevice as sd
from asr import ASR, WAKE_WORD
from llm import LocalLLM
from tts import TTS 
import asyncio
import numpy as np

SAMPLERATE = 16000
CHANNLES = 1

asr = ASR(model_size="small")
llm = LocalLLM(model_name="phi3")
tts = TTS(model_path="models/zh_CN-huayan-medium.onnx", engine="piper")

def record_seconds(seconds=5, out_path="user.wav"):
    print(f"开始录音 {seconds}s... 请说话")
    data = sd.rec(int(SAMPLERATE * seconds), samplerate=SAMPLERATE, channels=CHANNLES, dtype='int16')
    sd.wait()
    wavio.write(out_path, data, SAMPLERATE, sampwidth=2)
    print("录音保存: ", out_path)
    return out_path

def on_wakeup():
    """唤醒后执行完整对话"""
    print("🤖 皮皮：我在呢～ 你想聊什么？")
    text = asr.record_phrase(seconds=6)
    print("你说：", text)
    if not text:
        print("没听清，再试一次")
        return
    reply = llm.ask(text)
    print("AI:", reply)
    asyncio.run(tts.speak(reply))
    print("💤 回到待机模式")

def test():
    print("🎧 可用音频设备列表：")
    print(sd.query_devices())

    # 手动选择设备索引
    DEVICE_INDEX = int(input("请输入麦克风设备索引："))

    SAMPLERATE = 16000
    print("开始录制 2 秒测试音...")
    audio = sd.rec(int(SAMPLERATE * 2), samplerate=SAMPLERATE, channels=1, dtype='float32', device=DEVICE_INDEX)
    sd.wait()

    print("音量范围:", np.min(audio), np.max(audio))
    print("平均能量:", np.mean(np.abs(audio)))

    if np.max(np.abs(audio)) < 0.01:
        print("⚠️ 麦克风输入信号太小，几乎无声！请调整设备或音量。")
    else:
        print("✅ 麦克风正常，可以用于实时识别。")

if __name__ == '__main__':
    """
    print(f"🚀 启动语音助手，唤醒词：‘{WAKE_WORD}’")
    asr.start(on_wakeup)
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("🛑 已退出")
        """
    test()
