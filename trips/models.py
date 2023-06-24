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

class UserProduct(models.Model):
    usepro_code = models.AutoField(primary_key=True)
    usepro_state = models.CharField(max_length=15, default='PENDING')
    use_code = models.ForeignKey(User, models.DO_NOTHING, db_column='use_code')
    pro_code = models.ForeignKey(Product, models.DO_NOTHING, db_column='pro_code')

    class Meta:
        managed = False
        db_table = 'USER_PRODUCT'

class Appointment(models.Model):
    app_code = models.AutoField(primary_key=True)
    app_type = models.CharField(max_length=10, default='VIRTUAL')
    app_comment = models.CharField(max_length=300, blank=True, null=True)
    use_code = models.ForeignKey('User', models.DO_NOTHING, db_column='use_code')
    pro_code = models.ForeignKey('Product', models.DO_NOTHING, db_column='pro_code')

    class Meta:
        managed = False
        db_table = 'APPOINTMENT'