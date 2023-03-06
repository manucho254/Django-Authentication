from apps.utils.email_client import EmailClient
from django.conf import settings

client = EmailClient()


def confirm_account(data: dict) -> None:
    data["url"] = f"{settings.BACKEND_URL}/auth/change-password/data[""]token"
    client.send_email(data, "email_confirmation.html")


def reset_password(data: dict) -> None:
    client.send_email(data, "reset_password.html")
