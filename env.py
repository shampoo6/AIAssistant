import os
from pathlib import Path
from dotenv import load_dotenv

env = os.getenv("ENV", "development")  # 通过环境变量指定当前环境
print(f'当前环境: {env}')
# 加载顺序：先基础配置，后环境专用配置
load_dotenv()  # 加载 .env
current_env_file = Path(f".env.{env}")
current_env_file = current_env_file if current_env_file.exists() else Path(f"../.env.{env}")
if current_env_file.exists():
    load_dotenv(current_env_file, override=True)  # 覆盖式加载环境专用配置

print(f'ZHIPU_API_KEY: {os.getenv("ZHIPU_API_KEY")}')
print(f'SPARKAI_URL: {os.getenv("SPARKAI_URL")}')
print(f'SPARKAI_APP_ID: {os.getenv("SPARKAI_APP_ID")}')
print(f'SPARKAI_API_SECRET: {os.getenv("SPARKAI_API_SECRET")}')
print(f'SPARKAI_API_KEY: {os.getenv("SPARKAI_API_KEY")}')
print(f'SPARKAI_DOMAIN: {os.getenv("SPARKAI_DOMAIN")}')
