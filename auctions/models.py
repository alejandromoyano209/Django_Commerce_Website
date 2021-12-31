from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
	pass


class Bid(models.Model):
	user = models.CharField(max_length=64, default="")
	bid = models.IntegerField()
	auctionid = models.IntegerField(default=None)

class Comment(models.Model):
	user = models.CharField(max_length=64, default="")
	comment = models.CharField(max_length=256)
	auctionid = models.IntegerField(default=None)

	def __str__(self):
		return f"{self.comment}"

class Watchlist(models.Model):
	user = models.CharField(max_length=64, default="")
	auctionid = models.IntegerField()
	auction = models.CharField(max_length=64, default="")

class Category(models.Model):
	category = models.CharField(max_length=64, default="")


class AuctionList(models.Model):
	user = models.CharField(max_length=64, default="")
	auction = models.CharField(max_length=64)
	description = models.CharField(max_length=512, default="")
	img = models.URLField(default=None, blank=True)
	oferta = models.IntegerField(default=0)
	#monto = models.ManyToManyField(Bid, related_name="Amount", default=0)
	categoria = models.CharField(max_length=64, default="")
	status = models.BooleanField(default=True)
	winneruser = models.CharField(max_length=64)

	def __str__(self):
		return f"publicación {self.id}: {self.auction} | descripción: {self.description} {self.img} | oferta: {self.oferta} | categoría: {self.categoria} | user: {self.user} | winneruser: {self.winneruser}"	