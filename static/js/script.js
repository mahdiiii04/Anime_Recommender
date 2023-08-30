
document.addEventListener("DOMContentLoaded", function() {

var rec_button = document.getElementById("rec")


rec_button.addEventListener('click', ()=>{
    console.log("Button clicked");
    var select = document.getElementById("Anime_Dropdown");
    var selectedOption = select.options[select.selectedIndex];
    var anime_name = selectedOption.value;

    var form = document.createElement('form');
    form.style.display = 'none';

    form.method = 'POST';
    form.action = '/recommend_anime';

    var input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'Anime';
    input.value = anime_name;

    form.appendChild(input);

    document.body.appendChild(form);

    form.submit();
});
});