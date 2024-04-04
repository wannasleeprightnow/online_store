from ipaddress import ip_network

print(len(list(filter(lambda x: sum(map(int, list(bin(int(str(x)[-3:]))[2:]))) % 3, ip_network("123.222.111.192/255.255.255.192")))))


# import asyncio

# from database.database import create_db
# from models.user import UserModel
# from models.refresh_session import RefreshSessionModel

# asyncio.run(create_db())
