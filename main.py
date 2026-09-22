import json

from models import Patient, Doctor, Appointment


# ============================================================
# 1. LOAD DATA FROM JSON
# ============================================================

try:
    # data.json file ko read mode mein open kar rahe hain
    with open("data.json", "r") as file:
        data = json.load(file)

except FileNotFoundError:
    print("Error: data.json file not found.")
    data = {
        "patients": {},
        "doctors": {},
        "appointments": []
    }

except json.JSONDecodeError:
    print("Error: Invalid JSON format.")
    data = {
        "patients": {},
        "doctors": {},
        "appointments": []
    }


# ============================================================
# 2. CONVERT JSON DATA INTO DATACLASS OBJECTS
# ============================================================

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


# ============================================================
# 3. CLINIC CONFIGURATION
# ============================================================

# Test charges
test_prices = {
    "ECG": 1000,
    "Blood Test": 1500,
    "X-Ray": 2000
}


# Clinic configuration
clinic_config = {
    "currency": "$",
    "tax": 0.0,
    "senior_discount": 0.10
}


# ============================================================
# 4. FIND PATIENT
# ============================================================

def find_patient(patient_id):

    try:

        for patient in patients:

            if patient.patient_id == patient_id:
                return patient

        raise ValueError(
            f"Patient {patient_id} not found."
        )

    except ValueError as error:

        print(f"Error: {error}")
        return None


# ============================================================
# 5. FIND DOCTOR
# ============================================================

def find_doctor(doctor_id):

    try:

        for doctor in doctors:

            if doctor.doctor_id == doctor_id:
                return doctor

        raise ValueError(
            f"Doctor {doctor_id} not found."
        )

    except ValueError as error:

        print(f"Error: {error}")
        return None


# ============================================================
# 6. FIND APPOINTMENT
# ============================================================

def find_appointment(appointment_id):

    try:

        for appointment in appointments:

            if appointment.appointment_id == appointment_id:
                return appointment

        raise ValueError(
            f"Appointment {appointment_id} not found."
        )

    except ValueError:

        return None


# ============================================================
# 7. VALIDATE PATIENT
# ============================================================

def validate_patient(patient_id):

    patient = find_patient(patient_id)

    if patient is None:
        return False, f"Patient {patient_id} does not exist."

    return True, "Patient is valid."


# ============================================================
# 8. VALIDATE DOCTOR
# ============================================================

def validate_doctor(doctor_id):

    doctor = find_doctor(doctor_id)

    if doctor is None:
        return False, f"Doctor {doctor_id} does not exist."

    if not doctor.available:
        return False, f"Doctor {doctor_id} is not available."

    return True, "Doctor is valid."


# ============================================================
# 9. VALIDATE TESTS
# ============================================================

def validate_tests(tests):

    try:

        seen_tests = set()

        for test in tests:

            # Check whether test exists
            if test not in test_prices:
                raise ValueError(
                    f"Invalid test: {test}"
                )

            # Check duplicate tests
            if test in seen_tests:
                raise ValueError(
                    f"Duplicate test: {test}"
                )

            seen_tests.add(test)

        return True, "All tests are valid."

    except ValueError as error:

        return False, str(error)


# ============================================================
# 10. VALIDATE AGE
# ============================================================

def validate_age(age):

    if age < 0:
        return False, "Age cannot be negative."

    if age > 120:
        return False, "Invalid age."

    return True, "Age is valid."


# ============================================================
# 11. PROCESS APPOINTMENT
# ============================================================

def process_appointment(appointment_id):

    try:

        # Find appointment
        appointment = find_appointment(appointment_id)

        if appointment is None:
            raise ValueError(
                "Appointment does not exist."
            )

        # Find patient
        patient = find_patient(
            appointment.patient_id
        )

        if patient is None:
            raise ValueError(
                "Patient does not exist."
            )

        # Find doctor
        doctor = find_doctor(
            appointment.doctor_id
        )

        if doctor is None:
            raise ValueError(
                "Doctor does not exist."
            )

        # Validate appointment status
        if appointment.status not in [
            "pending",
            "completed",
            "cancelled"
        ]:
            raise ValueError(
                f"Invalid appointment status: "
                f"{appointment.status}"
            )

        # Completed appointment cannot be processed again
        if appointment.status == "completed":
            raise ValueError(
                "Appointment is already completed."
            )

        # Cancelled appointment cannot be processed
        if appointment.status == "cancelled":
            raise ValueError(
                "Cancelled appointment cannot be processed."
            )

        # Doctor must be available
        if not doctor.available:
            raise ValueError(
                f"Doctor {doctor.doctor_id} is not available."
            )

        # ----------------------------------------------------
        # IMPORTANT:
        # After successful processing, change status to
        # completed. This prevents processing the same
        # appointment twice.
        # ----------------------------------------------------

        appointment.status = "completed"

        return True, "Appointment processed successfully."

    except ValueError as error:

        return False, f"Error: {error}"


# ============================================================
# 12. CALCULATE TEST CHARGES
# ============================================================

def calculate_test_charges(tests):

    total = 0

    for test in tests:

        if test in test_prices:
            total += test_prices[test]

    return total


# ============================================================
# 13. CALCULATE SUBTOTAL
# ============================================================

def calculate_subtotal(
    consultation_fee,
    test_charges
):

    return consultation_fee + test_charges


# ============================================================
# 14. CALCULATE INSURANCE COVERAGE
# ============================================================

def calculate_insurance_coverage(
    consultation_fee,
    test_charges,
    insurance
):

    if not insurance:
        return 0

    # Insurance covers:
    # 20% of consultation fee
    # 50% of test charges

    consultation_coverage = (
        consultation_fee * 0.20
    )

    test_coverage = (
        test_charges * 0.50
    )

    return consultation_coverage + test_coverage


# ============================================================
# 15. CALCULATE PATIENT RESPONSIBILITY
# ============================================================

def calculate_patient_responsibility(
    subtotal,
    insurance_coverage
):

    return subtotal - insurance_coverage


# ============================================================
# 16. CALCULATE COMPLETE BILL
# ============================================================

def calculate_bill(
    consultation_fee,
    tests,
    insurance
):

    # Calculate test charges
    test_charges = calculate_test_charges(tests)

    # Calculate subtotal
    subtotal = calculate_subtotal(
        consultation_fee,
        test_charges
    )

    # Calculate insurance coverage
    insurance_coverage = calculate_insurance_coverage(
        consultation_fee,
        test_charges,
        insurance
    )

    # Calculate final patient amount
    patient_amount = calculate_patient_responsibility(
        subtotal,
        insurance_coverage
    )

    return {
        "Consultation_fee": consultation_fee,
        "test_charges": test_charges,
        "subtotal": subtotal,
        "insurance_coverage": insurance_coverage,
        "patient_amount": patient_amount
    }


# ============================================================
# 17. SENIOR CITIZEN DISCOUNT
# ============================================================

def apply_senior_discount(
    amount,
    age
):

    if age >= 60:

        discount = (
            amount
            * clinic_config["senior_discount"]
        )

        final_amount = amount - discount

        return discount, final_amount

    return 0, amount


# ============================================================
# 18. CANCEL APPOINTMENT
# ============================================================

def cancel_appointment(appointment_id):

    try:

        # Find appointment
        appointment = find_appointment(
            appointment_id
        )

        if appointment is None:
            raise ValueError(
                f"Appointment {appointment_id} does not exist."
            )

        # Get current status
        status = appointment.status

        # Completed appointment cannot be cancelled
        if status == "completed":
            raise ValueError(
                "Completed appointment cannot be cancelled."
            )

        # Already cancelled appointment
        if status == "cancelled":
            raise ValueError(
                "Appointment is already cancelled."
            )

        # Only pending appointment can be cancelled
        if status == "pending":

            appointment.status = "cancelled"

            return True, "Appointment cancelled successfully."

        # Invalid status
        raise ValueError(
            f"Invalid appointment status: {status}"
        )

    except ValueError as error:

        return False, str(error)


# ============================================================
# 19. DOCTOR STATISTICS
# ============================================================

def doctor_statistics():

    statistics = {}

    for appointment in appointments:

        if appointment.status == "cancelled":
            continue

        doctor = find_doctor(
            appointment.doctor_id
        )

        if doctor is None:
            continue

        specialization = doctor.specialization

        if specialization not in statistics:
            statistics[specialization] = 0

        statistics[specialization] += 1

    if not statistics:
        return []

    max_count = max(
        statistics.values()
    )

    return [
        specialization
        for specialization, count
        in statistics.items()
        if count == max_count
    ]


# ============================================================
# 20. PATIENT BILL REPORT
# ============================================================

def patient_bill_report(patient_id):

    patient = find_patient(patient_id)

    if patient is None:
        return None

    total_bill = 0

    for appointment in appointments:

        if (
            appointment.patient_id == patient_id
            and appointment.status == "completed"
        ):

            doctor = find_doctor(
                appointment.doctor_id
            )

            if doctor is None:
                continue

            bill = calculate_bill(
                doctor.fee,
                appointment.tests,
                patient.insurance
            )

            amount = bill["patient_amount"]

            # Apply senior discount
            _, final_amount = apply_senior_discount(
                amount,
                patient.age
            )

            total_bill += final_amount

    return total_bill


# ============================================================
# 21. HIGHEST SPENDING PATIENT
# ============================================================

def highest_spending_patient():

    patient_bills = {}

    for patient in patients:

        total = patient_bill_report(
            patient.patient_id
        )

        patient_bills[
            patient.patient_id
        ] = total

    if not patient_bills:
        return []

    highest_amount = max(
        patient_bills.values()
    )

    return [
        patient_id
        for patient_id, amount
        in patient_bills.items()
        if amount == highest_amount
    ]


# ============================================================
# 22. CLINIC DASHBOARD
# ============================================================

def clinic_dashboard():

    print("\n========================================")
    print("           CLINIC DASHBOARD")
    print("========================================")

    # Basic counts
    print(
        f"Total Patients: {len(patients)}"
    )

    print(
        f"Total Doctors: {len(doctors)}"
    )

    print(
        f"Total Appointments: {len(appointments)}"
    )

    # Appointment status counts
    completed = sum(
        1
        for appointment in appointments
        if appointment.status == "completed"
    )

    cancelled = sum(
        1
        for appointment in appointments
        if appointment.status == "cancelled"
    )

    pending = sum(
        1
        for appointment in appointments
        if appointment.status == "pending"
    )

    print(f"Completed: {completed}")
    print(f"Cancelled: {cancelled}")
    print(f"Pending: {pending}")

    # Revenue calculations
    consultation_revenue = 0
    test_revenue = 0
    insurance_revenue = 0
    patient_revenue = 0

    for appointment in appointments:

        if appointment.status != "completed":
            continue

        patient = find_patient(
            appointment.patient_id
        )

        doctor = find_doctor(
            appointment.doctor_id
        )

        if patient is None or doctor is None:
            continue

        bill = calculate_bill(
            doctor.fee,
            appointment.tests,
            patient.insurance
        )

        consultation_revenue += doctor.fee

        test_revenue += bill["test_charges"]

        insurance_revenue += (
            bill["insurance_coverage"]
        )

        patient_revenue += (
            bill["patient_amount"]
        )

    print(
        f"Total Consultation Revenue: "
        f"$ {consultation_revenue}"
    )

    print(
        f"Total Test Revenue: "
        f"$ {test_revenue}"
    )

    print(
        f"Total Insurance Coverage: "
        f"$ {insurance_revenue}"
    )

    print(
        f"Total Patient Revenue: "
        f"$ {patient_revenue}"
    )

    # Most requested specialization
    print(
        "Most Requested Specialization:",
        doctor_statistics()
    )

    # Highest spending patient
    print(
        "Highest Spending Patient:",
        highest_spending_patient()
    )

    print("========================================")


# ============================================================
# 23. *ARGS EXAMPLE
# ============================================================

def calculate_total_charges(*charges):

    # *args allows multiple charges
    # to be passed into one function.

    return sum(charges)


# ============================================================
# 24. **KWARGS EXAMPLE
# ============================================================

def calculate_configurable_bill(
    amount,
    **options
):

    # **kwargs allows optional configuration.

    tax = options.get("tax", 0)

    discount = options.get(
        "discount",
        0
    )

    tax_amount = amount * tax

    discount_amount = amount * discount

    return (
        amount
        + tax_amount
        - discount_amount
    )


# ============================================================
# 25. LAMBDA EXAMPLE
# ============================================================

def sort_patients_by_bill():

    patient_bills = []

    for patient in patients:

        total = patient_bill_report(
            patient.patient_id
        )

        patient_bills.append(
            (
                patient.patient_id,
                total
            )
        )

    # Lambda is used as the sorting key.
    patient_bills.sort(
        key=lambda item: item[1],
        reverse=True
    )

    return patient_bills


# ============================================================
# 26. COMPREHENSIONS
# ============================================================

def get_senior_patients():

    return [
        patient.patient_id
        for patient in patients
        if patient.age >= 60
    ]


def get_insured_patients():

    return [
        patient.patient_id
        for patient in patients
        if patient.insurance
    ]


# ============================================================
# 27. LEGB EXAMPLE
# ============================================================

clinic_name = "City Hospital"


def show_clinic_name():

    # This demonstrates the LEGB rule.
    # Python first checks Local,
    # then Enclosing,
    # then Global,
    # then Built-in.

    return clinic_name


# ============================================================
# 28. EDGE CASE TESTING
# ============================================================

def run_edge_case_tests():

    print("\n========================================")
    print("           EDGE CASE TESTING")
    print("========================================")

    # --------------------------------------------------------
    # 1. Invalid Patient ID
    # --------------------------------------------------------

    print("\n1. Invalid Patient ID:")

    result = validate_patient("P999")

    print(result)


    # --------------------------------------------------------
    # 2. Invalid Doctor ID
    # --------------------------------------------------------

    print("\n2. Invalid Doctor ID:")

    result = validate_doctor("D999")

    print(result)


    # --------------------------------------------------------
    # 3. Invalid Appointment ID
    # --------------------------------------------------------

    print("\n3. Invalid Appointment ID:")

    appointment = find_appointment("A999")

    if appointment is None:
        print(
            "False",
            "Appointment A999 does not exist."
        )


    # --------------------------------------------------------
    # 4. Doctor Unavailable
    # --------------------------------------------------------

    print("\n4. Doctor Unavailable:")

    # Temporarily make D003 unavailable.
    doctor = find_doctor("D003")

    original_status = doctor.available

    doctor.available = False

    result = validate_doctor("D003")

    print(result)

    # Restore original status.
    doctor.available = original_status


    # --------------------------------------------------------
    # 5. Invalid Test
    # --------------------------------------------------------

    print("\n5. Invalid Test:")

    result = validate_tests(
        ["CT Scan"]
    )

    print(result)


    # --------------------------------------------------------
    # 6. Duplicate Test
    # --------------------------------------------------------

    print("\n6. Duplicate Test:")

    result = validate_tests(
        ["ECG", "ECG"]
    )

    print(result)


    # --------------------------------------------------------
    # 7. Empty Test List
    # --------------------------------------------------------

    print("\n7. Empty Test List:")

    result = validate_tests([])

    print(result)


    # --------------------------------------------------------
    # 8. Negative Age
    # --------------------------------------------------------

    print("\n8. Negative Age:")

    result = validate_age(-5)

    print(result)


    # --------------------------------------------------------
    # 9. Invalid Appointment Status
    # --------------------------------------------------------

    print("\n9. Invalid Appointment Status:")

    # Create temporary appointment.
    test_appointment = Appointment(
        "TEST_STATUS",
        "P001",
        "D001",
        "wrong",
        []
    )

    appointments.append(test_appointment)

    result = process_appointment(
        "TEST_STATUS"
    )

    print(result)

    appointments.remove(
        test_appointment
    )


    # --------------------------------------------------------
    # 10. Cancel Completed Appointment
    # --------------------------------------------------------

    print("\n10. Cancel Completed Appointment:")

    result = cancel_appointment("A001")

    print(result)


    # --------------------------------------------------------
    # 11. Process Cancelled Appointment
    # --------------------------------------------------------

    print("\n11. Process Cancelled Appointment:")

    result = process_appointment("A003")

    print(result)


    # --------------------------------------------------------
    # 12. Process Same Appointment Twice
    # --------------------------------------------------------

    print("\n12. Process Same Appointment Twice:")

    # A temporary pending appointment is created.
    # We do NOT change data.json.

    test_appointment = Appointment(
        "TEST001",
        "P001",
        "D001",
        "pending",
        []
    )

    appointments.append(
        test_appointment
    )

    # First processing should succeed.
    print(
        process_appointment("TEST001")
    )

    # Second processing should fail because
    # the appointment is now completed.
    print(
        process_appointment("TEST001")
    )

    # Remove temporary appointment.
    appointments.remove(
        test_appointment
    )


    # --------------------------------------------------------
    # 13. Patient With No Appointments
    # --------------------------------------------------------

    print("\n13. Patient With No Appointments:")

    # Temporary patient
    test_patient = Patient(
        "TEST_P",
        "Test Patient",
        30,
        "Lahore",
        False
    )

    patients.append(
        test_patient
    )

    result = [
        appointment.appointment_id
        for appointment in appointments
        if appointment.patient_id == "TEST_P"
    ]

    print(result)

    # Remove temporary patient.
    patients.remove(
        test_patient
    )


    # --------------------------------------------------------
    # 14. Doctor With No Appointments
    # --------------------------------------------------------

    print("\n14. Doctor With No Appointments:")

    # Temporary doctor
    test_doctor = Doctor(
        "TEST_D",
        "Dr. Test",
        "General",
        1000,
        True
    )

    doctors.append(
        test_doctor
    )

    result = [
        appointment.appointment_id
        for appointment in appointments
        if appointment.doctor_id == "TEST_D"
    ]

    print(result)

    # Remove temporary doctor.
    doctors.remove(
        test_doctor
    )


    # --------------------------------------------------------
    # 15. Empty Data Handling
    # --------------------------------------------------------

    print("\n15. Empty Data Handling:")

    empty_patients = []
    empty_doctors = []
    empty_appointments = []

    print(
        "Empty Patients:",
        len(empty_patients)
    )

    print(
        "Empty Doctors:",
        len(empty_doctors)
    )

    print(
        "Empty Appointments:",
        len(empty_appointments)
    )

    print("\n========================================")


# ============================================================
# 29. MAIN FUNCTION
# ============================================================

def main():

    print("========================================")
    print("     HOSPITAL APPOINTMENT & BILLING")
    print("========================================")

    # Basic data counts
    print(
        f"\nTotal Patients: {len(patients)}"
    )

    print(
        f"Total Doctors: {len(doctors)}"
    )

    print(
        f"Total Appointments: {len(appointments)}"
    )


    # --------------------------------------------------------
    # Sample Bill
    # --------------------------------------------------------

    print("\nSample Bill:")

    sample_bill = calculate_bill(
        5000,
        ["ECG", "Blood Test"],
        True
    )

    print(sample_bill)


    # --------------------------------------------------------
    # Senior Discount
    # --------------------------------------------------------

    senior_discount, final_amount = (
        apply_senior_discount(
            5000,
            67
        )
    )

    print(
        f"\nSenior Discount: {senior_discount}"
    )

    print(
        f"Final Amount: {final_amount}"
    )


    # --------------------------------------------------------
    # Clinic Dashboard
    # --------------------------------------------------------

    clinic_dashboard()


    # --------------------------------------------------------
    # *ARGS
    # --------------------------------------------------------

    total_charges = calculate_total_charges(
        5000,
        1500,
        1000
    )

    print(
        f"\nTotal Charges: {total_charges}"
    )


    # --------------------------------------------------------
    # **KWARGS
    # --------------------------------------------------------

    configurable_bill = (
        calculate_configurable_bill(
            5200,
            tax=0.0,
            discount=0.0
        )
    )

    print(
        f"Configurable Bill: {configurable_bill}"
    )


    # --------------------------------------------------------
    # Lambda
    # --------------------------------------------------------

    print(
        "Patients Sorted By Bill:",
        sort_patients_by_bill()
    )


    # --------------------------------------------------------
    # Comprehensions
    # --------------------------------------------------------

    print(
        "Senior Patients:",
        get_senior_patients()
    )

    print(
        "Insured Patients:",
        get_insured_patients()
    )


    # --------------------------------------------------------
    # LEGB
    # --------------------------------------------------------

    print(
        f"\nCurrency: {clinic_config['currency']}"
    )

    print(
        f"Tax: {clinic_config['tax']}"
    )

    print(
        f"Senior Discount: "
        f"{clinic_config['senior_discount']}"
    )


    # --------------------------------------------------------
    # Edge Cases
    # --------------------------------------------------------

    run_edge_case_tests()


# ============================================================
# PROGRAM START
# ============================================================

if __name__ == "__main__":
    main()