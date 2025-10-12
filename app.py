import wavio
import sounddevice as sd
from asr import ASR
from llm import LocalLLM
from tts import TTS
import asyncio

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

if __name__ == '__main__':
    print("本地语音 AI 聊天(Ctrl+C 退出)")
    while True:
        try:
            input("回车开始说话（或 Ctrl+C 退出")
            path = record_seconds(5, "user.wav")
            text = asr.transcribe_file(path)
            print("识别：", text)
            if not text.strip():
                print("识别为空，重新说一次")
                continue
            reply = llm.ask(text)
            print("AI: ", reply)
            asyncio.run(tts.speak(reply))
        except KeyboardInterrupt:
            print("退出")
            break
        except Exception as e:
            print("错误: ", e)