var selection_state=1;

// arrays of modal form IDs
var forms = [];

var forms_zindex=1;

var border_colors = ["border-primary", "border-secondary", "border-success", "border-danger", "border-warning", "border-info", "border-dark"];

window.addEventListener('resize', function() {
  ResizeModalForms();
});

window.onload = async function(event) {
  // global variables for connect to APIServer
  console.log(UserName, UserUUID, APIServer);

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      CloseToplevelDynamicForm();
    }
  });
  

  Load_Books_List();
  LoadSimpleData(); 
  if(document.getElementById('index_table_of_syllables')!=null){
        LoadPaginatorBlock();
        Load_words_slice(100,
                      Number(getCookie('syllables_curent_page'+document.getElementById('index_table_of_syllables').dataset.ready, 1)),
                      Number(document.getElementById('index_table_of_syllables').dataset.ready));

    }

    Load_Word_in_Progress_Data();
    Load_Phrase_in_Progress_Data();
    Load_Phrase_in_Edit_Data();
    Load_Syllable_Into_Add_New_Word();
    Load_Book_Page();
    if (document.getElementById('index_table_of_phrases')!=null){
        Load_phrases(Number(document.getElementById('index_table_of_phrases').dataset.ready));
    }
  }

async function asyncRequest (uri, method, data, debug=false){
    data[`username`]=UserName;
    data[`useruuid`]=UserUUID;
    let uuid = create_UUID();
    if (debug){
              console.log(uuid, method, uri, 'SEND DATA:', data);
    }
    let response_promise = await fetch(uri, {method: method, headers: { 'Content-Type': 'application/json;charset=utf-8' }, body: JSON.stringify(data) } )
    return response_promise.json();
}

// save phrase data into DB, if link parameter not empty goes by it link
function SavePhrase(link){
  console.log(`SavePhrase`);
  console.log(`${APIServer}/Save_Phrase/`);
  console.log(`${document.querySelector(`#body_phrase_edit`).dataset.phraseid}`);
  asyncRequest( `${APIServer}/Save_Phrase/`,
                `POST`,
                {command:`${document.querySelector(`#body_phrase_edit`).dataset.phraseid}`, comment:`${document.getElementById('phrase_text').value}`, data:`${document.getElementById('phrase_translation').value}`})
  if (link.length>0){
                     window.location.href = link;
  }
              
}


  async function Load_Phrase_in_Edit_Data(){
    if(!document.querySelector(`#body_phrase_edit`)){
      console.log('Load_Phrase_in_Edit_Data', 'no phrase edit')
      return
    }
    if (!(Number(document.querySelector(`#body_phrase_edit`).dataset.phraseid)>=0)){
      console.log('Load_Phrase_in_Edit_Data', 'no right phrase id')
      return
    }
    let answer = await asyncRequest(`${APIServer}/Get_Phrase/`, `POST`, {command:``, comment:``, data:`${document.querySelector(`#body_phrase_edit`).dataset.phraseid}`})
    document.getElementById('phrase_text').value = answer.phrase
    document.getElementById('phrase_translation').value = answer.translation;
  }



async function FlipPages(step){
  if(!document.querySelector(`#id_body_book`)){
    return;
  }
  showOverlay();
  let jresponse =  await asyncRequest(`${APIServer}/Set_Book_Position/`, `POST`, {command:``, comment:``, data:`${document.querySelector(`#id_body_book`).dataset.idbook},${Number(document.querySelector(`#id_body_book`).dataset.currentparagraph)+step}`});
  if (jresponse.data='Ok'){
    document.querySelector(`#id_body_book`).dataset.currentparagraph = Number(document.querySelector(`#id_body_book`).dataset.currentparagraph)+step;
    await Load_Book_Page();
  }
  LoadSimpleData();
  hideOverlay();
}

async function Load_Book_Page(){
  if( !document.querySelector(`#id_body_book`)){
    return;
  }
  showOverlay();
  let answer = await asyncRequest(`${APIServer}/Get_Book_Information/`, `POST`, {command:``, comment:``, data:`${document.querySelector(`#id_body_book`).dataset.idbook}`});
                            document.getElementById(`id_book_name`).innerHTML = answer.book_name;
                            document.getElementById(`id_book_position_percent`).innerHTML = ((answer.current_paragraph      - answer.Min_Paragraph_Number) * 100 / 
                                                                                      (answer.Max_Paragraph_Number  - answer.Min_Paragraph_Number)).toFixed(2) + `% &nbsp;&nbsp;&nbsp;`
                            document.getElementById(`id_book_position`).innerHTML = (answer.current_paragraph     - answer.Min_Paragraph_Number) + ` / ` + (answer.Max_Paragraph_Number- answer.Min_Paragraph_Number);

                            document.querySelector(`#id_body_book`).dataset.currentparagraph = answer.current_paragraph;
                            let wordlist = await asyncRequest(`${APIServer}/Get_List_Of_User_Syllable_From_Paragraphs_Id/`, `POST`, {command:``, comment:`${answer.id_book}`, data:`${answer.current_paragraph},${Number(answer.current_paragraph)+1},${Number(answer.current_paragraph)+2},${Number(answer.current_paragraph)+3},${Number(answer.current_paragraph)+4}`})
                            console.log(wordlist);
                            let sentence_number = 0;
                                                          document.getElementById(`id_div_book_body`).innerHTML=``;
                                                          let jresponse = await asyncRequest(`${APIServer}/Get_Paragraphs/`,`POST`,{command:``, comment:``, data:`${answer.id_book},${answer.current_paragraph},5`});
                                                          for (let paragrath of jresponse){
                                                                                            lc_book_paragraph = `<br><p class="my_class_p_my_class_p_examples color_block_book_paragraph">`;
                                                                                            for (let sentence of paragrath){
                                                                                                                            let modified_sentence = sentence.sentence;
                                                                                                                            for (word of wordlist.words){
                                                                                                                              if (~sentence.sentence.toLowerCase().indexOf(word.toLowerCase())){
                                                                                                                                console.log(`${word}: ${sentence.sentence}`);
                                                                                                                                let startindex = sentence.sentence.toLowerCase().indexOf(word.toLowerCase());
                                                                                                                                let endindex = startindex + word.length;
                                                                                                                                modified_sentence =   modified_sentence.slice(0, startindex) + 
                                                                                                                                                      `<span style="color:#7a8500">` + 
                                                                                                                                                      modified_sentence.slice(startindex,endindex) +
                                                                                                                                                      `</span>` +
                                                                                                                                                      modified_sentence.slice(endindex,modified_sentence.length);
                                                                                                                              }
                                                                                                                            }
                                                                                                                            sentence_number += 1;
                                                                                                                            lc_book_paragraph += `<span id ="sentence_${sentence_number}"  onclick="selectText('sentence_${sentence_number}');" class = '${sentence_number%2==0 ? 'my_class_p_my_class_p_books_even':'my_class_p_my_class_p_books'}'>`;
                                                                                                                            lc_book_paragraph += modified_sentence;
                                                                                                                            lc_book_paragraph += `</span>`;
                                                                                                                            lc_book_paragraph += `&nbsp; `
                                                                                                                            lc_book_paragraph += `<IMG class='img_with_backlight_on_hover' WIDTH='48' HEIGHT='48'  title = '' src='/static/images/audio.svg' onclick = 'new Audio("/sentence/${sentence.mime}").play(); return false;'>`
                                                                                                                            lc_book_paragraph += `&nbsp;&nbsp;&nbsp; `
                                                                                                                          }
                                                                                            lc_book_paragraph += `</p>`
                                                                                            document.getElementById(`id_div_book_body`).insertAdjacentHTML('beforeend',lc_book_paragraph)
                                                          }
  hideOverlay();
}

function selectText(containerid) {
  if (selection_state==1)
  {
      if (document.selection) { // IE
          var range = document.body.createTextRange();
          range.moveToElementText(document.getElementById(containerid));
          range.select();
      } else if (window.getSelection) {
          var range = document.createRange();
          range.selectNode(document.getElementById(containerid));
          window.getSelection().removeAllRanges();
          window.getSelection().addRange(range);
      }
  }
}

function clickAutoSelectEvent(obj)
{
if (selection_state==1)
    {
        selection_state=2
        obj.src="/static/images/angle_text.png"
    }
else 
    {
        selection_state=1
        obj.src="/static/images/angle_text_bright.png"
    }
}

async function Load_Books_List(){
    if(!document.querySelector(`#id_table_of_books`)){
      return;
    }
    showOverlay();
    let answer = await asyncRequest( `${APIServer}/Get_User_Books/`,
                                     `POST`,
                                     {command:``, comment:``, data:``})
    let pattern = `    
    <div class="row mt-1 color_block_blue_green">
    <div class="col-8">
        <span class="font_blue_larger"> <a href="/book/{ _id_book_ }/">{ _book_name_ }</a> </span>
    </div>
    <div class="col-2">
        <span class="font_blue_larger"> { _book_position_information_percent_ } </span>
    </div>
    <div class="col-2">
        <span class="font_blue_larger"> { _book_position_information_from_to_ } </span>
    </div>
    </div>
    `;
    for (let book of answer) {
                              document.getElementById(`id_table_of_books`).
                              insertAdjacentHTML('beforeend', pattern.
                              replaceAll(`{ _id_book_ }`, String(book.id_book)).
                              replaceAll(`{ _book_name_ }`, book.book_name).
                              replaceAll(`{ _book_position_information_percent_ }`, ((book.current_paragraph - book.Min_Paragraph_Number) * 100 / (book.Max_Paragraph_Number- book.Min_Paragraph_Number)).toFixed(2)).
                              replaceAll(`{ _book_position_information_from_to_ }`, (book.current_paragraph - book.Min_Paragraph_Number) + ` / ` + (book.Max_Paragraph_Number- book.Min_Paragraph_Number))
                              )}
    hideOverlay();          
    }


  function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
  }



  
// return object of examples for the JSON serialization  
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
    subresult.rowid = ((example_element.dataset.rowid === `undefined`)? -1 : example_element.dataset.rowid);
    console.log(subresult.rowid)
    result.push(subresult);
  }
  return result
}

// save syllable data into DB, if link parameter not empty goes by it link
function SaveSyllable(link){
  if(!document.querySelector(`#body_add_new_word`)){
    return;
  }
  let obody = {   username:``,
                  command:`Save_Syllabe`,
                  word:document.getElementById(`id_word`).value,
                  syllable_id:(document.querySelector(`#body_add_new_word`).dataset.syllable_id==='undefined'? -1:document.querySelector(`#body_add_new_word`).dataset.syllable_id),
                  transcription:document.getElementById(`id_transcription`).value,
                  translations:document.getElementById(`id_translations`).value,
                  examples:GetAllExamplesFromNewSyllablePage()
              }
  console.log(`obody`, obody)
  let response = fetch('/api/v1/cross_request/', {
                                                  method: 'POST',
                                                  headers: {
                                                    'Content-Type': 'application/json;charset=utf-8'
                                                  },
                                                  body: JSON.stringify(obody)
                                                  }
                      )
  if (link.length>0){
    window.location.href = link;
  }
}

function AddExamplToNewSyllablePage(parent, example, translate, rowid, id_int){
  let pattern = `<div class="div_example_class" data-rowid="{ _rowid_ }" id="example_section_{ _random_ }" style="text-align:right;"><IMG class ="image_little_button" WIDTH="64" HEIGHT="64"  title = "Удалить пример" src="/static/images/delete.png" onclick="document.getElementById('example_section_{ _random_ }').remove();"'>
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

async function LoadSyllableFromWoordhunt(word){
  if (document.querySelector(`#body_add_new_word`)==null){
           return}
        else {
              if (document.querySelector(`#body_add_new_word`).dataset.word.length=0){
                   return
                 }
              }
  showOverlay();
  let req = new XMLHttpRequest(); // may be sync
  req.open(`GET`, `/GetWoorhuntDataJSON/${word}/`, true);
  req.send();
  req.onload = function(){
    let answer = JSON.parse(req.responseText);
    console.log(answer)
    document.querySelector(`#body_add_new_word`).dataset.syllable_id = answer.syllable_id;
    document.getElementById(`id_transcription`).value = answer.transcription
    document.getElementById(`id_translations`).value = answer.translations
    for (var example of answer.examples) {
                                          AddExamplToNewSyllablePage(document.getElementById(`id_examples`), example.example, example.translate, example.rowid, getRandomInt(1000000000000, 9999999999999));
                                        }
  hideOverlay();
}

}

  async function Load_Syllable_Into_Add_New_Word(){
    console.log('Load_Syllable_Into_Add_New_Word');
    if(!document.querySelector(`#body_add_new_word`)){
      console.log("isn't Load_Syllable_Into_Add_New_Word");
      return
    }
    if (document.querySelector(`#body_add_new_word`).dataset.word.length<=0){ // for empty new word case
      console.log("Load_Syllable_Into_Add_New_Word  word's length is zero");
      return
    }
                            let answer = await asyncRequest(`${APIServer}/get_syllable_full_data/`, `POST`, {command:``, comment:``, data:`${document.querySelector(`#body_add_new_word`).dataset.word}`});
                            console.log(answer)
                            document.querySelector(`#body_add_new_word`).dataset.syllable_id = answer.syllable_id;
                            document.getElementById(`id_transcription`).value = answer.transcription
                            document.getElementById(`id_translations`).value = answer.translations
                            for (var example of answer.examples) {
                                                                  AddExamplToNewSyllablePage(document.getElementById(`id_examples`), example.example, example.translate, example.rowid, getRandomInt(1000000000000, 9999999999999));
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
      if(!document.querySelector('#body_phrase_in_progress')){
        return
      }
      if (document.querySelector('#body_phrase_in_progress').dataset.phraseid=='' | Number(document.querySelector('#body_phrase_in_progress').dataset.phraseid)==0 ){
        document.querySelector('#body_phrase_in_progress').dataset.phraseid = await LoadNextProcessingPhraseIntoBody();
      }
      let answer = await asyncRequest( `${APIServer}/Get_Phrase/`,`POST`,{command:``, comment:``, data:`${document.querySelector('#body_phrase_in_progress').dataset.phraseid}`}, true)
      document.getElementById('id_class_p_my_class_p_examples').innerHTML         = answer.phrase +`&nbsp;&nbsp;&nbsp;<IMG class='img_with_backlight_on_hover' WIDTH='48' HEIGHT='48'  title = '' src='/static/images/audio.svg' onclick = 'new Audio("/sentence/`+answer.linkcode+`" ).play(); return false;'>`;
      document.getElementById('id_class_p_my_class_p_examples_russian').innerHTML = answer.translation;
     }

    async function LoadNextProcessingPhraseIntoBody(){
        let answer = await asyncRequest(`${APIServer}/Get_Next_Phrase_For_Learning/`, 'POST', {command:``, comment:``, data:``});
        return answer.id_phrase;
    }

    async function UpdateCurrentPhraseAsViewed(){
      await asyncRequest(`${APIServer}/Update_phrase_as_viewed/`,'POST',{command:``, comment:``, data:`${document.querySelector('#body_phrase_in_progress').dataset.phraseid}`})
    }

    async function NextPhrase(){
      showOverlay();
      await UpdateCurrentPhraseAsViewed();
      document.querySelector('#body_phrase_in_progress').dataset.phraseid= await LoadNextProcessingPhraseIntoBody();
      await Load_Phrase_in_Progress_Data();
      hideOverlay();
    }

    async function Load_Word_in_Progress_Data(){
      if(!document.querySelector(`#dataset`)){
        console.log('no Load_Word_in_Progress_Data')
        return
      }
      console.log('Load_Word_in_Progress_Data')
      if (document.querySelector(`#dataset`).dataset.word.replaceAll(' ','')==''){
        await LoadNextProcessingWordIntoBody();
      }

      let answer = await asyncRequest(`${APIServer}/get_syllable_full_data/`, `POST`, {command:``, comment:``, data:`${document.querySelector(`#dataset`).dataset.word}`},true)

        console.log(answer)
        document.title = `${answer.word}`;
        document.getElementById('id_link_on_wooordhunt').href=`https://wooordhunt.ru/word/${answer.word}`;
        document.getElementById('id_link_on_glosbe').href=`https://ru.glosbe.com/en/ru/${answer.word}`;
        
        document.getElementById('id_my_class_p_word').innerHTML = answer.word;
        document.getElementById('id_my_class_p_transcription').onclick = function(){new Audio( `/static/sounds/${document.querySelector(`#dataset`).dataset.word}.mp3` ).play(); return false;};
        document.getElementById('id_my_class_p_transcription').innerHTML = answer.transcription;
        document.getElementById('id_my_class_p_my_class_p_translations').innerHTML = ``;
        let st = '';
        for (element of answer.translations.split(/(?:\r?\n)+/)){
            st += element+'<br>'
        }
        document.getElementById('id_my_class_p_my_class_p_translations').insertAdjacentHTML('beforeend',add_format_for_russian(st, 'my_class_p_my_class_p_translations_russian'));
        document.getElementById('id_my_class_p_my_class_p_examples').innerHTML = ``;
        for (sl of answer.examples){
          if (sl.example!=null){
                    document.getElementById('id_my_class_p_my_class_p_examples').insertAdjacentHTML('beforeend',`<p class = "my_class_p_my_class_p_examples">` + sl.example+ `<IMG class='img_with_backlight_on_hover' WIDTH='48' HEIGHT='48'  title = '' src='/static/images/audio.svg' onclick = 'new Audio("/sentence/`+sl.linkcode+`" ).play(); return false;'></p>`);
          }
          if (sl.translate!=null){
                    document.getElementById('id_my_class_p_my_class_p_examples').insertAdjacentHTML('beforeend',`<p class = "my_class_p_my_class_p_examples_russian">` + sl.translate+ `</p><br>`);
          }
        }
      
    }

    async function LoadNextProcessingWordIntoBody(){
      let answer = await asyncRequest(`${APIServer}/Get_Next_Syllable_For_Learning/`, `POST`, {command:``, comment:``, data:``})
      console.log(answer)
      document.querySelector(`#dataset`).dataset.word = answer.data;
      document.querySelector(`#link_on_word_redo`).href=`/add_new_word/${answer.data}/`;
      document.querySelector(`#img_into_link_on_word_redo`).title=`Редактировать слово ${answer.data}`;
      console.log(document.querySelector(`#dataset`).dataset.word);
    }

    async function SetSyllableAsViewedAndLoadNext(word){
      showOverlay();
      console.log(`send: ${word}`)
      let req = new XMLHttpRequest();
      let body =      `{"username":"`+`"`+`,`+` "command":"update_syllable_as_viewed"`+`,`+` "comment":"`+`"`+`,`+` "data":"`+word+`"` +`}`;
      req.open(`POST`, `/api/v1/cross_request/`, false);
      req.send(body);
      console.log(req.responseText);
      let answer = JSON.parse(req.responseText);
      await LoadNextProcessingWordIntoBody();
      await Load_Word_in_Progress_Data();
      hideOverlay();
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
        let answer = await asyncRequest(`${APIServer}/syllables/`, `POST`, {command:``, ready:`${ready}`, slice_number:`${slice_number}`, slice_size:`${slice_size}`, word_part:``});
        table = document.querySelector(`#index_table_of_syllables`);
        table_content = ''
        row_pattern =   `
        
        <div class="row mt-1 color_block_blue_green" id="tr_of_index_words__{{ word.word }}">
        <div class="col-1">
            <span class="font_blue_larger" > {{ forloop.counter }} </span>
        </div>
        <div class="col-4 font_blue_larger">
            <span> <a href="/word_in_progress/{{ word.word }}/">{{ word.word }}</a> </span>
        </div>
        <div class="col-4" style="color:DarkRed"  onclick="new Audio('/static/sounds/{{ word.word }}.mp3').play(); return false;">
            <span class="font_red_larger"> {{ word.transcription }} </span>
        </div>
        <div class="col-1">
            <span class="font_blue_larger"> {{ word.show_count }} </span>
        </div>
        <div class="col-1">
            <span class="font_blue_larger"> <a href="/add_new_word/{{ word.word }}/"><IMG class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Редактировать слово {{ word.word }}" src="/static/images/redo.png"></a> </span>
        </div>
        <div class="col-1">
            <span class="font_blue_larger"> <a onclick='SetWordStatus("{{ word.word }}", (document.getElementById("index_table_of_syllables").dataset.ready==1?0:1)); document.getElementById("tr_of_index_words__{{ word.word }}").remove(); LoadSimpleData();'><IMG  class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Слово выученно" src="/static/images/ok.png"></a> </span>
        </div>
        </div>`
        
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
    

  async function SetPhraseStatus(id, status){
    await asyncRequest(`${APIServer}/Set_Phrase_Status/`,`POST`, {command:``, comment:`${id}`, data:`${status}`})
  }

    async function Load_phrases(ready){
      let answer = await asyncRequest(  `${APIServer}/Get_Phrases/`,
      `POST`, 
      {command:``, comment:``, data:`${ready}`});
        table = document.getElementById('index_table_of_phrases');
        table_content = ''
        row_pattern =`    
        <div class="row mt-1 color_block_blue_green" id="tr_of_index_phrases__{{ phrase.id_phrase }}">
          <div class="col-5">
              <span class="font_blue_larger"> <a href="/phrases/in_progress/{{ phrase.id_phrase }}/">{{ phrase.phrase }}</a> </span>
          </div>
          <div class="col-4">
              <span class="font_green_larger"> {{ phrase.translation }} </span>
          </div>
          <div class="col-1">
              <span class="font_blue_larger"> {{ phrase.show_count }} </span>
          </div>
          <div class="col-1">
              <span class="font_blue_larger"> <a href="/phrases/add_new/{{ phrase.id_phrase }}/"><IMG class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Редактировать фразу" src="/static/images/redo.png"></a> </span>
          </div>
          <div class="col-1">
              <span class="font_blue_larger"> <a><IMG  onclick='SetPhraseStatus("{{ phrase.id_phrase }}", (document.getElementById("index_table_of_phrases").dataset.ready==1?0:1));document.getElementById("tr_of_index_phrases__{{ phrase.id_phrase }}").remove();LoadSimpleData();' class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Фраза выученна" src="/static/images/ok.png"></a> </span>
          </div>
        </div>
        `
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


   
    async function LoadOneSimpleData(element){
          let answer = await asyncRequest(  `${APIServer}/${element.dataset.simplecommand}/`,
                                            `POST`, 
                                            {command:``, comment:``, data:``});
          element.innerHTML = answer.data;
    }
    
    
    async function LoadSimpleData(){
      let elements = document.querySelectorAll('[data-simplecommand]');
      for (element of elements) {
        LoadOneSimpleData(element)
     }
    }
    
    async function LoadPaginatorBlock(){
      let elements = document.querySelectorAll('.pagination_auto');
       //console.log('paginators count:'+elements.length);
       let syllables_curent_page = Number(getCookie('syllables_curent_page'+document.getElementById('index_table_of_syllables').dataset.ready, 1));
       for (let element of elements){
              let answer = await asyncRequest(`${APIServer}/syllables_slices_count/`, `POST`, {command:``, comment:``, data:`100,${document.getElementById('index_table_of_syllables').dataset.ready}`})
              if (Number(answer.data)>1){
                                          st=``
                                          for(let j=1, max=Number(answer.data)+1; j<max; j++) {
                                              st += `<td width="`+Math.floor(100/Number(answer.data))+`%" style="`+(j == syllables_curent_page ? `font-weight: bolder;text-shadow:1px 1px green,2px 2px #777;color: #333;transition: all 1s;border: 5px solid;`:`font-weight: normal;`)+`" ><a href="" onclick="Load_words_slice(100,`+j+`,`+Number(document.getElementById('index_table_of_syllables').dataset.ready)+`)"> `+j+`</a></td>`;
                                          }
                                          element.innerHTML = '';
                                          element.innerHTML = `<table width = "95%"><tr>` + st + `</tr></table>`;
                                        }
            }
  }




function create_UUID() {
  return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
  );
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
      row_pattern =   `
      <div class="row mt-1 color_block_blue_green" id="tr_of_index_words__{{ word.word }}">
        <div class="col-1">
            <span class="font_blue_larger" > {{ forloop.counter }} </span>
        </div>
        <div class="col-4 font_blue_larger">
            <span> <a href="/word_in_progress/{{ word.word }}/">{{ word.word }}</a> </span>
        </div>
        <div class="col-4" style="color:DarkRed"  onclick="new Audio('/static/sounds/{{ word.word }}.mp3').play(); return false;">
            <span class="font_red_larger"> {{ word.transcription }} </span>
        </div>
        <div class="col-1">
            <span class="font_blue_larger"> {{ word.show_count }} </span>
        </div>
        <div class="col-1">
            <span class="font_blue_larger"> <a href="/add_new_word/{{ word.word }}/"><IMG class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Редактировать слово {{ word.word }}" src="/static/images/redo.png"></a> </span>
        </div>
        <div class="col-1">
            <span class="font_blue_larger"> <a onclick='SetWordStatus("{{ word.word }}", (document.getElementById("index_table_of_syllables").dataset.ready==1?0:1)); document.getElementById("tr_of_index_words__{{ word.word }}").remove(); LoadSimpleData();'><IMG  class ="image_little_button" WIDTH="32" HEIGHT="32"  title = "Слово выученно" src="/static/images/ok.png"></a> </span>
        </div>
        </div>
        `;
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
}    


function setCookie(name, value, options = {}) {

    options = {
      path: '/',
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




  // Функция для отображения занавески
function showOverlay() {
  document.getElementById('overlay').style.display = 'block';
}

// Функция для скрытия занавески
function hideOverlay() {
  document.getElementById('overlay').style.display = 'none';
}



//'image/jpeg, image/png, image/bmp, image/x-icon, image/webp'
//handleFileUpload(`image/jpeg, image/png, image/bmp, image/x-icon, image/webp`, `/tiles_upload/`)
function handleFileUpload(list_of_file_types, url, callback) {
  
  var fileInput = document.createElement('input');
  fileInput.type = 'file';
  fileInput.style.display = 'none';
  fileInput.id = 'fileInput';
  fileInput.multiple = true;
  fileInput.accept = list_of_file_types;
  document.body.appendChild(fileInput);
  fileInput.click();
  fileInput.addEventListener('change', function(event) {
      var files = event.target.files;
      for (var i = 0; i < files.length; i++) {
          var formData = new FormData();
          formData.append('file_name', files[i]);
          var xhr = new XMLHttpRequest();
          xhr.open('POST', url, false);
          xhr.onload = function() {
              if (xhr.status === 200) {
                  console.log('Файл успешно загружен на сервер.');
                  callback();
              } else {
                  console.error('Произошла ошибка при загрузке файла на сервер.');
              }
          };
          xhr.send(formData);
      }
      document.body.removeChild(fileInput);
  });
  fileInput.value = '';
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}


// run in screen form, fill and show
function RunInScreenForm ({form_name, execute_after_load, request_link, execute_on_ok='', ok_id, ok_title, execute_on_cancel=''}) {
  let outerRootElement = document.getElementsByTagName(`body`)[0];
  form_name = form_name + `_${getRandomInt(999999999999999)}`
  forms_zindex++;
  // console.log(forms_zindex);
  outerRootElement.insertAdjacentHTML(
    `beforeEnd`,
    `<div id="${form_name}" style=" max-height: 90vh; overflow-y:auto; background-image: url('/static/images/background.gif');" class="dynamic-form col-12 border-5 ${border_colors[forms_zindex%9]}" data-zindex="${forms_zindex}"></div>`);

  forms.push(form_name);
  document.getElementById(forms[forms.length-1]).setAttribute(`z-index`, forms_zindex);
 
  let xhr = new XMLHttpRequest();
  xhr.open(`GET`, request_link);
  xhr.send();
  xhr.onload = function() {
    document.getElementById(`${forms[forms.length-1]}`).insertAdjacentHTML(`afterBegin`, xhr.responseText);
    if (!(execute_on_cancel.length==0 && execute_on_ok.length==0)){
        document.getElementById(`${forms[forms.length-1]}`).insertAdjacentHTML(
          `beforeEnd`,
          `<hr><br>
            <div class="row">
              <div class="col-6">`+
                ((execute_on_ok.length>0)
                ?
                `<button type="button" class="btn btn-primary btn-lg btn-block button_save col" id="${(ok_id.length>0,ok_id,'button_modal_dialog_ok')}">
                  &nbsp&nbsp&nbsp&nbsp${(ok_title.length>0,ok_title,'Ok')}&nbsp&nbsp&nbsp&nbsp
                </button>`
                :
                ``)
              +`</div>

              <div class="col-6">
                <button id="${forms[forms.length-1]}_dialog_escape_button" type="button" class="btn btn-secondary btn-lg btn-block button_save col" onclick="${execute_on_cancel}">
                  Отмена
                </button>
              </div>
            </div>
              `);
    }
    document.getElementById(`${forms[forms.length-1]}`).insertAdjacentHTML(`beforeend`, `<hr id="id_anchor_end">`);
    
    //document.getElementById(`${forms[forms.length-1]}`).style.height = document.getElementById(`${forms[forms.length-1]}`).querySelector('#id_anchor_end').getBoundingClientRect().top

    // document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().height = document.getElementById(`${forms[forms.length-1]}`).querySelector('#id_anchor_end').getBoundingClientRect().top + 50 + 24;
    // let new_form_height = document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().top + 
    //                       document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().height + 50;
    //document.getElementById(`${forms[forms.length-1]}`).style.height=`${document.getElementById(`${forms[forms.length-1]}`).querySelector('#id_anchor_end').getBoundingClientRect().top + 50 + 24}px`;

    
    
    eval(execute_after_load);
    ResizeModalForms();




}

}


function ResizeModalForms(){

  




  
  // document.getElementById(`${forms[forms.length-1]}`).style.height = 0.95 * document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().height;
  // document.getElementById(`${forms[forms.length-1]}`).style.width = 0.95 * document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().width ;
  
  
  

  // console.log( document.getElementById(`${forms[forms.length-1]}`).querySelector('#id_anchor_end').getBoundingClientRect() );

  // console.log(`height: ${document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().height}`);
  // // console.log(`top _dialog_escape_button: ${document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().top}`);
  // // console.log(`height _dialog_escape_button: ${document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().height}`);
  // // document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().height = document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().top
  //                                                                       //  + document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().height + 24;
  // //let new_form_height = document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().top + document.getElementById(`${forms[forms.length-1]}_dialog_escape_button`).getBoundingClientRect().height + 50;
  // // document.getElementById(`${forms[forms.length-1]}`).style.height=`${new_form_height}px`;

  // console.log(`width: ${document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().width}`);
  // let new_form_width = document.getElementById(`${forms[forms.length-1]}`).getBoundingClientRect().width*0.9;
  // document.getElementById(`${forms[forms.length-1]}`).style.width=`${new_form_width}px`;

}


function CloseInScreenForm(form_id){
  document.querySelector(`#${form_id}`).remove();
 }

 function CloseToplevelDynamicForm(){
   if (forms.length>0){
     CloseInScreenForm(forms[forms.length - 1]);
     forms.pop();
   }
 }




 function OnLoadTileSelect(currrent_icon){
  FillTilesField(currrent_icon);
}



function SelectImage(){
  document.querySelector(`#inputIcon`).value = GetSelectedFileName();
  CloseToplevelDynamicForm();
}



function GetSelectedFileName(){
  if (document.querySelector('.selected')==null){
    return '';
  }
  else{
    return document.querySelector('.selected').dataset.filename;
  }
}


function DeleteTileImage(){
  console.log(`DeleteTileImage()`);
  console.log(GetSelectedFileName());
  console.log(GetSelectedFileName().length);
  if (GetSelectedFileName().length>0){
                                    $.ajax({
                                                url: `/tile_delete/${GetSelectedFileName()}`,
                                                method: "GET",
                                                async: false,
                                                timeout: 0,
                                                });
  }
}

function GetTiles() {
var xhr = new XMLHttpRequest();
xhr.open("GET", "/tiles_JSON/", false);
xhr.setRequestHeader("Content-Type", "application/json");
xhr.send();
var jsonResponse = JSON.parse(xhr.responseText);
return jsonResponse;
}


function FillTilesField(currrent_icon){
field = document.querySelector('#tiles_field');
field.innerHTML = ``;
let tiles = GetTiles();
let rowcounter = 0;
for (let row of tiles){
  rowcounter++;
  let rowid = `tilesrowid${rowcounter}`;
  field.insertAdjacentHTML(`beforeend`,`<div class="row justify-content-center" id="${rowid}"></div>`);
  rowelement = document.querySelector(`#${rowid}`);
  for (element of row){
    rowelement.insertAdjacentHTML(`beforeend`,`<div class="col-1"><img onclick="SelectTileonClick(this);" src="/api/v1/get_asset/tiles/${element.icon}" class="img-fluid img-thumbnail bg-dark ${(currrent_icon==element.icon?'selected':'')}" style="width:100%; height:width" data-selected="no" data-filename="${element.icon}"></div>`);
    //console.log(element);
  }
}
document.addEventListener("DOMContentLoaded", function() {
    const images = document.querySelectorAll(".img-thumbnail");
    images.forEach(function(image) {
                                      image.addEventListener("click", function() {
                                          images.forEach(function(img) {
                                              img.classList.remove("selected");
                                              img.dataset.selected = `no`;
                                          });
                                          this.classList.add("selected");
                                          this.dataset.selected = `yes`;
                                          //console.log(this.dataset.filename);
                                      });
                                    });
                                  });
}



function SelectTileonClick(selectme){
const tiles = document.querySelectorAll(".img-thumbnail");
for (tile of tiles){
          tile.classList.remove("selected");
          tile.dataset.selected = `no`;
}
selectme.classList.add("selected");
selectme.dataset.selected = `yes`;
}


async function SaveTile() {

  
    const data = {
        username: "",
        tile_id: 0,
        name: document.getElementById('inputName').value,
        hyperlink: document.getElementById('inputLink').value,
        icon: document.getElementById('inputIcon').value,
        color: document.getElementById('inputColor').value
    };


    asyncRequest( `${APIServer}/Save_Tile/`,
    `POST`,
    data
    )
}