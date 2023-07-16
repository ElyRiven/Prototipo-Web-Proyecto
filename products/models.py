from django.db import models

class Role(models.Model):
    rol_code = models.AutoField(primary_key=True)
    rol_name = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'ROLE'

class User(models.Model):
    use_code = models.AutoField(primary_key=True)
    use_firstname = models.CharField(max_length=50)
    use_lastname = models.CharField(max_length=50)
    use_email = models.CharField(max_length=50)
    use_idnumber = models.CharField(max_length=10)
    use_phonenumber = models.CharField(max_length=10, blank=True, null=True)
    use_password = models.CharField(max_length=32)
    use_points = models.IntegerField(default=0)
    use_bensection = models.IntegerField(default=0)
    use_firstlogin = models.DateField(default='2000-01-01')
    rol_code = models.ForeignKey(Role, models.DO_NOTHING, db_column='rol_code')

    class Meta:
        managed = False
        db_table = 'USER'

class Product(models.Model):
    pro_code = models.AutoField(primary_key=True)
    pro_name = models.CharField(max_length=100)
    pro_price = models.DecimalField(max_digits=10, decimal_places=2)
    pro_description = models.CharField(max_length=500)
    pro_country = models.CharField(max_length=100)
    pro_startdate = models.DateField()
    pro_enddate = models.DateField()
    pro_state = models.CharField(max_length=15, default='SELLING')

    class Meta:
        managed = False
        db_table = 'PRODUCT'

class Place(models.Model):
    pla_code = models.AutoField(primary_key=True)
    pla_name = models.CharField(max_length=75)
    pla_description = models.CharField(max_length=500)
    pla_activity = models.CharField(max_length=100)
    pla_city = models.CharField(max_length=50)
    pla_startdate = models.DateField()
    pla_enddate = models.DateField()
    pla_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    pla_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    pro_code = models.ForeignKey('Product', models.DO_NOTHING, db_column='pro_code')

    class Meta:
        managed = False
        db_table = 'PLACE'
