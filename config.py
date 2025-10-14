import yaml
import os

env = os.getenv("APP_ENV", "dev")
with open(f"config/{env}.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 加载.env文件，然后合并到config中，如果重复 以.env为准
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        env_config = yaml.safe_load(f)
    config.update(env_config)

print('config', config)
print('config[llm]', config['llm'])
print('config[llm][model-name]', config['llm']['model-name'])