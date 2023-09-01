window.onload = async function(event) {
  console.log(`window.onload: start`);
  console.log('global_api_server_adress:' + get_server_api_address());
  if (!(document.body.dataset.phraseid=='0')){   await LoadSimpleData();   }
  if(document.getElementById('index_table_of_syllables')!=null){
        await LoadPaginatorBlock();
        await Load_words_slice(100,
                      Number(getCookie('syllables_curent_page'+document.getElementById('index_table_of_syllables').dataset.ready, 1)),
                      Number(document.getElementById('index_table_of_syllables').dataset.ready));

    }

    await Load_Word_in_Progress_Data();
    await Load_Phrase_in_Progress_Data();
    await Load_Syllable_Into_Add_New_Word();

    if (document.getElementById('index_table_of_phrases')!=null){
        await Load_phrases(Number(document.getElementById('index_table_of_phrases').dataset.ready));
    }


  }

  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
  }

  
function GetAllExamplesFromNewSyllablePage(){
  let example_elements = document.getElementsByClassName('div_example_class');
  let result = [];
  for (let example_element of example_elements) {
    subresult = {};
    let elements = example_element.getElementsByClassName('my_class_input_examples');
    for (let element of elements){
      if (element.dataset.type==`foreign`){
        subresult.example = element.value;
      }
      else{
        subresult.translate = element.value;
      }
    }
    subresult.rowid = element.dataset.rowid;
    result.push(subresult);
  }
  console.log(result);
}

function SaveSyllable(){
  if(document.body.id!='body_add_new_word'){
    return
  }

  let response = fetch('/api/v1/cross_request/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify({  username:``,
                            command:`save_syllabe`,
                            syllable_id:document.body.dataset.syllable_id,
                            transcription:document.getElementById(`id_transcription`).value,
                            translations:document.getElementById(`id_translations`).value,

                          })
                        }
    )
  let answer = response.json();

}

function AddExamplToNewSyllablePage(parent, example, translate, rowid, id_int){
  let pattern = `<div class="div_example_class" id="example_section_{ _random_ }" style="text-align:right;"><IMG class ="image_little_button" WIDTH="64" HEIGHT="64"  title = "Удалить пример" src="/static/images/delete.png" onclick="document.getElementById('example_section_{ _random_ }').remove();"'>
  <div id="example_div" data-rowid="{ _rowid_ }" style='outline: 2px solid #7B68EE; border: 2px solid #707076; text-align: center; margin: 10px; border-radius:10px;'>
                   <textarea data-type="foreign" autocomplete="off" name="examples"  rows="3" class="my_class_input_examples" data-rowid="{ _rowid_ }" data-sequense="{ _sequense_ }" id="id_example_foreign">{ _foreign_ }</textarea>
                      <br>
                   <textarea data-type="native" autocomplete="off" name="examples" rows="3" class="my_class_input_examples" data-rowid="{ _rowid_ }" data-sequense="{ _sequense_ }" id="id_example_native">{ _naitive_ }</textarea>
  </div>
  <hr>
  </div>`;
  parent.insertAdjacentHTML('beforeend', pattern .  replaceAll(`{ _foreign_ }`, example).
                                                    replaceAll(`{ _naitive_ }`, translate).
                                                    replaceAll(`{ _rowid_ }`, rowid).
                                                    replaceAll(`{ _random_ }`, id_int ));
}

  async function Load_Syllable_Into_Add_New_Word(){
    if(document.body.id!='body_add_new_word'){
      return
    }
                          let body =      `{"username":"`+`"`+`,`+
                          ` "command":"get_syllable_full_data"`+`,`+
                          ` "comment":"`+`"`+`,`+
                          ` "data":"`+document.body.dataset.word+`"` +
                          `}`;
                          let req = new XMLHttpRequest();
                          req.open(`POST`, `/api/v1/cross_request/`, true);
                          req.send(body);
                          req.onload = function(){
                            let answer = JSON.parse(req.responseText);
                            console.log(answer)
                            document.body.dataset.syllable_id = answer.syllable_id;
                            document.getElementById(`id_transcription`).value = answer.transcription
                            document.getElementById(`id_translations`).value = answer.translations
                            for (var example of answer.examples) {
                                                                  AddExamplToNewSyllablePage(document.getElementById(`id_examples`), example.example, example.translate, example.rowid, getRandomInt(1000000000000, 9999999999999));
                                                                }
                    }
    }



    function add_format_for_russian(pc_source, lc_style_name){
      lc_russian = 'йцукенгшщзхъфывапролджэячсмитьбюё';
      lc_russian += lc_russian.toUpperCase();
      lc_result = '';
      for (lc_chr of pc_source){
        if (lc_russian.includes(lc_chr)){
          lc_result = lc_result + '<span class = "' + lc_style_name+'">' + lc_chr + '</span>';
          }
        else{
          lc_result = lc_result + lc_chr;
        }
      }
      return lc_result.
                    replaceAll(`</span><span class = "`+lc_style_name+`">`,   ''  ).
                    replaceAll(`</span> <span class = "`+lc_style_name+`">`,  ' ' ).
                    replaceAll(`</span>/ <span class = "`+lc_style_name+`">`, '/ ').
                    replaceAll(`</span> /<span class = "`+lc_style_name+`">`, ' /').
                    replaceAll(`</span>; <span class = "`+lc_style_name+`">`, '; ').
                    replaceAll(`</span>, <span class = "`+lc_style_name+`">`, ', ').
                    replaceAll(`</span>(<span class = "`+lc_style_name+`">`,  '(' ).
                    replaceAll(`</span>)<span class = "`+lc_style_name+`">`,  ')' ).
                    replaceAll(`</span>( <span class = "`+lc_style_name+`">`, '( ').
                    replaceAll(`</span>) <span class = "`+lc_style_name+`">`, ') ').
                    replaceAll(`</span> (<span class = "`+lc_style_name+`">`, ' (').
                    replaceAll(`</span> )<span class = "`+lc_style_name+`">`, ' )').
                    replaceAll(`</span>- <span class = "`+lc_style_name+`">`, '- ').
                    replaceAll(`</span> -<span class = "`+lc_style_name+`">`, ' -').
                    replaceAll(`</span>-<span class = "`+lc_style_name+`">`,  '-' ).
                    replaceAll(`</span>. <span class = "`+lc_style_name+`">`, '. ');
    }


    async function Load_Phrase_in_Progress_Data(){
      if(document.body.id!='body_phrase_in_progress'){
        return
      }
      if (document.body.dataset.phraseid=='' | Number(document.body.dataset.phraseid)==0 ){
        document.body.dataset.phraseid = LoadNextProcessingPhraseIntoBody();
      }
      let body =      `{"username":"`+`"`+`,`+
      ` "command":"Get_Phrase"`+`,`+
      ` "comment":"`+`"`+`,`+
      ` "data":"`+document.body.dataset.phraseid+`"` +
      `}`;
      let req = new XMLHttpRequest();
      req.open(`POST`, `/api/v1/cross_request/`, true);
      req.send(body);
      req.onload = function(){
                                console.log(req.responseText)
                                let answer = JSON.parse(req.responseText);
                                document.getElementById('id_class_p_my_class_p_examples').innerHTML         = answer.phrase;
                                document.getElementById('id_class_p_my_class_p_examples_russian').innerHTML = answer.translation;
                              }
                            
    }

    function LoadNextProcessingPhraseIntoBody(){
      let req = new XMLHttpRequest();
      let body =      `{"username":"`+`"`+`,`+` "command":"Get_Next_Phrase_For_Learning"`+`,`+` "comment":"`+`"`+`,`+` "data":"`+`"` +`}`;
      req.open(`POST`, `/api/v1/cross_request/`, false);
      req.send(body);
        let answer = JSON.parse(req.responseText);
        console.log(`LoadNextProcessingPhraseIntoBody() -> ${answer.id_phrase}`);
        return answer.id_phrase;
        //window.location.href=`/phrases/in_progress/`+answer.id_phrase+`/`
    }

    function UpdateCurrentPhraseAsViewed(){
      console.log(`UpdatePhraseAsViewed => document.body.dataset.phraseid:${document.body.dataset.phraseid}`)
      let req = new XMLHttpRequest();
      let body =      `{"username":"`+`"`+`,`+` "command":"Update_phrase_as_viewed"`+`,`+` "comment":"`+`"`+`,`+` "data":"`+document.body.dataset.phraseid+`"` +`}`;
      req.open(`POST`, `/api/v1/cross_request/`, false);
      req.send(body);
      req.responseText
    }

    function NextPhrase(){
      UpdateCurrentPhraseAsViewed();
      document.body.dataset.phraseid=LoadNextProcessingPhraseIntoBody();
      Load_Phrase_in_Progress_Data();
    }

    async function Load_Word_in_Progress_Data(){
      if(document.body.id!='body_word_in_progress'){
        return
      }
      if (document.body.dataset.word.replaceAll(' ','')==''){
        LoadNextProcessingWordIntoBody();
      }
      let body =      `{"username":"`+`"`+`,`+
      ` "command":"get_syllable_full_data"`+`,`+
      ` "comment":"`+`"`+`,`+
      ` "data":"`+document.body.dataset.word+`"` +
      `}`;
      let req = new XMLHttpRequest();
      req.open(`POST`, `/api/v1/cross_request/`, true);
      req.send(body);
      req.onload = function(){
        let answer = JSON.parse(req.responseText);
        console.log(answer)
        document.getElementById('id_my_class_p_word').innerHTML = answer.word;
        document.getElementById('id_my_class_p_transcription').innerHTML = answer.transcription;
        let st = '';
        for (element of answer.translations.split(/(?:\r?\n)+/)){
            st += element+'<br>'
        }
        document.getElementById('id_my_class_p_my_class_p_translations').insertAdjacentHTML('beforeend',add_format_for_russian(st, 'my_class_p_my_class_p_translations_russian'));
        document.getElementById('id_my_class_p_my_class_p_examples').innerHTML = ``;
        for (sl of answer.examples){
          if (sl.example!=null){
                    document.getElementById('id_my_class_p_my_class_p_examples').insertAdjacentHTML('beforeend',`<p class = "my_class_p_my_class_p_examples">` + sl.example+ `<IMG WIDTH='48' HEIGHT='48'  title = '' src='/static/images/audio.svg' onclick = 'new Audio("/sentence/`+sl.linkcode+`" ).play(); return false;'></p>`);
          }
          if (sl.translate!=null){
                    document.getElementById('id_my_class_p_my_class_p_examples').insertAdjacentHTML('beforeend',`<p class = "my_class_p_my_class_p_examples_russian">` + sl.translate+ `</p><br>`);
          }
        }
      }
    }

    function LoadNextProcessingWordIntoBody(){
      let req = new XMLHttpRequest();
      let body =      `{"username":"`+`"`+`,`+` "command":"Get_Next_Syllable_For_Learning"`+`,`+` "comment":"`+`"`+`,`+` "data":"`+`"` +`}`;
      req.open(`POST`, `/api/v1/cross_request/`, false);
      req.send(body);
      let answer = JSON.parse(req.responseText);
      console.log(answer)
      document.body.dataset.word = answer.data;
      console.log(document.body.dataset.word);
    }

    function SetSyllableAsViewedAndLoadNext(word){
      let req = new XMLHttpRequest();
      let body =      `{"username":"`+`"`+`,`+` "command":"update_syllable_as_viewed"`+`,`+` "comment":"`+`"`+`,`+` "data":"`+word+`"` +`}`;
      req.open(`POST`, `/api/v1/cross_request/`, false);
      req.send(body);
      console.log(req.responseText);
      let answer = JSON.parse(req.responseText);
      LoadNextProcessingWordIntoBody();
      Load_Word_in_Progress_Data();
    }

    function GetBackGroundColorByIndex(id){
      let ll = ["#1C1C1C","#181513","#140F0B","#1E1112","#121910","#230D21","#022027","#16251C","#270A1F","#320A18","#131313","#1B1116","#1D1E33","#282828","#151719","#002137",
          "#35170C","#321011","#232C16","#302112","#1A162A","#32221A","#464544","#452D35","#1E1E1E","#343E40","#212121","#412227","#3B3C36","#23282B","#18171C","#141613",
          "#1F0E11","#1D1018","#161A1E","#0A0A0A"];
      return ll[Math.floor((ll.length-1)/id)]
    }
    
    function SetWordStatus(word, status){
      let body = `{"username":"`+`"`+`,`+` "command":"Set_Syllable_Status"`+`,`+` "comment":"`+word+`"`+`,`+` "data":"`+status+`"` +`}`;
      let req = new XMLHttpRequest();
      req.open(`POST`, `/api/v1/cross_request/`, false);
      req.setRequestHeader('Content-Type', 'application/json');
      req.send(body);
    }

    async function Load_words_slice(slice_size, slice_number, ready){
      setCookie('syllables_curent_page'+ready, slice_number, {});
      let body = `{"username":"","command":"syllables", "ready":"`+ready+`", "slice_number":"`+slice_number+`", "slice_size":"`+slice_size+`", "word_part":""}`;
      let req = new XMLHttpRequest();
      req.open(`POST`, `/api/v1/cross_request/`, true);
      req.send(body);
      req.onload=function(){
        let answer = JSON.parse(req.responseText);
        table = document.getElementsByClassName('my_class_table_of_words')[0];
        table_content = ''
        row_pattern =   `<tr id="tr_of_index_words__{{ word.word }}">
        <td width="7%" style="background:{{ word.word_background_color }}">{{ forloop.counter }}</td>
        <td with = "24%" style="color:Blue"><a href="./word_in_progress/{{ word.word }}/">{{ word.word }}</a></td>
        <td width="24%" align = "center" style="color:DarkRed"  onclick="new Audio('/static/sounds/{{ word.word }}.mp3').play(); return false;" >{{ word.transcription }}</td>
        <td width="7%" align = "center">{{ word.show_count }}</td>
        <td width="7%" align = "center"><a href="./add_new_word/{{ word.word }}/"><IMG class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Редактировать слово {{ word.word }}" src="/static/images/redo.png"></a></td>
        <td width="7%" align = "center"><a onclick='SetWordStatus("{{ word.word }}", (document.getElementById("index_table_of_syllables").dataset.ready==1?0:1)); document.getElementById("tr_of_index_words__{{ word.word }}").remove(); LoadSimpleData();'><IMG  class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Слово выученно" src="/static/images/ok.png"></a></td>
        </tr>`
        
        for(let i = 0; i < answer.length; i++) {
          let row = answer[i];
          table.insertAdjacentHTML('beforeend',row_pattern
                                                .replaceAll('{{ word.word }}', row.word)
                                                .replaceAll('{{ forloop.counter }}',i+1)
                                                .replaceAll('{{ word.transcription }}', row.transcription)
                                                .replaceAll('{{ word.show_count }}', row.show_count)
                                                .replaceAll('{{ word.word_background_color }}',GetBackGroundColorByIndex(Number(row.last_view.substring(5,7)))))
        }
    }
      //console.log(table)
      
    }
    

  async function SetPhraseStatus(id, status){
      let body = `{"username":"`+`"`+`,`+` "command":"Set_Phrase_Status"`+`,`+` "comment":"`+id+`"`+`,`+` "data":"`+status+`"` +`}`;
      let req = new XMLHttpRequest();
      req.open(`POST`, `/api/v1/cross_request/`, true);
      req.send(body);
      req.onload = function() {
    }
  }

    async function Load_phrases(ready){
      let body = `{"username":"`+`"`+`,`+` "command":"Get_Phrases"`+`,`+` "comment":"`+`"`+`,`+` "data":"`+ready+`"` +`}`;
      let req = new XMLHttpRequest();
      req.open(`POST`, `/api/v1/cross_request/`, true);
      req.send(body);
      req.onload = function() {
        let answer = JSON.parse(req.responseText);
        table = document.getElementById('index_table_of_phrases');
        table_content = ''
        row_pattern =`    <tr id="tr_of_index_phrases__{{ phrase.id_phrase }}">
        <td width="65%"><a href="/phrases/in_progress/{{ phrase.id_phrase }}/">{{ phrase.phrase }}</a></td>
        <td width="20%">{{ phrase.translation }}</td>
        <td width="5%" align = "center">{{ phrase.show_count }}</td>
        <td width="5%" align = "center"><a href="/phrases/add_new/{{ phrase.id_phrase }}/"><IMG class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Редактировать фразу" src="/static/images/redo.png"></a></td>
        <td width="5%" align = "center"><a><IMG  onclick='SetPhraseStatus("{{ phrase.id_phrase }}", (document.getElementById("index_table_of_phrases").dataset.ready==1?0:1));document.getElementById("tr_of_index_phrases__{{ phrase.id_phrase }}").remove();LoadSimpleData();' class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Фраза выученна" src="/static/images/ok.png"></a></td>
        </tr>`
        for(let i = 0; i < answer.length; i++) {
          let row = answer[i];
          table.insertAdjacentHTML('beforeend',row_pattern
                                                .replaceAll('{{ phrase.id_phrase }}', row.id_phrase)
                                                .replaceAll('{{ phrase.phrase }}',row.phrase)
                                                .replaceAll('{{ phrase.translation }}', row.translation)
                                                .replaceAll('{{ phrase.show_count }}', row.show_count)
                                                )

        }

        }
    }


    function get_server_api_address(){
      return document.body.dataset.apiserver
    }
    
    
    async function LoadOneSimpleData(element){
          //console.log('source:');
          //console.log('simplecommand: '+elements[i].dataset.simplecommand);
          let body =      `{"username":"`+`"`+`,`+
                          ` "command":"`+element.dataset.simplecommand+`"`+`,`+
                          ` "comment":"`+`"`+`,`+
                          ` "data":"`+`"` +
                          `}`;
          let req = new XMLHttpRequest();
          req.open(`POST`, `/api/v1/cross_request/`, true);
          req.send(body);
          req.onload = function(){
          let answer = JSON.parse(req.responseText);
          element.innerHTML = answer.data
        }
          //console.log("answer.data: "+answer.data);
    }
    
    
    async function LoadSimpleData(){
      
      let elements = document.querySelectorAll('[data-simplecommand]');
      for (element of elements) {
        await LoadOneSimpleData(element)
     }
    }
    
    async function LoadPaginatorBlock(){
      let elements = document.querySelectorAll('.pagination_auto');
       //console.log('paginators count:'+elements.length);
       let syllables_curent_page = Number(getCookie('syllables_curent_page'+document.getElementById('index_table_of_syllables').dataset.ready, 1));
       for (let element of elements){
            //console.log('pagination_auto:'+i)
            //console.log(elements[i])
            let body =      `{"username":"`+`"`+`,`+
                            ` "command":"syllables_slices_count"`+`,`+
                            ` "comment":"`+`"`+`,`+
                            ` "data":"100,`+document.getElementById('index_table_of_syllables').dataset.ready+`"` +
                            `}`;
            let req = new XMLHttpRequest();
            req.open(`POST`, `/api/v1/cross_request/`, true);
            req.send(body);
            req.onload=function(){
              let answer = JSON.parse(req.responseText);
              st=``
              for(let j=1, max=Number(answer.data)+1; j<max; j++) {
                  //console.log(j)
                  st += `<td width="`+Math.floor(100/Number(answer.data))+`%" style="`+(j == syllables_curent_page ? `font-weight: bolder;text-shadow:1px 1px green,2px 2px #777;color: #333;transition: all 1s;border: 5px solid;`:`font-weight: normal;`)+`" ><a href="" onclick="Load_words_slice(100,`+j+`,`+Number(document.getElementById('index_table_of_syllables').dataset.ready)+`)"> `+j+`</a></td>`;
              }
              element.innerHTML = '';
              element.innerHTML = `<table width = "95%"><tr>` + st + `</tr></table>`;
            }
       }
    
  }


  document.addEventListener('keyup', function (event) {
    //alert(`Клавиша ${event.key} отпущена`)
    if (event.key == 'Escape'){
      Close_Findind();
    }
})


function Close_Findind(){
    document.getElementById("search_result").hidden=true;
}

function Find_Word(){
    document.getElementById("search_result").hidden=false;
    document.getElementById("text_for_finding").focus()
    }


async  function get_finding(lc_value){
  let response = await fetch('/api/v1/cross_request/', {
                                                          method: 'POST',
                                                          headers: {
                                                            'Content-Type': 'application/json;charset=utf-8'
                                                          },
                                                          body: JSON.stringify({  username:``,
                                                                                  command:`syllables_look_for_word_part`,
                                                                                  ready:0,
                                                                                  slice_number:1,
                                                                                  slice_size:100,
                                                                                  word_part:lc_value
                                                                                })
                                                                              }
                                                          )
      let answer = await response.json();
      table_content = '';
      row_pattern =   `<tr id="tr_of_index_words__{{ word.word }}">
      <td width="7%" style="background:{{ word.word_background_color }}">{{ forloop.counter }}</td>
      <td with = "24%" style="color:Blue"><a href="./word_in_progress/{{ word.word }}/">{{ word.word }}</a></td>
      <td width="24%" align = "center" style="color:DarkRed"  onclick="new Audio('/static/sounds/{{ word.word }}.mp3').play(); return false;" >{{ word.transcription }}</td>
      <td width="7%" align = "center">{{ word.show_count }}</td>
      <td width="7%" align = "center"><a href="./add_new/{{ word.word }}/"><IMG class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Редактировать слово {{ word.word }}" src="/static/images/redo.png"></a></td>
      <td width="7%" align = "center"><a onclick='SetWordStatus("{{ word.word }}", (document.getElementById("index_table_of_syllables").dataset.ready==1?0:1)); document.getElementById("tr_of_index_words__{{ word.word }}").remove(); LoadSimpleData();'><IMG  class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Слово выученно" src="/static/images/ok.png"></a></td>
      </tr>`;
      document.getElementById("span_search_result").innerHTML='';
      for(let i = 0; i < answer.length; i++) {
        let row = answer[i];
        document.getElementById("span_search_result").insertAdjacentHTML('beforeend',row_pattern
                                              .replaceAll('{{ word.word }}', row.word)
                                              .replaceAll('{{ forloop.counter }}',i+1)
                                              .replaceAll('{{ word.transcription }}', row.transcription)
                                              .replaceAll('{{ word.show_count }}', row.show_count)
                                              .replaceAll('{{ word.word_background_color }}',GetBackGroundColorByIndex(Number(row.last_view.substring(5,7)))))
      }


    return
    if (lc_value.length>1){
            let response = await fetch("/api/"+lctype+"/"+lc_value+"/");
            let commits = await response.text();
            console.log(commits);
            document.getElementById("span_search_result").innerHTML = commits;
    } else {
        document.getElementById("span_search_result").innerHTML = '';
    }
}    

/*  tsts
  var req = new XMLHttpRequest();
  req.open(`POST`, get_server_api_address()+`/tsts/`, false);
  req.setRequestHeader('Content-Type', 'application/json');
  req.send('{"username":"admin"}');
  //Content-Type : 'application/x-www-form-urlencoded'
  console.log('req.responseText:')
  console.log(req.responseText)
  var answer = JSON.parse(req.responseText);
  console.log('answer');
  console.log(answer);
  console.log('answer length: ' + answer.length);
*/


/*   
  if(document.getElementById('invisible_link_for_link_path')!=null) {
    new Audio( document.getElementById('invisible_link_for_link_path').getAttribute('href') ).play();
  }

  var books_information = document.querySelectorAll(".book_position");
  for (var elem of books_information) {
      get_book_information(elem, "book_position");
      }
  var books_name = document.querySelectorAll(".book_name");
  for (var elem of books_name) {
      get_book_information(elem, "book_name");
  }
  var span_number_of_words_to_study = document.querySelectorAll(".span_number_of_words_to_study");
  for (var elem of span_number_of_words_to_study) {
      get_book_information(elem, "span_number_of_words_to_study");
  }
  var span_number_of_words_study_today = document.querySelectorAll(".span_number_of_words_study_today");
  for (var elem of span_number_of_words_study_today) {
      get_book_information(elem, "span_number_of_words_study_today");
  }
  var link_last_added_word = document.querySelectorAll(".link_last_added_word");
  for (var elem of link_last_added_word) {
      get_book_information(elem, "link_last_added_word");
  }
  var number_of_words_learned = document.querySelectorAll(".number_of_words_learned");
  for (var elem of number_of_words_learned) {
      get_book_information(elem, "number_of_words_learned");
  }

  var class_user_view = document.querySelectorAll(".class_user_view");
  for (var elem of class_user_view) {
      get_book_information(elem, "class_user_view");
  }
  */


//Устанавливает куки с именем name и значением value, с настройкой path=/ по умолчанию

function setCookie(name, value, options = {}) {

    options = {
      path: '/',
      // при необходимости добавьте другие значения по умолчанию
      ...options
    };
  
    if (options.expires instanceof Date) {
      options.expires = options.expires.toUTCString();
    }
  
    let updatedCookie = encodeURIComponent(name) + "=" + encodeURIComponent(value);
  
    for (let optionKey in options) {
      updatedCookie += "; " + optionKey;
      let optionValue = options[optionKey];
      if (optionValue !== true) {
        updatedCookie += "=" + optionValue;
      }
    }
  
    document.cookie = updatedCookie;
  }

function deleteCookie(name) {
    setCookie(name, "", {
      'max-age': -1
    })
  }

// возвращает куки с указанным name,
// или undefined, если ничего не найдено
function getCookie(name, default_value) {
  
    let matches = document.cookie.match(new RegExp(
      "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    let result =  (matches ? decodeURIComponent(matches[1]) : undefined) ;
    
    if (result == null){
      result = default_value;
    }
    console.log('name:'+name+'   default_value:'+default_value+'   result:'+result)
    //console.log('matches:'+(result == null))
    return result;
  }


function get_book_information(element, lctype){
    if (lctype == "book_position") {
              let settings = {
                              "url": "/api/book_position/"+element.dataset.idbook+"/",
                              "method": "GET",
                              "timeout": 0,
                              };
                  $.ajax(settings).done(function (response) {
                                                                  element.innerHTML = response.book_position;
                        });
                      }
    if (lctype == "book_name") {
              let settings = {
                              "url": "/api/book_name/"+element.dataset.idbook+"/",
                              "method": "GET",
                              "timeout": 0,
                              };
                  $.ajax(settings).done(function (response) {
                                                                  element.innerHTML = response.book_name ;
                        });
                      }
    if (lctype == "span_number_of_words_to_study") {
              let settings = {
                              "url": "/api/span_number_of_words_to_study/any/",
                              "method": "GET",
                              "timeout": 0,
                              };
                  $.ajax(settings).done(function (response) {
                                                                  element.innerHTML = response.span_number_of_words_to_study ;
                        });
                      }
    //console.log('111')
    if (lctype == "span_number_of_words_study_today") {
              let settings = {
                              "url": "/api/span_number_of_words_study_today/any/",
                              "method": "GET",
                              "timeout": 0,
                              };
                  $.ajax(settings).done(function (response) {
                                                                  element.innerHTML = response.span_number_of_words_study_today ;
                        });
                      }
    if (lctype == "link_last_added_word") {
              let settings = {
                              "url": "/api/link_last_added_word/any/",
                              "method": "GET",
                              "timeout": 0,
                              };
                  $.ajax(settings).done(function (response) {
                                                                  element.innerHTML = response.link_last_added_word ;
                        });
                      }
    if (lctype == "number_of_words_learned") {
              let settings = {
                              "url": "/api/number_of_words_learned/any/",
                              "method": "GET",
                              "timeout": 0,
                              };
                  $.ajax(settings).done(function (response) {
                                                                  element.innerHTML = response.number_of_words_learned ;
                        });
                      }
    if (lctype == "class_user_view") {
              let settings = {
                              "url": "/api/user_view/any/",
                              "method": "GET",
                              "timeout": 0,
                              };
                  $.ajax(settings).done(function (response) {
                                                                  element.innerHTML = response.user_view ;
                        });
                      }


  }

  function speakText(text) {
    // остановим все, что уже синтезируется в речь
    window.speechSynthesis.cancel();
    // прочитать текст
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
  }
  
  function speak(text) {
     speechSynthesis.speak(new SpeechSynthesisUtterance(text));
      }

  function WordChange() {document.getElementById('id_link_on_wooordhunt').href='https://wooordhunt.ru/word/'+escape(this.value)}

/*
  function getCookie(name) {
          var cookieValue = null;
          if (document.cookie && document.cookie !== '') {
              const cookies = document.cookie.split(';');
              for (var i = 0; i < cookies.length; i++) {
                  const cookie = cookies[i].trim();
                  // Does this cookie string begin with the name we want?
                  if (cookie.substring(0, name.length + 1) === (name + '=')) {
                      cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                      break;
                  }
              }
          }
          return cookieValue;
      }
*/






