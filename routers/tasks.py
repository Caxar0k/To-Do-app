from typing import Annotated
from authx import TokenPayload
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_session
from models import TaskModel 
from schemas import TaskAddSchema 
from config import security 



router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"],
)


SessionDep = Annotated[AsyncSession, Depends(get_session)]



@router.post(
    "",
    summary="Create task",
    status_code = status.HTTP_201_CREATED,
)
async def create_task(
    data: TaskAddSchema,
    session: SessionDep,
    token: TokenPayload = Depends(security.access_token_required),

):

    new_task = TaskModel(
        title=data.title,
        description=data.description,
        completed=data.completed,
        user_id = token.sub
    )

    session.add(new_task)
    await session.commit()

    return {
        "success": True,
        "message": "Task creation successful",
        "task_id": new_task.id
    }


@router.get(
    "",
    summary="Geting all tasks",
)
async def get_tasks(
    session: SessionDep,
    token :  TokenPayload = Depends(security.access_token_required),
):
    query = select(TaskModel).where(TaskModel.user_id == token.sub)
    result = await session.execute(query)

    return {
        "success": True,
        "message": "Geting all tasks successful",
        "Tasks": result.scalars().all()
        }
    


@router.get(
    "/{task_id}",
    summary="Geting tasks by id",
    
)
async def get_task(
    task_id: int,
    session: SessionDep,
    token :  TokenPayload = Depends(security.access_token_required),
):
    query = select(TaskModel).where(TaskModel.id == task_id , TaskModel.user_id == token.sub)

    result = await session.execute(query)
    task_db = result.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task by this id",
        )

    return {
        "success": True,
        "message": "Geting tasks by id successful",
        "Task_by_id": task_db
        }


@router.put(
    "/{task_id}",
    summary="Editing tasks by id",
)
async def put_task(
    task_id: int,
    task: TaskAddSchema,
    session: SessionDep,
    token :  TokenPayload = Depends(security.access_token_required),
):
    query = select(TaskModel).where(TaskModel.id == task_id , TaskModel.user_id == token.sub)

    result = await session.execute(query)
    task_db = result.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task by this id",
        )

    task_db.title = task.title
    task_db.description = task.description
    task_db.completed = task.completed

    await session.commit()

    return {
        "success": True,
        "message": "Task editing successful",
    }


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete tasks by id",
)
async def delete_task(
    task_id: int,
    session: SessionDep,
    token :  TokenPayload = Depends(security.access_token_required),
):
    query = select(TaskModel).where(TaskModel.id == task_id , TaskModel.user_id == token.sub)

    result = await session.execute(query)
    task_db = result.scalar_one_or_none()

    if task_db is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No task by this id",
        )

    await session.delete(task_db)
    await session.commit()

