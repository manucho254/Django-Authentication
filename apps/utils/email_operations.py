from apps.utils.email_client import EmailClient
from django.conf import settings

client = EmailClient()


def confirm_account(data: dict) -> None:
    data["url"] = f"{settings.BACKEND_URL}auth/confirm-email/{data['token']}/"
    del data["token"]
    data.update({"subject": "Confirm Account", "send_to": [data["email"]]})
    client.send_email(data, "email_confirmation.html")


def reset_password(data: dict) -> None:
    data["url"] = f"{settings.BACKEND_URL}auth/change-password/{data['token']}/"
    del data["token"]
    data.update({"subject": "Reset Password", "send_to": [data["email"]]})
    client.send_email(data, "reset_password.html")
