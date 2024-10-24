from django.db import models

# Create your models here.
class Users(models.Model):
    Name=models.CharField(max_length=250)
    Email=models.CharField(max_length=250)
    Password=models.CharField(max_length=250)
    PhoneNumber=models.BigIntegerField()
    ProfilePic=models.ImageField(upload_to='static/users/')
class Architectures(models.Model):
    Name=models.CharField(max_length=250)
    Email=models.CharField(max_length=250)
    Password=models.CharField(max_length=250)
    PhoneNumber=models.BigIntegerField()
    ProfilePic=models.ImageField(upload_to='static/architectures/')
class Designers(models.Model):
    Name=models.CharField(max_length=250)
    Email=models.CharField(max_length=250)
    
    Password=models.CharField(max_length=250)
    PhoneNumber=models.BigIntegerField()
    ProfilePic=models.ImageField(upload_to='static/designers/')
class Contractors(models.Model):
    Name=models.CharField(max_length=250)
    Email=models.CharField(max_length=250)
    Password=models.CharField(max_length=250)
    PhoneNumber=models.BigIntegerField()
    ProfilePic=models.ImageField(upload_to='static/contractors/')
class Works(models.Model):
    Picture=models.ImageField(upload_to='static/images/works/')
    TypeOfDesign=models.CharField(max_length=100)
    Upload_by=models.CharField(max_length=100)
class ArchitectBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    STATUS_CHOICES1 = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    BookingPerson=models.CharField(max_length=100)
    PersonID=models.IntegerField()
    SquareFeet=models.IntegerField()
    Budget=models.IntegerField()
    Architect=models.ForeignKey(Architectures,on_delete=models.CASCADE)
    Plotsize=models.CharField(max_length=100)
    Plotpic=models.ImageField(upload_to='static/images/bookings/')
    Rougharchitecture=models.ImageField(upload_to='static/images/bookings/',default='default')
    Message=models.TextField()
    RequesttoArchitect=models.CharField(max_length=200,choices=STATUS_CHOICES, default='pending')
    RequestfromArchitect=models.CharField(max_length=200,choices=STATUS_CHOICES, default='pending')
    Payment=models.CharField(max_length=200,choices=STATUS_CHOICES1, default='pending')
    File=models.ImageField(upload_to='static/images/architectdesigns/',default='pending')
    Price=models.IntegerField(default=0)
    status=models.CharField(max_length=200,default='pending')
    interest=models.CharField(max_length=200,default='pending')
    def __str__(self):
        return self.BookingPerson
class DesignerBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    STATUS_CHOICES1 = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    BookingPerson=models.CharField(max_length=100)
    PersonID=models.IntegerField()
    HomeStyle=models.CharField(max_length=100)
    designer=models.ForeignKey(Designers,on_delete=models.CASCADE)
    Plotsize=models.CharField(max_length=100)
    Plotpic=models.ImageField(upload_to='static/images/bookings/')
    Message=models.TextField()
    RequesttoDesigner=models.CharField(max_length=200,choices=STATUS_CHOICES, default='pending')
    RequestfromDesigner=models.CharField(max_length=200,choices=STATUS_CHOICES, default='pending')
    Payment=models.CharField(max_length=200,choices=STATUS_CHOICES1, default='pending')
    File=models.ImageField(upload_to='static/images/designerdesigns/',default='pending')
    Price=models.IntegerField(default=0)
    status=models.CharField(max_length=200,default='pending')
    interest=models.CharField(max_length=200,default='pending')
    def __str__(self):
        return self.BookingPerson
class  ContractorBooking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    STATUS_CHOICES1 = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]
    BookingPerson=models.CharField(max_length=100)
    PersonID=models.IntegerField()
    SquareFeet=models.IntegerField()
    TimeLimit=models.CharField(max_length=100)
    Contractor=models.ForeignKey(Contractors,on_delete=models.CASCADE)
    Plotsize=models.CharField(max_length=100)
    Plan=models.ImageField(upload_to='static/images/bookings/')
    Plotpic=models.ImageField(upload_to='static/images/bookings/')
    Message=models.TextField()
    RequesttoContractor=models.CharField(max_length=200,choices=STATUS_CHOICES, default='pending')
    RequestfromContractor=models.CharField(max_length=200,choices=STATUS_CHOICES, default='pending')
    Payment=models.CharField(max_length=200,choices=STATUS_CHOICES1, default='pending')
    Price=models.IntegerField(default=0)
    status=models.CharField(max_length=200,default='pending')
    def __str__(self):
        return self.BookingPerson
class Payment(models.Model):
    UserName=models.CharField(max_length=200)
    User_ID=models.IntegerField()
    Amount=models.IntegerField(default=0)
    Account_Number=models.CharField(max_length=200)
    Cvv=models.IntegerField()
    ExpiryDate=models.CharField(max_length=200)
    def __str__(self):
        return self.UserName