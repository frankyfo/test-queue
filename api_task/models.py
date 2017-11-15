from django.db import models


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    create_time  = models.TimeField(auto_now_add=True)
    start_time = models.TimeField(null=True)
    exec_time = models.IntegerField(null=True)  
    
    def __str__(self):
        return self.id
