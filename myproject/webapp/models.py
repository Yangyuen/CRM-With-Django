from django.db import models

class assets(models.Model):

    creation_date =models.DateTimeField(auto_now_add=True)
    asset_no = models.CharField(max_length=100)
    asset_name = models.CharField(max_length=300)
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=20)
    department_name = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    status = models.CharField(max_length=150)
    remark = models.CharField(max_length=200)

    def __str__(self):

        return "รหัสทรัพย์สิน : " + self.asset_no + " - " + self.asset_name + self.brand + self.model + " S/N : " + self.serial_no
    

