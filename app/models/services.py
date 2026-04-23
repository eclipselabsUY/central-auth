from sqlalchemy import Integer, String, DateTime, func, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

from app.core.database import Base


class Service(Base):

    __tablename__ = "services"

    id : Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    service_name : Mapped[str] = mapped_column(String(128), unique=True, nullable=False)

    created_at : Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)

    apikey_id : Mapped[uuid.UUID] = mapped_column(ForeignKey("apikeys.id"), nullable=False, unique=True, index=True)