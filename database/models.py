from sqlalchemy import Table, Column, Integer, String, MetaData, BigInteger, Date

metadata_obj = MetaData()

# Таблица с клиентами
requests_table = Table(
    "users",
    metadata_obj,
    Column("id", BigInteger, primary_key=True),
    Column("id_user", Integer),
    Column("command_bot", String),
    Column("date_time", Date),
    Column("message_bot", String),
)
