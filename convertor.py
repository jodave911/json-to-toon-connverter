import random
import re
import json
import datetime
from faker import Faker

# ============================================================================
# PART 1: STUDENT DATA GENERATION (from previous step)
# ============================================================================

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
    all_students = []
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
        selected_subjects = random.sample(SUBJECT_POOL, NUM_SUBJECTS_PER_STUDENT)

        for subject_name in selected_subjects:
            score = random.randint(65, 100)
            letter_grade, gpa_point = get_grade_details(score)
            credits = random.choice([3, 4])
            courses.append({
                "subject_name": subject_name,
                "teacher": f"{fake.prefix_female()} {fake.last_name()}" if random.random() > 0.5 else f"{fake.prefix_male()} {fake.last_name()}",
                "credits": credits,
                "semester": f"Fall {datetime.date.today().year - random.randint(1, 2)}",
                "grade_numeric": score,
                "grade_letter": letter_grade,
                "gpa_point": gpa_point
            })
            total_credits += credits
            total_gpa_points += (gpa_point * credits)

        overall_gpa = round(total_gpa_points / total_credits, 2) if total_credits > 0 else 0.0
        academic_info = {
            "student_id": f"S{2024000 + i + 1}",
            "major": random.choice(["Computer Science", "Physics", "English", "Economics", "Biology", "History"]),
            "enrollment_status": random.choice(["Full-Time", "Part-Time"]),
            "expected_graduation": f"Spring {datetime.date.today().year + random.randint(1, 3)}",
            "overall_gpa": overall_gpa,
            "total_credits_earned": total_credits,
            "courses": courses
        }
        
        # 3. Add Extracurriculars
        extracurriculars = random.sample(
            ["Debate Club", "Chess Team", "Volunteer Services", "Soccer Team", "Coding Club", "University Band"],
            k=random.randint(1, 3)
        )

        # 4. Combine all data
        all_students.append({
            "personal_info": personal_info,
            "academic_info": academic_info,
            "extracurricular_activities": extracurriculars
        })

    print("...Data generation complete.")
    return all_students

# ============================================================================
# PART 2: PYTHON TOON ENCODER
# ============================================================================

# --- TOON Quoting & Type Helpers ---

# Regex to check if a key needs to be quoted.
# Unquoted keys: start with letter/_ , contain letters/digits/_/.
TOON_KEY_IDENTIFIER_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_.]*$")
# Regex to check if a string looks like a number
TOON_NUMBER_LIKE_RE = re.compile(r"^-?(0|[1-9]\d*)(\.\d+)?([eE][+-]?\d+)?$")

def _quote_toon_key(key: str) -> str:
    """Quotes an object key if it's not a valid TOON identifier."""
    if TOON_KEY_IDENTIFIER_RE.match(key):
        return key
    # Use json.dumps for safe, standard string quoting
    return json.dumps(key)

def _quote_toon_value(value, delimiter: str = ",") -> str:
    """
    Safely converts a Python primitive to its TOON string representation,
    quoting strings only when necessary.
    """
    # 1. Handle non-string primitives
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        # TOON spec prefers no scientific notation, but str() is robust
        return str(value)
        
    if not isinstance(value, str):
        # Fallback for other types (though our data doesn't have them)
        return json.dumps(str(value))

    # 2. Handle strings, applying TOON quoting rules
    s = value
    
    # Rule: Empty string
    if s == "":
        return '""'
    
    # Rule: Leading or trailing spaces
    if s.strip() != s:
        return json.dumps(s)

    # Rule: Contains special characters
    if any(c in s for c in [delimiter, ':', '"', '\\']):
        return json.dumps(s)
    
    # Rule: Starts with a list-like marker
    if s.startswith("- "):
        return json.dumps(s)

    # Rule: Looks like boolean or null
    if s in ["true", "false", "null"]:
        return json.dumps(s)

    # Rule: Looks like a number
    if TOON_NUMBER_LIKE_RE.match(s):
        return json.dumps(s)

    # If no rules match, it's safe to be unquoted
    return s

def _check_is_primitive(val) -> bool:
    """Checks if a value is a TOON primitive."""
    return val is None or isinstance(val, (str, int, float, bool))

def _check_is_primitive_list(arr: list) -> bool:
    """Checks if a list contains only primitive values."""
    if not arr:
        return True # An empty list is a primitive list
    return all(_check_is_primitive(item) for item in arr)

def _check_is_tabular(arr: list) -> (bool, list | None):
    """
    Checks if a list of objects is "tabular" (all dicts, same keys, primitive values).
    Returns (True, sorted_headers_list) or (False, None).
    """
    if not arr:
        return False, None
    if not all(isinstance(item, dict) for item in arr):
        return False, None

    first_keys = set(arr[0].keys())
    
    # All objects must have the *exact same set of keys*
    if not all(set(item.keys()) == first_keys for item in arr[1:]):
        return False, None
        
    # All values in all objects must be primitives
    for item in arr:
        if not all(_check_is_primitive(val) for val in item.values()):
            return False, None
            
    # Success
    return True, sorted(list(first_keys))


# --- Recursive TOON Encoder Functions ---

def _encode_dict(obj: dict, indent_level: int, indent_str: str, delimiter: str) -> str:
    """Recursively encodes a dictionary's key-value pairs."""
    indent = indent_str * indent_level
    lines = []

    if not obj and indent_level == 0:
        return "" # Special case: root object is empty

    for key, val in obj.items():
        q_key = _quote_toon_key(key)
        
        if isinstance(val, dict):
            if not val:
                # Empty object: key:
                lines.append(f"{indent}{q_key}:")
            else:
                # Nested object
                lines.append(f"{indent}{q_key}:")
                lines.append(_encode_dict(val, indent_level + 1, indent_str, delimiter))
        
        elif isinstance(val, list):
            # Nested list (handled by list encoder)
            lines.append(_encode_list(val, indent_level, indent_str, delimiter, key=q_key))
        
        else:
            # Primitive value
            lines.append(f"{indent}{q_key}: {_quote_toon_value(val, delimiter)}")
            
    return "\n".join(lines)

def _encode_list(arr: list, indent_level: int, indent_str: str, delimiter: str, 
                 key: str | None = None, is_root: bool = False) -> str:
    """
    Recursively encodes a list.
    Handles primitive, tabular, and mixed-content lists.
    """
    indent = indent_str * indent_level

    # 1. Construct the header (e.g., "key[N]:" or "[N]:")
    if is_root:
        header_prefix = f"{indent}[{len(arr)}]"
    elif key:
        header_prefix = f"{indent}{key}[{len(arr)}]"
    else: # List-in-a-list item
        header_prefix = f"{indent}[{len(arr)}]"

    if not arr:
        return f"{header_prefix}:" # key[0]: or [0]:

    # 2. Case: Primitive List (e.g., extracurricular_activities)
    if _check_is_primitive_list(arr):
        vals = [_quote_toon_value(v, delimiter) for v in arr]
        return f"{header_prefix}: {delimiter.join(vals)}"

    # 3. Case: Tabular List (e.g., courses)
    is_tabular, headers = _check_is_tabular(arr)
    if is_tabular:
        lines = [f"{header_prefix}{{{delimiter.join(headers)}}}:"]
        child_indent = indent + indent_str
        for row_obj in arr:
            # .get(h, None) safely handles if a key was missing, though _check_is_tabular prevents this
            row_vals = [_quote_toon_value(row_obj.get(h, None), delimiter) for h in headers]
            lines.append(f"{child_indent}{delimiter.join(row_vals)}")
        return "\n".join(lines)

    # 4. Case: Mixed/Non-Uniform List (e.g., the root ALL_STUDENT_DATA list)
    lines = [f"{header_prefix}:"]
    child_indent = indent + indent_str
    for item in arr:
        if isinstance(item, dict) and item:
            # Encode the dict's items, indented one level deeper
            item_str = _encode_dict(item, indent_level + 1, indent_str, delimiter)
            item_lines = item_str.split('\n')
            
            # First line of dict goes next to the hyphen
            lines.append(f"{child_indent}- {item_lines[0].lstrip()}")
            # The rest of the dict's lines follow
            lines.extend(item_lines[1:])
        
        elif isinstance(item, list):
            # Handle list-in-a-list (e.g., `pairs: - [2]: 1,2`)
            list_str = _encode_list(item, indent_level + 1, indent_str, delimiter)
            lines.append(f"{child_indent}- {list_str.lstrip()}")
        
        else:
            # Primitive item in a mixed list
            lines.append(f"{child_indent}- {_quote_toon_value(item, delimiter)}")
            
    return "\n".join(lines)


# --- Public TOON Converter Function ---

def toon_converter(data, indent_spaces=2, delimiter=","):
    """
    Converts a Python data structure (dict or list) into a TOON-formatted string.

    Args:
        data: The Python list or dict to encode.
        indent_spaces: The number of spaces to use per indentation level (default: 2).
        delimiter: The delimiter to use for arrays (default: ',').

    Returns:
        A string containing the data in TOON format.
    """
    print("Converting Python data to TOON format...")
    indent_str = " " * indent_spaces
    
    if isinstance(data, dict):
        return _encode_dict(data, 0, indent_str, delimiter)
    if isinstance(data, list):
        # The root object is a list (of students)
        return _encode_list(data, 0, indent_str, delimiter, is_root=True)
    
    # Handle primitive root (e.g., toon_converter("hello"))
    return _quote_toon_value(data, delimiter)


# ============================================================================
# PART 3: MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    
    # 1. Generate the sophisticated Python variable
    ALL_STUDENT_DATA = generate_all_student_data()

    # 2. Convert the Python variable to TOON format
    #    (This is the function you requested)
    toon_output = toon_converter(ALL_STUDENT_DATA)

    # 3. Save the converted output to a .toon file
    output_filename = "students.toon"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(toon_output)
        print(f"\nSuccessfully exported TOON data to '{output_filename}'")
    except IOError as e:
        print(f"\nError writing to file: {e}")

    # 4. Print a small snippet to the console for verification
    print("\n--- SNIPPET OF TOON OUTPUT (first 25 lines) ---")
    print("\n".join(toon_output.split('\n')[:25]))
    print("...")