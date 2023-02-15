import os
from dotenv import load_dotenv

cwd = os.getcwd()
print(cwd)
dotenv_path = os.path.join(cwd, ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

print('getting dburl')
DATABASE_URL = os.environ.get("SQLALCHEMY_DATABASE_URL")
print('dburl', DATABASE_URL)