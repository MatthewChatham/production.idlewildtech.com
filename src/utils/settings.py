import os
from dotenv import load_dotenv

cwd = os.getcwd()
dotenv_path = os.path.join(cwd, ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")
