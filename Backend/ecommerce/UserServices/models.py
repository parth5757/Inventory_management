from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField()
    city = models.CharField(max_length=150, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    country=models.CharField(max_length=50,blank=True,null=True,default='India',choices=(('India','India'),('USA','USA'),('UK','UK'),('Australia','Australia'),('Canada','Canada'),('Germany','Germany'),('France','France'),('Italy','Italy'),('Japan','Japan'),('China','China'),('Russia','Russia'),('Brazil','Brazil'),('South Africa','South Africa'),('Nigeria','Nigeria'),('Mexico','Mexico'),('Argentina','Argentina'),('Spain','Spain'),('Portugal','Portugal'),('Greece','Greece'),('Sweden','Sweden'),('Norway','Norway'),('Finland','Finland'),('Denmark','Denmark'),('Netherlands','Netherlands'),('Belgium','Belgium'),('Switzerland','Switzerland'),('Austria','Austria'),('Poland','Poland'),('Czech Republic','Czech Republic'),('Turkey','Turkey'),('Ukraine','Ukraine'),('Hungary','Hungary'),('Romania','Romania'),('Bulgaria','Bulgaria'),('Croatia','Croatia'),('Slovenia','Slovenia'),('Slovakia','Slovakia'),('Lithuania','Lithuania'),('Latvia','Latvia'),('Estonia','Estonia'),('Ireland','Ireland'),('Scotland','Scotland'),('Wales','Wales'),('Northern Ireland','Northern Ireland'),('New Zealand','New Zealand'),('Singapore','Singapore'),('Malaysia','Malaysia'),('Thailand','Thailand'),('Indonesia','Indonesia'),('Philippines','Philippines'),('Vietnam','Vietnam'),('South Korea','South Korea'),('North Korea','North Korea'),('Taiwan','Taiwan'),('Hong Kong','Hong Kong'),('Macau','Macau'),('Bangladesh','Bangladesh'),('Pakistan','Pakistan'),('Sri Lanka','Sri Lanka'),('Nepal','Nepal'),('Bhutan','Bhutan'),('Maldives','Maldives'),('Afghanistan','Afghanistan'),('Iran','Iran'),('Iraq','Iraq'),('Syria','Syria'),('Lebanon','Lebanon')))
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    account_status = models.CharField(max_length=50, blank=True, null=True, default='Active', choices=(('Active', 'Active'),('Inactive', 'Inactive'), ('Blocked', 'Blocked')))
    role = models.CharField(max_length=50, blank=True, null=True, default='Admin', choices=(('Admin', 'Admin'), ('User', 'User'), ('Customer', 'Customer'), ('Staff', 'Staff'), ('Manager', 'Manager')))
    dob = models.DateField(blank=True,null=True)
    dob = models.DateField(blank=True,null=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    addition_details = models.JSONField(blank=True, null=True)
    language=models.CharField(max_length=50,blank=True, null=True, default='English',choices=(('English','English'),('Hindi','Hindi'),('Spanish','Spanish'),('French','French'),('German','German'),('Italian','Italian'),('Portuguese','Portuguese'),('Russian','Russian'),('Chinese','Chinese'),('Japanese','Japanese'),('Korean','Korean'),('Arabic','Arabic'),('Turkish','Turkish'),('Dutch','Dutch'),('Polish','Polish'),('Swedish','Swedish'),('Danish','Danish'),('Norwegian','Norwegian'),('Finnish','Finnish'),('Greek','Greek'),('Czech','Czech'),('Hungarian','Hungarian'),('Romanian','Romanian'),('Bulgarian','Bulgarian'),('Croatian','Croatian'),('Slovak','Slovak'),('Slovenian','Slovenian'),('Lithuanian','Lithuanian'),('Latvian','Latvian'),('Estonian','Estonian'),('Ukrainian','Ukrainian'),('Belarusian','Belarusian'),('Serbian','Serbian'),('Macedonian','Macedonian'),('Bosnian','Bosnian'),('Albanian','Albanian'),('Montenegrin','Montenegrin'),('Catalan','Catalan'),('Basque','Basque'),('Galician','Galician'),('Welsh','Welsh'),('Irish','Irish'),('Scots Gaelic','Scots Gaelic'),('Manx','Manx'),('Cornish','Cornish'),('Breton','Breton')))
    departMent=models.CharField(max_length=50,blank=True,null=True,choices=(('IT','IT'),('HR','HR'),('Finance','Finance'),('Sales','Sales'),('Marketing','Marketing'),('Production','Production'),('Quality Control','Quality Control'),('Purchase','Purchase'),('Logistics','Logistics'),('Customer Service','Customer Service'),('R&D','R&D'),('Legal','Legal'),('Admin','Admin'),('Security','Security'),('Housekeeping','Housekeeping'),('Maintenance','Maintenance'),('Engineering','Engineering'),('Design','Design'),('Testing','Testing'),('Training','Training'),('Consulting','Consulting'),('Support','Support'),('Operations','Operations'),('Management','Management'),('Others','Others')))
    designation
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)