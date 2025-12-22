"""
环境配置类
"""
import os
from pathlib import Path
from dotenv import load_dotenv

############################
# ROOT PATH
#########################
ROOT_PATH = Path(__file__).resolve().parent


###########################
# Load .env file
############################

ENV_FILE_PATH = ROOT_PATH / ".env"
load_dotenv(dotenv_path=ENV_FILE_PATH)

ENV_EXIST = os.getenv("ENV_FILE")

if ENV_EXIST:
    print("环境变量加载成功")
else:
    print("环境变量加载失败")

#############
# DATA_DIR
############

DATA_DIR = ROOT_PATH / "data"

#####################
# Log Path
#####################

LOG_DIR = ROOT_PATH / "data/logs"

###############################
# 数据库配置
###############################
DB_TYPE = os.environ.get("DB_TYPE", "sqlite")
DATABASE_HOST = os.environ.get("DATABASE_HOST", "localhost")
DATABASE_USER = os.environ.get("DATABASE_USER", "fwy")
DATABASE_PASSWORD = os.environ.get("DATABASE_PASSWORD", "Abcd1234.")
DATABASE_NAME = os.environ.get("DATABASE_NAME", "tender_data")

############################
# 权限验证base_url
############################
PORT = os.environ.get("PORT", "8085")
AUTHZ_BASE_URL = f"http://localhost:{str(PORT)}"
