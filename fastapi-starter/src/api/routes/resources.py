from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.api.schemas.resource import ResourceIn, ResourceOut, ResourceUpdate
from src.infrastructure.db.database import get_session
from src.infrastructure.db.models.resource import Resource

router = APIRouter()


@router.post("/resources/", status_code=status.HTTP_201_CREATED)
def create_resource(
    resource_in: ResourceIn,
    session: Annotated[Session, Depends(get_session)],
) -> ResourceOut:
    resource = Resource(**resource_in.model_dump())

    try:
        session.add(resource)
        session.commit()
        session.refresh(resource)
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Error creating resource") from e

    return ResourceOut.model_validate(resource, from_attributes=True)


@router.get("/resources/", status_code=status.HTTP_200_OK)
def view_resources(
    session: Annotated[Session, Depends(get_session)],
) -> list[ResourceOut]:
    try:
        query = select(Resource)
        results = session.execute(query).scalars().all()
    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error viewing resources") from e

    return [ResourceOut.model_validate(result, from_attributes=True) for result in results]


@router.put("/resources/{resource_id}", status_code=status.HTTP_200_OK)
def update_resource(
    resource_id: int,
    resource_update: ResourceUpdate,
    session: Annotated[Session, Depends(get_session)],
) -> ResourceOut:
    try:
        query = select(Resource).where(Resource.id == resource_id)
        result = session.execute(query).scalar_one_or_none()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")

        update_data = resource_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(result, key, value)

        session.add(result)
        session.commit()
        session.refresh(result)
        return ResourceOut.model_validate(result, from_attributes=True)

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error updating resource") from e


@router.delete("/resources/{resource_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_resource(
    resource_id: int,
    session: Annotated[Session, Depends(get_session)],
) -> None:
    try:
        query = select(Resource).where(Resource.id == resource_id)
        result = session.execute(query).scalar_one_or_none()
        if result:
            session.delete(result)
            session.commit()

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error deleting resource") from e
