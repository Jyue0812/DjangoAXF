$(document).ready(function () {
    // //修改购物车
    // var addShoppings = document.getElementsByClassName("addShopping");
    // var subShoppings = document.getElementsByClassName("subShopping");
    //
    // for (var i = 0; i < addShoppings.length; i++){
    //     addShopping = addShoppings[i];
    //     addShopping.addEventListener("click", function(){
    //         pid = this.getAttribute("ga");
    //         $.post("/changecart/0/",{"productid":pid}, function(data){
    //             if (data.status == "success"){
    //                 //添加成功，把中间的span的innerHTML变成当前的数量
    //                 document.getElementById(pid).innerHTML = data.data;
    //                 document.getElementById(pid+"price").innerHTML = data.price
    //             }
    //         })
    //     })
    // }
    //
    //
    // for (var i = 0; i < subShoppings.length; i++){
    //     subShopping = subShoppings[i];
    //     subShopping.addEventListener("click", function(){
    //         pid = this.getAttribute("ga");
    //         $.post("/changecart/1/",{"productid":pid}, function(data){
    //             if (data.status == "success"){
    //                 //添加成功，把中间的span的innerHTML变成当前的数量
    //                 document.getElementById(pid).innerHTML = data.data;
    //                 document.getElementById(pid+"price").innerHTML = data.price;
    //                 if(data.data == 0) {
    //                     //window.location.href = "http://127.0.0.1:8001/cart/"
    //                     var li = document.getElementById(pid+"li");
    //                     li.parentNode.removeChild(li)
    //                 }
    //             }
    //         })
    //     })
    // }

    $('.subShopping').click(function () {

        //商品ｉｄ
        var ele = $(this);
        console.info($(this).attr('goodsid'));
        console.info($(this).attr('class'));

        $.ajax({
            url: '/sub_shopcar/',
            data: {'goodsid': $(this).attr('goodsid')},
            type: 'post',
            success: function (result) {

                //代表没有登陆，我们需要跳转到登陆页面
                if (result.result_code == '10009') {

                    //跳转到登陆页面
                    window.open('/login/', '_self');

                } else if (result.result_code == '10000' || result.result_code == '10008') {

                    //把数量反馈到ｓｐａｎ
                    //$('#shopcar_number').val(result.number);

                    //需要获取　当前控件的    上一个控件。
                    ele.next().html(result.number);

                }

                if (result.number == 0) {
                    var li = document.getElementById(ele.attr('goodsid') + "li");
                    console.log(li)
                    li.parentNode.removeChild(li)
                }
            }
        });

    });

    //添加到购物车
    $('.addShopping').click(function () {
        var ele = $(this);
        console.info($(this).attr('goodsid'));
        console.info($(this).attr('class'));
        //商品ｉｄ
        $.ajax({
            url: '/add_shopcar/',
            data: {'goodsid': $(this).attr('goodsid')},
            type: 'post',
            success: function (result) {
                console.log(result);
                //代表没有登陆，我们需要跳转到登陆页面
                if (result.result_code == '10009') {

                    //跳转到登陆页面
                    window.open('/login/', '_self');

                } else if (result.result_code == '10000') {

                    // alert($(this).prev().val());

                    //把数量反馈到ｓｐａｎ
                    //$('#shopcar_number').val(result.number);
                    //$('#shopcar_number').html(result.number);
                    ele.prev().html(result["number"]);
                }
            }
        });


    });


    var ok = document.getElementById("ok")
    ok.addEventListener("click", function () {
        var f = confirm("是否确认下单？")
        if (f) {
            $.post("/saveorder/", function (data) {
                if (data.status = "success") {
                    window.location.href = "http://127.0.0.1:8000/cart/"
                }
            })
        }
    }, false)
})