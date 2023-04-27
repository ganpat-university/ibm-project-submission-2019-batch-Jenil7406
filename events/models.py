from django.db import models

# Create your models here.
class Events(models.Model):
    event_name         = models.CharField(max_length=30)
    event_description  = models.CharField(max_length=100)
    max_tickets        = models.TextField()
    start_date         = models.CharField(max_length=13)
    end_date           = models.CharField(max_length=13)
    event_created      = models.DateTimeField(auto_now_add = True)
    image_path         = models.ImageField(null=True,upload_to='static/images')
    account_id         = models.CharField(max_length=45)
    contract_hash      = models.TextField()
    contract_address   = models.TextField(default="False")
    abi                = models.TextField()
    nft_metadata       = models.TextField(default="False")
