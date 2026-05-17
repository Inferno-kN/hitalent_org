from typing import Optional
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.employee import Employee


class Department(Base):
    __tablename__ = 'departments'

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("departments.id", ondelete="CASCADE"),nullable=True)
    employees: Mapped[list["Employee"]] = relationship("Employee", back_populates="department", cascade="all, delete-orphan")

    parent: Mapped[Optional["Department"]] = relationship("Department", back_populates="children", remote_side="Department.id")
    children: Mapped[list["Department"]] = relationship("Department", back_populates="parent")