from datetime import date
from typing import Optional
from sqlalchemy import String, Integer, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.department import Department


class Employee(Base):
    __tablename__ = 'employees'

    department_id: Mapped[int] = mapped_column(Integer, ForeignKey("departments.id", ondelete='CASCADE'))
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    position: Mapped[str] = mapped_column(String(255), nullable=False)
    hired_at: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    department: Mapped["Department"] = relationship("Department", back_populates="employees")
