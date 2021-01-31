import os
import uuid

from django.db import models
from django.utils.deconstruct import deconstructible


@deconstructible
class GenerateAttachmentFilePath(object):
    def __init__(self):
        pass

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        path = f"media/tasks/{instance.task.id}/attachments"
        name = f"{instance.id}.{ext}"

        return os.path.join(path, name)


attachment_file_path = GenerateAttachmentFilePath()


class TaskStatus(object):
    COMPLETED = "CO"
    NOT_COMPLETED = "NC"


TASK_STATUS_CHOICES = [
    (TaskStatus.NOT_COMPLETED, "Not Completed"),
    (TaskStatus.COMPLETED, "Completed"),
]


class TimeStampdModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class TaskList(TimeStampdModel):
    created_by = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="lists",
    )
    house = models.ForeignKey(
        "house.House", on_delete=models.CASCADE, related_name="lists"
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=TASK_STATUS_CHOICES, default=TaskStatus.NOT_COMPLETED
    )

    def __str__(self):
        return f"{self.id} | {self.name}"


class Task(TimeStampdModel):
    created_by = models.ForeignKey(
        "users.Profile",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="created_tasks",
    )
    completed_by = models.ForeignKey(
        "users.Profile",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="completed_tasks",
    )
    task_list = models.ForeignKey(
        "task.TaskList", on_delete=models.CASCADE, related_name="tasks"
    )
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=2, choices=TASK_STATUS_CHOICES, default=TaskStatus.NOT_COMPLETED
    )

    def __str__(self):
        return f"{self.id} | {self.name}"


class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_on = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=attachment_file_path, null=True, blank=True)
    task = models.ForeignKey(
        "task.Task", on_delete=models.CASCADE, related_name="attachments"
    )

    def __str__(self):
        return f"{self.id} | {self.task}"
