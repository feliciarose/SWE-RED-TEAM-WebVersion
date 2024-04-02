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
    instance = YourClass()
    instance.notifications = {}
    instance.user_credentials = {'username': 'test'}
    instance.messages = []
    return instance


def test_send_notification(instance):
    instance.send_notification("user1", "Test message")
    assert "user1" in instance.notifications
    assert instance.notifications["user1"][0]["message"] == "Test message"
    assert not instance.notifications["user1"][0]["read"]


@patch('builtins.print')
def test_view_notifications_with_notifications(instance, mocked_print):
    instance.notifications = {"test": [{"message": "Message 1", "read": False}]}
    instance.view_notifications("test")
    mocked_print.assert_called_with("Notification: Message 1")


@patch('builtins.print')
def test_view_notifications_without_notifications(instance, mocked_print):
    instance.view_notifications("test")
    mocked_print.assert_called_with("No notifications found.")


@patch.object(datetime, 'now')
@patch.object(YourClass, 'send_notification')
def test_check_job_application_reminder(mocked_send_notification, mocked_datetime_now, instance):
    mocked_datetime_now.return_value = datetime.now() - timedelta(days=5)
    instance.last_application_date = {"user1": datetime.now()}
    instance.check_job_application_reminder()
    mocked_send_notification.assert_not_called()

    mocked_datetime_now.return_value = datetime.now() - timedelta(days=7)
    instance.last_application_date = {"user2": datetime.now()}
    instance.check_job_application_reminder()
    mocked_send_notification.assert_called_once_with("user2", "Remember - you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")
