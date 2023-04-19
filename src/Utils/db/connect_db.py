from sqlmodel import SQLModel, create_engine


class ConnectDB():
    def __init__(self, **kwargs):
        self.engine = create_engine("sqlite:///database.db")

    def create_db_and_tables(self):
        SQLModel.metadata.create_all(self.engine)


Connection = ConnectDB()


class ConnectDBTest():
    def __init__(self, **kwargs):
        self.engine = create_engine("sqlite:///testing.db", connect_args={
            "check_same_thread": False
        })
        SQLModel.metadata.create_all(self.engine)
