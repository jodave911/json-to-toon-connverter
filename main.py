import random
from faker import Faker
import json
import datetime

# Initialize Faker to generate mock data
fake = Faker()

# --- Configuration ---
NUM_STUDENTS = 23
NUM_SUBJECTS_PER_STUDENT = 15

# A pool of subjects to choose from
SUBJECT_POOL = [
    "Advanced Calculus", "Quantum Physics", "Organic Chemistry", "Data Structures & Algorithms",
    "Modernist Literature", "World History 1800-Present", "Geopolitical Strategy", 
    "Machine Learning", "Studio Art: Oil Painting", "Music Theory & Composition",
    "Advanced Biomechanics", "Macroeconomics", "Cognitive Psychology", "Sociological Theory",
    "Ethical Philosophy", "Statistical Analysis", "Spanish Language & Culture",
    "French Literature", "Advanced Engineering", "Molecular Biology", "Astrophysics"
]

# Helper function to get a letter grade and GPA point
def get_grade_details(score):
    """Calculates letter grade and GPA point from a numeric score."""
    if score >= 93: return "A", 4.0
    if score >= 90: return "A-", 3.7
    if score >= 87: return "B+", 3.3
    if score >= 83: return "B", 3.0
    if score >= 80: return "B-", 2.7
    if score >= 77: return "C+", 2.3
    if score >= 73: return "C", 2.0
    if score >= 70: return "C-", 1.7
    if score >= 67: return "D+", 1.3
    if score >= 63: return "D", 1.0
    if score >= 60: return "D-", 0.7
    else: return "F", 0.0

# --- Main Data Generation Function ---

def generate_all_student_data():
    """
    Generates a sophisticated list of student data.
    """
    print(f"Generating data for {NUM_STUDENTS} students...")
    
    # This will be our main "JSON-like" variable
    all_students = []

    # Use a fixed seed for reproducible "random" data
    Faker.seed(42)
    random.seed(42)

    for i in range(NUM_STUDENTS):
        # 1. Generate Personal Info
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        personal_info = {
            "first_name": first_name,
            "last_name": last_name,
            "full_name": f"{first_name} {last_name}",
            "email": f"{first_name.lower()}.{last_name.lower()}@{fake.free_email_domain()}",
            "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=23).isoformat(),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "zip_code": fake.zipcode()
            },
            "phone_number": fake.phone_number()
        }

        # 2. Generate Academic Info & Subjects
        courses = []
        total_credits = 0
        total_gpa_points = 0
        
        # Ensure each student has 15 unique subjects
        selected_subjects = random.sample(SUBJECT_POOL, NUM_SUBJECTS_PER_STUDENT)

        for subject_name in selected_subjects:
            score = random.randint(65, 100) # Assign a random score
            letter_grade, gpa_point = get_grade_details(score)
            credits = random.choice([3, 4]) # Subjects are 3 or 4 credits
            
            courses.append({
                "subject_name": subject_name,
                "teacher": f"{fake.prefix_female()} {fake.last_name()}" if random.random() > 0.5 else f"{fake.prefix_male()} {fake.last_name()}",
                "credits": credits,
                "semester": f"Fall {datetime.date.today().year - random.randint(1, 2)}",
                "grade_numeric": score,
                "grade_letter": letter_grade,
                "gpa_point": gpa_point
            })
            
            # Add to totals for final GPA calculation
            total_credits += credits
            total_gpa_points += (gpa_point * credits)

        # Calculate final GPA
        overall_gpa = round(total_gpa_points / total_credits, 2) if total_credits > 0 else 0.0

        academic_info = {
            "student_id": f"S{2024000 + i + 1}",
            "major": random.choice(["Computer Science", "Physics", "English", "Economics", "Biology", "History"]),
            "enrollment_status": random.choice(["Full-Time", "Part-Time"]),
            "expected_graduation": f"Spring {datetime.date.today().year + random.randint(1, 3)}",
            "overall_gpa": overall_gpa,
            "total_credits_earned": total_credits,
            "courses": courses # This is the nested list of 15 subjects
        }
        
        # 3. Add Extracurriculars
        extracurriculars = random.sample(
            ["Debate Club", "Chess Team", "Volunteer Services", "Soccer Team", "Coding Club", "University Band"],
            k=random.randint(1, 3) # Each student is in 1-3 clubs
        )

        # 4. Combine all data for one student
        student_record = {
            "personal_info": personal_info,
            "academic_info": academic_info,
            "extracurricular_activities": extracurriculars
        }
        
        all_students.append(student_record)

    print("...Data generation complete.")
    return all_students

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    
    # This is the "highly sophisticated JSON variable" you requested
    # It's a Python list of dictionaries, which is equivalent to a JSON array of objects.
    ALL_STUDENT_DATA = generate_all_student_data()

    # --- You can now use this variable ---
    
    # 1. Print the total number of students
    print(f"\nTotal students in variable: {len(ALL_STUDENT_DATA)}")
    
    # 2. Print a sample of the first student's data to check the structure
    print("\n--- SAMPLE DATA (First Student) ---")
    # Use json.dumps for pretty-printing the dictionary
    print(json.dumps(ALL_STUDENT_DATA[0], indent=2))
    
    # 3. Example of accessing nested data
    print("\n--- DATA ACCESS EXAMPLE ---")
    student_name = ALL_STUDENT_DATA[0]["personal_info"]["full_name"]
    first_subject = ALL_STUDENT_DATA[0]["academic_info"]["courses"][0]["subject_name"]
    print(f"First student '{student_name}' is taking '{first_subject}'.")

    # 4. (Optional) Save the data to an actual JSON file for inspection
    with open("student_data.json", "w") as f:
        json.dump(ALL_STUDENT_DATA, f, indent=2)
    print(f"\nSuccessfully saved all {len(ALL_STUDENT_DATA)} records to 'student_data.json'")