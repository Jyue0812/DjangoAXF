from django.db import models

# Create your models here.
from django.db.models import CASCADE


class BaseModel(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=100)
    trackid = models.CharField(max_length=20)

    class Meta:
        abstract=True

class WheelModel(BaseModel):
     class Meta:
         db_table = 'axf_wheel'


class NavModel(BaseModel):
    class Meta:
        db_table = 'axf_nav'

class MustBuyModel(BaseModel):
    class Meta:
        db_table = 'axf_mustbuy'

class ShopModel(BaseModel):
    class Meta:
        db_table = 'axf_shop'

class MainShow(BaseModel):
    categoryid = models.IntegerField(null=True)
    brandname = models.CharField(max_length=100)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=200)
    productid1 = models.CharField(max_length=200)
    longname1 = models.CharField(max_length=200)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=200)
    productid2 = models.CharField(max_length=200)
    longname2 = models.CharField(max_length=200)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=200)
    productid3 = models.CharField(max_length=200)
    longname3 = models.CharField(max_length=200)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'

class FoodTypes(models.Model):
    typeid = models.IntegerField(default=0)
    typename = models.CharField(max_length=50)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(null=True)

    class Meta:
        db_table = 'axf_foodtypes'

class Goods(models.Model):
    # 商品id
    productid = models.CharField(max_length=10)
    # 商品图片
    productimg = models.CharField(max_length=150)
    # 商品名称
    productname = models.CharField(max_length=50)
    # 商品长名称
    productlongname = models.CharField(max_length=100)
    # 是否精选
    isxf = models.NullBooleanField(default=False)
    # 是否买一赠一
    pmdesc = models.CharField(max_length=10)
    # 规格
    specifics = models.CharField(max_length=20)
    # 价格
    price = models.CharField(max_length=10)
    # 超市价格
    marketprice = models.CharField(max_length=10)
    # 组id
    categoryid = models.CharField(max_length=10)
    # 子类组id
    childcid = models.CharField(max_length=10)
    # 子类组名称
    childcidname = models.CharField(max_length=10)
    # 详情页id
    dealerid = models.CharField(max_length=10)
    # 库存
    storenums = models.IntegerField()
    # 销量
    productnum = models.IntegerField()

    class Meta:
        db_table= 'axf_goods'


class UserInfo(models.Model):
    user_name = models.CharField(max_length=20)
    user_pass = models.CharField(max_length=20)

    class Meta:
        db_table = 'axf_userinfo'


class ShopCar(models.Model):
    goods =models.ForeignKey(Goods, on_delete=CASCADE)
    # user = models.ForeignKey(UserInfo, on_delete=CASCADE)
    number = models.IntegerField(default=1)