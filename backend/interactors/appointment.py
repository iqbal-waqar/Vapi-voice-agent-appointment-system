from sqlalchemy.orm import Session
from sqlalchemy import select
import datetime as dt
import logging

from backend.database.database import Appointment
from backend.schemas.appointment import (
    Appointment_Request,
    Appointment_Response,
    CancleAppointment_Request,
    CancleAppointment_Response
)


logger = logging.getLogger(__name__)


def schedule_appointment_logic(request: Appointment_Request, db: Session):

    new_apointment=Appointment(
        patient_name=request.patient_name,
        reason=request.reason,
        start_time=request.start_time
    )

    db.add(new_apointment)
    db.commit()
    db.refresh(new_apointment)

    new_appointment_return_obj=Appointment_Response(
        id=new_apointment.id,
        patient_name=new_apointment.patient_name,
        reason=new_apointment.reason,
        start_time=new_apointment.start_time,
        canceled=new_apointment.canceled,
        created_at=new_apointment.created_at
    )

    return new_appointment_return_obj




def list_appointment_logic(request, db: Session):

    start_dt=dt.datetime.combine(request.date, dt.time.min)
    end_dt=start_dt + dt.timedelta(days=1)

    result=db.execute(
        select(Appointment)
        .where(Appointment.canceled==False)
        .where(Appointment.start_time>=start_dt)
        .where(Appointment.start_time<end_dt)
        .order_by(Appointment.start_time.asc())
    )

    booked_appointments=[]

    for appointment in result:

        appointment_obj=Appointment_Response(
            id=appointment.id,
            patient_name=appointment.patient_name,
            reason=appointment.reason,
            start_time=appointment.start_time,
            canceled=appointment.canceled,
            created_at=appointment.created_at
        )

        appointment_obj.append(booked_appointments)

    return




def cancle_appointment_logic(request: CancleAppointment_Request, db: Session):

    start_dt=dt.datetime.combine(request.date, dt.time.min)
    end_dt=start_dt + dt.timedelta(days=1)

    result=db.execute(
        select(Appointment)
        .where(Appointment.patient_name==request.patient_name)
        .where(Appointment.start_time>=start_dt)
        .where(Appointment.start_time<end_dt)
        .where(Appointment.canceled==False)
    )

    appointments=result.scalars().all()

    if not appointments:

        from fastapi import HTTPException

        raise HTTPException(
            status_code=404,
            detail="No matching appointments for the details found"
        )


    for appointment in appointments:

        appointment.canceled=True


    db.commit()


    return CancleAppointment_Response(
        canceled_count=len(appointments)
    )
