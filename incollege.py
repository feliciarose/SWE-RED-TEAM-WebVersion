# incollege_app.py

import re
from deep_translator import GoogleTranslator
from flask import Flask

app = Flask(__name__)

class InCollegeApp:

  def __init__(self):
    self.profiles = {}
    self.user_credentials = {} 
    self.MAX_ACCOUNTS = 10
    self.applied_jobs = {}
    self.saved_jobs = {}

    self.students = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "ejeyd@example.com",
            "university": "MIT",
            "major": "Computer Science",
            "friend_requests":[],
            "friends": [],
            "user_tier": "Free",
        },
        {
            "first_name": "Lia",
            "last_name": "Homes",
            "email": "lia@gmail.com",
            "university": "Harvard",
            "major": "Physics",
            "friend_requests":["Lia"],
            "friends":[],
            "user_tier": "Free",
        },
        {
          "first_name": "Jane",
          "last_name": "Smith",
          "email": "jane@example.com",
          "university": "Stanford",
          "major": "Mathematics",
          'friend_requests': ["Jane"],
          'friends':["Lia"],
          'user_tier': 'Free',
        }
        # Add more student records as needed
        # Added students 
    ]
      
    
    self.user_credentials = {
        "test": {
            'password': "test",
            'first_name': "test",
            'last_name': "test",
            'email': "test",
            'login_status': False,
            'friend_requests': ["Jane","Lia"],
            'friends': ["John"],
            'user_tier': 'Free',
        },
    }  # Dictionary to store username and password
    self.MAX_ACCOUNTS = 10  # Maximum number of accounts
    self.job_posts = []  # List to store job posts
    self.friends = []  # List to store friends
    self.user_tiers = "Free"  # User tier status

    self.language = "english"  # Default language
    self.email = False  # Email notification status
    self.sms = False  # SMS notification status
    self.targeted_advertising = False  # Targeted ads status
    self.messages = []  # List to store messages

  def create_account(self, username, password, first_name, last_name):
    # Check if maximum number of accounts has been reached
    if len(self.user_credentials) >= self.MAX_ACCOUNTS:
        return "Maximum number of student accounts created."

    # restrictions for password
    if len(password) < 8 or len(password) > 13:
        return "Password must be between 8 and 13 characters."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one capital letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*()_+{}|:\"<>?]", password):
        return "Password must contain at least one special character."

    # Check if username already exists
    if username in self.user_credentials:
        return "Username already exists. Please choose another username."

    # Create the account
    self.user_credentials[username] = {
        'password': password,
        'first_name': first_name,
        'last_name': last_name,
        'login_status': False  # Newly created account should not be logged in automatically
    }

    return "Account created successfully. Please log in."

  def login(self, username, password):
      # Check if username exists
      if username in self.user_credentials:
          # Check if username and password match
          if self.user_credentials[username]['password'] == password:
              # Increment the login attempt counter if it exists
              if 'login_attempts' in self.user_credentials[username]:
                  self.user_credentials[username]['login_attempts'] += 1
              else:
                  self.user_credentials[username]['login_attempts'] = 1
              
              self.user_credentials[username]['login_status'] = True
              # Correct login
              return True
      # Incorrect login or username doesn't exist
      return False



  #---------------- epic 1 -----------------#

  def get_post_login_options(self):

    # added a new option to the list #4 for epic#2
    options_list = [
        "1. Job search/Internship", "2. Find someone you know",
        "3. Learn a new skill", "4. Useful Links",
        "5. InCollege Important Links", "6. Friends List",
        "7. Tier check",
        "8. message management",
        "9. Log out"
    ]
    select_option = "\n".join(options_list)
    print(self.translate_language(select_option))
    selected_option = input(self.translate_language("Select an option: "))
    self.select_option(selected_option)

  def select_option(self, option_number):
    if option_number == "1":
      return self.under_construction()
    elif option_number == "2":
      self.find_person()
    elif option_number == "3":
      self.list_skills()
    elif option_number == "4":
      self.display_useful_links()
    elif option_number == "5":
      self.important_links()
    elif option_number == "6":
      self.friend_management_menu(
      )  # <-- Call the function for friend management
    elif option_number == "7":
      self.user_tier_check()
    elif option_number == "8":
      self.message_management()
    elif option_number == "9":
      print(self.translate_language("You have successfully logged out."))
      self.main_menu()
    else:
      print(self.translate_language("Invalid Option"))

  def friend_management_menu(self):
    print(self.translate_language("Friend Management Menu"))
    friend_management_options = [
        "1. Search and Connect with Friends",
        "2. Manage Pending Friend Requests",
        "3. Other Friend Management Options",  # Add more options as needed
        "4. Return to Previous Menu"
    ]
    friend_management_menu = "\n".join(friend_management_options)
    print(self.translate_language(friend_management_menu))
    selected_option = input(self.translate_language("Select an option: "))

    if selected_option == "1":
      self.search_and_connect_friends(
      )  # <-- Call the function for searching and connecting
    elif selected_option == "2":
      self.manage_pending_friend_requests(username="test")  # <-- Call the function for managing pending requests
    elif selected_option == "3":
      self.other_friend_management_options(
      )  # <-- Add more options and functions
    elif selected_option == "4":
      self.get_post_login_options()  # <-- Return to the post-login menu
    else:
      print(self.translate_language("Invalid Option"))

  def list_skills(self):
    skills = [
        "1. Programming", "2. Data Analysis", "3. Graphic Design",
        "4. Digital Marketing", "5. Project Management",
        "6. return to previous level"
    ]
    skill_options = "\n".join(skills)
    print(self.translate_language(skill_options))
    print("\nSelect a skill to learn.")
    selected_skill = input(self.translate_language("Enter a number: "))
    self.select_skill(selected_skill)

  def select_skill(self, skill_number):
    if skill_number in ["1", "2", "3", "4", "5"]:
      print(self.under_construction())
    elif skill_number == "6":
      self.get_post_login_options()
    else:
      print(self.translate_language("Invalid Option"))

  #---------------- epic 2 -----------------#

  def display_success_story_and_video_option(self):
    success_story = "Meet Hideo Kojima, a recent graduate who landed their dream job at a top tech company using InCollege."
    print(self.translate_language(success_story))

    play_video_option = input(
        self.translate_language("Would you like to watch a video?") +
        " (y/n): ")
    if play_video_option.lower() == "y":
      print(self.translate_language("Video is now playing."))
    else:
      print(self.translate_language("Thank you for visiting InCollege."))\

  def post_job(self, username, title=None, description=None, employer=None, location=None, salary=None, role=None, experience_level=None):
      if len(self.job_posts) >= 5:
          return self.translate_language("Maximum number of jobs posted. Please try again later.")

      # Append the job details to the job_posts list
      self.job_posts.append({
          'title': title,
          'description': description,
          'employer': employer,
          'location': location,
          'salary': salary,
          'role': role,
          'experience_level': experience_level
      })

      return self.translate_language("Job posted successfully.")


  def find_person(self):
    first_name = input(self.translate_language("Enter the first name of the person you are looking for: "))
    last_name = input(self.translate_language("Enter the last name of the person you are looking for: "))

    for user_info in self.user_credentials.values():
        if user_info['first_name'].lower() == first_name and user_info['last_name'].lower() == last_name:
            print(self.translate_language("They are a part of the InCollege system."))
    print(self.translate_language("They are not a part of the InCollege system."))

  def main_menu(self):
    self.choose_language()
    menu_options = [
        "Welcome to InCollege", "Main Menu", "1. Create Account", "2. Login",
        "3. View Success Story and Video", "4. Exit", "5. Useful Links",
        "6. InCollege Important Links"
    ]
    menu = "\n".join(menu_options)
    print(self.translate_language(menu))

    # print("\nWelcome to InCollege")
    # print("\nMain Menu")
    # print("\n1. Create Account")
    # print("\n2. Login")
    # print("\n3. View Success Story and Video")
    # print("\n4. Exit")

    choice = input(self.translate_language("\nSelect an option: "))

    if choice == "1":
      username = input(self.translate_language("Enter your username: "))
      password = input(self.translate_language("Enter your password: "))
      self.create_account(username, password)
    elif choice == "2":
      username = input(self.translate_language("Enter your username: "))
      password = input(self.translate_language("Enter your password: "))
      login_result = self.login(username, password)
      print(login_result)
      if login_result == self.translate_language(
          "You have successfully logged in"):
        self.get_post_login_options()
    elif choice == "3":
      self.display_success_story_and_video_option()
    elif choice == "4":
      print(self.translate_language("Thank you for visiting InCollege."))
    elif choice == "5":
      self.display_useful_links()
    elif choice == "6":
      self.important_links()
    else:
      print(self.translate_language("Invalid Option"))

  #---------------- epic 3 --------------------------------#

  def any_user_logged_in(self):
    return any(user_info['login_status']
               for user_info in self.user_credentials.values())

  def translate_language(self, msg):
    if self.language.lower() == 'spanish':
      translated = GoogleTranslator(source='en', target='es').translate(msg)
      return translated
    else:
      return msg

  def under_construction(self):
    return self.translate_language("Under construction.")

  def display_useful_links(self):
    useful_links = [
        "1. General", "2. Browse InCollege", "3. Business Solutions",
        "4. Directories", "5. return to previous level"
    ]
    useful_links_options = "\n".join(useful_links)
    print(self.translate_language(useful_links_options))
    print(self.translate_language("\nSelect a link to view."))
    selected_link = input(self.translate_language("Enter a number: "))
    self.select_useful_link(selected_link)

  def select_useful_link(self, link_number):
    if link_number == "1":
      self.display_general_links()
    elif link_number in ["2", "3", "4"]:
      print(self.under_construction())
    elif link_number == "5":
      if self.any_user_logged_in():
        self.get_post_login_options()
      else:
        self.main_menu()
    else:
      print(self.translate_language("Invalid Option"))

  def display_general_links(self):
    general_links = [
        "1. Sign up", "2. Help Center", "3. About", "4. Press", "5. Blog",
        "6. Careers", "7. Developers", "8. Go back to previous level"
    ]
    general_links_options = "\n".join(general_links)
    print(self.translate_language(general_links_options))
    print(self.translate_language("\nSelect a link to view."))
    selected_link = input(self.translate_language("Enter a number: "))
    self.select_general_link(selected_link)

  def select_general_link(self, link_number):
    if link_number == "1":
      username = input(self.translate_language("Enter your username: "))
      password = input(self.translate_language("Enter your password: "))
      self.create_account(username, password)
    elif link_number == "2":
      print(self.translate_language("\nWe're here to help"))
    elif link_number == "3":
      print(
          self.translate_language(
              "\nIn College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
          ))
    elif link_number == "4":
      print(
          self.translate_language(
              "\nIn College Pressroom: Stay on top of the latest news, updates, and reports"
          ))
    elif link_number in ["5", "6", "7"]:
      print(self.under_construction())
    elif link_number == "8":
      self.display_useful_links()
    else:
      print(self.translate_language("Invalid Option"))

  """
    def display_important_links(self):
        important_links = [
            "1. Copyright Notice",
            "2. About",
            "3. Brand Policy",
            "4. Guest Controls",
            "5. Languages",
            "6. return to previous level"
        ]
        important_links_options = "\n".join(important_links)
        print(important_links_options)
        print("\nSelect a link to view.")
        selected_link = input("Enter a number: ")
        self.select_important_link(selected_link)


    def select_important_link(self, link_number):
        if link_number in ["1", "2", "3", "4"]:
            return self.under_construction()
        elif link_number == "5":
            self.display_languages()
        elif link_number == "6":
            if self.any_user_logged_in():
                self.get_post_login_options()
            else:
                self.main_menu()
        else:
            return "Invalid Option"

    def display_languages(self):
        languages = [
            "1. English",
            "2. Spanish"
        ]
        languages_options = "\n".join(languages)
        print(languages_options)
        print("\nSelect a language.")
        selected_language = input("Enter a number: ")
        self.select_language(selected_language)

    def select_language(self, language_number):
        if language_number in ["1", "2"]:
            return self.set_language(language_number)
        else:
            return "Invalid Option"

    def set_language(self, language_number):
        if language_number == "1":
            self.current_language = "English"
        elif language_number == "2":
            self.current_language = "Spanish"

        if self.any_user_logged_in():
            self.get_post_login_options()
        else:
            self.main_menu()

    """

  def important_links(self):
    links = [
        "1. Copyright Notice", "2. About", "3. Accessibility",
        "4. User Agreement", "5. Privacy Policy", "6. Cookie Policy",
        "7. Copyright Policy", "8. Brand Policy", "9. Back to previous"
    ]
    link_options = "\n".join(links)
    return self.translate_language(link_options + "\nSelect a link to visit.")

  # will need to be changed if we are given information about the links
  def select_link(self, link_number):
    if link_number in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
      return self.translate_language("Under construction.")
    else:
      return self.translate_language("Invalid Option")

  def guest_controls(self):
    settings = [
        "1. Email", "2. SMS", "3. Targeted Advertising", "4. Back to previous"
    ]
    setting_options = "\n".join(settings)
    return self.translate_language(setting_options +
                                   "\nSelect a setting to change.")

  def toggle_guest_controls(self, setting_number):
    if setting_number in "1":
      self.email = not self.email
      return self.translate_language(
          "Email notifications have been turned off.")
    elif setting_number in "2":
      self.sms = not self.sms
      return self.translate_language("SMS notifications have been turned off.")
    elif setting_number in "3":
      self.targeted_advertising = not self.targeted_advertising
      return self.translate_language(
          "Targeted advertising has been turned off.")
    elif setting_number in "4":
      print(
          self.translate_language("Returning to Post Login.")
      )  # i dont know where exiting this menu goes back to but i assume main menu
      return self.get_post_login_options()
    else:
      return self.translate_language("Invalid Option")

  def choose_language(self):
    language = input("Choose a language: ")
    if language.lower() in ['english', 'spanish']:
      self.language = language
      return f"Language has been set to {language}."
    else:
      return "Invalid language. Please choose English or Spanish."


# ----------------------- epic 4 -----------------------#

# task 1 above
# ------------- task 2 -------------------------------#

  def friends_list(self):
    if self.friends == []:
      print(self.translate_language("You currently have no friends."))
    else:
      for friend in self.friends:
        print(friend)
      print(self.translate_language("End of friends list."))

    # Return to the post-login menu
    self.get_post_login_options()

  # -------- task 3 -------------------------------#
  def search_students(self, last_name=None, university=None, major=None):
    matching_students = []
    for student in self.students:
        if (last_name and student['last_name'].lower() == last_name.lower()) or \
           (university and 'university' in student and student['university'].lower() == university.lower()) or \
           (major and 'major' in student and student['major'].lower() == major.lower()):
            matching_students.append(student)
    return matching_students

  def search_and_connect_friends(self):
    print(self.translate_language("Find someone you know"))
    search_criteria = input(
        "Do you want to search by last name, university, or major? ").strip(
        ).lower()
    search_value = input(f"Enter the {search_criteria}: ").strip()
    if search_criteria == 'last name':
      results = self.search_students(last_name=search_value)
    elif search_criteria == 'university':
      results = self.search_students(university=search_value)
    elif search_criteria == 'major':
      results = self.search_students(major=search_value)
    if results:
      print(f"Found {len(results)} matching student(s):")
      for student in results:
          print(f"- {student['first_name']} {student['last_name']}, Email: {student['email']}, University: {student.get('university', 'N/A')}, Major: {student.get('major', 'N/A')}")
      # Ask user if they want to send a friend request to the first matching user
      send_request = input("Do you want to send a friend request to the first matching user? (yes/no): ").strip().lower()
      if send_request == 'yes' and results:
        print(f"Friend request sent to {results[0]['email']}.")
    else:
      print(
          "Invalid search criteria. Please choose 'last name', 'university', or 'major'."
      )
      return
    

  def send_friend_request(self, sender_username, receiver_username):

    # Check if sender and receiver exist
    if sender_username in self.user_credentials and receiver_username in self.user_credentials:
      sender_info = self.user_credentials[sender_username]
      receiver_info = self.user_credentials[receiver_username]

      # Check privacy settings and permissions
      if sender_info['login_status'] and receiver_info['login_status']:
        # Assuming a simple friends list without confirmation for now
        self.friends.append({
            'sender_username': sender_username,
            'receiver_username': receiver_username
        })
        return self.translate_language(
            f"Friend request sent to {receiver_info['first_name']} {receiver_info['last_name']}."
        )
      else:
        return self.translate_language(
            "Cannot send friend request. Check user login status.")
    else:
      return self.translate_language("Invalid sender or receiver username.")


# ------------------ task4 ----------------------------------------
  def manage_pending_friend_requests(self, username):
    # Check if the user exists in user_credentials
    if username not in self.user_credentials:
        print(f"No user found with username: {username}")
        return

    user_data = self.user_credentials[username]
    friend_requests = user_data['friend_requests']
    friends = user_data['friends']

    # Iterate over a copy of the list to safely modify the original list
    for request in friend_requests[:]:
        response = input(f"Do you want to accept the friend request from {request}? (accept/reject): ").strip().lower()
        if response == 'accept':
            friends.append(request)  # Add to friends list
            print(f"Friend request from {request} accepted.")
        else:
            print(f"Friend request from {request} rejected.")
        friend_requests.remove(request)  # Remove from friend_requests regardless of accept/reject

    # Update the user data
    self.user_credentials[username]['friend_requests'] = friend_requests
    self.user_credentials[username]['friends'] = friends
    print("updated friends list",self.user_credentials["test"]["friends"])


# ----------------------- epic 5 -----------------------#

# ------------------ task4 ----------------

  def create_profile(self, username, profile_title, major, university, about='', experience=[], education=''):
    major = major.capitalize()
    university = university.capitalize()

    # Check if the username exists in user_credentials
    if username not in self.user_credentials:
        print(f"Error: User with username '{username}' does not exist.")
        return

    # Create the profile
    self.profiles[username] = {
        'profile_title': profile_title,
        'major': major,
        'university': university,
        'about': about,
        'experience': experience[:3], 
        'education': education
    }

    # Print the saved profile
    print(f"Profile saved for {username}: {self.profiles[username]}")

  def view_profile(self, username):
      return self.profiles.get(username, {})



# ----------------------- epic 6 -----------------------#


# ------------------ task3 ---------------- 

  def job_search(self, company=None, role=None, experience_level=None):
      filtered_jobs = self.job_posts

      if company:
          filtered_jobs = [job for job in filtered_jobs if job.get('employer') == company]

      if role:
          filtered_jobs = [job for job in filtered_jobs if job.get('role') == role]

      if experience_level:
          filtered_jobs = [job for job in filtered_jobs if job.get('experience_level') == experience_level]

      return filtered_jobs

  def apply_for_job(self, username, job_title, job_description, employer, location, salary, role, experience_level):
      # Store the job details in the applied_jobs dictionary
      job_details = {
          'title': job_title,
          'description': job_description,
          'employer': employer,
          'location': location,
          'salary': salary,
          'role': role,
          'experience_level': experience_level
      }

      if username in self.applied_jobs:
          self.applied_jobs[username].append(job_details)
      else:
          self.applied_jobs[username] = [job_details]
          
      self.applied_jobs.setdefault(username, 0)
      self.applied_jobs[username] += 1
      
      if self.applied_jobs[username] == 5:
          self.user_tiers[username] = 'Silver'
      elif self.applied_jobs[username] == 10:
          self.user_tiers[username] = 'Gold'
          
      
  def save_job(self, username, job_title, job_description, employer, location, salary, role, experience_level):
      # Create a dictionary with the job details
      job_details = {
          'title': job_title,
          'description': job_description,
          'employer': employer,
          'location': location,
          'salary': salary,
          'role': role,
          'experience_level': experience_level
      }
      
      # Check if the username already has saved jobs
      if username in self.saved_jobs:
          # Append the job details to the existing list of saved jobs
          self.saved_jobs[username].append(job_details)
      else:
          # Create a new list with the job details as the first item
          self.saved_jobs[username] = [job_details]

  def remove_job(self, username, job_title, job_description, employer, location, salary, role, experience_level):
    job_details = {
        'title': job_title,
        'description': job_description,
        'employer': employer,
        'location': location,
        'salary': salary,
        'role': role,
        'experience_level': experience_level
    }
    
    # Check if the username already has saved jobs
    if username in self.saved_jobs:
        # Append the job details to the existing list of saved jobs
      self.saved_jobs[username].remove(job_details)
      return {"line":"Job removed successfully.","status":"removed"}
    else:
      return {"line":"No Such Job for this User","status":"not removed"}

  
  #BACKEND USE ONLY! No display!
  def calculate_jobs_not_applied(self):
        jobs_not_applied = []

        # Extract job IDs from job_posts
        applied_job_ids = [job['id'] for job in self.job_posts]

        # Iterate over all jobs
        for job_id, job_details in self.all_jobs.items():
            if job_id not in applied_job_ids:
                jobs_not_applied.append((job_id, job_details))

        return jobs_not_applied
      
# ----------------------- epic 7 -----------------------#
# ------------------ task 2 ------------------#

  def user_tier_check(self):
    username = input(self.translate_language("Enter the username to check the tier: "))
    if username in self.user_tiers:
        print (self.translate_language(f"{username} is at the {self.user_tiers[username]} tier."))
        print (self.translate_language("Would you like to upgrade the tier?"))
        upgrade = input(self.translate_language("Enter 'yes' to upgrade or 'no' to cancel: "))
        if upgrade.lower() == 'yes':
            tier = input(self.translate_language("Tier upgrade price: Silver ($10) or Gold ($20)"))
            price = float(input(self.translate_language("Enter the payment amount: ")))
            self.purchase_tier_upgrade(username, tier, price)
        else:
            print(self.translate_language("Tier upgrade canceled."))
            self.get_post_login_options()
    else:
        print(self.translate_language("User tier not found."))
        self.get_post_login_options()

  def purchase_tier_upgrade(self, username, tier, price):
    if username in self.user_tiers:
        current_tier = self.user_tiers[username]
        if current_tier == 'Free':
            if tier == 'Silver' and price >= 10:
                self.user_tiers[username] = 'Silver'
                print(self.translate_language("Tier upgraded to Silver."))
                self.get_post_login_options()
            elif tier == 'Gold' and price >= 20:
                self.user_tiers[username] = 'Gold'
                print(self.translate_language("Tier upgraded to Gold."))
                self.get_post_login_options()
            else:
                print(self.translate_language("Insufficient payment for the selected tier upgrade."))
                self.get_post_login_options()
        elif current_tier == 'Silver':
            if tier == 'Gold' and price >= 10:
                self.user_tiers[username] = 'Gold'
                print(self.translate_language("Tier upgraded to Gold."))
                self.get_post_login_options()
            else:
                print(self.translate_language("Insufficient payment for the selected tier upgrade."))
                self.get_post_login_options()
        else:
            print(self.translate_language("You are already at the highest tier."))
            self.get_post_login_options()
    else:
        print(self.translate_language("User not found or not eligible for tier upgrade."))
        self.get_post_login_options()
      
# ------------------ task 1 & 3 ------------------#

  def message_management(self, user=None):
    new_msg = [msg for msg in self.messages if not msg['read']]
    if user is None:
      user = "test"
    else:
      user = self.user_credentials['username']
    print(self.translate_language("Message Management"))
    if new_msg:
        print(self.translate_language(f"You have {len(new_msg)} new messages.\n"))
    message_options = [
        "1. Send Message",
        "2. View Messages",
        "3. Return to Previous Menu"
    ]
    message_menu = "\n".join(message_options)
    print(self.translate_language(message_menu))
    selected_option = input(self.translate_language("Select an option: "))

    if selected_option == "1":
        if self.user_credentials[user]['user_tier'] == 'Gold':
            self.send_message(user)
        elif self.user_credentials[user]['user_tier'] == 'Silver':
            friend_username = input(self.translate_language("Enter your friend's username: "))
            if friend_username in self.user_credentials[user]['friends']:
                self.send_message(user,recipient=friend_username)
            else:
                print(self.translate_language("You can only message friends at Silver tier."))
        else:
            print(self.translate_language("You must upgrade to at least Silver tier to send messages."))
        # self.message_management() #commented out to avoid recursion error in testing
    elif selected_option == "2":
        self.view_messages()
    elif selected_option == "3":
        self.get_post_login_options()
    else:
        print(self.translate_language("Invalid Option, please try again."))
        self.message_management()

  def send_message(self, user, recipient=None):
    if recipient is None:
        recipient = input(self.translate_language("Enter the recipient's username: "))
    message = input(self.translate_language("Enter your message: "))
    self.messages.append({
        'sender': self.user_credentials[user],
        'recipient': recipient,
        'message': message,
        'read': False
    })
    print(self.translate_language("Message sent successfully."))
    
  def view_messages(self):
    if self.messages:
      if message['recipient'] == self.user_credentials['username']:
        for message in self.messages:
            print(f"From: {message['sender']}\nMessage: {message['message']}")
            message['read'] = True
    else:
        print(self.translate_language("No messages found."))
        # self.message_management() #commented out to avoid recursion error in testing