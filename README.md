# 🏥 Hospital Appointment & Billing System

A Python-based Hospital Appointment & Billing System designed to manage patients, doctors, appointments, billing, insurance coverage, senior citizen discounts, cancellations, and clinic reports.

The project uses **JSON for data storage**, **Python Dataclasses as data models**, and **Error Handling** for invalid inputs and edge cases.

---

## 🚀 Features

### 👤 Patient Management
- Store patient information
- Patient ID, name, age, city, and insurance status
- Search patients by ID
- Validate patient information
- Identify senior and insured patients

### 👨‍⚕️ Doctor Management
- Store doctor information
- Doctor ID, name, specialization, fee, and availability
- Search doctors by ID
- Check doctor availability
- Generate doctor statistics

### 📅 Appointment Management
- Manage hospital appointments
- Process pending appointments
- Mark processed appointments as completed
- Prevent completed appointments from being processed again
- Cancel pending appointments
- Prevent completed appointments from being cancelled
- Handle cancelled appointments correctly

### 💰 Billing System
- Calculate consultation fees
- Calculate test charges
- Calculate subtotal
- Calculate insurance coverage
- Calculate patient's final responsibility
- Apply senior citizen discount

### 🛡️ Insurance
Insurance coverage is calculated as:

- 20% of consultation fee
- 50% of test charges

### 👴 Senior Citizen Discount
Patients aged **60 or above** receive an additional **10% discount**.

### 📊 Clinic Dashboard
The dashboard displays:

- Total patients
- Total doctors
- Total appointments
- Completed appointments
- Cancelled appointments
- Pending appointments
- Total consultation revenue
- Total test revenue
- Total insurance coverage
- Total patient revenue
- Most requested specialization
- Highest spending patient

### ⚠️ Error Handling
The project handles different errors and invalid cases using Python exception handling.

Examples:

- Missing `data.json`
- Invalid JSON format
- Invalid patient ID
- Invalid doctor ID
- Invalid appointment ID
- Invalid appointment status
- Unavailable doctor
- Invalid test
- Duplicate test
- Invalid age
- Processing cancelled appointment
- Processing completed appointment
- Cancelling completed appointment

### 🧪 Edge Case Testing
The project includes tests for:

- Invalid patient
- Invalid doctor
- Invalid appointment
- Unavailable doctor
- Invalid test
- Duplicate test
- Empty test list
- Negative age
- Invalid appointment status
- Cancelling completed appointment
- Processing cancelled appointment
- Processing the same appointment twice
- Patient with no appointments
- Doctor with no appointments
- Empty data

---

## 🧱 Data Models

The project uses Python's built-in `dataclasses` module.

### Patient

```python
@dataclass
class Patient:
    patient_id: str
    name: str
    age: int
    city: str
    insurance: bool

Doctor
@dataclass
class Doctor:
    doctor_id: str
    name: str
    specialization: str
    fee: int
    available: bool
Appointment
@dataclass
class Appointment:
    appointment_id: str
    patient_id: str
    doctor_id: str
    status: str
    tests: list
📂 Project Structure
hospital_appointment_billing/
│
├── main.py
├── mainP.py
├── models.py
├── data.json
├── README.md
└── .gitignore
File Description
File	Description
main.py	Main application logic
mainP.py	Practice/testing file
models.py	Python Dataclasses / Data Models
data.json	Patient, doctor, and appointment data
README.md	Project documentation
📄 JSON Data

The project stores its data in data.json.

The JSON file contains:

patients
doctors
appointments

The JSON data is loaded using Python's built-in json module and then converted into Python Dataclass objects.

🛠️ Technologies Used
Python 3
JSON
Dataclasses
Exception Handling
Functions
Lists
Dictionaries
Sets
Lambda Functions
List Comprehensions
*args
**kwargs

No external libraries are required.

▶️ How to Run
1. Clone the repository
git clone https://github.com/BushraInam01/hospital_appointment_billing.git
2. Navigate to the project
cd hospital_appointment_billing
3. Run the application
python3 main.py
🧪 Example Output
========================================
     HOSPITAL APPOINTMENT & BILLING
========================================

Total Patients: 4
Total Doctors: 3
Total Appointments: 5

Sample Bill:
{
    'Consultation_fee': 5000,
    'test_charges': 2500,
    'subtotal': 7500,
    'insurance_coverage': 2250.0,
    'patient_amount': 5250.0
}

Senior Discount: 500.0
Final Amount: 4500.0
📚 Concepts Practiced

This project demonstrates practical use of:

Functions
Conditional statements
Loops
Lists and dictionaries
Sets
Exception handling
JSON file handling
Python Dataclasses
Object-oriented concepts
*args
**kwargs
Lambda functions
List comprehensions
LEGB rule
Edge case testing
🎯 Learning Objective

The main objective of this project was to practice Python programming concepts by building a real-world hospital appointment and billing system.

The project also demonstrates how structured JSON data can be converted into Python data models using dataclasses, while handling invalid data and runtime errors safely.
