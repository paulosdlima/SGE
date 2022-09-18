import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://root:root@mongo:27017/?retryWrites=true&w=majority')

database = client.sge
