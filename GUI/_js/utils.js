/**
 * Normalize the browser animation API across implementations. This requests
 * the browser to schedule a repaint of the window for the next animation frame.
 * Checks for cross-browser support, and, failing to find it, falls back to setTimeout.
 * @param {function}    callback  Function to call when it's time to update your animation for the next repaint.
 * @param {HTMLElement} element   Optional parameter specifying the element that visually bounds the entire animation.
 * @return {number} Animation frame request.
 */


//global variables

var mouseControl=1;
var keyControl=2;  //how user control player
var shiftY=0;
var shiftX=0;
var levelCO=1;    //level of CO increase productivity of plant in interval 0-1;
var world; //world player exist now
var plantExist;  //how many plants in world
var table;
var table1;
var table2;
var recordID=0;
var pageText="";
var ln="rus";
var textInput="entry"


var lastTime=Date.now();  //main program loop timer
var loopRequest=0;        //display animation flag
var dt;  				  //main time synchronisation variable
var showMainMenu=0;

function print(text){
	///console.log(text);
	alert(text);
}//_____________________________________________________

function hex2char(str){
	return parseInt('0x'+str);
}//_____________________________________________________

function hex2int(str){
	return parseInt('0x'+str);
}//_____________________________________________________

function hex2float(str){
	return parseInt('0x'+str);
}//_____________________________________________________

function cout(text){
	//getNode("text").value+=text+'\n';
	console.log(text);
}//_____________________________________________________



function parseC(str)
{
	var res="";
	
	var lines=str.split("\n");
	//cout(lines.length);
	for(var i=0;i<lines.length;i++)
	{
		var line=lines[i];
		line=line.replace(/[ \t]*\/\/.*/g,"");
		if(line!=""){
			line=line.replace(/[ \t]*([^ ]+)[ \t]+([^; ]+).*\[([^\]]+)\].*;.*/g,"$1 $2 $3");
			if(line!=""){
				line=line.replace(/[ \t]*([^ ]+)[ \t]+([^; ]+).*;.*/g,"$1 $2");
				res+=line+':|:';
			}else{
		
			}
		}
	}
	
	return res;
}//_____________________________________________________

/* функция чтения С структур
	при проектировании структуры в коде С необходимо учитывать
	что элементы типа char в структуре выравниваются по четыре байта
	также и элементы типа short.
	Поэтому такие элементы необходимо располагать в структуре блоками
	кратными 4 байтам
*/
function parseStructC(str, textC, structC) {
    var print=0;
    var textCStruct=textC[structC.structType];
    if(print) cout(structC.structType + "=>" + textCStruct);

    var cCodeArray=textCStruct.split(":|:");
    for(var index=0; index < cCodeArray.length; index++) {
        var item=cCodeArray[index];
        if(print) cout(">>" + item + "/");
        if(item=="") { continue; }
        if(print > 1) cout("pos:" + pos);
        var line=item.split(" ");

        if(line[0]=="uchar") {
            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var hex=str[pos] + str[pos + 1];
                    pos +=2;
                    structC[line[1]].push(hex2char(hex));
                    if(print > 1) cout("c->" + line[1] + ": " + hex2char(hex));
                }
            } else {
                var hex=str[pos] + str[pos + 1];
                pos +=2;
                structC[line[1]]=hex2char(hex);
                if(print > 1) cout("c->" + line[1] + ": " + hex2char(hex));
            }
        } else if(line[0]=="char") {
            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var hex=str[pos] + str[pos + 1];
                    pos +=2;
                    var data=hex2char(hex);
                    if(data > 128) data -=256;
                    structC[line[1]].push(data);
                    if(print > 1) cout("c->" + line[1] + ": " + data);
                }
            } else {
                var hex=str[pos] + str[pos + 1];
                pos +=2;
                var data=hex2char(hex);
                if(data > 128) data -=256;
                structC[line[1]]=data;
                if(print > 1) cout("c->" + line[1] + ": " + data);
            }
        } else if(line[0]=="ushort") {
            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var hex=str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                    pos +=4;
                    structC[line[1]].push(hex2int(hex));
                    if(print > 1) cout("s->" + line[1] + ": " + hex2int(hex));
                }
            } else {
                var hex=str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                pos +=4;
                structC[line[1]]=hex2int(hex);
                if(print > 1) cout("s->" + line[1] + ": " + hex2int(hex));
            }
        } else if(line[0]=="short") {
            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var hex=str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                    pos +=4;
                    var data=hex2int(hex);
                    if(data > 32767) data -=65536;
                    structC[line[1]].push(data);
                    if(print > 1) cout("c->" + line[1] + ": " + data);
                }
            } else {
                var hex=str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                pos +=4;
                var data=hex2int(hex);
                if(data > 32767) data -=65536;
                structC[line[1]]=data;
                if(print > 1) cout("c->" + line[1] + ": " + data);
            }
        } else if(line[0]=="uint") {
            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var hex=str[pos + 6] + str[pos + 7] + str[pos + 4] + str[pos + 5] +
                        str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                    pos +=8;
                    structC[line[1]].push(hex2int(hex));
                    if(print > 1) cout("i->" + line[1] + ": " + hex2int(hex));
                }
            } else {
                var hex=str[pos + 6] + str[pos + 7] + str[pos + 4] + str[pos + 5] +
                    str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                pos +=8;
                structC[line[1]]=hex2int(hex);
                if(print > 1) cout("i->" + line[1] + ": " + hex2int(hex));
            }

        } else if(line[0]=="int") {
            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var hex=str[pos + 6] + str[pos + 7] + str[pos + 4] + str[pos + 5] +
                        str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                    pos +=8;
                    var data=hex2int(hex);
                    if(data > 2147483647) data -=4294967296;
                    structC[line[1]].push(data);
                    if(print > 1) cout("c->" + line[1] + ": " + data);
                }
            } else {
                var hex=str[pos + 6] + str[pos + 7] + str[pos + 4] + str[pos + 5] +
                    str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                pos +=8;
                var data=hex2int(hex);
                if(data > 2147483647) data -=4294967296;
                structC[line[1]]=data;
                if(print > 1) cout("c->" + line[1] + ": " + data);
            }
        } else if(line[0]=="float") {
            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var hex=str[pos + 6] + str[pos + 7] + str[pos + 4] + str[pos + 5] +
                        str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                    pos +=8;
                    structC[line[1]].push(hex2float(hex));
                    if(print > 1) cout("i->" + line[1] + ": " + hex2float(hex));
                }
            } else {
                var hex=str[pos + 6] + str[pos + 7] + str[pos + 4] + str[pos + 5] +
                    str[pos + 2] + str[pos + 3] + str[pos] + str[pos + 1];
                pos +=8;
                structC[line[1]]=hex2float(hex);
                if(print > 1) cout("i->" + line[1] + ": " + hex2float(hex));
            }
        } else {
            if(print) cout("STRUCT:" + item + " ");

            if(line.length > 2) {
                var count=parseInt(line[2]);
                structC[line[1]]=new Array();
                for(var n=0; n < count; n++) {
                    var list={};
                    list.structType=line[0];
                    if(print > 1) cout("parse struct:" + line[0]);
                    parseStructC(str, textC, list);
                    structC[line[1]].push(list);
                    if(print > 1) cout("done")
                }
            } else {
                var list={};
                list.structType=line[0];
                if(print > 1) cout("parse struct:" + line[0]);
                parseStructC(str, textC, list);
                structC[line[1]]=list;
                if(print > 1) cout("done")
            }
        }
    }
}  //_____________________________________________________


function ahah(url, target) {
  document.getElementById(target).innerHTML = ' Fetching data...';
  if (window.XMLHttpRequest) {
    req = new XMLHttpRequest();
  } else if (window.ActiveXObject) {
    req = new ActiveXObject("Microsoft.XMLHTTP");
  }
  if (req != undefined) {
    req.onreadystatechange = function() {ahahDone(url, target);};
    req.open("GET", url, false);
    req.send("");
  }
}  

function ahahDone(url, target) {
  if (req.readyState == 4) { // only if req is "loaded"
    if (req.status == 200) { // only if "OK"
      document.getElementById(target).value = req.responseText;
      //eval(req.responseText);
      selectAction();
    } else {
      document.getElementById(target).value=" AHAH Error:\n"+ req.status + "\n" +req.statusText;
    }
  }
}

function load(name, div) {
	ahah(name,div);
	return false;
}

function setCookie(cname, cvalue, exdays) {
		var d = new Date();
		d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
		var expires = "expires="+d.toUTCString();
		document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
	
function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i = 0; i <ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0) == ' ') {
			c = c.substring(1);
		}
		if (c.indexOf(name) == 0) {
			return c.substring(name.length, c.length);
		}
	}
	return "";
}

function sendHTTP(type,url,body,callback){

			var XHR=("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr=new XHR();	
			xhr.open('POST', url, true);
								
			xhr.setRequestHeader('Content-Type', type);
			xhr.setRequestHeader('Accept',type);
			//xhr.setRequestHeader('X-Requested-With','XMLHttpRequest');
			xhr.onload=function() {
			  callback(this.responseText);
			}
			//callback(this.responseText+"1");
			xhr.onerror=function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);
}		

function sendHTTP_GET(url,callback){

			var XHR=("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr=new XHR();	
			xhr.open('GET', url, true);

			xhr.onload=function() {
			  callback(this.responseText);
			}

			xhr.onerror=function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send();
}	

	
function byteToHexString(uint8arr) {
  if (!uint8arr) {
    return '';
  }
  
  var hexStr = '';
  for (var i = 0; i < uint8arr.length; i++) {
    var hex = (uint8arr[i] & 0xff).toString(16);
    hex = (hex.length === 1) ? '0' + hex : hex;
    hexStr += hex;
  }
  
  return hexStr.toUpperCase();
}

function hexStringToByte(str) {
  if (!str) {
    return new Uint8Array();
  }
  
  var a = [];
  for (var i = 0, len = str.length; i < len; i+=2) {
    a.push(parseInt(str.substr(i,2),16));
  }
  
  return new Uint8Array(a);
}
		

 // Book over :)
function bookOver() {
    //document.getElementById('book-over').style.display='block';
    //document.getElementById('book-over-overlay').style.display='block';
    //isBookOver=true;
}

function getNode(el){return document.getElementById(el);}

function getSelector(id){
	var  e = document.getElementById (id);
	var  str = e.options [e.selectedIndex] .value;
	return str;
}
 
function getParam(parameterName) { 
    var result = "",
        tmp = [];
    window.location.search
        .substr(1)
        .split("&")
        .forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

function getParamStr(parameterName,request) { 
    var result = "",
        tmp = [];
    request.split("&").forEach(function (item) {
          tmp = item.split("=");
          if (tmp[0] === parameterName) result = decodeURIComponent(tmp[1]);
        });
    return result;
}

function encodeURL(s){
	return encodeURIComponent(s).replace(/[!'()*]/g, escape);
}

function arr2str(arr) {
  // or [].slice.apply(arr)
  var utf8 = Array.from(arr).map(function (item) {
    return String.fromCharCode(item);
  }).join('');
  
  return decodeURIComponent(escape(utf8));
}
function str2arr(str) {
  var utf8 = unescape(encodeURIComponent(str));
  return new Uint8Array(utf8.split('').map(function (item) {
    return item.charCodeAt();
  }));
}

// A cross-browser requestAnimationFrame
// See https://hacks.mozilla.org/2011/08/animating-with-javascript-from-setinterval-to-requestanimationframe/
var requestAnimFrame=(function(){
    return window.requestAnimationFrame       ||
        window.webkitRequestAnimationFrame ||
        window.mozRequestAnimationFrame    ||
        window.oRequestAnimationFrame      ||
        window.msRequestAnimationFrame     ||
        function(callback){
            window.setTimeout( callback , 17);
        };
})();

/**
 * ERRATA: 'cancelRequestAnimationFrame' renamed to 'cancelAnimationFrame' to reflect an update to the W3C Animation-Timing Spec.
 *
 * Cancels an animation frame request.
 * Checks for cross-browser support, falls back to clearTimeout.
 * @param {number}  Animation frame request.
 */
if (!window.cancelAnimationFrame) {
  window.cancelAnimationFrame=(window.cancelRequestAnimationFrame ||
                                 window.webkitCancelAnimationFrame || window.webkitCancelRequestAnimationFrame ||
                                 window.mozCancelAnimationFrame || window.mozCancelRequestAnimationFrame ||
                                 window.msCancelAnimationFrame || window.msCancelRequestAnimationFrame ||
                                 window.oCancelAnimationFrame || window.oCancelRequestAnimationFrame ||
                                 window.clearTimeout);
}

/* Object that contains our utility functions.
 * Attached to the window object which acts as the global namespace.
 */
window.utils={};

/**
 * Keeps track of the current mouse position, relative to an element.
 * @param {HTMLElement} element
 * @return {object} Contains properties: x, y, event
 */
window.utils.captureMouse=function (element) {
  var mouse={x: 0, y: 0, event: null},
      body_scrollLeft=document.body.scrollLeft,
      element_scrollLeft=document.documentElement.scrollLeft,
      body_scrollTop=document.body.scrollTop,
      element_scrollTop=document.documentElement.scrollTop,
      offsetLeft=element.offsetLeft,
      offsetTop=element.offsetTop;
  
  element.addEventListener('mousemove', function (event) {
    var x, y;
    
    if (event.pageX || event.pageY) {
      x=event.pageX;
      y=event.pageY;
    } else {
      x=event.clientX+ body_scrollLeft+ element_scrollLeft;
      y=event.clientY+ body_scrollTop+ element_scrollTop;
    }
    x -=offsetLeft;
    y -=offsetTop;
    
    mouse.x=x;
    mouse.y=y;
    mouse.event=event;
  }, false);
  
  return mouse;
};

/**
 * Keeps track of the current (first) touch position, relative to an element.
 * @param {HTMLElement} element
 * @return {object} Contains properties: x, y, isPressed, event
 */
window.utils.captureTouch=function (element) {
  var touch={x: null, y: null, isPressed: false, event: null},
      body_scrollLeft=document.body.scrollLeft,
      element_scrollLeft=document.documentElement.scrollLeft,
      body_scrollTop=document.body.scrollTop,
      element_scrollTop=document.documentElement.scrollTop,
      offsetLeft=element.offsetLeft,
      offsetTop=element.offsetTop;

  element.addEventListener('touchstart', function (event) {
    touch.isPressed=true;
    touch.event=event;
  }, false);

  element.addEventListener('touchend', function (event) {
    touch.isPressed=false;
    touch.x=null;
    touch.y=null;
    touch.event=event;
  }, false);
  
  element.addEventListener('touchmove', function (event) {
    var x, y,
        touch_event=event.touches[0]; //first touch
    
    if (touch_event.pageX || touch_event.pageY) {
      x=touch_event.pageX;
      y=touch_event.pageY;
    } else {
      x=touch_event.clientX+ body_scrollLeft+ element_scrollLeft;
      y=touch_event.clientY+ body_scrollTop+ element_scrollTop;
    }
    x -=offsetLeft;
    y -=offsetTop;
    
    touch.x=x;
    touch.y=y;
    touch.event=event;
  }, false);
  
  return touch;
};

/**
 * Returns a color in the format: '#RRGGBB', or as a hex number if specified.
 * @param {number|string} color
 * @param {boolean=}      toNumber=false  Return color as a hex number.
 * @return {string|number}
 */
window.utils.parseColor=function (color, toNumber) {
  if (toNumber===true) {
    if (typeof color==='number') {
      return (color | 0); //chop off decimal
    }
    if (typeof color==='string' && color[0]==='#') {
      color=color.slice(1);
    }
    return window.parseInt(color, 16);
  } else {
    if (typeof color==='number') {
      color='#'+ ('00000'+ (color | 0).toString(16)).substr(-6); //pad
    }
    return color;
  }
};

/**
 * Converts a color to the RGB string format: 'rgb(r,g,b)' or 'rgba(r,g,b,a)'
 * @param {number|string} color
 * @param {number}        alpha
 * @return {string}
 */
window.utils.colorToRGB=function (color, alpha) {
  //number in octal format or string prefixed with #
  if (typeof color==='string' && color[0]==='#') {
    color=window.parseInt(color.slice(1), 16);
  }
  alpha=(alpha===undefined) ? 1 : alpha;
  //parse hex values
  var r=color >> 16 & 0xff,
      g=color >> 8 & 0xff,
      b=color & 0xff,
      a=(alpha < 0) ? 0 : ((alpha > 1) ? 1 : alpha);
  //only use 'rgba' if needed
  if (a===1) {
    return "rgb("+ r+","+ g+","+ b+")";
  } else {
    return "rgba("+ r+","+ g+","+ b+","+ a+")";
  }
};

/**
 * Determine if a rectangle contains the coordinates (x,y) within it's boundaries.
 * @param {object}  rect  Object with properties: x, y, width, height.
 * @param {number}  x     Coordinate position x.
 * @param {number}  y     Coordinate position y.
 * @return {boolean}
 */
window.utils.containsPoint=function (rect, x, y) {
  return !(x < rect.x ||
           x > rect.x+ rect.width ||
           y < rect.y ||
           y > rect.y+ rect.height);
};

/**
 * Determine if two rectangles overlap.
 * @param {object}  rectA Object with properties: x, y, width, height.
 * @param {object}  rectB Object with properties: x, y, width, height.
 * @return {boolean}
 */
window.utils.intersects=function (rectA, rectB) {
  return !(rectA.x+ rectA.width < rectB.x ||
           rectB.x+ rectB.width < rectA.x ||
           rectA.y+ rectA.height < rectB.y ||
           rectB.y+ rectB.height < rectA.y);
};


///draw on canvas functions
///common function


function drawDot(pos,color,context){
	  context.beginPath();
      context.arc(pos[0], pos[1], 3, 0, 2 * Math.PI, false);
      context.fillStyle=color;
      context.fill();
}

/**
 * Returns a random number between min (inclusive) and max (exclusive)
 */
function getRandom(min, max) {
	if(max<=0)return 0;
    return Math.random() * (max - min)+ min;
}

/**
 * Returns a random integer between min (inclusive) and max (inclusive)
 * Using Math.round() will give you a non-uniform distribution!
 */
function getRandomInt(min, max) {
	if(max<=0)return 0;
    return Math.floor(Math.random() * (max - min+ 1))+ min;
}

function memcpy(dst, dstOffset, src, srcOffset, length) {
  var dstU8 = new Uint8Array(dst, dstOffset, length);
  var srcU8 = new Uint8Array(src, srcOffset, length);
  dstU8.set(srcU8);
};

function newBuffer(dataBuf,offset,size){
    buf=new ArrayBuffer(size);
	memcpy(buf,0,dataBuf,offset,size);
	return buf;
}

function encode_utf8(s) {
  return unescape(encodeURIComponent(s));
}

function decode_utf8(s) {
  return decodeURIComponent(escape(s));
}

function ab2str(buf) {
   var s = String.fromCharCode.apply(null, new Uint8Array(buf));
   return decode_utf8(s)
}

function str2ab(str) {
   var s = encode_utf8(str)
   var buf = new ArrayBuffer(s.length); 
   var bufView = new Uint8Array(buf);
   for (var i=0, strLen=s.length; i<strLen; i++) {
     bufView[i] = s.charCodeAt(i);
   }
   //print (bufView)
   //print (buf);
   //print("________");
   return buf;
}


function stringFromUTF8Array(data)
  {
    const extraByteMap = [ 1, 1, 1, 1, 2, 2, 3, 0 ];
    var count = data.length;
    var str = "";
    
    for (var index = 0;index < count;)
    {
      var ch = data[index++];
      if (ch & 0x80)
      {
        var extra = extraByteMap[(ch >> 3) & 0x07];
        if (!(ch & 0x40) || !extra || ((index + extra) > count))
          return null;
        
        ch = ch & (0x3F >> extra);
        for (;extra > 0;extra -= 1)
        {
          var chx = data[index++];
          if ((chx & 0xC0) != 0x80)
            return null;
          
          ch = (ch << 6) | (chx & 0x3F);
        }
      }
      
      str += String.fromCharCode(ch);
    }
    
    return str;
  }


    /**строка с размеченными подстроками используется как формат передачи данных
     в таблицах GVector. Записанную в GVector TString можно только читать.
     в памяти стороку можно изменять и записывать в GVector новую стороку.
     измененная в памяти строка сериализуется функцией save();
     */

class TString {
    constructor(dataBuf) {
    	if(!dataBuf){
    		this.init();
    	}else{
    		this.data=dataBuf;
    		var v=new Uint32Array(dataBuf,0,4);
			this.len=v[0];
			this.index=new Uint32Array(dataBuf,4,this.len*4+4);
    		this.sizeData=this.index[this.len];
		}	
    }; 
    
    init(){
        this.data=new ArrayBuffer(12);
        this.len=0; 
        var v=new Uint32Array(this.data,0,4);
		v[0]=0;
		this.index=new Uint32Array(this.data,4,8);
		this.index[0]=0;
		this.index[1]=0;
        this.sizeData=0;
    }
    
    
    //восстановление указателей на данные после записи в vector и другиз перемещений данных
	reloadPtr(){
    }

    push_back(record){
    	var bin;
		if(typeof(record)=="string"){
			bin=str2ab(record);
			print ("str2ab");
		    print(bin);
		}else{
			print("push_back data is not string");
		}
	    //memcpy(dst, dstOffset, src, srcOffset, length)
		var size=bin.byteLength;
		
		var data=new ArrayBuffer(this.len*4+12+this.sizeData+size);
		var v=new Uint32Array(data,0,4);
		v[0]=this.len+1;
		memcpy(data,4,this.data,4,this.len*4+8); 								//копируем индекс
		memcpy(data,this.len*4+12,this.data,this.len*4+8,this.dataSize);	 	//копируем данные		
		memcpy(data,this.len*4+12+this.dataSize,bin,0,size); 					//копируем данные новой записи
		this.data=data;
		this.len++;
		this.index=new Uint32Array(this.data,4,this.len*4+4);
		this.index[this.len-1]=size;											//записываем длинну новой записи
		this.index[this.len]=this.dataSize+size;								//записываем новый размер раздела данных
		this.dataSize+=size;
    
    }
    getStr(index){
    	var size=this.index[index+1]-this.index[index];
    	if(size>this.dataSize)return;
    	var bin=new ArrayBuffer(size);
    	memcpy(bin,0,this.data,this.index[index]+this.len*4+8,size);
    	return ab2str(bin);
    }
    getBin(index){
    	var size=this.index[index+1]-this.index[index];
    	if(size>this.dataSize)return;
    	var bin=new ArrayBuffer(size);
    	memcpy(bin,0,this.data,this.index[index]+this.len*4+8,size);
    	return bin;
    }
    
}    


