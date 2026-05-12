from config.env import config
import json

print(json.dumps(config, indent=2, ensure_ascii=False))
print(f"\n用户数量：{len(config['user'])}")