from app.schemas.department import DepartmentTree
from app.schemas.employee import EmployeeResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from sqlalchemy import update
from app.models import Employee
from app.models.department import Department
from app.schemas.department import DepartmentCreate, DepartmentUpdate
from app.core.exceptions import NotFoundError, ConflictError, ValidationError


class DepartmentService:

    @staticmethod
    async def _check_name_uniqueness(session: AsyncSession, name: str, parent_id: Optional[int], exclude_id: Optional[int] = None):
        query = select(Department).where(Department.name == name, Department.parent_id == parent_id)
        if exclude_id is not None:
            query = query.where(Department.id != exclude_id)

        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            raise ConflictError(f"Department with name '{name}' already exists under parent {parent_id}")


    @staticmethod
    async def _check_cycle(session: AsyncSession, department_id: int, new_parent_id: int):
        if department_id == new_parent_id:
            raise ValidationError
        current_id = new_parent_id
        while current_id is not None:
            if current_id == department_id:
                raise ConflictError
            parent = await session.get(Department, current_id)
            if parent:
                current_id = parent.parent_id
            else:
                return None


    @staticmethod
    async def create(session: AsyncSession, data: DepartmentCreate):
        await DepartmentService._check_name_uniqueness(session, data.name, data.parent_id)
        if data.parent_id is not None:
            parent = await session.get(Department, data.parent_id)
            if parent is None:
                raise NotFoundError

        department = Department(name=data.name, parent_id=data.parent_id)
        session.add(department)
        await session.commit()
        await session.refresh(department)
        return department

    @staticmethod
    async def update(session: AsyncSession, data: DepartmentUpdate, department_id: int):
        department = await session.get(Department, department_id)
        if not department:
            raise NotFoundError(f"Department with id {department_id} not found")

        if data.name is not None:
            await DepartmentService._check_name_uniqueness(session, data.name, department.parent_id, exclude_id=department_id)
            department.name = data.name

        if data.parent_id is not None:
            await DepartmentService._check_cycle(session, department_id, data.parent_id)

            new_parent = await session.get(Department, data.parent_id)
            if not new_parent:
                raise NotFoundError(f"Parent department with id {data.parent_id} not found")

            department.parent_id = data.parent_id

        await session.commit()
        await session.refresh(department)
        return department


    @staticmethod
    async def delete(session: AsyncSession, department_id: int, mode: str, reassign_to: Optional[int] = None):
        department = await session.get(Department, department_id)
        if not department:
            raise NotFoundError
        if mode == "cascade":
            await session.delete(department)
        elif mode == "reassign":
            if reassign_to is None:
                raise ValidationError
            target_dept = await session.get(Department, reassign_to)
            if not target_dept:
                raise NotFoundError
            await session.execute(update(Employee).where(Employee.department_id == department_id).values(department_id=reassign_to))
            await session.execute(update(Department).where(Department.parent_id == department_id).values(parent_id=reassign_to))
            await session.delete(department)
        else:
            raise ValidationError
        await session.commit()


    @staticmethod
    async def get_tree(session: AsyncSession, department_id: int, depth: int = 1, max_depth: int = 5, include_employees: bool = True):
        department = await session.get(Department, department_id)
        if not department:
            raise NotFoundError
        list_employees = []
        if include_employees:
            result = await session.execute(select(Employee).where(Employee.department_id == department_id).order_by(Employee.created_at))
            list_employees = result.scalars().all()
        list_children = []
        if depth < max_depth:
            result = await session.execute(select(Department).where(Department.parent_id == department_id))
            childrens = result.scalars().all()
            for child in childrens:
                child_tree = await DepartmentService.get_tree(
                    session, child.id, depth + 1, max_depth, include_employees
                )
                list_children.append(child_tree)
        return DepartmentTree(id=department.id, name=department.name, parent_id=department.parent_id, created_at=department.created_at, employees=[EmployeeResponse.model_validate(emp) for emp in list_employees],children=list_children)