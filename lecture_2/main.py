
def generate_profile(age: int) -> str:
    """Determine user's life stage based on age."""
    if 0 <= age <= 12:
        return "Child"
    elif 13 <= age <= 19:
        return "Teenager"
    elif age >= 20:
        return "Adult"
    else:
        return "Incorrect age"

print("Hello!")
user_name = input("Enter your full name: ") # Asking a user to enter their full name

birth_year_str = input("Enter your birth year: ") # Asking a user to enter their year of birth and storing it as string
if birth_year_str.isdigit():
    birth_year = int(birth_year_str) # Converting birth year to type integer
current_age = 2025 - birth_year # Calculating the user's current age

hobbies = [] # Creating an empty list hobbies

# Using a loop to repeatedly ask the user to enter a hobbies and collecting them until we get a string 'stop'
while True:
    current_hobby = input("Enter a favorite hobby or type 'stop' to finish: ")
    if current_hobby.lower() == "stop":
        break
    hobbies.append(current_hobby)

life_stage = generate_profile(age=current_age) # Calling generate_profile function, passing current_age as an argument

# Creating a dictionary called user_profile to store name, age, stage and the hobbies
user_profile = {"name": user_name,
                "age": current_age,
                "stage": life_stage,
                "hobbies": hobbies}

# Printing user's profile using f-strings
print()
print("---")
print("Profile Summary:")
print(f"Name: {user_profile['name']}")
print(f"Age: {user_profile['age']}")
print(f"Life Stage: {user_profile['stage']}")

# Checking if the hobbies list is empty and printing a hobbies
if not hobbies:
    print("You didn't mention any hobbies.")
else:
    print(f"Favorite Hobbies ({len(hobbies)}):")
    print("\n".join(f"- {hobby}" for hobby in user_profile["hobbies"]))

print("---")


