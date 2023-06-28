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

class Benefit(models.Model):
    ben_code = models.AutoField(primary_key=True)
    ben_name = models.CharField(max_length=100)
    ben_type = models.CharField(max_length=100)
    ben_description = models.CharField(max_length=250)

    class Meta:
        managed = False
        db_table = 'BENEFIT'

class UserBenefit(models.Model):
    useben_code = models.AutoField(primary_key=True)
    useben_state = models.CharField(max_length=10, default='INCOMPLETE')
    use_code = models.ForeignKey(User, models.DO_NOTHING, db_column='use_code')
    ben_code = models.ForeignKey(Benefit, models.DO_NOTHING, db_column='ben_code')

    class Meta:
        managed = False
        db_table = 'USER_BENEFIT'

class BenefitLog(models.Model):
    benlog_code = models.AutoField(primary_key=True)
    benlog_date = models.DateField()
    use_code = models.ForeignKey('User', models.DO_NOTHING, db_column='use_code')
    ben_code = models.ForeignKey(Benefit, models.DO_NOTHING, db_column='ben_code')

    class Meta:
        managed = False
        db_table = 'BENEFIT_LOG'

class Country(models.Model):
    cou_code = models.AutoField(primary_key=True)
    cou_name = models.CharField(max_length=150)

    class Meta:
        managed = False
        db_table = 'COUNTRY'

class Question(models.Model):
    que_code = models.AutoField(primary_key=True)
    que_description = models.CharField(max_length=100)
    que_answer = models.CharField(max_length=100)
    cou_code = models.ForeignKey(Country, models.DO_NOTHING, db_column='cou_code')

    class Meta:
        managed = False
        db_table = 'QUESTION'