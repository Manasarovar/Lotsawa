var searchText=''
var oldSelect=''
var startSelect=''
var endSelect=''
var editMode=1;

var host="localhost";

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


function readText(){
		return getNode("text").innerHTML
}
function readStr(){
		return searchText
}
function edit(id){
  str=getNode(id).innerHTML
  if(str.indexOf("textarea")!=-1)return;
  str=str.replace(/<[^>]*>/g,"");
  str=str.replace(/=/g,"/")
    if(getNode(id).className=="tib"){
  	if(str.indexOf("/"==-1)){
  		str=str.replace(/[།༔༴]+/,"");
  		str="["+str+"་/__]";
  		str=str.replace(/\[[\[]+/,"[");
  		str=str.replace(/__\]་\/__\]/,"__]");
  		str=str.replace(/་[་]+/,"་");
  	}
  }
  if(str.length==1){  
	  str="<textarea onkeyup=\"v('"+id+"',this.value)\" style=\"width:250px;height:35px;position:relative;top:22px; font-size:0.9em;font-family:YagpoUni\">"+str+"</textarea>";
  }else{
  	  var w=str.length*12;
  	  if(w>800){
  	  	str="<textarea onkeyup=\"v('"+id+"',this.value)\" style=\"width:1024px;height:128px;position:relative;top:0px;font-size:0.9em;font-family:YagpoUni\">"+str+"</textarea>";
  	  }else{
   	  	str="<textarea onkeyup=\"v('"+id+"',this.value)\" style=\"width:"+w+"px;height:35px;position:relative;top:22px;font-size:0.9em;font-family:YagpoUni\">"+str+"</textarea>";
   	  }
  }
  getNode(id).innerHTML=str
  //getNode(id).contentEditable = "true";
  startSelect=''
  //if(endSelect!='')
 //		getNode('s'+endSelect).contentEditable 
//		= "false"
  endSelect=''
}


function set(id){
	str=getNode(id).innerHTML;
	if(str.indexOf("textarea")!=-1)return;
	str=str.replace(/<[^>]*>/g,"");
	searchText=str;
	//str="<font color='#007AFF'>"+searchText+"</font>"
	//getNode(id).innerHTML=str

	if (event.altKey) {
		if(startSelect==''){
			str="<textarea onkeyup=\"v('"+id+"',this.value)\" style=\"width:250px;height:35px;position:relative;top:22px; font-size:0.9em;font-family:YagpoUni\">"+str+"</textarea>";
			getNode(id).innerHTML=str
			startSelect=parseInt(id.replace(/s/g,''))
		}else{
			endSelect=parseInt(id.replace(/s/g,''))
			if(endSelect!=startSelect){
				str=getNode('s'+startSelect).innerHTML
				str+=getNode('s'+endSelect).innerHTML
				str=str.replace(/<[^>]*>/g,'')
				str=str.replace(/་-/g,'')
				str0=getNode('s'+
					(startSelect+1)).innerHTML
				str1=getNode('s'+
					(endSelect+1)).innerHTML
				str0 =str0 + " " + str1
				str0="/"+str0.replace(/[@\/=]/g,'')
				str0=str0.replace(/<[^>]*>/g,'')
				getNode('s'+
					(startSelect+1)).innerHTML=str0
				getNode('s'+startSelect).innerHTML=str
			}
			str=getNode('s'+startSelect).innerHTML
			str="<textarea onkeyup=\"v('s"+startSelect+"',this.value)\" style=\"width:250px;height:35px;position:relative;top:22px; font-size:0.9em;font-family:YagpoUni\">"+str+"</textarea>";
			getNode('s'+startSelect).innerHTML=str

			//getNode('s'+startSelect).contentEditable = "true"
		}	
	}else if(event.shiftKey){
		getNode("user_text").focus();
		var list = getNode('ocrData');
		if(lang=="eng"){
	    	list.selectedIndex=7;
	    }
	    if(lang=="rus"){	
	    	list.selectedIndex=8;
	    }	
	    
    	//getNode("textEntry").value=searchText;
    	getNode("user_text").value=searchText;
    	//textInput="entry";
	    readAction();
		
	}else{
		 //var list = getNode('ocrData');
    	 //list.selectedIndex=1;
    	 //getNode("textEntry").value=searchText;
    	 getNode("user_text").value=searchText;
    	 textInput="entry";
	     //readAction();
	     
	     getNode("startBtn").src="/_img/Preloader_8.gif";    
    
		 sendHTTP('application/json','/create/post.esp',
			 '{"user_text":"'+searchText+'","ln":"' +ln+'", "ocrData":"dictionaryReport"}',
				 function(text){
					//print("report:"+text);
					text=text.replace(/"s([\d])/g,"\"sd$1");
					text=text.replace(/'s/g,"'sd");
					getNode("dictionaryReport").style.visibility="visible";
					getNode("dictionaryReport").innerHTML=text;
					getNode("startBtn").src="/_img/Start.jpg";
					
				 }
		 );
	}
	
}

function link(){
 getNode("text").contentEditable = "false";
}



function v(id,t){
     //str=getNode(id).innerHTML
     //alert(t);
	 //str=str.replace(/<[^>]*>/g,"")
	 if(t.indexOf("\n")==-1)return;
	 t=t.replace(/\n/g,"");
	 t=t.replace(/\//g,"་/");
	 t=t.replace(/་[་]+/g,"་");
	 t=t.replace(/^་/g,"");
	 getNode(id).innerHTML=t
}


function openText(id){
   var link="?db=DHARMABOOK&record="+id;
   window.open(link , "_blank","width=1024,height=800,resizable=yes,scrollbars=yes");
}

function openTextField(index,field){
   var link="?db=DHARMABOOK&record="+index+"&field="+field+"&ln=rus&page=0";
   window.open(link , "_blank","width=1024,height=800,resizable=yes,scrollbars=yes");
}

function editCell(idCell){
//alert(getNode(idCell))
getNode(idCell).contentEditable='true';
}

function editText(idLine){
	//alert(getNode(idLine))
	//
	if(getNode(idLine).contentEditable=='true'){
	  getNode(idLine).contentEditable='false';
	  getNode(idLine).className="showDict";
	}else{
	  getNode(idLine).contentEditable='true';
	  getNode(idLine).className="editLine";
	}  
}

function displayEdit(){
	var st=getNode("editField").style.display;
	//if(st=="none"){
		getNode("editField").style.display="block";
	//}else{
	//	getNode("editField").style.display="none";
	//}	
}


function submitMainForm(){
	textInput="form";
	if(readAction()){
		form = document.getElementById("mainForm");
		form.submit();
	}else{
		return false;
	}
}

Mousetrap.bind(['alt+s'], function (e) {
    reloadDict(); 
    //location.href=nextPageURL
    return false; 
});


function reloadDict(){
		 var text=getNode("pageEdit").innerHTML;
		 text=text.replace(/\n/g,"");
		 text=text.replace(/\&nbsp;/g," ");
		 text=text.replace(/#/g,"/");
		 text=text.replace(/\[/g,"\n[");
		 text=text.replace(/\]/g,"]\n");
		 text=text.replace(/{/g,"༼");
 		 text=text.replace(/}/g,"༽");
 		 text=text.replace(/«/g,"༼");
 		 text=text.replace(/»/g,"༽");
		 text=text.replace(/\<[^\>]*\>/g,"");
		 text=text.replace(/་[༌]+\//g,"་/");
		 

		  		 
		 text=text.split("\n");
		 var data=""; var t=0,d=0;
		 //alert(text)
		 for(i=0;i<text.length;i++){
			 if(!text[i].length)continue;
			 if(text[i][0]!='[')continue;
			 if(text[i][text[i].length-1]!=']')continue;
			 if(text[i].indexOf("/")==-1)continue;
			 data+=text[i];
		 }
		
		 if(data.length){
			//getNode("user_text").value=data;
			//getNode("mainForm").target = "_self";
			saveWords(data);
		 } 
}

function readAction(){

    var list = getNode('ocrData');
    var selectedValue = list.options[list.selectedIndex].value;
    checkEdit();// set background in textEntry
    
    var text;
    if(textInput=="entry"){
    	text=getNode("textEntry").value;
    }else{
    	text=getNode("user_text").value;
    }
    //if(getNode("startBtn").src=="/images/Preloader_8.gif")return;
    
    if(!text)text=getNode("user_text").value;
    if(!text)text=getNode("textEntry").value;
    if(!text)return false;
    text=text.replace(/"/g,'');
    
    //print('{"user_text":"'+text+'","ln":"' +ln+'", "ocrData":"'+selectedValue+'"}');
    
    if(selectedValue=="SearchLib"||selectedValue=="SearchLibText"){
    	getNode("user_text").value=text;
    	return true;
    }
    

	getNode("startBtn").src="/img_/Preloader_8.gif";    
    
    sendHTTP('application/json','/create/post.esp',
			 '{"user_text":"'+text+'","ln":"' +ln+'", "ocrData":"'+selectedValue+'"}',
			 function(text){
			 	//print("report:"+text);
			 	text=text.replace(/"s([\d])/g,"\"sd$1");
			 	text=text.replace(/'s/g,"'sd");
				getNode("dictionaryReport").style.visibility="visible";
				getNode("dictionaryReport").innerHTML=text;
				getNode("startBtn").src="/img_/Start.jpg";
					
			 }
	);
	
	return false;

      
}

function readActionPage(){
	
    var list = getNode('ocrDataPage');
    var selectedValue = list.options[list.selectedIndex].value;
    var form = getNode("pageForm");	

	if(selectedValue=="savePage")savePage();
	if(selectedValue=="rebuildCategory")rebuildCategory();
	if(selectedValue=="addRecord")addRecord();
	if(selectedValue=="addPage")addPage();
	if(selectedValue=="importText")importText();
	if(selectedValue=="exportText")exportText();
 
 return true;
  
}

function editPageRecord(){
	getNode("pageText").style.display="none";
	getNode("pageEdit").style.display="block";
	getNode("pageEdit").style.top="165px";
	getNode("pageEdit").style.left="41px";
    getNode("pageEdit").style.height="calc(100% - 165px)";
    getNode("pageEdit").style.width="calc(100% - 850px)";
	//getNode("OSBL_DICT").style.left="563px";
	//getNode("OSBL_DICT").style.width="calc(100% - 557px)";
	getNode("textEntry").style.zIndex="7";
	getNode("textEntry").style.left="41px";
	getNode("textEntry").style.width="calc(100% - 47px)";
	var list = getNode('ocrData');
    list.selectedIndex=6;
    editMode=2;

}


function checkEditInput(){
	var textEntry=getNode("textEntry").value;
	var letter=textEntry.charAt(textEntry.length-1);
	if(letter=="་"||letter=="།"||letter==" "||letter=="༔"||letter=="༴"){
		textEntry=textEntry.replace(/ིི/g,"ི");
		textEntry=textEntry.replace(/ོོ/g,"ོ");
		textEntry=textEntry.replace(/ེེ/g,"ེ");
		textEntry=textEntry.replace(/ུུ/g,"ུ");
		textEntry=textEntry.replace(/༔་/g,"༔ ");
		textEntry=textEntry.replace(/།་/g,"། ");
		textEntry=textEntry.replace(/༴་/g,"༴ ");
		/*
		textEntry=textEntry.replace(/ཧཧ/g,"ཧཱུྃ");
		textEntry=textEntry.replace(/༔་/g,"༔ ");
		textEntry=textEntry.replace(/།་/g,"། ");
		textEntry=textEntry.replace(/༴་/g,"༴ ");
		textEntry=textEntry.replace(/ཡཡ་/g,"ཡེ་ཤེས་");
		textEntry=textEntry.replace(/ཧཧ་/g,"ཧཱུྂ་");
		textEntry=textEntry.replace(/ཧཧཧ་/g,"ཨོཾ་ཨཱཿཧཱུྃ");
		textEntry=textEntry.replace(/་ྷ་/g,"་ཧྲཱིཿ");
		textEntry=textEntry.replace(/§/g,"བའི");
		textEntry=textEntry.replace(/±/g,"པའི");
		textEntry=textEntry.replace(/`/g,"འི");
		textEntry=textEntry.replace(/རར/g,"བཛྲ");
		textEntry=textEntry.replace(/ྙྙ/g,"྅");
		textEntry=textEntry.replace(/ཨཨཨ/g,"ཨྠྀི");
		textEntry=textEntry.replace(/-ི/g,"ྀ");
		textEntry=textEntry.replace(/མམ/g,"མཁའ་འགྲོ");
		textEntry=textEntry.replace(/༈༄/g,"༁ྃ༔");
		*/
		textEntry=textEntry.replace(/ཨཨཨ/g,"ཨྠྀི");
		textEntry=textEntry.replace(/༎/g,"༎ ");
		textEntry=textEntry.replace(/_/g," ");
		textEntry=textEntry.replace(/ཿ་/g,"ཿ ");
		
		getNode("textEntry").value=textEntry;
		var lines=textEntry.split(" ");
		textEntry=textEntry.replace(/[ ་།]/g,"་");
	 	textEntry=textEntry.replace(/ /g,"་");
	 	textEntry=textEntry.replace(/།/g,"་");
	 	textEntry=textEntry.replace(/༔/g,"་");
		var token=textEntry.split("་");
		var i=2;
		var word=token[token.length-i];
		
		while(word==""){
			word=token[token.length-i];
			i++;
		}	
		//print(token);
		//print("/"+word+"/");
		
		var list = getNode('ocrData');

        var selectedValue = list.options[list.selectedIndex].value;
    	//print(selectedValue);
    	
    	var report="";
        if(word=="་"||word==" "||word=="")return;
        
	    sendHTTP('application/json','/create/post.esp',
			 '{"user_text":"'+word+'་","ln":"'+ln+'", "ocrData":"'+selectedValue+'"}',
			 function(text){
			 	//print("report:"+text);
			 	text=text.replace(/"s([\d])/g,"\"st$1");
			 	text=text.replace(/'s/g,"'st");
			 	text=text.replace(/<p[^\/]*\/p>/g,"");
				//getNode("dictionaryReport").style.visibility="visible";
				getNode("pageEdit").innerHTML=text;
				//getNode("startBtn").src="/work_file/_img/Start.jpg";
				
				
				if(ln=="eng"){
					selectedValue="TibetanUTFToEng";
				}else{
					selectedValue="TibetanUTFToRus";
				}
				var line="";
				var i=1;
				while(line==""){
					line=lines[lines.length-i];
					i++;
				}	
				line=line.replace(/[ ་།]/g,"་");
				line=line.replace(/^[་]+/g,"");
				sendHTTP('application/json','/create/post.esp',
					 '{"user_text":"'+line+'་","ln":"'+ln+'", "ocrData":"'+selectedValue+'"}',
					 function(text){
						//print("report:"+text);
						//text=text.replace(/"s([\d])/g,"\"sd$1");
						//text=text.replace(/'s/g,"'sd");
						//text=text.replace(/<p[^\/]*\/p>/g,"");
						//text=report+"<hr/>"+text;
						//print("done "+text);
						//getNode("dictionaryReport").style.visibility="visible";
						getNode("pageEdit").innerHTML+=text;
						//getNode("startBtn").src="/work_file/_img/Start.jpg";
				
					 }
				);
				
					
			 }
		);
		
		
	
	}
		

}

function rebuildCategory(){
			//check pass first
			if(!checkPass())return;

			var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr = new XHR();
			var body = "ocrData=rebuildCategory";
			
			xhr.open('POST', '/create/post.esp', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function() {
				alert("done rebuild category");
				//location.reload();
			}
			xhr.onerror = function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);
			
			
}

function saveWords(newText){
			sendHTTP('application/json',
				'/create/post.esp',
				'{"user_text":"'+newText+'","ln":"' +lang+'", "ocrData":"reloadDict"}',
				function(){
					if(editMode==1){
						translatePage();
					}
					//window.location.reload(false); 	
				}
			);
}

function checkPass(){
			var pass=getNode("editPass").value;	
			if(pass==""){	
				pass=getCookie("passEdit");
			}		
			var passFlag=0;
			passList=["dharma_work","a","A","а","А","ཨ"];
			for (i = 0; i < 10; i++){
				if(passList[i]==pass){
					passFlag=1;
					break;
				}
			}
			if(!passFlag){
				pass = prompt("Please input password \nfor file edit access or send \npassword request to gomde@mail.ru\nThank you.");
				for (i = 0; i < 10; i++){
					if(passList[i]==pass){
						passFlag==1;
						break;
					}
				}	
			}
				
			if(pass=="dharma_work"){
				setCookie("passEdit","dharma_work",128);
				passFlag=1;
			}	
			if(!passFlag) return false;
			return true;
}

function savePage(){
			
			//check pass first
			if(!checkPass())return;
			
			var newText=getNode("editField").value;
			var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr = new XHR();
			var body = 'user_text='+encodeURIComponent(newText)+'&index='+index+'&field='+field+"&ocrData=savePage";
			
			xhr.open('POST', '/create/post.esp', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function() {
			    //alert( this.responseText+" 1" );
				//d.innerHTML="";
				//d.innerHTML=this.responseText;
				//alert("done / "+this.responseText+"/");
				location.reload();
			}
			xhr.onerror = function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);

}

function addRecord(){

			//check pass first
			if(!checkPass())return;

			
			var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr = new XHR();
			var body = "&ocrData=addRecord";
			
			
			xhr.open('POST', '/create/post.esp', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function() {
			    //alert( this.responseText+" 1" );
				//d.innerHTML="";
				//d.innerHTML=this.responseText;
				alert("done / "+this.responseText+"/");
				location.href="/?field=1&index="+this.responseText+"&ocrData=read";
			}
			xhr.onerror = function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);

}

function addPage(){

			//check pass first
			if(!checkPass())return;
			var count=getNode("editPage1").value;
			if(count=="")count=1;
			
			var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr = new XHR();
			var body = "&ocrData=addPage&index="+index+"&field="+count;
			
			xhr.open('POST', '/create/post.esp', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function() {
			    //alert( this.responseText+" 1" );
				//d.innerHTML="";
				//d.innerHTML=this.responseText;
				alert("done / "+this.responseText+"/");
				//location.href="/?field=1&index="+this.responseText+"&ocrData=read";
			}
			xhr.onerror = function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);

}


function importText(){
			alert(31);
			//check pass first
			if(!checkPass())return;

			
			var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr = new XHR();
			var str=getNode("editPage1").value;		
			var body = "&ocrData=importText&user_text="+str+'&index='+index;
			
			
			xhr.open('POST', '/create/post.esp', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function() {
			    //alert( this.responseText+" 1" );
				//d.innerHTML="";
				//d.innerHTML=this.responseText;
				alert("done / "+this.responseText+"/");
				location.href="/?field=1&index="+this.responseText+"&ocrData=read";
			}
			xhr.onerror = function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);

}
function exportText(){

			alert(index);
			
			var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr = new XHR();
			var str=getNode("editPage1").value;		
			var body = "&ocrData=exportText&index="+index;
			
			
			xhr.open('POST', '/create/post.esp', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function() {
			    //alert( this.responseText+" 1" );
				//d.innerHTML="";
				//d.innerHTML=this.responseText;
				getNode("editField").innerHTML=this.responseText
				//alert("done / "+this.responseText.length+"/");
				//alert("done /");
				
			}
			xhr.onerror = function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);
			

}



function submitForm(formID){
//alert(formID);
form=getNode(formID)
form.submit();
}

function readText(ln){
	var text=getNode("textOCR").innerHTML;
	text=text.replace(/\<[^>]*>/g,"");
	getNode("user_text").value=text;
    var list = getNode('ocrData');
    list.value="TibetanUTFTo"+ln;
    submitForm("mainForm");
}

function post(path, params, method) {
    method = method || "post"; // Set method to post by default if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    //var form = document.createElement("form");
    var form=getNode("OCRDataForm");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        if(params.hasOwnProperty(key)) {
            var hiddenField = document.createElement("input");
            hiddenField.setAttribute("type", "hidden");
            hiddenField.setAttribute("name", key);
            hiddenField.setAttribute("value", params[key]);

            form.appendChild(hiddenField);
         }
    }

   // document.body.appendChild(form);
    //form.submit();
    //Example: post('/contact/', {name: 'Johnny Bravo'});
    
}


function saveOCRPage(){
	var textData=getNode("textOCR").innerHTML;
	
	textData=textData.replace(/<br>/g,"\n");
	textData=textData.replace(/\&nbsp;/g," ");
	textData=textData.replace(/<div>/g,"\n");
	textData=textData.replace(/<[^>]*>/g,"");
	textData=textData.replace(/ [ ]+/g," ");
	textData=textData.replace(/་[་]+/g,"་");
	textData-textData.replace(/\"/g,"'");
	
	if(textData.indexOf("/")!=-1){
		var user_text=textData.replace(/\n/g,"");
		post('/ocr/ocr.php', {user_text: user_text, ocrData:'ReloadDict'});
		$.post('https://'+host+'/ocr/ocr.php', $('#OCRDataForm').serialize(), function(data){
			data=data.replace(/<[^>]*>/g,"");
			alert(data)
		});
	}	
	textData=textData.replace(/^\@.*$/gm,"");
	if(textData.indexOf("￨")!=-1){
	 textData=textData.replace(/\n/g," ");
	 textData=textData.replace(/￨/g,"\n");
	}
	textData=textData.replace(/\n\n+/g,"\n");
	textData=textData.replace(/\n/g,"<br>\n");
	textData=getNode("textOCR").innerHTML=textData;
	
	post('/ocr/ocr.php', {text: textData, ocrData:'saveOCRPage', ocr: 2});
	$.post('https://'+host+'/ocr/ocr.php', $('#OCRDataForm').serialize(), function(){alert("Text saved.")});
}



function translateText(mode){
	var textData=getNode("textOCR").innerHTML;
	textData=textData.replace(/<[^>]*>/g,"");
	textData=textData.replace(/\&nbsp;/g," ");
	textData=textData.replace(/ [ ]+/g," ");
	textData=textData.replace(/་ /g,"་");
	textData=textData.replace(/་[་]+/g,"་");
	textData=textData.replace(/་\n/g,"་￨");
	textData=textData.replace(/\n/g,"￨ ");
	textData=textData.replace(/ /g,"\n");
	//alert(textData);
	post("https://"+host+"/ocr/ocr_ajax.php", {text: textData, ln:mode});
	$.post('https://'+host+'/ocr/ocr_ajax.php', $('#OCRDataForm').serialize(), function(data){
		//alert(data );
		textData=getNode("textOCR").innerHTML=data;
	});


}

function  imageResize(){
}


function fullTextSearch(){
			var str = window.location.search;
			var objURL = {};

			str.replace(
				new RegExp( "([^?=&]+)(=([^&]*))?", "g" ),
				function( $0, $1, $2, $3 ){
					objURL[ $1 ] = $3;
				}
			);

			var user_text=objURL["user_text"];
			var ln=objURL["ln"];
			//alert(user_text+" - "+ln);

			var XHR = ("onload" in new XMLHttpRequest()) ? XMLHttpRequest : XDomainRequest;
			var xhr = new XHR();
			var body = 'user_text='+encodeURIComponent(user_text)+'&ln=' + encodeURIComponent(ln)+"&ocrData=fullSearchTextNew";
			
			xhr.open('POST', 'https://'+host+'/ocr/ocr_ajax.php', true);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function(report) {
			    alert( this.responseText+" 1" );
				//d.innerHTML="";
				//d.innerHTML=this.responseText;
				//alert("done save words/ "+this.responseText+"/");
				//location.reload();
			}
			xhr.onerror = function() {
			  alert( 'Ошибка ' + this.status );
			}
			xhr.send(body);
		
	
	
}

function translatePage(ln){
	pageText=getNode("pageText").innerHTML;
	//print(pageText.length)
	if(pageText.length>2048)window.location.reload(false); 
	pageText=pageText.replace(/ /g,"\n");
	var request='{"ocrData":"translateLine","user_text":"'+encodeURL(pageText)+'","ln":"'+lang+'"}';
	print(request);
	sendHTTP("application/json","/create/post.esp",
			request,
			function(text){
				getNode("pageEdit").innerHTML=text;
			}
	);
}












