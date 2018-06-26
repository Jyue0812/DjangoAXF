from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from App.models import WheelModel, NavModel, MustBuyModel, ShopModel, MainShow, FoodTypes, Goods, ShopCar


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
        'title': '购物车'
    }

    user_id = request.session.get('_auth_user_id')

    if not user_id:
        return render(request, 'mine/login.html', {'error': '用户或者密码错误'})
    else:
        shopcars = ShopCar.objects.filter(user__id = user_id)
        print(shopcars)
        # shopcars = ShopCar.objects.filter(goods__id = goods_id )
        # print(shopcars)
        # shopcars = ShopCar.objects.all()
        return render(request, 'cart/cart.html', {'title': '购物车', 'shopcars': shopcars})


def mine(request):
    username = request.session.get("username", "未登录")
    data = {
        "title": "我的",
        "username":username
    }
    return render(request, 'mine/mine.html', context=data)



# 做登陆
def loginp(request):
    if request.method == 'POST':
        username = request.POST["username"]
        request.session["username"] = username
        user = authenticate(request, username = request.POST["username"], password = request.POST["userpass"])
        if user is None:
            return HttpResponse("用户名或密码有误，请重新输入")
        else:
            login(request, user)
            return redirect('/home/')
    else:
        return render(request, 'mine/login.html')

def logoutp(request):
    logout(request)
    return render(request, 'mine/login.html')

# 添加到购物车
def add_shopcar(request):
    user_id = request.session.get('_auth_user_id')
    data = {}
    if not user_id:
        data['result_code'] = '10009'
        data['message'] = 'no login'
    else:
        goods_id = request.POST.get('goodsid')  # 获取商品ｉｄ

        # 去购物车查询一下，如果商品存在，就对数量进行加减，如果商品不存在，直接添加该商品
        shopcar = ShopCar.objects.filter(goods__id=goods_id).first()
        print(shopcar)

        if shopcar:
            shopcar.number = shopcar.number + 1
            shopcar.save()
        else:
            shopcar = ShopCar()  # 构建一条购物车的数据
            # shopcar.user_id = user_id
            shopcar.goods_id = goods_id
            shopcar.save()

        data['result_code'] = '10000'
        data['message'] = 'success'
        data['number'] = shopcar.number
    return JsonResponse(data)

def sub_shopcar(request):
    user_id = request.session.get('_auth_user_id')
    data = {}

    if not user_id:
        data['result_code'] = '10009'
        data['message'] = 'no login'
    else :
        goods_id = request.POST.get('goodsid')

        # 去购物车查询一下，如果商品存在，就对数量进行加减，如果商品不存在，直接添加该商品
        shopcar = ShopCar.objects.filter(goods__id=goods_id).first()

        #如果商品存在，就代表需要进行加减
        if shopcar:

            #如果商品数量等于一个，就需要从购物车删除这个商品
            if shopcar.number <= 1:

                shopcar.delete()

                data['result_code'] = '10008'
                data['message'] = 'delete success'
                data['number'] = 0

            #数量进行－１
            else:
                shopcar.number = shopcar.number-1
                shopcar.save()
                data['result_code'] = '10000'
                data['message'] = 'success'
                data['number'] = shopcar.number
        else:
            data['result_code'] = '10007'
            data['message'] = 'goods not exist'

    return JsonResponse(data)

def register(request):
    return render(request, 'mine/register.html', {"title":"注册"})
