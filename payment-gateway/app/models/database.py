from sqlalchemy import create_engine, Column, String, Numeric, Enum, DateTime,Integer, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship,sessionmaker
import enum
import os
from dotenv import load_dotenv

load_dotenv()


# MySQL connection string
DATABASE_URL = os.getenv("DATABASE_URL","sqlite:///./test.db")

# For MySQL, we need to add pool_recycle and other parameters
engine = create_engine(
    DATABASE_URL,
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True  # Enable connection health checks
)

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

Base = declarative_base()

class TransactionStatus(enum.Enum):
    PENDING = "PENDING"
    SUCCESSFUL = "SUCCESSFUL"
    FAILED = "FAILED"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ref_code = Column(String(36),unique=True, index=True)  # String length for UUID
    payer_account = Column(String(10), nullable=False)
    payee_account = Column(String(10), nullable=False)
    amount = Column(Numeric(19, 4), nullable=False)
    currency = Column(String(3), nullable=False)
    payer_reference = Column(String(255))  # MySQL TEXT would be too large
    status = Column(Enum(TransactionStatus), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    error_message = Column(String(255))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()