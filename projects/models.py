import secrets

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.db import models


class Status(models.Model):
    status_text = models.CharField(max_length=50)

    def __str__(self):
        return self.status_text


class Task(models.Model):
    task_text = models.CharField(max_length=25)

    def __str__(self):
        return self.task_text


class DTContact(models.Model):
    dtcontact_fname = models.CharField(max_length=50)
    dtcontact_lname = models.CharField(max_length=50)
    dtcontact_phone = models.CharField(max_length=50)

    def __str__(self):
        return self.dtcontact_lname


class Contact(models.Model):
    contact_fname = models.CharField(max_length=50)
    contact_lname = models.CharField(max_length=50)
    contact_email = models.EmailField(null=True)
    contact_username = models.CharField(max_length=50, null=True)
    contact_phone = models.CharField(max_length=50)

    def __str__(self):
        if self.contact_username:
            return self.contact_username
        return f"{self.contact_lname}, {self.contact_fname}"


class Alignment(models.Model):
    alignment_text = models.CharField(max_length=50)

    def __str__(self):
        return self.alignment_text


class Keyword(models.Model):
    keyword_text = models.CharField(max_length=50)

    def __str__(self):
        return self.keyword_text


class MaturityModel(models.Model):
    maturitymodel_text = models.CharField(max_length=100)

    def __str__(self):
        return self.maturitymodel_text


class Tracker(models.Model):
    task = models.ForeignKey(Task, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=100)
    contact = models.ForeignKey(Contact, on_delete=models.SET_NULL, null=True)
    dtcontact = models.ForeignKey(
        DTContact,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True)
    alignment = models.ForeignKey(
        Alignment,
        on_delete=models.SET_NULL,
        null=True,
    )
    keywords = models.ManyToManyField(Keyword, blank=True)
    maturitymodel = models.ForeignKey(
        MaturityModel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    start_date = models.DateField("date_started", null=True, blank=True)
    end_date = models.DateField("date_ended", null=True, blank=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment_date = models.DateField()
    comment_text = models.CharField(max_length=200)
    comment_user = models.ForeignKey(Contact, on_delete=models.CASCADE)
    comment_tracker = models.ForeignKey(
        Tracker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.comment_text


class Update(models.Model):
    update_date = models.DateField()
    update_text = models.CharField(max_length=150)
    update_user = models.ForeignKey(Contact, on_delete=models.CASCADE)
    update_tracker = models.ForeignKey(
        Tracker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.update_text


class DeveloperAPIKey(models.Model):
    """Hashed API credential for developer access."""

    class Plan(models.TextChoices):
        FREE = "free", "Free"
        DEVELOPER = "developer", "Developer"
        INTERNAL = "internal", "Internal"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="developer_api_keys",
    )
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=16, unique=True, editable=False)
    key_hash = models.CharField(max_length=128, editable=False)
    plan = models.CharField(max_length=20, choices=Plan.choices, default=Plan.FREE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def issue(cls, *, owner, name, plan=Plan.FREE):
        prefix = secrets.token_hex(6)
        secret = secrets.token_urlsafe(32)
        raw_key = f"ptk_{prefix}_{secret}"
        api_key = cls.objects.create(
            owner=owner,
            name=name,
            prefix=prefix,
            key_hash=make_password(raw_key),
            plan=plan,
        )
        return api_key, raw_key

    def matches(self, raw_key):
        return check_password(raw_key, self.key_hash)

    def __str__(self):
        return f"{self.name} ({self.prefix})"
