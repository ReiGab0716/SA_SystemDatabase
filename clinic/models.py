from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid


phone_validator = RegexValidator(
    regex=r'^09\d{9}$',
    message='Enter a valid Philippine mobile number in the format 09XXXXXXXXX.'
)

# Stores the treatment catalog shown to patients and staff booking screens.
class Service(models.Model):
    CATEGORY_CHOICES = [
        ('FACIAL', 'Facial Treatments'),
        ('ZO', 'ZO Professional Facial'),
        ('DOCTOR', 'Doctors Procedure'),
        ('LASER', 'Laser Gynecology'),
        ('ADDON', 'Add-On Treatment'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='FACIAL')
    description = models.TextField(blank=True, null=True) 
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'services'

    def __str__(self):
        return f"[{self.get_category_display()}] {self.name}"

# Stores role-specific account details and generates display IDs for staff and patients.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)   
    phone_number = models.CharField(max_length=11, blank=True, null=True, validators=[phone_validator])
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    employee_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    doctor_id = models.CharField(max_length=12, unique=True, blank=True, null=True)
    ROLE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('SECRETARY', 'Secretary'),
        ('PATIENT', 'Patient'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='PATIENT')

    class Meta:
        db_table = 'user_profiles'

    @property
    def display_id(self):
        if self.role == 'DOCTOR':
            return self.doctor_id or f"DOC-{self.user_id:04d}"
        if self.role == 'SECRETARY':
            return self.employee_id or f"EMP-{self.user_id:04d}"
        return f"#SA-{self.user_id:04d}"

    def save(self, *args, **kwargs):
        if self.role == 'DOCTOR':
            self.doctor_id = self.doctor_id or f"DOC-{self.user_id:04d}"
            self.employee_id = None
        elif self.role == 'SECRETARY':
            self.employee_id = self.employee_id or f"EMP-{self.user_id:04d}"
            self.doctor_id = None
        else:
            self.employee_id = None
            self.doctor_id = None
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class PatientProfileAudit(models.Model):
    """Records important profile changes for clinic accountability."""
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile_audit_entries')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile_changes_made')
    field_name = models.CharField(max_length=50)
    old_value = models.CharField(max_length=255, blank=True, null=True)
    new_value = models.CharField(max_length=255, blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'patient_profile_audits'
        ordering = ['-changed_at']

    def __str__(self):
        return f"{self.patient.username} {self.field_name} changed at {self.changed_at:%Y-%m-%d %H:%M}"

# Stores bookings, reference numbers, clinic location, status, and pricing at booking time.
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    LOCATION_CHOICES = [
        ('Baseline', 'Shields Aesthetic Clinic - Baseline Center'),
        ('CebuDoc', 'OB-Gynecology Clinic - Cebu Doctors Hospital'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='main_appointments')
    
    addon_service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='addon_appointments')
    
    reference_number = models.CharField(max_length=12, unique=True, editable=False, null=True, blank=True)
    has_addon = models.BooleanField(default=False)
    specialist = models.CharField(max_length=255, default='Dr. Rass Shields Pimentel')
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, default='Baseline')

    date = models.DateField()
    time = models.TimeField()
    
    notes = models.TextField(blank=True, null=True) 
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    price_at_booking = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    doctor_notes = models.TextField(blank=True, null=True, help_text="Private notes for doctor only")
    doctor_notes_created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    doctor_notes_updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'appointments'
        ordering = ['-date', '-time']

    def save(self, *args, **kwargs):
        if not self.reference_number:
            unique_id = uuid.uuid4().hex[:6].upper()
            self.reference_number = f"TRN-{unique_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.reference_number} - {self.patient.username if self.patient else 'Guest'}"

# Keeps a Profile row available for every Django auth user.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if kwargs.get('raw'):
        return
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if kwargs.get('raw'):
        return
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance)
