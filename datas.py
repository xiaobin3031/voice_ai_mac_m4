import json
import os

class Datas:
    """数据处理类"""

    def __init__(self, filename):
        self.filename = os.path.join('data', filename)

    def store(self, data):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {}