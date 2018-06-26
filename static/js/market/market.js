$(function () {
    $('#alltypes').click(function () {
        $('#alltype').toggle();
        $(this).children().children().toggleClass("glyphicon glyphicon-menu-down glyphicon glyphicon-menu-up");
    });
    $('#orderbys').click(function () {
        $('#orderby').toggle();
        $(this).children().children().toggleClass("glyphicon glyphicon-menu-down glyphicon glyphicon-menu-up");
    });
    
             //添加到购物车
    $('.subShopping').click(function(){

        //商品ｉｄ
        var ele = $(this);
        console.info($(this).attr('goodsid'));
        console.info($(this).attr('class'));

        $.ajax({
            url:'/sub_shopcar/',
            data:{'goodsid':$(this).attr('goodsid')},
            type:'post',
            success:function(result){

                //代表没有登陆，我们需要跳转到登陆页面
                if(result.result_code == '10009'){

                    //跳转到登陆页面
                    window.open('/login/','_self');

                }else if(result.result_code == '10000' || result.result_code == '10008'){

                    //把数量反馈到ｓｐａｎ
                    //$('#shopcar_number').val(result.number);

                    //需要获取　当前控件的    上一个控件。
                    ele.next().html(result.number);

                }
            }
        });


    });

    //添加到购物车
    $('.addShopping').click(function(){
        var ele = $(this);
        //商品ｉｄ
        $.ajax({
            url:'/add_shopcar/',
            data:{'goodsid':$(this).attr('goodsid')},
            type:'post',
            success:function(result){

                //代表没有登陆，我们需要跳转到登陆页面
                if(result.result_code == '10009'){

                    //跳转到登陆页面
                    window.open('/login/','_self');

                }else if(result.result_code == '10000'){

                    // alert($(this).prev().val());

                    //把数量反馈到ｓｐａｎ
                    //$('#shopcar_number').val(result.number);
                    //$('#shopcar_number').html(result.number);
                    ele.prev().html(result["number"]);
                }
            }
        });


    });
})