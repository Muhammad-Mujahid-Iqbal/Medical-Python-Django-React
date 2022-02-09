from django.db import models



class Patient(models.Model):
    """Patient model class

    Parameters
    ----------
    models : django.db

    """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob =  models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = (
            "first_name",
            "last_name",
        )


class Visit(models.Model):
    """Visit model class

    Parameters
    ----------
    models : django.db

    """

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="p_visits")
    reason = models.CharField(max_length=1000)
    visit_date =  models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = (
            "patient",
            "reason",
        )
