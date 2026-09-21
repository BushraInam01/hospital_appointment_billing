# 1. STARTER DATA
#patients
patients = {
    "P001" :{
        "name": "Ali Khan",
        "age": 32,
        "city": "Lahore",
        "insurance": True
    },

    "P002":{
        "name": "Ahmed Raza",
        "age":45,
        "city": "Multan",
        "insurance": False
    },

    "P003":{
        "name": "sara Ahmed",
        "age": 28,
        "city": "Lahore",
        "insurance": True
    },

    "P004":{
        "name": "Usman Ali",
        "age": 67,
        "city": "Islamabad",
        "insurance": False
    }
}

#Doctors
doctors = {
    "D001":{
        "name": "Dr. Hassan",
        "specialization": "cardiology",
        "fee": 5000,
        "available": True
    },

    "D002":{
        "name": "Dr. Sara",
        "specialization": "Dermatology",
        "fee": 3000,
        "available": True
    },

    "D003":{
        "name": "Dr. Ahmed",
        "specialization": "General",
        "fee": 2000,
        "available": True
    }
}

#appointments
appointments = [
    {
        "appointment_id": "A001",
        "patient_id": "P001",
        "doctor_id": "D001",
        "status": "completed",
        "test":["ECG", "Blood Test"]
    },

    {
        "appointment_id": "A002",
        "patient_id": "P002",
        "doctor_id": "D003",
        "status": "completed",
        "test":[]
    },

    {
        "appointment_id": "A003",
        "patient_id": "P003",
        "doctor_id": "D002",
        "status": "cancelled",
        "test":[]
    },

    {
        "appointment_id": "A004",
        "patient_id": "P004",
        "doctor_id": "D001",
        "status": "completed",
        "test": ["ECG"]
    },
    # Add this cancel_appointment("A005") for testing purpose.
    {
        "appointment_id": "A005",
        "patient_id": "P001",
        "doctor_id": "D002",
        "status": "pending",
        "test": []
    }
]

#Test Prices
test_prices = {
    "ECG": 1500,
    "Blood Test": 1000,
    "X-Ray": 2500,
    "MRI": 8000
}

#Clinic Configuartion
clinic_config = {
    "tax": 0.0,
    "currency": "$",
    "senior_discount": 0.10 #10% = 10 / 100 = 0.10
}


#Test Validates
print(patients)
print(doctors)
print(appointments)
print(test_prices)
print(clinic_config)


#-------------------------------------------------------------------------------
#2. Appointment Processing
#------------------------------------------------------------------------------

#2.1 Validate Patient ID
def validate_patient(patient_id):
    if patient_id not in patients:
        return False, f"Patient {patient_id} does not exist"

    return True

#2.2 Validate Doctor ID
def validate_doctor(doctor_id):
    if doctor_id not in doctors:
        return False, f"doctor {doctor_id} does not exist"
    
    return True, "Doctor is Valid"

#2.3 Check Doctor Availability
def validate_doctor_availability(doctor_id):
    if doctor_id not in doctors:
        return False, f"Doctor {doctor_id} does not exist"

    if not doctors[doctor_id]["available"]:
        return False, f"Doctor {doctor_id} is not available"

    return True

#2.4 Validate Appointment Status

valid_statuses = {"pending", "completed", "cancelled"} #A set is appropriate for this kind of lookup.

def validate_appointment_status(status):
    if status not in valid_statuses:
        return False, f"Invalid appointmnet status: {status}"
    
    return True, "Appointment status is valid"


#2.5 Validate every requested test ---- Suppose -----> tests = ["ECG", "Blood Test"]
def validate_test(tests):
    seen_tests = set()

    for test in tests:
        if test not in test_prices:                         #tests = ["ECG", "CT Scan"]
            return False, f"Invalid Test: {test}"

        if test in seen_tests:                              #tests = ["ECG", "ECG"]
            return False, f"duplicate test: {test}"
        
        seen_tests.add(test)                                #tests = ["ECG", "Blood Test"]

    return True, "All test are valid"


#2.6 Calculate the bill for valid completed appointments
def find_appointment(appointment_id):
    for appointment in appointments:
        if appointment["appointment_id"] == appointment_id:
            return appointment
    return None

#Test Validations

print(validate_patient("P001"))
print(validate_patient("P999"))

print(validate_doctor("D001"))
print(validate_doctor("D999"))

print(validate_doctor_availability("D001"))
print(validate_doctor_availability("D999"))

print(validate_appointment_status("completed"))
print(validate_appointment_status("wrong"))

print(validate_test(["ECG", "Blood Test"]))
print(validate_test(["ECG", "CT Scan"]))
print(validate_test(["ECG", "ECG"]))

print(find_appointment("A001"))
print(find_appointment("A999"))


#-------------------------------------------------------------------------
#3. Billing Rules
#------------------------------------------------------------------------

#3.1 Calculate Test Charges
def calculate_test_charges(tests):
    total = 0

    for test in tests:
        total += test_prices[test]
    return total

print(calculate_test_charges(["ECG", "Blood Test"]))


#3.2 Calculate Insurance Coverage
def calculate_insurance_coverage(consultation_fee, test_charges, insurance):
    if not insurance:
        return 0

    consultation_coverage = consultation_fee * 0.20   #20%
    test_coverage = test_charges * 0.50               #50%

    total_coverage = consultation_coverage + test_coverage

    return total_coverage 


#3.3 Calculate Subtotal
def calculate_subtotal(consultation_fee, test_charges):
    subtotal = consultation_fee + test_charges

    return subtotal


#3.4 Calculate Patient Responsibility
def calculate_patient_responsibilty(subtotal, insurance_coverage):
    patient_amount = subtotal - insurance_coverage
    return patient_amount


#3.5 Now combine the billing calculations
def calculate_bill(consultation_fee, tests, insurance):
    test_charges = calculate_test_charges(tests)

    subtotal = calculate_subtotal(consultation_fee, test_charges)

    insurance_coverage = calculate_insurance_coverage(consultation_fee, test_charges, insurance)

    patient_amount = calculate_patient_responsibilty(subtotal, insurance_coverage)

    return {
        "Consultation_fee": consultation_fee,
        "test_charges": test_charges,
        "subtotal": subtotal,
        "insurance_coverage": insurance_coverage,
        "patient_amount": patient_amount
    }

bill = calculate_bill(5000, ["ECG", "Blood Test"], True)
print(bill)

#------------------------------------------------------------------------------
#4. Senior Citizen Discount
#------------------------------------------------------------------------------

def calculate_senior_discount(amount_after_insurance, age):
    if age >= 60:
        discount_rate = clinic_config["senior_discount"]
        discount_amount = amount_after_insurance * discount_rate
        final_amount = amount_after_insurance - discount_amount

        return discount_amount, final_amount
    return 0, amount_after_insurance

#Test
discount, final_amount = calculate_senior_discount(5000, 67)

print("Senior Discount:", discount)
print("Final Amount:", final_amount)


#--------------------------------------------------------------------------
#5. Cancellation Rules
#-------------------------------------------------------------------------

def cancel_appointment(appointment_id):

    #Find the appointment
    appointment = find_appointment(appointment_id)

    #Appointment does not exist                                             
    if appointment is None:
        return False, f"Appointment {appointment_id} does not exist."      #example: cancel_appointment("A999")

    #Get current status
    status = appointment["status"]

    #Completed appointment cannot be cancelled
    if status == "completed":
        return False, "Completed appointment cannot be cancelled."

    #Already canceled appointment
    if status == "cancelled":
        return False, "Appointment already cancelled."

    #Pending appointment can be cancelled
    if status == "pending":
        appointment["status"] = "cancelled"
        return True, "Appointment cancelled successfully."

    #Invalid status
    return False, f"cannot cancel appointment with status. {status}"

#example for Pending
{
    "appointment_id": "A005",
    "patient_id": "P001",
    "doctor_id": "D002",
    "status": "pending",
    "tests": []
}

# Test Cancellation
print(cancel_appointment("A001"))  # completed
print(cancel_appointment("A003"))  # cancelled
print(cancel_appointment("A005"))  # pending
print(cancel_appointment("A999"))  # does not exist


#------------------------------------------------------------------------
#6. Doctor Statistics
#-----------------------------------------------------------------------

#6.1 Appointments Per Doctor
def appointment_per_doctor():
    statistics = {}

    for doctor_id in doctors:
        statistics [doctor_id] = 0

    for appointment in appointments:
        doctor_id = appointment["doctor_id"]
        statistics[doctor_id] +=1

    return statistics

#Test
print(appointment_per_doctor())

#----------------------------------------------------------
#6.2 Completed Appointments
def completed_appointment():
    count = 0

    for appointment in appointments:
        if appointment["status"] == "completed":
            count +=1
    return count

#Test 
print("Completed Appointments:",completed_appointment())

#-----------------------------------------------------------

#6.3 Cancelled Appointments
def cancelled_appointments():
    count = 0

    for appointment in appointments:
        if appointment["status"] == "cancelled":
            count +=1

    return count

#Test
print("Canclled Appointments: ", cancelled_appointments())

#----------------------------------------------------------------
#6.4 Total Revenue Generated
def total_revenue():
    total = 0

    for appointment in appointments:
        if appointment["status"] == "completed":

            doctor_id = appointment["doctor_id"]
            doctor_fee = doctors[doctor_id]["fee"]

            tests = appointment["test"]

            bill = calculate_bill(doctor_fee, tests, patients[appointment["patient_id"]]["insurance"])

            total += bill["patient_amount"]

    return total

#Test
print("Total Revenue:", total_revenue())


#----------------------------------------------------------------
#6.5 Average Bill
def average_bill():

    completed = completed_appointment()

    if completed == 0:
        return 0

    total = total_revenue()
    average = total / completed

    return average

#Test
print("Average Bill:", round(average_bill(), 2))


#--------------------------------------------------------------
#6.6 Most Requested Doctor
def most_requested_doctor():

    statistics = appointment_per_doctor()

    if not statistics:
        return []

    heighest_count = max(statistics.values())
    most_requested = []

    for doctor_id, count in statistics.items():
        if count == heighest_count:
            most_requested.append(doctor_id)

    return most_requested

#Test
print("Most Requested Doctor: ", most_requested_doctor())


#-----------------------------------------------------------------
#6.7 Most Requested Specialization
# 6.7 Most Requested Specialization

def most_requested_specialization():

    specialization_counts = {}

    for appointment in appointments:

        doctor_id = appointment["doctor_id"]

        specialization = doctors[doctor_id]["specialization"]

        if specialization not in specialization_counts:
            specialization_counts[specialization] = 0

        specialization_counts[specialization] += 1

    if not specialization_counts:
        return []

    highest_count = max(specialization_counts.values())

    most_requested = []

    for specialization, count in specialization_counts.items():

        if count == highest_count:
            most_requested.append(specialization)

    return most_requested
#Test
print("Most Requested Specialization: ", most_requested_specialization())    


#---------------------------------------------------------------------------------------
#7. Patient Report
#--------------------------------------------------------------------------------------

#7.1 Appointments Per Patient
# 7.1 Appointments Per Patient

def appointments_per_patient():

    statistics = {}

    # Start every patient with 0 appointments
    for patient_id in patients:
        statistics[patient_id] = 0

    # Count appointments
    for appointment in appointments:
        patient_id = appointment["patient_id"]
        statistics[patient_id] += 1

    return statistics

#Test
print("Appointments Per Patient:", appointments_per_patient())


#-------------------------------------------------------------------------

#7.2 Completed/Cancelled Appointments
def patient_appointment_status():

    statistics = {}

    # Start every patient with 0 completed and 0 cancelled
    for patient_id in patients:
        statistics[patient_id] = {
            "completed": 0,
            "cancelled": 0
        }

    # Count appointment status for each patient
    for appointment in appointments:

        patient_id = appointment["patient_id"]
        status = appointment["status"]

        if status == "completed":
            statistics[patient_id]["completed"] += 1

        elif status == "cancelled":
            statistics[patient_id]["cancelled"] += 1

    return statistics

#Test
print("Patient Appointment Status:", patient_appointment_status())

#----------------------------------------------------------------------------------
#7.3 Total Medical Charges
def total_medical_charges():
    charges = {}

    #start every patient with 0 charges
    for patient_id in patients:
        charges[patient_id] = 0

    #calculate charges for completed appointments
    for appointment in appointments:
        if appointment ["status"] != "completed":
            continue

        patient_id = appointment["patient_id"]
        doctor_id = appointment["doctor_id"]

        doctor_fee = doctors[doctor_id]["fee"]
        test = appointment["test"]
        insurance = patients[patient_id]["insurance"]

        bill = calculate_bill(doctor_fee, test, insurance)

        charges[patient_id] +=bill["patient_amount"]

    return charges

#Test
print("Total Medical Charges: ", total_medical_charges())

#---------------------------------------------------------------------------
#7.4 Insurance Coverage
def insurance_coverage_per_patient():
    coverage = {}

    #start every patient with 0 insurance coverage
    for patient_id in patients:
        coverage[patient_id] = 0

    #calculate insurane coverage for completed appointments
    for appointment in appointments:
        if appointment["status"] != "completed":
            continue

        patient_id = appointment["patient_id"]
        doctor_id = appointment["doctor_id"]

        doctor_fee = doctors[doctor_id]["fee"]
        test = appointment["test"]
        insurance = patients[patient_id]["insurance"]

        bill = calculate_bill(doctor_fee, test, insurance)
        coverage [patient_id] += bill["insurance_coverage"]

    return coverage

#Test
print("Insurance Coverage:", insurance_coverage_per_patient())

#-----------------------------------------------------------------------------
#Now we'll calculate how much each patient actually paid after insurance coverage.
#7.5 Patient-Paid Amount
def patient_paid_amount():
    paid_amount = {}

    #start every patient with 0
    for patient_id in patients:
        paid_amount[patient_id] = 0

    #calculate amount paid for completed appointments
    for appointment in appointments:
        if appointment["status"] != "completed":
            continue

        patient_id = appointment["patient_id"]
        doctor_id = appointment["doctor_id"]

        doctor_fee = doctors[doctor_id]["fee"]
        tests = appointment["test"]
        insurance = patients[patient_id]["insurance"]

        bill = calculate_bill(doctor_fee, tests, insurance)
        paid_amount[patient_id] += bill["patient_amount"]

    return paid_amount

#Test
print("Patient Paid Amount:", patient_paid_amount())

#-----------------------------------------------------------------------------
#Now we need to find the patient who has spent the highest amount.
#We'll reuse our patient_paid_amount() function instead of calculating everything again.

#7.6 Highest-Spending Patient
def heighest_spending_patient():
    paid_amount = patient_paid_amount()

    if not paid_amount:
        return []

    heighest_amount = max(paid_amount.values())
    heighest_spenders = []

    for patient_id, amount in paid_amount.items():
        if amount == heighest_amount:
            heighest_spenders.append(patient_id)

    return heighest_spenders

#Test
print("Heighest Spending Patient:", heighest_spending_patient())


#-----------------------------------------------------------------------------
#Now we'll find which patient has the highest number of appointments.
#We already have appointments_per_patient(), so we'll reuse it:

#7.7 Patient with Most Appointments
def patient_with_most_appointments():
    statistics = appointments_per_patient()

    if not statistics:
        return []

    heighest_count = max(statistics.values())
    most_appointments = []

    for patient_id, count in statistics.items():
        if count == heighest_count:
            most_appointments.append(patient_id)

    return most_appointments

#Test
print("Patient with most Appointment:", patient_with_most_appointments())


#-----------------------------------------------------------------------------------------
#Now we'll find patients who do not have any completed appointment.
#We'll reuse patient_appointment_status():

#7.8 Patients with No Completed Appointment
def patients_with_no_completed_appointment():

    status = patient_appointment_status()
    no_completed = []

    for patient_id, data in status.items():

        if data["completed"] == 0:
            no_completed.append(patient_id)

    return no_completed

#Test
print("Patient with no completed Appointment:", patients_with_no_completed_appointment())


#------------------------------------------------------------------------------------------------
#Now we'll find all patients whose insurance is True.

#7.9 Insured Patients
def insured_patients():
    insured = []

    for patient_id, data in patients.items():
        if data["insurance"] is True:
            insured.append(patient_id)

    return insured

#Test
print("Insured Patients:", insured_patients())


#-----------------------------------------------------------------------------------------
#Our rule is: Age >= 60 → Senior Citizen

#7.10 Senior-Citizen Patients
def senior_citizen_patients():
    senior_patients = []

    for patient_id, data in patients.items():

        if data["age"] >= 60:
            senior_patients.append(patient_id)

    return senior_patients

#Test
print("Senior Citizen Patients:", senior_citizen_patients())


#----------------------------------------------------------------------------
#8. Clinic Management Dashboard
#----------------------------------------------------------------------------
#I reused existing functions instead of duplicating the same logic, which makes the code more maintainable and reduces repetition.


# 8.1 Total Patients
def total_patients():
    return len(patients)


# 8.2 Total Doctors
def total_doctors():
    return len(doctors)


# 8.3 Total Appointments
def total_appointments():
    return len(appointments)


# 8.4 Completed Appointments
# Already created in Part 6
# We will reuse completed_appointments()


# 8.5 Cancelled Appointments
# Already created in Part 6
# We will reuse cancelled_appointments()


# 8.6 Pending Appointments
def pending_appointments():

    count = 0

    for appointment in appointments:

        if appointment["status"] == "pending":
            count += 1

    return count


# 8.7 Total Consultation Revenue
def total_consultation_revenue():

    total = 0

    for appointment in appointments:

        if appointment["status"] != "completed":
            continue

        doctor_id = appointment["doctor_id"]

        doctor_fee = doctors[doctor_id]["fee"]

        total += doctor_fee

    return total


# 8.8 Total Test Revenue
def total_test_revenue():

    total = 0

    for appointment in appointments:

        if appointment["status"] != "completed":
            continue

        tests = appointment["test"]

        test_charges = calculate_test_charges(tests)

        total += test_charges

    return total


# 8.9 Total Insurance Coverage
def total_insurance_coverage():

    coverage = insurance_coverage_per_patient()

    total = sum(coverage.values())

    return total


# 8.10 Total Patient Revenue
def total_patient_revenue():

    paid_amount = patient_paid_amount()

    total = sum(paid_amount.values())

    return total


# 8.11 Most Requested Specialization
# Already created in Part 6
# We will reuse most_requested_specialization()


# 8.12 Highest Spending Patient
# Already created in Part 7
# We will reuse highest_spending_patient()


# ==========================================
# 8.13 CLINIC DASHBOARD
# ==========================================

def clinic_dashboard():

    print("\n========================================")
    print("           CLINIC DASHBOARD")
    print("========================================")

    print("Total Patients:", total_patients())

    print("Total Doctors:", total_doctors())

    print("Total Appointments:", total_appointments())

    print("Completed:", completed_appointment())

    print("Cancelled:", cancelled_appointments())

    print("Pending:", pending_appointments())

    print(
        "Total Consultation Revenue: $",
        total_consultation_revenue()
    )

    print(
        "Total Test Revenue: $",
        total_test_revenue()
    )

    print(
        "Total Insurance Coverage: $",
        total_insurance_coverage()
    )

    print(
        "Total Patient Revenue: $",
        total_patient_revenue()
    )

    print(
        "Most Requested Specialization:",
        most_requested_specialization()
    )

    print(
        "Highest Spending Patient:",
        heighest_spending_patient()
    )

    print("========================================")


# RUN DASHBOARD

clinic_dashboard()

#----------------------------------------------------------------------------
#9. REQUIRED *ARGS CHALLENGE

def calculate_total(*charges): # *charges ---> function accept multiple arguments
    total = 0

    for charge in charges:
        total += charge

    return total

print("Total Charges:", calculate_total(5000, 1500, 1000))


#----------------------------------------------------------------------------------------
# 10. Required **kwargs Challenge

def calculate_configurable_bill(amount, **options):

    total = amount

    if options.get("insurance", False):
        total -= 500

    if options.get("senior_discount", False):
        total -= 300

    if options.get("include_tests", False):
        total += 1000

    return total


# Calling Function

print(
    "calculate_bill:",
    calculate_configurable_bill(
        5000,
        insurance=True,
        senior_discount=True,
        include_tests=True
    )
)

#-----------------------------------------------------------------------------------------
#11. Lambda Requirement
def sort_patients_by_bill():

    paid_amount = patient_paid_amount()

    sorted_patients = sorted(
        paid_amount.items(),
        key=lambda item: item[1],
        reverse= True
    )

    return sorted_patients

print("Sort Patients by Bill:", sort_patients_by_bill())

#--------------------------------------------------------------------------------------
#12. Comprehension Requirement

# 12.1 Senior Patients using List Comprehension
def senior_patients_comprehension():
    senior_patients = [
        patient_id
        for patient_id, data in patients.items()
        if data["age"] >= 60
    ]

    return senior_patients

# 12.2 Insured Patients using List Comprehension
def insured_patient_comprehension():
    insured_patients = [
        patient_id 
        for patient_id, data in patients.items()
        if data["insurance"] is True
    ]

    return insured_patients

#calling function
print("Senior Patients:", senior_patients_comprehension())
print("Insured Patients", insured_patient_comprehension())


#----------------------------------------------------------------------------------------
# 13. LEGB Challenge

def get_clinic_config():

    currency = clinic_config["currency"]
    tax = clinic_config["tax"]
    senior_discount = clinic_config["senior_discount"]

    return currency, tax, senior_discount


# Calling Function

currency, tax, senior_discount = get_clinic_config()

print("Currency:", currency)
print("Tax:", tax)
print("Senior Discount:", senior_discount)


#----------------------------------------------------------------------------------------
# 14. REQUIRED EDGE CASES


print("\n========================================")
print("           EDGE CASE TESTING")
print("========================================")


# 1. Invalid Patient ID
print("\n1. Invalid Patient ID:")
print(validate_patient("P999"))


# 2. Invalid Doctor ID
print("\n2. Invalid Doctor ID:")
print(validate_doctor("D999"))


# 3. Invalid Appointment ID
print("\n3. Invalid Appointment ID:")
print(find_appointment("A999"))


# 4. Doctor Unavailable
print("\n4. Doctor Unavailable:")

doctors["D003"]["available"] = False

print(validate_doctor_availability("D003"))

doctors["D003"]["available"] = True


# 5. Invalid Test
print("\n5. Invalid Test:")
print(validate_test(["CT Scan"]))


# 6. Duplicate Test
print("\n6. Duplicate Test:")
print(validate_test(["ECG", "ECG"]))


# 7. Empty Test List
print("\n7. Empty Test List:")
print(validate_test([]))


# 8. Negative Age
print("\n8. Negative Age:")

def validate_age(age):

    if not isinstance(age, int):
        return False, "Age must be an integer."

    if age < 0:
        return False, "Age cannot be negative."

    return True, "Age is valid."


print(validate_age(-5))


# 9. Invalid Appointment Status
print("\n9. Invalid Appointment Status:")
print(validate_appointment_status("wrong"))


# 10. Cancel Completed Appointment
print("\n10. Cancel Completed Appointment:")
print(cancel_appointment("A001"))


# 11. Process Cancelled Appointment
print("\n11. Process Cancelled Appointment:")

cancelled_appointment = find_appointment("A003")

if cancelled_appointment is not None:
    if cancelled_appointment["status"] == "cancelled":
        print(False, "Cancelled appointment cannot be processed.")


# 12. Process Same Appointment Twice
print("\n12. Process Same Appointment Twice:")

processed_appointments = set()


def process_appointment(appointment_id):

    appointment = find_appointment(appointment_id)

    if appointment is None:
        return False, "Appointment does not exist."

    if appointment_id in processed_appointments:
        return False, "Appointment has already been processed."

    if appointment["status"] == "cancelled":
        return False, "Cancelled appointment cannot be processed."

    processed_appointments.add(appointment_id)

    return True, "Appointment processed successfully."


print(process_appointment("A002"))
print(process_appointment("A002"))


# 13. Patient With No Appointments
print("\n13. Patient With No Appointments:")

patient_appointments = appointments_per_patient()

no_appointments = [
    patient_id
    for patient_id, count in patient_appointments.items()
    if count == 0
]

print(no_appointments)


# 14. Doctor With No Appointments
print("\n14. Doctor With No Appointments:")

doctor_appointments = appointment_per_doctor()

no_doctor_appointments = [
    doctor_id
    for doctor_id, count in doctor_appointments.items()
    if count == 0
]

print(no_doctor_appointments)


# 15. Empty Data Handling
print("\n15. Empty Data Handling:")

empty_patients = {}
empty_doctors = {}
empty_appointments = []

print("Empty Patients:", len(empty_patients))
print("Empty Doctors:", len(empty_doctors))
print("Empty Appointments:", len(empty_appointments))


print("\n========================================")


