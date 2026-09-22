from dataclasses import dataclass


@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    city: str
    insurance: bool

@dataclass
class Doctor:
    doctor_id: str
    name: str
    specialization: str
    fee: str
    available: bool

@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    status: str
    tests: list


