from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from App.forms.forms import LoginForm, RegisterForm
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
        'title': '购物车'
    }

    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'mine/login.html', {'error': '用户或者密码错误'})
    else:
        shopcars = ShopCar.objects.filter(user__id=user_id)
        return render(request, 'cart/cart.html', {'shopcars': shopcars, 'title': '购物车'})


def mine(request):
    data = {
        "title": "我的",
    }
    return render(request, 'mine/mine.html', context=data)



# 做登陆
def login(request):
    if request.method == 'GET':
        return render(request, 'mine/login.html')

    # 先去会话里面查找用户是否登陆
    user_info = request.session.get('user_info')

    # 没有登陆，执行登陆过程，并且保存ｕｓｅｒ
    if not user_info:

        user_name = request.POST.get('userName')
        user_pass = request.POST.get('userPass')

        # 执行登陆
        user = UserInfo.objects.filter(user_name=user_name).first()

        if user:

            if user.user_passwd == user_pass:
                # session里面能否保存一个　对象（还是说只能保存一个ｊｓｏｎ串)
                request.session['user_info'] = user_name
                request.session['user_id'] = user.id
                return render(request, 'home/home.html')

        return render(request, 'mine/login.html', {'error': '用户或者密码错误'})

    return render(request, 'home/home.html')


# 添加到购物车
def add_shopcar(request):
    user_id = request.session.get('user_id')

    data = {}

    if not user_id:
        data['result_code'] = '10009'
        data['message'] = 'no login'
    else:

        goods_id = request.POST.get('goodsid')  # 获取商品ｉｄ

        # 去购物车查询一下，如果商品存在，就对数量进行加减，如果商品不存在，直接添加该商品
        shopcar = ShopCar.objects.filter(goods__id=goods_id).first()

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
    user_id = request.session.get('user_id')
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
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['passwd']
            # 添加到数据库
            registAdd = UserInfo.objects.get_or_create(user_name=username, user_passwd=password)[1]
            user = UserInfo.objects.filter(user_name=username).first()
            request.session["user_info"] = username
            request.session["user_id"] = user.id
            # User.objects.get_or_create(username = username,password = password)

            return render(request, 'mine/mine.html', {'registAdd': registAdd, 'username': username})
    else:
        form = RegisterForm()
    return render(request, 'mine/register.html', {"title":"注册", "form":form})
