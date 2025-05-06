# utils.py
import requests
from django.conf import settings

def send_winsms(phone_number, message):
    """
    Sends an SMS message using the WinSMS API.

    Args:
        phone_number (str): The recipient's phone number (in international format, e.g., 27821234567).
        message (str): The text of the SMS message.

    Returns:
        bool: True if the SMS was sent successfully, False otherwise.
        str: The response message from WinSMS.
    """
    url = "https://rest.winsms.co.za/v1/api/message/send"  # Use the correct WinSMS API endpoint
    username = settings.WINSMS_USERNAME  # Use Django settings
    password = settings.WINSMS_PASSWORD  # Use Django settings

    if not username or not password:
        print("WinSMS credentials not configured in settings.py")
        return False, "WinSMS credentials not configured"

    payload = {
        "destination": phone_number,
        "message": message,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {username}:{password}"  # Basic Auth. See WinSMS docs.
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return True, response.text

    except requests.exceptions.RequestException as e:
        print(f"Error sending SMS: {e}")
        return False, str(e)


# settings.py
# WinSMS Settings
WINSMS_USERNAME = "your_winsms_username"  # Replace with your WinSMS username
WINSMS_PASSWORD = "your_winsms_password"  # Replace with your WinSMS password or API Key

