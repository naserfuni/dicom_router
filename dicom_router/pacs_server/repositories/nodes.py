from django.db import models

class DicomNode(models.Model):
    ae_title = models.CharField(max_length=64, help_text="AE Title of the DICOM client")
    ip_address = models.GenericIPAddressField(help_text="IP address of the DICOM client")
    description = models.TextField(blank=True, null=True, help_text="Optional description")
    is_active = models.BooleanField(default=True, help_text="Whether this authorization is active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('ae_title', 'ip_address')
        verbose_name = "DICOM Authorization"
        verbose_name_plural = "DICOM Authorizations"

    def __str__(self):
        return f"{self.ae_title} @ {self.ip_address}"

def is_authorized(ae_title, ip):
    return DicomNode.objects.filter(
        ae_title=ae_title,
        ip_address=ip,
        is_active=True
    ).exists()