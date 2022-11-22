from database.database import Database
from dotenv import load_dotenv
import os

load_dotenv()

db = Database(user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'), host=os.getenv('DB_HOST'), database=os.getenv('DB_NAME'))
