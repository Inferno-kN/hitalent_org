from sqlalchemy.ext.asyncio import AsyncSession
from app.models.employee import Employee
from app.models.department import Department
from app.schemas.employee import EmployeeCreate
from app.core.exceptions import NotFoundError


class EmployeeService:

    @staticmethod
    async def create(session: AsyncSession, department_id: int, data: EmployeeCreate):
        department = await session.get(Department, department_id)
        if not department:
            raise NotFoundError
        employee = Employee(department_id=department_id, full_name=data.full_name, position=data.position, hired_at=data.hired_at)
        session.add(employee)
        await session.commit()
        await session.refresh(employee)
        return employee