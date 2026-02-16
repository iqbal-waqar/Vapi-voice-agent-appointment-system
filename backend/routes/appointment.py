from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
import logging

from backend.database.database import get_db
from backend.schemas.appointment import (
    Appointment_Request,
    CancleAppointment_Request
)

from backend.interactors.appointment import (
    schedule_appointment_logic,
    list_appointment_logic,
    cancle_appointment_logic
)


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/schedule_appointment")
def schedule_appointment(request: Appointment_Request, db: Session=Depends(get_db)):

    logger.info(f"Received appointment request")

    return schedule_appointment_logic(request, db)




@router.post("/list_appointment")
def list_appointment(request: Appointment_Request, db: Session=Depends(get_db)):

    return list_appointment_logic(request, db)




@router.post("/cancle_appointment")
def cancle_appointment(request: CancleAppointment_Request, db: Session=Depends(get_db)):

    return cancle_appointment_logic(request, db)
