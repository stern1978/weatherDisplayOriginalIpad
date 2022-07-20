fetch('https://api.weather.gov/alerts/active/zone/NYZ075')
.then(function(response){
    return response.json();
}).then(function(text){
    console.log(text);
    var title = text.title;
    document.getElementById('title').innerHTML = title;
});