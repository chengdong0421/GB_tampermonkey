// ==UserScript==
// @name         国标下载
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       wcd
// @match        http://c.gb688.cn/*
// @icon         https://www.google.com/s2/favicons?sz=64&domain=gb688.cn
// @grant        none
// @require      https://code.jquery.com/jquery-3.6.0.min.js

// ==/UserScript==

(function() {
    'use strict';
$(function(){

    $("head").append('<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>');

    let my_script=`<script>

            function px2Num(px) {
                return Number(px.split("px")[0].toString());
            }


            function getPages(){
                if( $("canvas[id^=canvas_]").length > 0 ) {
                    $("canvas[id^=canvas_]").delete();

                }
                var baseurl = "http://c.gb688.cn/bzgk/gb/";
                var pagecount = $("div.page").length;
                var pages = new Array(pagecount);
                var pagebg = new Array(pagecount);
                var title = $("title").text().split("|")[1].toString().trim();
                var pheight = $("#0").css("height");
                var pwidth = $("#0").css("width");

                $(".page").each(function(i, elem) {
                    if (elem.hasAttribute("bg")) {
                        pagebg[i] = elem.getAttribute("bg");
                    } else {
                        pagebg[i] = $(elem).children("span").first().css("background-image").split('"')[
                            1].split(/\\//).slice(-1)[0];
                    }
                });


                //拼合图片
                $(".page").each(function(i, elem) {
                    var canvasclone = $("canvas#canvas").clone();
                    canvasclone.attr("id","canvas_"+i).css("background-color","#FFFFFFFF");
                    $("#newimg").append(canvasclone);
                    var canvas = document.getElementById('canvas_'+i);
                    var ctx = canvas.getContext('2d');
                    ctx.fillStyle="white";
                    ctx.fillRect(0,0,px2Num(pwidth), px2Num(pheight));

                    $("#imgContainer").append("<img id=img_" + i + " src='" + baseurl+pagebg[i] + "' />")
                    var image = document.getElementById('img_'+i);

                    image.addEventListener('load', e => {
                        $(elem).children("span").each(function(j,s){
                             ctx.drawImage(image, -px2Num($(s).css("background-position-x")), -px2Num($(s).css("background-position-y")),  119, 168,
                             $(s).attr("class").split('-')[1]*119, $(s).attr("class").split('-')[2]*168, 119, 168);
                        });
                    });

                });
            }

            function isimgComplete(imgs){
                //$("img[id^=img_]")
                flag = true;
                for(i=0;i<imgs.length;i++){
                    flag=flag && imgs[i].complete;
                }
                return flag;
            }

            function downloadPDF(){
                if( $("canvas[id^=canvas_]").length == 0 ) {
                    alert("请先点击获取页面！");
                    return;
                }

                var images = $("img[id^=img_]");
                //alert(isimgComplete(images));
                if(!isimgComplete(images)){
                    alert("页面尚未提取完，稍后再试");
                    return;
                }

                var pheight = $("#0").css("height");
                var pwidth = $("#0").css("width");
                const { jsPDF } = window.jspdf;
                const pdf = new jsPDF('p','px',[px2Num(pwidth), px2Num(pheight)]);

                var title = $("title").text().split("|")[1].toString().trim();

                let [imgX, imgY] = [595.28, 841.89];
                let imgHeight = imgX / (px2Num(pwidth) / px2Num(pheight));

                $("canvas[id^=canvas_]").each(function(i,e){
                    pdf.addImage(document.getElementById('canvas_'+i).toDataURL('image/jpeg'), 'jpeg', 0, 0, px2Num(pwidth), px2Num(pheight), '', 'MEDDIUM');
                    //pdf.addImage(document.getElementById('canvas_'+i).toDataURL('image/png'), 'jpeg', 0, 0, imgX, imgHeight, '', 'SLOW');
                    pdf.addPage();
                });

                let targetPage = pdf.internal.getNumberOfPages();
                pdf.deletePage(targetPage); // 删除最后一页

                pdf.save(title + ".pdf");
            }

             function downloadPDF0(){
                while($("canvas[id^=canvas_]").length < $(".page").length){
                    setTimeout(function(){

                    },1000);
                }
             }


        </script>`;

    let source_img = `
        <div id="canvas_container">
            <input type="button" value="获取页面" onclick="getPages()"/>
            <input type="button" value="下载pdf" onclick="downloadPDF()"/>
        </div>
        <div id="imgContainer" style="display:none;"><img id="source" src=""></div>
        <div id="newimg" width="1190px"></div>
        <canvas id="canvas" width="1190px" height="1680px" style="display:none;"></canvas>`;

    //let btn = `<input type="button" value="获取页面" onclick="getPages()"/>
               //<input type="button" value="下载pdf" onclick="downloadPDF()"/>`;

    let style = `
        <style>
            #canvas_container {
                position: fixed;
                height: 30px;
                width: 150px;
                top: 50px;
                left: 10px;
                border: 1px;
                /*background-color: #00ff0099;*/
                border-radius: 3px;
            }
        </style>
    `;

    $("head").append(style);
    $("body").append(source_img);
    $("body").append(my_script);
    //$("body").append(btn);

    //alert($("title").text());
});

})();
