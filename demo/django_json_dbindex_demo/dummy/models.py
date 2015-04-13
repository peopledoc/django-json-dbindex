from django.db import models


class Duck(models.Model):
    """A duck
    """
    name = models.CharField(max_length=300)
    indice = models.IntegerField(default=0)
    status_int = models.IntegerField(default=0)
    status_str = models.CharField(default="", max_length=16)
    
    def __unicode__(self):
        return self.name
