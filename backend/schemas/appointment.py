import datetime as dt
from pydantic import BaseModel, field_validator
from typing import Union


class Appointment_Request(BaseModel):
    patient_name: str
    reason: str
    start_time: Union[dt.datetime, str]

    @field_validator('start_time', mode='before')
    @classmethod
    def parse_start_time(cls, v):

        if isinstance(v, dt.datetime):
            return v

        if isinstance(v, str):

            try:
                return dt.datetime.fromisoformat(v.replace('Z', '+00:00'))
            except:
                pass

            formats = [
                "%Y-%m-%d %I:%M %p",
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%d %H:%M",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%S.%f",
                "%m/%d/%Y %H:%M",
                "%m/%d/%Y %I:%M %p",
            ]

            for fmt in formats:
                try:
                    return dt.datetime.strptime(v, fmt)
                except:
                    continue

            raise ValueError(f"Unable to parse datetime from: {v}")

        return v


class Appointment_Response(BaseModel):

    id: int
    patient_name: str
    reason: str
    start_time: dt.datetime
    canceled: bool
    created_at: dt.datetime


class CancleAppointment_Request(BaseModel):

    patient_name: str
    date: dt.date


class CancleAppointment_Response(BaseModel):

    canceled_count: int
