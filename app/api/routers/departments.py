from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.core.database import get_session
from app.services.department_service import DepartmentService
from app.services.employee_service import EmployeeService
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentTree, DepartmentResponse
from app.schemas.employee import EmployeeCreate


router = APIRouter(prefix='/departments', tags=['Departments'])


@router.post('/', response_model=DepartmentResponse, status_code=status.HTTP_201_CREATED, summary='создать подразделение')
async def create_departments(data: DepartmentCreate, session: AsyncSession = Depends(get_session)):
    service = DepartmentService()
    return await service.create(session, data)


@router.post('/{department_id}/employees', summary='создать сотрудника в подразделении')
async def create_employee(data: EmployeeCreate, department_id: int, session: AsyncSession = Depends(get_session)):
    service = EmployeeService()
    return await service.create(session, department_id, data)


@router.get('/{department_id}', response_model=DepartmentTree, summary='получить подразделение в виде дерева')
async def get_department_tree(department_id: int, depth: int = Query(1, ge=1, le=5), include_employees: bool = Query(True), session: AsyncSession = Depends(get_session)):
    service = DepartmentService()
    return await service.get_tree(session, department_id, depth, include_employees)


@router.patch("/{department_id}", response_model=DepartmentResponse, summary="обновить подразделение")
async def update_department(data: DepartmentUpdate, department_id: int, session: AsyncSession = Depends(get_session)):
    service = DepartmentService()
    return await service.update(session, data, department_id)


@router.delete("/{department_id}", summary='удалить подразделение')
async def delete_department(department_id: int, mode: str, reassign_to_department_id: Optional[int] = Query(None), session: AsyncSession = Depends(get_session)):
    service = DepartmentService()
    return await service.delete(session, department_id, mode, reassign_to_department_id)