import pytest
from unittest.mock import patch
from incollege import InCollegeApp
# make sure to run `pytest epic7_test.py` in the terminal to test the code

@pytest.fixture


def app():
    return InCollegeApp()

#-----------Vynze-----------------#
def custom_gold_tier_input(msg):
    if msg == "Select an option: ":
        return "1"
    elif msg == "Enter the recipient's username: ":
        return "John Doe"
    elif msg == "Enter the message: ":
        return "Hello, John!"

def test_message_management_gold_send(app, capfd, monkeypatch):
    app.user_credentials["test"]["user_tier"] = "Gold"
    monkeypatch.setattr('builtins.input', custom_gold_tier_input)
    result = app.message_management()
    out, err = capfd.readouterr()
    assert "Message sent successfully." in out, "Message sent successfully as a Gold tier user."


def custom_silver_tier_input(msg):
    if msg == "Select an option: ":
        return "1"
    elif msg == "Enter your friend's username: ":
        return "John Doe"
    elif msg == "Enter the message: ":
        return "Hello, John!"

def test_message_management_silver_send(app, capfd, monkeypatch):
    app.user_credentials["test"]["user_tier"] = "Silver"
    app.user_credentials["test"]["friends"] = ["John Doe"]
    monkeypatch.setattr('builtins.input', custom_silver_tier_input)
    result = app.message_management()
    out, err = capfd.readouterr()
    assert "Message sent successfully." in out, "Message sent successfully as a Gold tier user."
    
def custom_free_tier_input(msg):
    if msg == "Select an option: ":
        return "1"
    elif msg == "Enter the recipient's username: ":
        return "John Doe"
    elif msg == "Enter the message: ":
        return "Hello, John!"
    

def test_message_management_free_send(app, capfd, monkeypatch):
    app.user_credentials["user_tier"] = "Standard"
    monkeypatch.setattr('builtins.input', custom_free_tier_input)
    result = app.message_management()
    out, err = capfd.readouterr()
    assert "You must upgrade to at least Silver tier to send messages." in out, "Message not sent as a Free tier user."

def test_message_management_view_messages(app, capfd, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "2")
    result = app.message_management()
    out, err = capfd.readouterr()
    assert "No messages found." in out, "No messages to display."