from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.translation import gettext_lazy as _
from utils.models import TimestampedModel


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    password = models.CharField(
        _('password'),
        max_length=150,
        null=True
    )


class UserPasswordHistory(TimestampedModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_histories'
    )
    password = models.CharField(_('password'), max_length=150)

    def __str__(self) -> str:
        return self.user.username if self.user else str(self.pk)
