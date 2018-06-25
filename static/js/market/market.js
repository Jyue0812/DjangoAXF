$(function () {
    $('#alltypes').click(function () {
        $('#alltype').toggle();
        $(this).children().children().toggleClass("glyphicon glyphicon-menu-down glyphicon glyphicon-menu-up");
    });
    $('#orderbys').click(function () {
        $('#orderby').toggle();
        $(this).children().children().toggleClass("glyphicon glyphicon-menu-down glyphicon glyphicon-menu-up");
    });
    
    $(".addShopping").click(function () {
        $.ajax({
            url:'/add_shopcar/',
            data: {'goodsid': $(this).attr("goodsid")},
            type:"post",
            success:function(result) {
                console.log(result);
                if (result.result_code == '0009'){
                    window.open('/mine/mine/')

                }else if (result.result_code == '1000'){
                    $("#shopcar_number").html(result.number)
                }
            }

        })
    });
    $(".subShopping").click(function () {
        $.ajax({
            url:'/sub_shopcar/',
            data: {'goodsid': $(this).attr("goodsid")},
            type: "post",
            success: function(result) {
                console.log(result);
                if (result.result_code == '0009'){
                    window.open('/mine/mine/')

                }else if (result.result_code == '1000'){
                    $("#shopcar_number").html(result.number)
                }
            }

        })
    })
})