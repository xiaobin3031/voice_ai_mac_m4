voice_ai_mac_m4/ # 项目根目录
├─ README.md # 本文件
├─ requirements.txt # Python 依赖
├─ install_tools.sh # 推荐的本机工具安装脚本（brew/ollama/piper）
├─ app.py # 主程序：循环式语音对话（终端版）
├─ asr.py # 语音识别模块（Whisper 接口）
├─ llm.py # LLM 调用模块（Ollama 的简单封装）
├─ tts.py # 语音合成模块（Piper 封装）
├─ gradio_app.py # 可选：基于 Gradio 的网页界面（录音 + 播放 + 聊天）
└─ models/ # 放置本地模型（可选）



额外软件
1. ffmpeg