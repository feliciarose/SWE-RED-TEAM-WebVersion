import pytest
from unittest.mock import patch
from incollege import InCollegeApp


@pytest.fixture
def app():
    return InCollegeApp()

# ----------------- Epic 1 ----------------- #
def test_successful_account_creation(app, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "User1")
    result = app.create_account("user1", "ValidPass123!")
    assert result == "Account created successfully", "Account should be created successfully with valid credentials"

def test_account_creation_with_invalid_password(app):
    result = app.create_account("user2", "pass")
    assert "Password must" in result, "Account should not be created with an invalid password"

def test_account_creation_with_invalid_password_CAPITAL(app):
    result = app.create_account("user2", "pass1234!")
    assert "Password must" in result, "Account should not be created with an invalid password"

def test_account_creation_with_invalid_password_digit(app):
    result = app.create_account("user2", "passWord!")
    assert "Password must" in result, "Account should not be created with an invalid password"

def test_account_creation_with_invalid_password_special(app):
    result = app.create_account("user2", "passW0rds")
    assert "Password must" in result, "Account should not be created with an invalid password"

# def test_account_creation_limit(app, monkeypatch):
#     monkeypatch.setattr('builtins.input', lambda _: "User1")
#     for i in range(1, 6):
#         app.create_account(f"user{i}", "ValidPass123!")

#     result = app.create_account("user6", "ValidPass123!")
#     assert result == "Maximum number of student accounts created.", "Should not allow creating more than 5 accounts"

def test_successful_login(app, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "user1")
    app.create_account("user1", "ValidPass123!")
    result = app.login("user1", "ValidPass123!")
    assert result == "You have successfully logged in", "Login should be successful with correct credentials"

def test_failed_login(app):
    result = app.login("nonexistent_user", "wrongpassword")
    assert result == "Incorrect username / password, please try again.", "Login should fail with incorrect credentials"

def test_post_login_options(app):
    result = app.get_post_login_options()
    assert result == "1. Job search/Internship\n2. Find someone you know\n3. Learn a new skill\n4. Log out / return to previous level", "Post-login options should be correctly listed"

@pytest.mark.parametrize("option_number, expected_result", [
    ("1", None),
    ("2", "part of the InCollege system."),
    ("3", "1. Programming\n2. Data Analysis\n3. Graphic Design\n4. Digital Marketing\n5. Project Management\n6. return to previous level\nSelect a skill to learn."),
    ("4", "You have been logged out."),
    ("5", "Invalid Option")  # Test an invalid option
])

def test_select_option(app, option_number, expected_result, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "user1")
    app.create_account("user1", "ValidPass123!")
    result = app.select_option(option_number, "user1")
    assert result == expected_result or expected_result in result, f"Response for option number '{option_number}' should be correct"

def test_select_skill(app):
    result = app.select_skill("1")
    assert result == "Under construction.", "Selecting a skill should be under construction"

    result = app.select_skill("6")
    assert result == "1. Job search/Internship\n2. Find someone you know\n3. Learn a new skill\n4. Log out / return to previous level", "Selecting the last skill should return to previous level"

    result = app.select_skill("7")
    assert result == "Invalid Option", "Selecting an invalid skill should return an invalid option message"

# ----------------- Epic 2 ----------------- #

def test_view_success_story_and_video(app,monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "yes")
    result = app.display_success_story_and_video_option()
    assert result == "Video is now playing.", "Success story should be correctly listed and video should be played"

    
def test_view_success_story_and_no_video(app,monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "no")
    result = app.display_success_story_and_video_option()
    assert result == "Thank you for visiting InCollege.", "Success story should be correctly listed and thank you message should be displayed"

def custom_post_job_input(msg):
    if msg == "Enter your username: ":
        return "user1"
    else:
        return "user1"


def test_post_job(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "user1")
    result = app.post_job("user1")
    out, err = capfd.readouterr()
    assert "Job posted successfully." in out, "Job should be posted successfully"
    

def test_post_job_max_limit(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "user1")
    app.create_account("user1", "ValidPass123!")
    
    
    for i in range(1, 6):
        app.post_job("user1")
        out, err = capfd.readouterr()
        assert "Job posted successfully." in out, "Should allow posting up to 5 jobs"

    app.post_job("user1")
    out, err = capfd.readouterr()
    assert "Maximum number of jobs posted. Please try again later." in out, "Should not allow posting more than 5 jobs"

def custom_find_person_input(msg):
    if msg == "Enter the first name of the person you are looking for: ":
        return "user1"
    elif msg == "Enter the last name of the person you are looking for: ":
        return "user1"
    else:
        return "user1"

def test_find_person_fail(app, monkeypatch):
    monkeypatch.setattr('builtins.input', custom_find_person_input)
    result = app.find_person()
    assert result == "They are not a part of the InCollege system.", "Find person should fail if the person is not found"

def test_find_person_success(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', custom_find_person_input)
    app.create_account("user1", "ValidPass123!")
    result = app.find_person()
    assert result == "They are a part of the InCollege system." , "Find person should succeed if the person is found"

def custom_main_menu_input_for_create_account(msg):
    if msg == "\nSelect an option: ":
        return "1"
    elif msg == "Enter your username: ":
        return "user1"
    elif msg == "Enter your password: ":
        return "ValidPass123!"
    else:
        return "user1"


def test_main_menu_create_account(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', custom_main_menu_input_for_create_account)
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "Account created successfully" in out, "Create account should be successful with valid credentials"


def custom_main_menu_input_for_login_and_job_post(msg):
    if msg == "\nSelect an option: ": #for main menu option
        return "2"
    if msg == "Select an option: ": #for post login option
        return "1"
    elif msg == "Enter your username: ":
        return "user1"
    elif msg == "Enter your password: ":
        return "ValidPass123!"
    else:
        return "user1"
    
def test_main_menu_login_and_job_post(app, capfd, monkeypatch):
    
    monkeypatch.setattr('builtins.input', custom_main_menu_input_for_login_and_job_post)

    app.create_account("user1", "ValidPass123!")
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "Job posted successfully." in out, "Login should be successful and job post should be successful"

def custom_main_menu_input_for_login_and_didnt_find_person(msg):
    if msg == "\nSelect an option: ": #for main menu option
        return "2"
    if msg == "Select an option: ": #for post login option
        return "2"
    elif msg == "Enter your username: ":
        return "user1"
    elif msg == "Enter your password: ":
        return "ValidPass123!"
    elif msg == "Enter the first name of the person you are looking for: ":
        return "user2"
    elif msg == "Enter the last name of the person you are looking for: ":
        return "user2"
    else:
        return "user1"
    
def test_main_menu_login_and_didnt_find_person(app, capfd, monkeypatch):
    
    monkeypatch.setattr('builtins.input', custom_main_menu_input_for_login_and_didnt_find_person)

    app.create_account("user1", "ValidPass123!")
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "They are not a part of the InCollege system." in out, "Login should be successful and find person should be successful"

def custom_main_menu_input_for_login_and_find_person(msg):
    if msg == "\nSelect an option: ": #for main menu option
        return "2"
    if msg == "Select an option: ": #for post login option
        return "2"
    elif msg == "Enter your username: ":
        return "user1"
    elif msg == "Enter your password: ":
        return "ValidPass123!"
    elif msg == "Enter the first name of the person you are looking for: ":
        return "user1"
    elif msg == "Enter the last name of the person you are looking for: ":
        return "user1"
    else:
        return "user1"
    
def test_main_menu_login_and_find_person(app, capfd, monkeypatch):
    
    monkeypatch.setattr('builtins.input', custom_main_menu_input_for_login_and_find_person)

    app.create_account("user1", "ValidPass123!")
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "They are not a part of the InCollege system." in out, "Login should be successful and find person should be successful"

def custom_main_menu_input_success_story_and_video(msg):
    if msg == "\nSelect an option: ":
        return "3"
    elif msg =="Would you like to watch a video? (yes/no): ":
        return "Yes"
    else:
        return "user1"


def test_main_menu_success_story_and_video(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', custom_main_menu_input_success_story_and_video)
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "Video is now playing." in out, "Success story should be correctly listed and video should be played"

def custom_main_menu_input_success_story_without_video(msg):
    if msg == "\nSelect an option: ":
        return "3"
    elif msg =="Would you like to watch a video? (yes/no): ":
        return "No"
    else:
        return "user1"

def test_main_menu_success_story_without_video(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', custom_main_menu_input_success_story_without_video)
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "Thank you for visiting InCollege." in out, "Success story should be correctly listed and thank you message should be displayed"

def test_main_menu_goodbye(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "4")
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "Thank you for visiting InCollege." in out, "Goodbye message should be displayed"

def test_main_menu_invalid(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "5")
    result = app.main_menu()
    out, err = capfd.readouterr()
    assert "Invalid Option" in out, "Invalid option should be handled correctly"

# ----------------- Epic 3 -----------------  #

def test_any_user_logged_in(app):
        # Ensure the method returns a boolean value
        result = app.any_user_logged_in()
        assert isinstance(result, bool)

def test_translate_language(app):
        # Ensure the method returns a string
        msg = "Hello, World!"
        result = app.translate_language(msg)
        assert isinstance(result, str)

def test_under_construction(app):
        # Ensure the method returns a string
        result = app.under_construction()
        assert isinstance(result, str)

def test_display_useful_links(app, capsys, monkeypatch):
        # Simulate user input to select a link
        monkeypatch.setattr('builtins.input', lambda _: "1")
        app.display_useful_links()

        # Capture the output and check if it contains the expected options menu
        captured = capsys.readouterr()
        assert "1. General" in captured.out  # Adjust based on actual output


def test_select_useful_link(app, monkeypatch, capsys):
        # Simulate user input to select a link
        monkeypatch.setattr('builtins.input', lambda _: "1")
      
        # Check if the method performs the expected action
        app.select_useful_link("1")
      
        # Capture the output and check if it contains the expected options menu
        captured = capsys.readouterr()
        assert "1. Sign up" in captured.out  # Adjust based on actual output

def test_any_user_logged_in_with_logged_in_user(app):
    # Assuming user_credentials is properly set up with at least one user logged in
    app.user_credentials = {
        "user1": {"login_status": True},
        "user2": {"login_status": False}
    }
    assert app.any_user_logged_in() == True

def test_any_user_logged_in_with_no_logged_in_user(app):
    # Assuming user_credentials is properly set up with no user logged in
    app.user_credentials = {
        "user1": {"login_status": False},
        "user2": {"login_status": False}
    }
    assert app.any_user_logged_in() == False

def test_under_construction(app):
    assert app.under_construction() == "Under construction."

def test_select_general_link_help_message(app, capfd):
    app.select_general_link("2")
    out, _ = capfd.readouterr()
    assert "We're here to help" in out, "Help message should be displayed"

def test_select_useful_link_under_construction(app, monkeypatch, capfd):
    for link_number in ["2", "3", "4"]:
        monkeypatch.setattr('builtins.input', lambda _: link_number)
        app.select_useful_link(link_number)
        out, _ = capfd.readouterr()
        assert "Under construction" in out, f"Option {link_number} should be under construction"

def test_select_useful_link_invalid_option(app, monkeypatch, capfd):
    monkeypatch.setattr('builtins.input', lambda _: "invalid")
    app.select_useful_link("invalid")
    out, _ = capfd.readouterr()
    assert "Invalid Option" in out, "Invalid Option should be displayed"

def test_select_general_link_help_center():
    link_number = "2"
    expected_output = "We're here to help"
    
    instance = InCollegeApp()  # Instantiate your class
    with patch('builtins.print') as mock_print:
        instance.select_general_link(link_number)
        mock_print.assert_called_with(instance.translate_language("\n" + expected_output))

def test_select_general_link_about():
    link_number = "3"
    expected_output = "In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide"
    
    instance = InCollegeApp()  # Instantiate your class
    with patch('builtins.print') as mock_print:
        instance.select_general_link(link_number)
        mock_print.assert_called_with(instance.translate_language("\n" + expected_output))

def test_select_general_link_pressroom():
    link_number = "4"
    expected_output = "In College Pressroom: Stay on top of the latest news, updates, and reports"
    
    instance = InCollegeApp()  # Instantiate your class
    with patch('builtins.print') as mock_print:
        instance.select_general_link(link_number)
        mock_print.assert_called_with(instance.translate_language("\n" + expected_output))

def test_select_general_link_display_useful_links():
    link_number = "8"
    
    instance = InCollegeApp()  # Instantiate your class
    with patch.object(instance, 'display_useful_links') as mock_display_useful_links:
        instance.select_general_link(link_number)
        mock_display_useful_links.assert_called_once()

def test_select_general_link_invalid_option():
    link_number = "9"
    expected_output = "Invalid Option"
    
    instance = InCollegeApp()  # Instantiate your class
    with patch('builtins.print') as mock_print:
        instance.select_general_link(link_number)
        mock_print.assert_called_with(instance.translate_language(expected_output))
        
# ----------------- Epic 4 -----------------  #
        
def test_account_creation_limit(app, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "User1")
    for i in range(1, 11):
        app.create_account(f"user{i}", "ValidPass123!")

    result = app.create_account("user11", "ValidPass123!")
    assert result == "Maximum number of student accounts created.", "Should not allow creating more than 10 accounts"

def test_friends_list_no_friends(app):
    app.friends = []
    with patch('incollege.InCollegeApp.translate_language') as mocked_translate_language:
        mocked_translate_language.return_value = "Translated message"
        result = app.friends_list()
        mocked_translate_language.assert_called_with("You currently have no friends.")
        assert result == "Translated message"

def test_friends_list_with_friends(app):
    app.friends = ['Alice', 'Bob', 'Charlie']
    with patch('incollege.InCollegeApp.translate_language') as mocked_translate_language:
        mocked_translate_language.return_value = "Translated message"
        with patch('builtins.print') as mocked_print:
            result = app.friends_list()
            mocked_translate_language.assert_called_with("End of friends list.")
            assert result == "Translated message"
            mocked_print.assert_any_call('Alice')
            mocked_print.assert_any_call('Bob')
            mocked_print.assert_any_call('Charlie')
            
# ---- F----

def test_search_by_last_name(app):
    # Create a mock list of students
    app.matching_students = [
        {'first_name': 'John', 'last_name': 'Doe', 'university': 'Stanford', 'major': 'Computer Science'},
        {'first_name': 'Alice', 'last_name': 'Smith', 'university': 'MIT', 'major': 'Electrical Engineering'},
        {'first_name': 'Bob', 'last_name': 'Jones', 'university': 'Harvard', 'major': 'Biology'}
    ]
    
    result = app.search_students(last_name='Doe')
    assert len(result) == 1
    assert result[0]['first_name'] == 'John'


def test_search_and_connect_friends(app, monkeypatch, capsys):
    search_results = [{'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'university': 'Stanford', 'major': 'Computer Science'}]
    with patch.object(app, 'translate_language') as mocked_translate_language:
        mocked_translate_language.return_value = "Find someone you know"
        user_inputs = ['last name', 'Doe', 'yes']
        monkeypatch.setattr('builtins.input', lambda _: user_inputs.pop(0))
        with patch.object(app, 'search_students') as mocked_search_students:
            mocked_search_students.return_value = search_results  
            app.search_and_connect_friends()
    captured = capsys.readouterr()
    assert "Find someone you know" in captured.out
    assert "Do you want to search by last name, university, or major? " not in captured.out
   
def test_send_friend_request_success(app):
    app.user_credentials = {
        'sender_username': {'login_status': True, 'first_name': 'Sender', 'last_name': 'User'},
        'receiver_username': {'login_status': True, 'first_name': 'Receiver', 'last_name': 'User'}
    }
    
    result = app.send_friend_request('sender_username', 'receiver_username')
    assert result == "Friend request sent to Receiver User."
    assert len(app.friends) == 1
    assert app.friends[0] == {'sender_username': 'sender_username', 'receiver_username': 'receiver_username'}

def test_send_friend_request_sender_not_exist(app):
    app.user_credentials = {
        'receiver_username': {'login_status': True, 'first_name': 'Receiver', 'last_name': 'User'}
    }
    
    result = app.send_friend_request('sender_username', 'receiver_username')
    assert result == "Invalid sender or receiver username."
    assert len(app.friends) == 0

def test_send_friend_request_sender_not_logged_in(app):
    app.user_credentials = {
        'sender_username': {'login_status': False, 'first_name': 'Sender', 'last_name': 'User'},
        'receiver_username': {'login_status': True, 'first_name': 'Receiver', 'last_name': 'User'}
    }
    
    result = app.send_friend_request('sender_username', 'receiver_username') 
    assert result == "Cannot send friend request. Check user login status."
    assert len(app.friends) == 0

def test_manage_pending_friend_requests_accept(app, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'accept')
    app.user_credentials = {
        'test': {
            'friend_requests': ['user1', 'user2'],
            'friends': []
        }
    }
    app.manage_pending_friend_requests('test')
    captured = capsys.readouterr()
    assert app.user_credentials['test']['friends'] == ['user1', 'user2']  # Updated expectation
    assert app.user_credentials['test']['friend_requests'] == []  # User2 is removed from friend requests
    assert "Friend request from user1 accepted." in captured.out
    assert "updated friends list ['user1', 'user2']" in captured.out  # Updated expectation

def test_manage_pending_friend_requests_no_user(app, capsys):

    app.user_credentials = {}
    app.manage_pending_friend_requests('nonexistent_user')
    captured = capsys.readouterr()
    assert "No user found with username: nonexistent_user" in captured.out


def test_remove_job(app):
    
    result = app.remove_job


def test_job_search_by_company(app):
    
    app.job_posts = [
        {'id': 1, 'employer': 'Company A', 'role': 'Developer', 'experience_level': 'Mid'},
        {'id': 2, 'employer': 'Company B', 'role': 'Designer', 'experience_level': 'Senior'},
    ]
    filtered_jobs = app.job_search(company='Company A')
    assert len(filtered_jobs) == 1
    assert filtered_jobs[0]['employer'] == 'Company A'

def test_job_search_with_multiple_filters(app):
    
    app.job_posts = [
        {'id': 1, 'employer': 'Company A', 'role': 'Developer', 'experience_level': 'Entry'},
        {'id': 2, 'employer': 'Company B', 'role': 'Designer', 'experience_level': 'Senior'},
        {'id': 3, 'employer': 'Company A', 'role': 'Developer', 'experience_level': 'Senior'},
    ]
    filtered_jobs = app.job_search(company='Company A', role='Developer', experience_level='Senior')
    assert len(filtered_jobs) == 1
    assert filtered_jobs[0]['id'] == 3

def test_apply_for_job_updates_applied_jobs(app):
    
    with patch.object(app, 'applied_jobs', new={}):
        app.apply_for_job(
            username='user1',
            job_title='Developer',
            job_description='Develop stuff',
            employer='Company A',
            location='Location A',
            salary=50000,
            role='Developer',
            experience_level='Mid'
        )
        assert 'user1' in app.applied_jobs
        assert len(app.applied_jobs['user1']) == 1
        assert app.applied_jobs['user1'][0]['employer'] == 'Company A'

def test_apply_for_job_nonexistent_user(app):
    
    username = 'new_user'
    app.apply_for_job(
        username=username,
        job_title='QA Engineer',
        job_description='Quality assurance engineering tasks',
        employer='Company C',
        location='Location C',
        salary=70000,
        role='QA',
        experience_level='Mid'
    )
    assert username in app.applied_jobs
    assert len(app.applied_jobs[username]) == 1

def test_save_job_updates_saved_jobs(app):
    
    with patch.object(app, 'saved_jobs', new={}):
        app.save_job(
            username='user2',
            job_title='Designer',
            job_description='Design stuff',
            employer='Company B',
            location='Location B',
            salary=60000,
            role='Designer',
            experience_level='Senior'
        )
        assert 'user2' in app.saved_jobs
        assert len(app.saved_jobs['user2']) == 1
        assert app.saved_jobs['user2'][0]['employer'] == 'Company B'

def test_save_job_for_existing_user(app):
    
    username = 'existing_user'
    app.saved_jobs[username] = [
        {'title': 'Existing Job', 'employer': 'Existing Company'}
    ]
    app.save_job(
        username=username,
        job_title='New Job',
        job_description='New job description',
        employer='New Company',
        location='New Location',
        salary=80000,
        role='New Role',
        experience_level='New Level'
    )
    assert len(app.saved_jobs[username]) == 2
    assert app.saved_jobs[username][1]['title'] == 'New Job'

def test_calculate_jobs_not_applied(app):
    
    app.job_posts = [{'id': 1}]
    app.all_jobs = {1: {'details': 'Details of Job 1'}, 2: {'details': 'Details of Job 2'}}
    with patch.object(app, 'apply_for_job') as mocked_apply:
        app.apply_for_job(
            username='user1',
            job_title='Developer',
            job_description='Develop stuff',
            employer='Company A',
            location='Location A',
            salary=50000,
            role='Developer',
            experience_level='Mid'
        )
    jobs_not_applied = app.calculate_jobs_not_applied()
    assert len(jobs_not_applied) == 1

def test_calculate_jobs_not_applied_with_no_applications(app):
    app.all_jobs = {
        1: {'details': 'Details of Job 1'},
        2: {'details': 'Details of Job 2'}
    }

    app.job_posts = []
    jobs_not_applied = app.calculate_jobs_not_applied()
    assert len(jobs_not_applied) == len(app.all_jobs)

def test_remove_jobs_success(app):
    username = 'existing_user'
    app.saved_jobs[username] = [
        {'title': 'Existing Job', 'employer': 'Existing Company'}
    ]
    app.save_job(
        username=username,
        job_title='New Job',
        job_description='New job description',
        employer='New Company',
        location='New Location',
        salary=80000,
        role='New Role',
        experience_level='New Level'
    )

    
    result = app.remove_job(username, 'New Job', 'New job description', 'New Company', 'New Location', 80000, 'New Role', 'New Level')
    #assert app.saved_jobs == {}
    assert result["line"] == "Job removed successfully."

def test_remove_jobs_fail(app):
    username = 'existing_user'
    
    result = app.remove_job(username, 'New Job', 'New job description', 'New Company', 'New Location', 80000, 'New Role', 'New Level')
    assert result["line"] == "No Such Job for this User"