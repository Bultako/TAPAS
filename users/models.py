########################################################################3
## Users
########################################################################3

from django.db import models
from django.contrib.auth.models import User

#class User(models.Model):
    #username = models.CharField(max_length=90)
    #first_name = models.CharField(blank=True, max_length=90)
    #last_name = models.CharField(blank=True, max_length=90)
    #email = models.CharField(blank=True, max_length=45)
    #passwd = models.CharField(blank=True, max_length=255)
    #is_staff = models.IntegerField(null=True, blank=True)
    #is_active = models.IntegerField(null=True, blank=True)
    #is_superuser = models.IntegerField(null=True, blank=True)
    #last_login = models.DateTimeField(null=True, blank=True)
    #date_joined = models.DateTimeField(null=True, blank=True)
    #class Meta:
        #db_table = 'User'

class UserProfile(models.Model):
    user = models.ForeignKey(User)
    institute = models.CharField(blank=True, max_length=255)
    country = models.CharField(blank=True, max_length=180)
    phone = models.CharField(blank=True, max_length=25)
    
    class Meta:
        db_table = 'UsersProfiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'Users Profiles'

    def __unicode__(self):
        return u'%s' % (self.user)

