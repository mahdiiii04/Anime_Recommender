
document.addEventListener("DOMContentLoaded", function() {

const rec_button = document.getElementById("rec")
const add_button = document.getElementById("add")
const clear_button = document.getElementById("clear")
const buttonsParent = document.getElementById("buttons")


add_button.addEventListener('click', ()=>{
    var select = document.getElementById("Anime_Dropdown");
    var selectedOption = select.options[select.selectedIndex];
    var anime_name = selectedOption.textContent;        
    
    var form = document.createElement('form');
    form.style.display = 'none';

    form.method = 'POST';
    form.action = '/adding';

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'Anime';
    input.value = anime_name;

    form.appendChild(input);

    document.body.appendChild(form);

    form.submit();
});

rec_button.addEventListener('click', ()=>{       

    const rec_send = document.createElement('form');
    rec_send.method = 'POST';
    rec_send.action = '/recommend_anime';

    document.body.appendChild(rec_send);

    rec_send.submit();
});

clear_button.addEventListener('click', ()=>{
    const clear_send = document.createElement('form');
    clear_send.method = 'POST';
    clear_send.action = '/';

    document.body.appendChild(clear_send);

    clear_send.submit();
});



function ButtonClickedHandler (event){
    var btn = event.target;
    var id = btn.id;

    var form = document.createElement('form');
    form.style.display = 'none';

    form.method = 'POST';
    form.action = '/deleting';

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'ID';
    input.value = id;

    form.appendChild(input);

    document.body.appendChild(form);

    form.submit();

};

buttonsParent.addEventListener('click', ButtonClickedHandler);


});

