import datetime
import motor.motor_asyncio

from pydantic import BaseModel

from utils.connection_util import DB_URL

class AuthIn(BaseModel):
    username: str
    password: str

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.simpenan
collection = database.users

async def fetch_user_by_username(username):
    document = await collection.find_one({ "username": username })
    return document

async def put_lastlog_user(username):
    readable_date = datetime.datetime.today().strftime("%d %B, %Y %H:%M:%S")
    await collection.update_one(
        { "username": username }, 
        { 
            "$set": {"lastlog": datetime.datetime.today() } 
        }
    )
    result = await collection.find_one({ "username": username })
    if result :
        return f"User {username} telah login pada {readable_date}"
    return 0