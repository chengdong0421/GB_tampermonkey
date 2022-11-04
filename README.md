# GB_tampermonkey
## tampermonkey脚本

### 作用：拼接在线预览时响应回来的图片并生成pdf文件
### 用法：启用脚本后，会在预览界面左上角生成两个按钮，先点击左边“获取页面”按钮，稍等，再点击“下载pdf”按钮
### 缺点：生成的pdf文件稍大，生成过程比较耗内存，页数过多的标准可能没法使用

## 代码写的比较粗糙，见谅。




2022.11.04


有人反馈预览页面不显示按钮了，经测试，确实如此。
不过目前脚本功能是好的，但不知道是不是网站屏蔽了油猴还是其他什么原因，脚本不能自动运行。但是可以通过手动执行的方法来运行这个脚本，方法如下：

1. 复制以下代码；
2. 在预览界面，按Ctrl+Shift+I 调出调试工具（这是谷歌Chrome浏览器的快捷方式，其他浏览器不知道是不是这个）；
3. 选择第二个页签（Console）(如下图)，鼠标在下面 > 处点一下，把代码粘贴在光标处，按回车运行代码。这样按钮就出来了。
![E_20)K}VQIBX0`KGCU X G9](https://user-images.githubusercontent.com/12667799/199972675-038243b5-5677-40d7-a39c-df312eb68cba.png)

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
