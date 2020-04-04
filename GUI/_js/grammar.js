//main translation functions for first pages of text (translate word under cursor)

var text="";
var flag=1;


function getOffsetRect(elem) {
    // (1)
    var box = elem.getBoundingClientRect()
    
    // (2)
    var body = document.body
    var docElem = document.documentElement
    
    // (3)
    var scrollTop = window.pageYOffset || docElem.scrollTop || body.scrollTop
    var scrollLeft = window.pageXOffset || docElem.scrollLeft || body.scrollLeft
    
    // (4)
    var clientTop = docElem.clientTop || body.clientTop || 0
    var clientLeft = docElem.clientLeft || body.clientLeft || 0
    
    // (5)
    var top  = box.top +  scrollTop - clientTop
    var left = box.left + scrollLeft - clientLeft
    
    return { top: Math.round(top), left: Math.round(left) }
}

function httpGetAsync(theUrl, callback)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200){
            callback(xmlHttp.responseText);
        }    
    }
    xmlHttp.open("GET", theUrl, true); // true for asynchronous 
    xmlHttp.send(null);
}

var HttpClient = function() {
    this.get = function(aUrl, aCallback) {
        var anHttpRequest = new XMLHttpRequest();
        anHttpRequest.onreadystatechange = function() { 
            if (anHttpRequest.readyState == 4 && anHttpRequest.status == 200)
                aCallback(anHttpRequest.responseText);
        }

        anHttpRequest.open( "GET", aUrl, true );            
        anHttpRequest.send( null );
    }
}

function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

function response(text){
	//alert(text);
	document.getElementById('dictionaryReport').innerHTML="";
}

function getInnermostHovered() {
    var n = document.querySelector(":hover");
    var nn;
    while (n) {
        nn = n;
        n = nn.querySelector(":hover");
    }
    //alert((getInnermostHovered() ||   {}).textContent)
    return nn;
}

//document.write('<style>p.tib{font-size:16px;} tb{font-size:14px;} t{font-size:12px;} r{font-size:12px;</style>');
//document.write('<div id="report" style="position:absolute;top:256px;left:1156px;width:calc(100%-1119px);display:hidden; font-family:YagpoUni;"></div>')
//document.write('<style>p.tib{font-size:18px;} tb{font-size:16px;} t{font-size:16px;} r{font-size:16px;</style>');

var alt=1;
window.onload = function(){
	document.onkeydown = function(e){
	//alert(e);
		if(e.altKey){
			
			alt=-1*alt;
			document.getElementById('dictionaryReport').style.visibility="hidden";
			
		}else{
			//alt=-1;
		}
	};
};

function closePopUp(){
			alt=-1;
			document.getElementById('dictionaryReport').style.visibility="hidden";
}

setInterval(function () {
    //console.log((getInnermostHovered() ||   {}).textContent);
    var t=(getInnermostHovered() || {});
    
    if (alt>0) {
    

		if(t.nodeName=="TSH"){
			    var newText=t.textContent;
				if(newText.length>2048)newText=newText.substr(0,2048);
				newText+="་";
				var d = getNode('dictionaryReport');
				d.style.visibility="visible";
			
				if(newText!=text&&newText.length>0){
					//d.innerHTML=t.nodeName+"<br>"+t.textContent;
			
					flag++;
					text=newText;
				
					var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
					var xhr = new XHR();
					// (2) запрос на другой домен :)
					xhr.open('POST', 'https://www.buddism.ru:4443/create/grammar.esp?user_text='+newText+"&ln="+lang, true);
					xhr.onload = function() {
					 	//alert( this.responseText+" 1" );
					    var t=this.responseText;
						d.innerHTML="";
						d.innerHTML=t;
					}
					xhr.onerror = function() {
					  //alert( 'Ошибка ' + this.status );
					}
					xhr.send();
				
					/*
					httpGetAsync('https://buddism.ru:4443/www.grammar.esp?user_text='+newText+"&ln="+lang, function(response) {
						d.innerHTML="";
					//	alert(response);
						d.innerHTML=response;
					});
					*/
				
				
				}	
		}else { 
			//if(t.nodeName=="DIV")
			//document.getElementById('dictionaryReport').style. visibility="hidden";
	
		}
	}  

}, 1000);

