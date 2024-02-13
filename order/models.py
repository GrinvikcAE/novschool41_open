from datetime import datetime
from pytz import timezone

from sqlalchemy import Column, Integer, String, MetaData, Table, Date

metadata = MetaData()

order = Table(
    'order',
    metadata,
    Column('id', Integer, primary_key=True, index=True),
    Column('last_name', String(50), nullable=False),
    Column('first_name', String(50), nullable=False),
    Column('surname', String(50), nullable=False),
    Column('class_number', String(5), nullable=False),
    Column('email', String(50), nullable=True, default=''),
    Column('birth_date', Date, nullable=False),
    Column('registered_on_utc', Date, default=datetime.utcnow),
    Column('registered_on_now', Date, default=datetime.now(timezone('Asia/Yekaterinburg'))),
)

