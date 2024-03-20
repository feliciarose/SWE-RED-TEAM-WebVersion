import pytest
from unittest.mock import patch
from incollege import InCollegeApp
# make sure to run `pytest epic6_test.py` in the terminal to test the code

@pytest.fixture
def app():
    return InCollegeApp()

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