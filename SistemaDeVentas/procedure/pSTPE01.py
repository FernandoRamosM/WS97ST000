import libsql_client

class pSTPE01:
    def __init__(self):
        try:
            DATABASE_URL = "libsql://st97per000-st000.turso.io"  
            AUTH_TOKEN = "eyJhbGciOiJFZERTQSIsInR5cCI6IkpXVCJ9.eyJhIjoicnciLCJpYXQiOjE3MzA2NjkxODcsImlkIjoiMmZmNGQ2MmUtYmQ2OC00MzFlLWJkNjYtMTIxNjhkODEyZTUwIn0.w2q-IwU9ElHjGUCTOq5KFgBpGgFannEwPe8vDXV3KfEhOstiXE-oH_JAwjnVfuKGE8tkcghEuC8DRAq-BJtyAA"
            self.conn = libsql_client.create_client_sync(DATABASE_URL, auth_token=AUTH_TOKEN)
        except Exception as e:
            self.conn = None
            return e
    def Conecction(self):
        return self.conn