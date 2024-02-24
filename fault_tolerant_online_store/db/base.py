from sqlalchemy.orm import DeclarativeBase

from fault_tolerant_online_store.db.meta import meta


class Base(DeclarativeBase):
    """Base for all models."""

    metadata = meta
