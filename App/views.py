from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from App.models import WheelModel, NavModel, MustBuyModel, ShopModel, MainShow, FoodTypes, Goods, UserInfo, ShopCar


def home(request):
    wheels = WheelModel.objects.all()
    navs = NavModel.objects.all()
    mustbuys = MustBuyModel.objects.all()
    cvsList = ShopModel.objects.all()
    mainshows = MainShow.objects.all()

    shop_0 = cvsList[:1]
    shop_1 = cvsList[1:3]
    shop_2 = cvsList[3:7]
    shop_3 = cvsList[7:11]

    data = {
        "title": "首页",
        "wheels": wheels,
        "navs": navs,
        "mustbuys": mustbuys,
        "mainshows": mainshows,
        "shop_0": shop_0,
        "shop_1_3": shop_1,
        "shop_3_7": shop_2,
        "shop_7_11": shop_3,
    }
    return render(request, 'home/home.html', context=data)


def market(request):
    typeid = request.GET.get("typeid", 104749)
    childid = request.GET.get("childid", 0)
    orderby = int(request.GET.get("orderby", 0))
    foodtypes = FoodTypes.objects.all()

    fts = FoodTypes.objects.filter(typeid=typeid).first()
    child = fts.childtypenames



    childList = []
    for foo in child.split("#"):
        ft = foo.split(":")
        obj = {"name": ft[0],
               "id": ft[1]}
        childList.append(obj)
        print(obj)

    if int(childid) == 0:
        goods = Goods.objects.filter(categoryid=typeid)
    else:
        goods = Goods.objects.filter(categoryid=typeid, childcid=childid)


    if int(orderby) == 1:
        goods = goods.order_by("productnum")
    elif int(orderby) == 2:
        goods = goods.order_by("price")
    elif int(orderby) == 3:
        goods = goods.order_by("-price")

    data = {
        "title": "闪购超市",
        "foodtypes": foodtypes,
        "goods": goods,
        "typeid": int(typeid),
        "childList": childList,
        "childid": childid,
        "orderby": orderby,

    }
    return render(request, 'market/market.html', context=data)


def cart(request):
    data = {
        "title": "购物车",
    }
    return render(request, 'cart/cart.html', context=data)


def mine(request):
    data = {
        "title": "我的",
    }
    return render(request, 'mine/mine.html', context=data)


# def login(request):
#     user_info = request.session.get("user_info")
#
#     if not user_info:
#         user_name = request.POST.get("user_name")
#         user_pass = request.POST.get("user_pass")
#
#         user = UserInfo.objects.filter(user_name=user_name).first()
#         if user:
#             if user.pass_word == user_pass:
#                 request.session["user_name"] = user_name
#                 return redirect("/home/")
#             # return
#         # return


def add_shopcar(request):
    # user_id = request.session.get("user_id")
    data = {}
    # if not user_id:
    #     # return redirect(reversed(""))
    #     data["result_code"] = '0009'
    #     data["message"] = 'no login'
    # else:
    goods_id = request.POST.get("goodsid")

    shopcar = ShopCar.objects.filter(goods__id=goods_id).first()

    if shopcar:
        shopcar.number += 1
        shopcar.save()
    else:
        shopcar = ShopCar()
        shopcar.goods_id = goods_id
        shopcar.save()
        data["result_code"] = '1000'
        data["message"] = 'success'
    return JsonResponse(data)


def sub_shopcar(request):
    # user_id = request.session.get("user_id")
    data = {}
    # if not user_id:
    #     # return redirect(reversed(""))
    #     data["result_code"] = '0009'
    #     data["message"] = 'no login'
    # else:
    goods_id = request.POST.get("goodsid")

    shopcar = ShopCar.objects.filter(goods__id=goods_id).first()

    if shopcar:
        if shopcar.number <= 1:
            shopcar.delete()
            data["result_code"] = '1000'
            data["message"] = 'delete success'
            data["number"] = 0
        else:
            shopcar.number -= 1
            data["result_code"] = '1000'
            data["message"] = 'success'
            data["number"] = shopcar.number
    else:
        data["result_code"] = '1007'
        data["message"] = 'goods not exit'
    return JsonResponse(data)
