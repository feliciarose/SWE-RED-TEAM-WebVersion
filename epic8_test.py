import pytest
from unittest.mock import patch
from incollege import InCollegeApp
from datetime import datetime, timedelta
# make sure to run `pytest epic8_test.py` in the terminal to test the code

# ------------------ Felicia Tests ------------------#

@pytest.fixture
def app():
    return InCollegeApp()

def custom_send_notification_input(msg):
    if msg == "Enter the recipient's username: ":
        return "test"
    elif msg == "Enter the message: ":
        return "Test message"

def test_send_notification(app):
    # Define test input
    username = "test"
    message = "Test message"

    # Call the method being tested
    result = app.send_notification(username, message)

    # Assert that the notification is sent successfully
    assert result == "Notification sent successfully."

    # Assert that the notification is correctly added to the notifications dictionary
    assert len(app.notifications) == 1
    assert app.notifications[username][0]["message"] == message


def test_view_notifications_no_messages(app, capsys):
    app.notifications = []  # Assuming no notifications
    app.view_notifications()
    out, _ = capsys.readouterr()
    assert "No notifications found." in out

@pytest.mark.parametrize("last_application_date, expected_notification_count", [
    (datetime.now() - timedelta(days=8), 1),  # Expect notification as application date is 8 days ago
    (datetime.now() - timedelta(days=5), 0),  # Don't expect notification as application date is 5 days ago
    (datetime.now() - timedelta(days=10), 1)  # Expect notification as application date is 10 days ago
])

def test_check_job_application_reminder(app, last_application_date, expected_notification_count):
    # Add a user and last application date to the app for testing
    username = "test"
    app.last_application_date[username] = last_application_date
    
    # Call the method being tested
    app.check_job_application_reminder()

    # Assert the number of notifications generated
    assert len(app.notifications.get(username, [])) == expected_notification_count

# -----------------Muhannad's test-------------------#
    

@pytest.fixture
def instance():
    # Initialize necessary objects for testing
    instance = InCollegeApp()
    instance.notifications = {}
    instance.user_credentials = {'username': 'test'}
    instance.messages = []
    return instance


def test_send_notification(instance):
    # Assuming send_notification correctly adds a message to notifications
    instance.send_notification("user1", "Test message")
    assert "user1" in instance.notifications  # Ensure the user is in notifications
    assert instance.notifications["user1"][0]["message"] == "Test message"  # Message matches
    assert not instance.notifications["user1"][0]["read"]  # Message is initially unread


@patch('builtins.print')
def test_view_notifications_with_notifications(mocked_print, instance):
    # Pre-populate notifications for a specific user
    instance.notifications = {"test": [{"message": "Message 1", "read": False}]}
    instance.view_notifications("test")
    mocked_print.assert_called_with("Notification: Message 1")  # Verify correct print output


@patch('builtins.print')
def test_view_notifications_without_notifications(mocked_print, instance):
    # Assuming no notifications are set for "test"
    instance.view_notifications("test")
    mocked_print.assert_called_with("No notifications found.")  # Correct message for no notifications


from unittest.mock import patch
from datetime import datetime, timedelta

@patch('incollege.InCollegeApp.send_notification')
def test_check_job_application_reminder(mocked_send_notification, instance):
    # Mock datetime to control the current date
    with patch('incollege.datetime') as mocked_datetime:
        # Set "now" to a specific point in time
        mocked_datetime.now.return_value = datetime.now() - timedelta(days=7)
        # Populate last_application_date to trigger notification
        instance.last_application_date = {"user2": datetime.now() - timedelta(days=8)}
        
        instance.check_job_application_reminder()
        
        # Verify send_notification was called once for user2
        mocked_send_notification.assert_called_once_with("user2", "Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")
