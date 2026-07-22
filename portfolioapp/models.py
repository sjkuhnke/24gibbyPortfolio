from django.db import models


class Show(models.Model):
    date = models.DateField()
    venue = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    ticket_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.date} — {self.venue}, {self.city}, {self.state}"
