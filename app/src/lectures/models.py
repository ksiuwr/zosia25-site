from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _

from conferences.models import Zosia
from users.models import User
from utils.constants import FULL_DURATION_CHOICES, LECTURE_TYPE, LectureInternals
from utils.forms import get_durations


class Lecture(models.Model):
    class Meta:
        verbose_name = _("Lecture")
        verbose_name_plural = _("Lectures")
        ordering = ['priority', 'id']

    # organizational information
    zosia = models.ForeignKey(Zosia, verbose_name=_("Conference"), related_name="lectures",
                              on_delete=models.CASCADE)
    requests = models.CharField(
        verbose_name=_("Requests or comments"), max_length=800, blank=True, null=True,
        help_text=_("Your requests, suggestions or comments intended for organizers")
    )
    create_date = models.DateTimeField(verbose_name=_("Creation date"), auto_now_add=True)
    accepted = models.BooleanField(verbose_name=_("Accepted"), default=False)
    priority = models.IntegerField(default=99, help_text=_("Set order on all lectures page"))

    # main data about lecture
    title = models.CharField(verbose_name=_("Title"), max_length=256)
    abstract = models.CharField(verbose_name=_("Abstract"), max_length=2048)
    lecture_type = models.CharField(verbose_name=_("Type"), max_length=1, choices=LECTURE_TYPE)
    duration = models.PositiveSmallIntegerField(
        choices=FULL_DURATION_CHOICES,
        verbose_name=_("Duration (in minutes)"),
        help_text=_("Please remember that organizers <u>ARE ALLOWED</u> to cut you off during your "
                    "lecture or workshop when you're out of declared time!")
    )
    events = models.CharField(
        verbose_name=_("Additional events"), max_length=800, blank=True, null=True,
        help_text=_(
            "Are you planning any event after your lecture or workshop (e.g. pizza, drinks, "
            "games, recruitment)? <b>TELL US ABOUT IT!</b> Beware that organizers <u>WON'T "
            "ALLOW</u> you to arrange your event if you don't announce it here!")
    )

    # about author
    description = models.CharField(verbose_name=_("Author description"), max_length=256, null=True,
                                   blank=True)
    author = models.ForeignKey(User, related_name="lectures", verbose_name=_("Author"),
                               on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} - {self.title}"

    def toggle_accepted(self):
        self.accepted = not self.accepted
        self.save()

    def clean(self):
        if self.duration is None:
            return

        try:
            durations = [d[0] for d in get_durations(self.lecture_type, self.author)]
        except User.DoesNotExist:
            return

        if self.duration not in durations:
            if self.lecture_type == LectureInternals.TYPE_LECTURE:
                raise ValidationError({
                    "duration": ValidationError(
                        _("Lecture is too long, maximal time for you is %(time)s minutes"),
                        code="invalid",
                        params={"time": durations[-1]}
                    )
                })

            if self.lecture_type == LectureInternals.TYPE_WORKSHOP:
                raise ValidationError({
                    "duration": ValidationError(
                        _("Workshop is too short, minimal time is %(time)s minutes"),
                        code="invalid",
                        params={"time": durations[0]}
                    )
                })


class Schedule(models.Model):
    zosia = models.ForeignKey(Zosia, verbose_name=_("Conference"), related_name="schedules",
                              on_delete=models.CASCADE)
    content = models.TextField(verbose_name=_("content"),
                               help_text=_("You can use html tags and materializecss classes"))
