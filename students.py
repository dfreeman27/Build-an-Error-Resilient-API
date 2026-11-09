

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.exceptions import NotFoundError, DuplicateError
from app.schemas.student import StudentCreate, StudentResponse
from app.models.student import Student
from app.database import get_db

router = APIRouter()


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """
    Creates a student. Raises DuplicateError (not HTTPException) if email taken.
    """
    db_student = Student(**student.model_dump())

    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except IntegrityError:
        db.rollback()
        raise DuplicateError(f"Email {student.email} already registered")
    return db_student


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """
    Gets a student. Raises NotFoundError if not found.

    TODO: raise NotFoundError(f"Student {student_id} not found")
    """
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise NotFoundError(f"Student {student_id} not found")
    return student


@router.delete("/{student_id}")
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """Deletes a student. Raises NotFoundError if not found."""

    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise NotFoundError(f"Student {student_id} not found")
    db.delete(student)
    db.commit()
    return {"message": f"Student {student_id} deleted successfully"}