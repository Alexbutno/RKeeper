import uuid
from sqlalchemy import String, Column, Table, MetaData, Boolean, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
    Column("email", String(length=320), index=True, nullable=False),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("account_created", String(length=100), nullable=False)
)


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String(length=320), index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    account_created = Column(String(length=100), nullable=False)


nonvalid_user_table = Table(
    "nonvalid_users",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False),
    Column("email", String(length=320), index=True, nullable=False),
    Column("hashed_password", String(length=1024), nullable=False),
    Column("token_expires_at", Integer(), nullable=False),
    Column("token_hashed_value", String(length=1024), nullable=False)
)


class NonvalidUser(Base):
    __tablename__ = "nonvalid_users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    email = Column(String(length=320), index=True, nullable=False)
    hashed_password = Column(String(length=1024), nullable=False)
    token_expires_at = Column(Integer(), nullable=False)
    token_hashed_value = Column(String(length=1024), nullable=False)

