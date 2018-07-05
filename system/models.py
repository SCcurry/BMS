from django.db import models
import django.utils.timezone as timezone

from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

#读者表
class Read_Person(models.Model):
	Person_Id = models.AutoField("ID",primary_key=True)
	Person_User = models.CharField("用户名",max_length=30)
	Person_Password = models.CharField("密码",max_length=30)
	Person_Name = models.CharField("读者姓名",max_length=30)
	#设置每个人借书的范围在0-20之间
	Person_CanBorrow = models.IntegerField("可借余量",validators=[MinValueValidator(0),MaxValueValidator(20)])
	Person_Phone = models.BigIntegerField("联系方式")
	

#系统管理员表
class System_Person(models.Model):
	System_Id = models.AutoField("ID",primary_key=True)
	System_User = models.CharField("用户名",max_length=30)
	System_Password = models.CharField("密码",max_length=30)
	System_Name = models.CharField("系统管理员姓名",max_length=30)
	System_Phone = models.BigIntegerField("联系方式")
	

#图书管理员表
class Booksys_Person(models.Model):
	BookSys_Id = models.AutoField("ID",primary_key=True)
	BookSys_User = models.CharField("用户名",max_length=30)
	BookSys_Password = models.CharField("密码",max_length=30)
	BookSys_Name = models.CharField("图书管理员姓名",max_length=30)
	BookSys_Phone = models.BigIntegerField("联系方式")

class Book(models.Model):
	book_id = models.AutoField("ID", primary_key=True)
	book_name = models.CharField("书名", max_length=30)
	book_author = models.CharField("作者", max_length=30, blank=True)
	book_introduction = models.CharField("书的简介", max_length=300, blank=True)
	book_publish = models.CharField("出版社", max_length=30, blank=True)
	book_language = models.CharField("语种", default="中文", max_length=5, blank=True)
	book_price = models.CharField("价格", max_length=10, blank=True)
	book_publish_date = models.DateField("出版时间", default=timezone.now, blank=True)
	book_ISBN = models.CharField("ISBN", max_length=20, blank=True)
	#book_remain = models.IntegerField("余量", default=10, validators=[MinValueValidator(0),MaxValueValidator(10)])
	book_status = models.IntegerField("状态", default=0)
	book_lend_count = models.IntegerField("借出次数", default=0)



class Lend_Stream(models.Model):
	lend_stream_id = models.AutoField("ID", primary_key=True)
	lend_stream_reader_name = models.CharField("读者姓名", max_length=30, blank=True)
	lend_stream_book_name = models.CharField("书名", max_length=30, blank=True)
	# 1为借出，2为归还
	lend_stream_type = models.IntegerField("操作类型", default=0)






