import json
from models import Patient, Doctor, Appointment

with open("data.json", "r") as file:
    data = json.load(file)


patients = []

for patient_id, patient_data in data["patients"].items():
    patient = Patient(
        patient_id,
        patient_data["name"],
        patient_data["age"],
        patient_data["city"],
        patient_data["insurance"]
    )

    patients.append(patient)

#print(patients)


doctors = []
for doctor_id, doctor_data in data["doctors"].items():
    doctor = Doctor(
        doctor_id,
        doctor_data["name"],
        doctor_data["specialization"],
        doctor_data["fee"],
        doctor_data["available"]
    )

    doctors.append(doctor)
#print(doctors)

appointments = []

for appointment_data in data["appointments"]:
    appointment = Appointment(
        appointment_data["appointment_id"],
        appointment_data["patient_id"],
        appointment_data["doctor_id"],
        appointment_data["status"],
        appointment_data["tests"]
    )

    appointments.append(appointment)

#print(appointments)

#Error Handling
try:
    with open("data.json", "r") as file:
        data = json.load(file)

except FileNotFoundError:
    print("Error: data.json file not found.")

except json.JSONDecodeError:
    print("Error: Invalid JSON format.")


#Dataclass validation with error handling

def find_patient(patient_id):

    try:
        for patient in patients:
            if patient.patient_id == patient_id:
                return patient
        raise ValueError(f"Patient {patient_id} not found.")

    except ValueError as error:
        print(f"Error: {error}")
        return None

"""print(find_patient("P001"))
print(find_patient("P999"))"""

#Doctor error handling
def find_doctor(doctor_id):

    try:
        for doctor in doctors:
            if doctor.doctor_id == doctor_id:
                return doctor
        raise ValueError (f"Doctor {doctor_id} not found. ")

    except ValueError as error:
        print(f"Error: {error}")
        return None

"""print(find_doctor("D001"))
print(find_doctor("D999"))"""


#Appointment Error Handling
def find_appointment(appointment_id):

    try:
        for appointment in appointments:
            if appointment.appointment_id == appointment_id:
                return appointment

        raise ValueError(f"Appointment {appointment_id} not found.")

    except ValueError:
        return None

"""print(find_appointment("A001"))
print(find_appointment("A999"))"""




#process_appointment()
# Real Appointment Error Handling

# Real Appointment Error Handling

def process_appointment(appointment_id):

    try:
        # 1. Find appointment
        appointment = find_appointment(appointment_id)

        if appointment is None:
            raise ValueError("Appointment does not exist.")

        # 2. Find patient
        patient = find_patient(appointment.patient_id)

        if patient is None:
            raise ValueError("Patient does not exist.")

        # 3. Find doctor
        doctor = find_doctor(appointment.doctor_id)

        if doctor is None:
            raise ValueError("Doctor does not exist.")

        # 4. Check appointment status
        if appointment.status not in ["pending", "completed", "cancelled"]:
            raise ValueError(
                f"Invalid appointment status: {appointment.status}"
            )

        # 5. Check completed appointment
        if appointment.status == "completed":
            raise ValueError("Appointment is already completed.")

        # 6. Check cancelled appointment
        if appointment.status == "cancelled":
            raise ValueError("Cancelled appointment cannot be processed.")

        # 7. Check doctor availability
        if not doctor.available:
            raise ValueError(f"Doctor {doctor.doctor_id} is not available.")

        return True, "Appointment processed successfully."

    except ValueError as error:
        return False, f"Error: {error}"


# Test
print(process_appointment("A001"))
print(process_appointment("A003"))
print(process_appointment("A999"))



# Test invalid patient ID
invalid_patient_appointment = Appointment(
    "A007",
    "P999",
    "D001",
    "pending",
    []
)
appointments.append(invalid_patient_appointment)

print(process_appointment("A007"))


# Test invalid doctor ID
invalid_doctor_appointment = Appointment(
    "A008",
    "P001",
    "D999",
    "pending",
    []
)
appointments.append(invalid_doctor_appointment)

print(process_appointment("A008"))


# Test unavailable doctor

unavailable_doctor = Doctor(
    "D004",
    "Dr. Unavailable",
    "Cardiology",
    5000,
    False
)
doctors.append(unavailable_doctor)

unavailable_doctor_appointment = Appointment(
    "A009",
    "P001",
    "D004",
    "pending",
    []
)
appointments.append(unavailable_doctor_appointment)

print(process_appointment("A009"))