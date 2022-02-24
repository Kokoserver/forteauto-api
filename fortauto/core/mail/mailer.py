import os
import smtplib
import ssl
from email.mime import multipart, text
from email.utils import formataddr
from typing import Optional, List, Union
import pydantic
from fortauto.core.mail import config as base_config
from fortauto.core.mail import exception
from fortauto.core.mail import template_finder


class Mailer(template_finder.Mail_Template):

    def __init__(
        self,
        website_name: str,
        subject: str,
        sender_email: Optional[pydantic.EmailStr] = None,
        sender_password: Optional[str] = None,
        email_server: Optional[str] = None,
        email_server_port: Optional[int] = None,
        template_folder: Optional[
            pydantic.DirectoryPath] = base_config.settings.template_folder,
        use_google: Optional[bool] = True,
        body: Optional[str] = None,
        template_name: Optional[str] = None,
        context: Optional[dict] = {},
    ) -> None:
        super().__init__(template_folder)
        self.admin_email = sender_email
        self.admin_password = sender_password
        self.template_name = template_name
        self.email_server = email_server
        self.email_server_port = email_server_port
        self.use_google = use_google
        self.website_name = website_name
        self.body = body
        self.context = context
        self.subject = subject

    def __check_credential(self) -> None:
        if not self.admin_email:
            _check_email = base_config.settings.admin_email
            if not _check_email:
                raise exception.InvalidCredentailError(
                    "Sender email can not be empty, either set 'ADMIN_EMAIL' in your envionment, or provide one"
                )
            self.admin_email = base_config.settings.admin_email

        if not self.admin_password:
            _check_password = base_config.settings.admin_password
            if not _check_password:
                raise exception.InvalidCredentailError(
                    "Sender password can not be empty, either set 'ADMIN_PASSWORD' in your envionment, or provide one"
                )
            self.admin_password = base_config.settings.admin_password

        if not self.email_server:
            if not self.use_google:
                raise exception.InvalidCredentailError(
                    "email server  can not be empty, either set 'EMAIL_SERVER' in your envionment, or 'use_google' to true"
                )
            self.email_server = base_config.settings.email_server

        if not self.email_server_port:
            if not self.use_google:
                raise exception.InvalidCredentailError(
                    "email server port  can not be empty, either set 'EMAIL_SERVER_PORT' in your envionment, or 'use_google' to true"
                )
            self.email_server_port = base_config.settings.email_server_port

        if self.template_folder:
            if not os.path.isdir(self.template_folder):
                raise NotADirectoryError(
                    f"Please provide a valid directory or create a template folder in {base_config.settings.base_dir}"
                )

        if self.template_name:
            if not os.path.isfile(
                    os.path.join(self.template_folder, self.template_folder,
                                 self.template_name)):
                raise NotADirectoryError(
                    f"template with name '{self.template_name}', can not be found in {self.template_folder}"
                )

    def send_mail(self, email: Union[List[pydantic.EmailStr],
                                     pydantic.EmailStr]):
        self.__check_credential()
        message = multipart.MIMEMultipart()
        if isinstance(email, list):
            message["To"] = ', '.join(email)
        if isinstance(email, str):
            message["To"] = email
        from_email = self.admin_email
        subject: str = self.subject
        message['Subject'] = subject
        message['From'] = formataddr((self.website_name, from_email))

        if self.template_name and self.template_folder:
            bodyContent = self.render(self.template_name, self.context)
            message.attach(text.MIMEText(bodyContent, 'html'))
        elif self.body:
            bodyContent = self.body
            message.attach(text.MIMEText(bodyContent, 'plain'))
        else:
            raise exception.InvalidEmailContenError(
                "Email body content is required")
        with smtplib.SMTP(self.email_server, self.email_server_port) as smtp:
            context = ssl.create_default_context()
            smtp.starttls(context=context)
            smtp.login(user=self.admin_email, password=self.admin_password)
            smtp.sendmail(from_email, email, message.as_string())
