# Hospital Appointment & Billing System

## Project Overview

The Hospital Appointment & Billing System is a Python-based project designed to manage patients, doctors, appointments, medical tests, billing, insurance coverage, and clinic reports.

The project uses basic Python concepts such as dictionaries, lists, functions, loops, conditional statements, `*args`, `**kwargs`, lambda functions, list comprehensions, and exception/edge-case handling.

The system is implemented using Python only, without classes, external libraries, databases, APIs, or frameworks.

---

## Features

The system provides the following features:

- Patient management
- Doctor management
- Appointment validation
- Doctor availability validation
- Appointment status validation
- Medical test validation
- Duplicate test detection
- Test charge calculation
- Insurance coverage calculation
- Patient bill calculation
- Senior citizen discount
- Appointment cancellation
- Appointment processing
- Doctor statistics
- Patient reports
- Clinic dashboard
- Revenue calculations
- Highest spending patient detection
- Most requested doctor and specialization
- Lambda function for sorting patients by bill
- List comprehensions for filtering patients
- `*args` for calculating multiple charges
- `**kwargs` for configurable billing
- Edge-case testing

---

## Technologies Used

- Python 3
- Lists
- Dictionaries
- Sets
- Functions
- Loops
- Conditional Statements
- `*args`
- `**kwargs`
- Lambda Functions
- List Comprehensions

No external libraries or frameworks are used.

---

## Project Structure

```text
hospital_appointment_billing/
│
├── main.py
└── README.md

Starter Data

The system contains sample data for:

Patients
P001 - Ali Khan
P002 - Ahmed Raza
P003 - Sara Ahmed
P004 - Usman Ali
Doctors
D001 - Dr. Hassan - Cardiology
D002 - Dr. Sara - Dermatology
D003 - Dr. Ahmed - General
Medical Tests
Test	Price
ECG	$1500
Blood Test	$1000
X-Ray	$2500
MRI	$8000
Billing Rules

The billing system follows these rules:

Consultation Fee

The doctor's consultation fee is added to the bill.

Test Charges

The prices of all selected medical tests are added to the bill.

Insurance Coverage

For insured patients:

20% coverage on consultation fee
50% coverage on test charges

For patients without insurance:

No insurance coverage
Senior Citizen Discount

Patients aged 60 or above receive a 10% senior citizen discount after insurance coverage.

Appointment Processing

Before processing an appointment, the system validates:

Patient ID
Doctor ID
Doctor availability
Appointment status
Medical tests

The system also prevents:

Invalid patient IDs
Invalid doctor IDs
Invalid appointment IDs
Invalid medical tests
Duplicate tests
Processing cancelled appointments
Processing the same appointment more than once
Cancelling completed appointments
Cancelling an already cancelled appointment
Reports

The system generates different types of reports.

Doctor Report

The doctor report provides:

Appointments per doctor
Completed appointments
Cancelled appointments
Most requested doctor
Most requested specialization
Consultation revenue
Patient Report

The patient report provides:

Appointments per patient
Patient appointment status
Total medical charges
Insurance coverage
Patient paid amount
Highest spending patient
Patient with most appointments
Patients with no completed appointments
Insured patients
Senior citizen patients
Clinic Report

The clinic report provides:

Total patients
Total doctors
Total appointments
Completed appointments
Cancelled appointments
Pending appointments
Consultation revenue
Test revenue
Insurance coverage
Patient revenue
Most requested specialization
Highest spending patient
Python Concepts Demonstrated
Functions

The project is divided into multiple functions so that each function performs a specific task.

Examples:

calculate_test_charges()
calculate_insurance_coverage()
calculate_bill()
cancel_appointment()
patient_appointment_status()
*args

*args is used to calculate the total of multiple charges.

Example:

calculate_total(5000, 1500, 1000)

Output:

7500
**kwargs

**kwargs is used for configurable billing options such as insurance, senior discount, and tests.

Example:

calculate_configurable_bill(
    5000,
    insurance=True,
    senior_discount=True,
    include_tests=True
)
Lambda Function

A lambda function is used to sort patients according to their bill amount.

sorted(
    paid_amount.items(),
    key=lambda item: item[1],
    reverse=True
)
List Comprehension

List comprehensions are used to filter senior and insured patients.

Example:

[
    patient_id
    for patient_id, data in patients.items()
    if data["age"] >= 60
]
LEGB

The project also demonstrates Python's LEGB scope rule:

Local
Enclosing
Global
Built-in

The global clinic_config dictionary is accessed inside functions.

Edge Case Testing

The project includes testing for important edge cases:

Invalid patient ID
Invalid doctor ID
Invalid appointment ID
Doctor unavailable
Invalid medical test
Duplicate medical test
Empty test list
Negative patient age
Invalid appointment status
Cancelling a completed appointment
Processing a cancelled appointment
Processing the same appointment twice
Patient with no appointments
Doctor with no appointments
Empty data handling

Example:

Invalid Patient ID:
(False, 'Patient P999 does not exist')

Invalid Test:
(False, 'Invalid Test: CT Scan')

Duplicate Test:
(False, 'duplicate test: ECG')

Negative Age:
(False, 'Age cannot be negative.')

Cancel Completed Appointment:
(False, 'Completed appointment cannot be cancelled.')
Sample Output
Clinic Dashboard
========================================
           CLINIC DASHBOARD
========================================
Total Patients: 4
Total Doctors: 3
Total Appointments: 5
Completed: 3
Cancelled: 2
Pending: 0
Total Consultation Revenue: $ 12000
Total Test Revenue: $ 4000
Total Insurance Coverage: $ 2250.0
Total Patient Revenue: $ 13750.0
Most Requested Specialization: ['cardiology', 'Dermatology']
Highest Spending Patient: ['P004']
========================================
Billing Example

For a $5000 consultation with ECG and Blood Test:

Consultation Fee: $5000
Test Charges: $2500
Subtotal: $7500
Insurance Coverage: $2250
Patient Amount: $5250
Design Decisions

The following design decisions were made while developing the system:

1. Dictionaries for Patients and Doctors

Dictionaries are used because each patient and doctor has a unique ID and multiple related attributes.

For example:

patients["P001"]
doctors["D001"]

This makes it easy to access records using their IDs.

2. List for Appointments

Appointments are stored in a list because multiple appointment records need to be maintained and processed.

3. Functions for Logical Separation

The project is divided into small functions. Each function handles one specific task, making the code easier to understand, test, and maintain.

4. Reusable Billing Functions

Billing calculations are separated into different functions such as:

calculate_test_charges()
calculate_insurance_coverage()
calculate_bill()

This avoids repeating the same billing logic in different parts of the program.

5. Edge Case Handling

Validation checks are included to prevent invalid data and incorrect operations, such as processing cancelled appointments or using invalid test names.

6. Set for Duplicate Processing

A set is used to keep track of already processed appointment IDs.

processed_appointments = set()

This prevents the same appointment from being processed multiple times.

7. No External Dependencies

The project uses only built-in Python features so it can run without installing additional packages.

How to Run

Make sure Python 3 is installed.

Run the following command:

python3 main.py

The program will execute the test cases, reports, dashboard, and other required functionality.

Conclusion

This project demonstrates practical use of Python fundamentals in a real-world hospital appointment and billing scenario.

It covers data management, validation, billing calculations, insurance handling, discounts, appointment processing, reporting, edge-case testing, and several important Python concepts including *args, **kwargs, lambda functions, list comprehensions, and LEGB scope.


### Important

Tumhare current project ke according **README mein koi coding change required nahi hai**. Ye documentation tumhare already completed code ko explain karti hai.  

Bas `README.md` mein paste karke save kar do.
