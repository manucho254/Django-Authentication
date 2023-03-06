from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from typing import Any


class EmailClient:
    def __init__(self) -> None:
        self.message = EmailMessage()
        self.html_file = None

    def send_email(self, data: dict[Any], html_file: str) -> None:
        self.html_file = html_file
        self.message.body: str = self._setup_html(data.get("content"))
        self.message.subject: str = data.get("subject")
        self.message.to: list = data.get("send_to")
        self.message.from_email: str = settings.Email
        self.content_subtype = "html"
        self.message.send()

    def _setup_html(self, data: dict) -> str:
        return render_to_string(self.html_file, {"data": data})
