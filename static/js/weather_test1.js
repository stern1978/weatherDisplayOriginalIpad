function datarefresh(){
    var refresh=10000; // Refresh rate in milli seconds
    mytime=setTimeout('data()',refresh);
    
    }

function data(){
fetch('http://192.168.1.200:8001/data')
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
    console.log(data);  
    var outsidetemp = data.outsidetemp;
    var feels_like = data.feels_like;
    var icon = data.icon;
    var avgtemp = data.avgtemp;
    var high = data.high;
    var low = data.low;
    var forcast = new data.forcastlst;

    document.getElementById("outsidetemp").innerHTML = outsidetemp + '&#8457;';
    document.getElementById("realfeel").innerHTML = 'Feels Like ' + feels_like + '&#8457;';
    document.getElementById("icon").src = icon;
    document.getElementById("high").innerHTML = high;
    document.getElementById("low").innerHTML = low;
    document.getElementById("avgtemp").innerHTML = avgtemp + '&#8457;';


    for (var days of forcast) {
        var row = document.getElementById('row');
        var cell1 = row.insertCell(-1);
        var fcast = days.day + "<img src = " + days.icon + ">" + days.max + days.min;
        cell1.innerHTML = fcast;
} 
    }) 
    datarefresh();
}