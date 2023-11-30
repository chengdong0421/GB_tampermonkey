// ==UserScript==
// @name         国标下载
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       wcd
// @match        http://c.gb688.cn/*
// @icon         data:image/png;base64,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
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
