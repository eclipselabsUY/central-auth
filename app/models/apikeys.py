from sqlalchemy import String, DateTime, Boolean, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import Base


class ApiKey(Base):
    
    __tablename__ = "apikeys"

    id : Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    service_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("services.id"), nullable=False, unique=True, index=True)

    key_hash : Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    salt : Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)

    is_active : Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
