from datetime import datetime, date

from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, MetaData, Table, Date

metadata = MetaData()

order = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('last_name', String(50), nullable=False),
    Column('first_name', String(50), nullable=False),
    Column('surname', String(50), nullable=False),
    Column('class_number', String(5), nullable=False),
    Column('email', String(50), nullable=False),
    Column('birth_date', Date, nullable=False),
    Column('filename', String(1024), nullable=True),
    Column('is_ready', Boolean, default=False,),
    Column('registered_on', TIMESTAMP, default=datetime.utcnow),
    Column('complete_on', TIMESTAMP, nullable=True),
)
