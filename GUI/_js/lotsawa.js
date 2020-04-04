var jsobj = {}
var Rus_Tr_Txt = '';
var wrd_id = '';
var sent_id = '';

function Upd_Header_Def_SentTr(opt) {
    //добавили в Шапку выбор пользователя
    document.getElementById('user_word').innerHTML = opt;

    //take key_word
    //var key = document.getElementById('key').innerText;

    // find Result.element(key) & set new def
    //let tag = document.getElementById(wrd_id);

    document.getElementById(wrd_id).setAttribute("def", opt);
    //alert(document.getElementById(wrd_id));
    // Update Sentence Translation
    //let Sent_prt_speach='';
    //let Sent_Html = '';
    let Sent_Tr_txt = '';
    sent_id = document.getElementById(wrd_id).parentNode.id

    var child = document.getElementById(sent_id).children;
    for (var i = child.length - 1; i >= 0; i--) {
        //Sent_prt_speach = Sent_prt_speach + '⇎<kbd class="draggable">' + child[i].className + '</kbd>';
        //Sent_Html = Sent_Html + '⇎<kbd class="draggable">' + child[i].getAttribute("def") + '</kbd>';
        Sent_Tr_txt = child[i].getAttribute("def") + ' ' + Sent_Tr_txt;
    };
    //document.getElementById('Sent_RusTr').innerHTML = Sent_Html;
    //document.getElementById('Sent_RusTr').innerHTML = Sent_prt_speach;
    document.getElementById('Sent_box').value = Sent_Tr_txt;
}

function new_pair(key, new_Word, rw) {
    // rw=0 - addWord - ДОБАВИТЬ ЗНАЧЕНИЕ к КЛЮЧУ
    // rw=1 - putWord - ПЕРЕЗАПИСЬ КЛЮЧ-ЗНАЧЕНИЕ
    var dataBase = 'dk'  //(словарь памяти переводов)
    sendHTTP('application/json', '/create/post.esp',
        '{"key":"' + key + '", "value":"' + new_Word + '", "rw":"' + rw + '", "db":"' + dataBase + '", "ocrData":"prs2txt"}',
        function (text) {
            console.log("done add: " + key + "=" + new_Word)
        }
    );

    // Добавить Пару в Индекс ДБ
    //Add_IndexedDb(key, new_Word, 'New_Pair');

    // Если это добавление нового ЗНАЧЕНИЯ к тиб слову из списка, то нужно не добавить новую строку в конец,
    // а прицепить спереди новое ЗНАЧЕНИЕ к значениям конкретного тиб слова.

    // Добавить Пару в jsobj
    if (key in jsobj && rw != true) {
        jsobj[key].unshift(new_Word);
    } else {
        //jsobj[key].concat(new_Word)
        jsobj[key] = [new_Word];
    }
    // Export new words
    //console.log(JSON.stringify(jsobj))

    // Добавить Пару в 'New_Wrds'
    let html = '';
    for (let i = 0; i < Object.keys(jsobj).length; i++) {
        html = Object.keys(jsobj)[i] + '=' + Object.values(jsobj)[i] + ' \n' + html
    }
    document.getElementById('New_Wrds').innerHTML = html;

    // Добавляем в Локал Сторадж
    /* localStorage.setItem(key, [new_Word]);
        let new_pair = key + '= xxx; ' + new_Word;
    */
}

function add_word() {
    var new_Word = document.Input_new_word.new_Word.value;

    Upd_Header_Def_SentTr(new_Word);

    // Add_New_Word in Dict
    //take key_word
    var key = document.getElementById('key').innerText;
    var elem = document.getElementById('h_' + key);

    //node.prepend(...nodes or strings) – вставляет в node в начало,
    //node.before(...nodes or strings) –- вставляет прямо перед node,
    //node.after(...nodes or strings) –- вставляет сразу после node,

    //for (let rus of new_Word) {
    var newDiv = document.createElement('div');
    newDiv.className = "usr_wrd";
    newDiv.id = '';
    newDiv.innerHTML = key + ' : ' + new_Word + '<div class="vote_line" style = "width: 57%;"></div >';
    elem.prepend(newDiv);
    //}

    new_pair(key, new_Word, rw_bo_ru.checked);

    document.getElementById('nw_opt').value = ""
}

function Add_Tib_Rus() {

    var Tib_Rus = document.getElementById('nw-pair').value;
    if (Tib_Rus.includes('=')) {
        Tib_Rus = Tib_Rus.split('=')
        let key = Tib_Rus[0];
        let new_Word = Tib_Rus[1];

        new_pair(key, new_Word, rw_bo_ru.checked);

    } else {
        let key = Tib_Rus;

        //ЗАПРОС по КЛЮЧ через стандартный API
        var dataBase = 'dk'  //(словарь Lotsawa)
        sendHTTP('application/json', '/create/post.esp',
            '{"key":"' + key + '", "db":"' + dataBase + '", "ocrData":"getWord"}',
            function (text) {
                document.getElementById('resp').innerHTML = text;
            }
        );
    }
    document.getElementById('nw-pair').value = ""
}

function modalWindowFill(event) {
    try {
        //calculate click ID
        wrd_id = event.target.id; // Получили ID, т.к. в e.target содержится элемент по которому кликнули
        //alert(wrd_id)
        // The substituted value will be contained in the result variable
        let idx = wrd_id.replace(/\d+_(.+)/gm, '$1');
        var key = idx; //document.getElementById(wrd_id).innerText;
        //alert(idx)
        idx = "h_" + idx;

        //take value from Dict
        var trnsl_opt = document.getElementById(idx).innerHTML;

        //clear modal window
        //document.getElementById("key").innerHTML = "";
        //document.getElementById("trnsl_opt").value = "";
        document.getElementById("user_word").innerHTML = "";

        //alert(key)
        //Put to Modal
        document.getElementById('key').innerText = key;
        document.getElementById('trnsl_opt').innerHTML = trnsl_opt;

        // координаты поля относительно окна браузера
        let ResultCoords = this.getBoundingClientRect();

        // мяч имеет абсолютное позиционирование (position:absolute), поле - относительное (position:relative)
        // таким образом, координаты мяча рассчитываются относительно внутреннего, верхнего левого угла поля
        let oknoCoords = {
            top: event.clientY + 25, //- ResultCoords.top - Result.clientTop + 35,
            left: event.clientX - 115,//- ResultCoords.left - Result.clientLeft - 115
        };

        // запрещаем пересекать верхнюю границу поля
        //if (oknoCoords.top < 0) oknoCoords.top = 0;

        //запрещаем пересекать левую границу поля
        if (oknoCoords.left < 0) oknoCoords.left = 0;

        // // запрещаем пересекать правую границу поля
        if (oknoCoords.left + 230 > Result.clientWidth) {
            oknoCoords.left = Result.clientWidth - 230;
        }
        //alert(oknoCoords.left);
        // запрещаем пересекать нижнюю границу поля
        //if (oknoCoords.top + 230 > Result.clientHeight) {
        //	oknoCoords.top = Result.clientHeight - 230;
        //}

        //document.querySelector('#WordModal').style = oknoCoords.top + 'px' + oknoCoords.left + 'px';
        //document.getElementById("WordModal").style.left = oknoCoords.left + 'px';
        //document.getElementById("WordModal").style.top = oknoCoords.top + 'px';

        // Open
        //currentBtn.addClass('focus');
        //btn.removeClass('focus');
        let styl = 'left:' + oknoCoords.left + 'px; top:' + oknoCoords.top + 'px;';
        document.querySelector('#ModalWindw').style = styl + "display: content; opacity: 1; pointer-events: auto; overflow-y: auto;";
        //document.querySelector('#WordModal').style = "display: content; opacity: 1; pointer-events: auto; overflow-y: auto;";
        //
        //Close on Esc and X
        //document.addEventListener('keypress', function (e) {
        //	if (e.keyCode === 27) document.querySelector('#WordModal').style = "";
        //});

        //document.querySelector('#close').addEventListener('click', function () {
        //	document.querySelector('#ModalWindw').style = "opacity: 0; pointer-events: none;";
        //});
    }
    catch (TypeError) {
        console.error('В Пустоте, на что опереться?! Жми на тибетские слова!');
        // expected output: ReferenceError: nonExistentFunction is not defined
        // Note - error messages will vary depending on browser
    }
}

function ConcatTxt () {
    //alert()
    let Rus_Tr_Txt = document.getElementById('Rus_Txt').value
    Rus_Tr_Txt = Rus_Tr_Txt + ' \n ' + document.getElementById('Sent_box').value;
    //alert(Rus_Tr_Txt);
    //  ru_txtbox+' \n  '+
    document.getElementById('Rus_Txt').value = Rus_Tr_Txt;
    let tib_snt = document.getElementById(sent_id).innerText

    let rus_trs = document.getElementById('Sent_box').value
    //localStorage.setItem(tib_snt, rus_trv);

    //Add_IndexedDb(tib_snt, rus_trv, 'Sentence')

    //выгружает переведенное предложение в файл Transl_Bo_Ru.txt в формате
    //номер предложения(id)	тибетское предложение	русский перевод
    var dataBase = 'dk'  //(словарь Lotsawa)
    sendHTTP('application/json', '/create/post.esp',
        '{"sent_id":"' + sent_id + '", "tib_snt":"' + tib_snt + '", "rus_trs":"' + rus_trs + '", "db":"' + dataBase + '", "ocrData":"snt2txt"}',
        function (text) {
            console.log('Export Transl Sent --> Transl_Bo_Ru.txt')
        }
    );
}

function addNote(db, key, new_Word, tab) {
    //let dbReq = indexedDB.open('Tib_Ris_Dict', 3);
    // Запустим транзакцию базы данных и получите хранилище объектов Notes

    let tx = db.transaction([tab], 'readwrite');
    let store = tx.objectStore(tab);
    if (tab == 'New_Pair') {
        try {
            //alert('Word', tab);
            //Добаляем заметку в хранилище объектов
            let pair = { Tib: key, Rus: new_Word };
            store.get(key).onsuccess = (event) => {
                if (event.target.result == undefined) {
                    store.add(new_Word, key);
                    //alert('add');
                } else {
                    //alert('put');
                    store.put(event.target.result + '; ' + new_Word, key);
                }
            };
            // Ожидаем завершения транзакции базы данных
            //console.log('stored note!')
        } catch{
            alert('error storing note ' + event.target.errorCode);
        };
    } else if (tab == 'Sentence') { store.put(new_Word, key); }
}

function Add_IndexedDb(key, new_Word, tab) {
    let dbReq = indexedDB.open('Tib_Ris_Dict', 3);
    dbReq.onupgradeneeded = (event) => {
        // Зададим переменной db ссылку на базу данных
        db = event.target.result;
        // Создадим хранилище объектов с именем pairs.
        let pairs = db.createObjectStore('New_Pair');//, {keyPath:'Tib'});
        let sent = db.createObjectStore('Sentence', { autoIncrement: true });
        alert('upgradeneeded')
        //pairs.createIndex('Rus', 'Rus', { unique: false });
    }
    dbReq.onsuccess = (event) => {
        db = event.target.result;
        //alert('success')
        addNote(db, key, new_Word, tab);
    }
    dbReq.onerror = (event) => {
        alert('error opening database ' + event.target.errorCode);
    }
}