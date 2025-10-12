import subprocess
import re

model_name = "gpt-oss:20b" # "qwen2:7b" 

class LocalLLM:
    def __init__(self, model_name="phi3"):
        self.model = model_name
    
    def clean_output(self, text: str) -> str:
        # 删除从 "Thinking..." 开始到下一个空行之间的所有内容（跨多行）
        text = re.sub(r"Thinking[\s\S]*?\n\s*\n", "", text)
        # 删除剩下的 "...done thinking." 等痕迹
        text = re.sub(r"\.\.\.done thinking\.*", "", text)
        # 删除类似 "User: ..." 这一类行
        text = re.sub(r"User:[^\n]*\n?", "", text)
        return text.strip()

    def ask(self, prompt: str, timeout: int = 60) -> str:
        cmd = ["ollama", "run", model_name]
        try:
            p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
            if p.returncode == 0:
                return self.clean_output(p.stdout)
            else:
                return f"[LLM ERROR] returncode={p.returncode}: {p.stderr.strip()}"
        except subprocess.TimeoutExpired:
            return "[LLM ERROR] timeout"
