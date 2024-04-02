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

# ------------------------------------#