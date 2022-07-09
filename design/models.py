from django.db import models


class Design(models.Model):
    name = models.CharField(max_length=1000)
    image = models.ImageField(null=True, blank=True, upload_to='designs/')

    # this date will never be updated
    created_at = models.DateTimeField(null=True, auto_now_add=True)
    # this date will change every time we update entry
    update_at = models.DateTimeField(null=True, auto_now=True)
    
    def __str__(self):
        return self.name



class Card(models.Model):
    first_name = models.CharField(max_length=1000)
    last_name = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.first_name




    