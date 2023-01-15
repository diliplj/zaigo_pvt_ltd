from django.db import models


DATAMODE_CHOICES = (("A", "ACTIVE"), ("IN", "INACTIVE"),("D","DELETED"))

class Roles(models.Model):
    '''
    roles is the main table and rights, members table should have role as a foreign key
    '''
    role_name = models.CharField(max_length=50,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=15)
    updated_by = models.CharField(max_length=15)

    def __str__(self):
        return self.role_name


class Members(models.Model):
    member_name = models.CharField(null=True, max_length=100)
    role = models.ForeignKey(Roles, on_delete=models.CASCADE)
    user_secret_key = models.CharField(max_length=32,unique=True, blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=15)
    updated_by = models.CharField(max_length=15)
    datamode = models.CharField(max_length=12, default='A', choices=DATAMODE_CHOICES, db_index=True)

    def __str__(self):
        return self.member_name +" id -"+ str(self.id)

class Rights(models.Model):
    role = models.ManyToManyField(Roles)
    rights     = models.CharField(max_length=200, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=15)
    updated_by = models.CharField(max_length=15)
    
    def __str__(self):
        return self.rights
