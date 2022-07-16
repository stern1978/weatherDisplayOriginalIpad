function display_c(){
    var refresh=1000; // Refresh rate in milli seconds
    mytime=setTimeout('display_ct()',refresh);
    }

function display_ct() {
    var now = new Date();
    var date = now.getMonth() + 1 + "/" + now.getDate() + "/" + now.getFullYear();
    var ampm = now.getHours() >= 12 ? ' pm' : ' am';
    hours = now.getHours() % 12;
    hours = hours ? hours : 12;
    minutes = now.getMinutes();
    minutes = minutes.length==1 ? 0+minutes : minutes;
    if(minutes < 10) {minutes  = '0' + minutes;}
    seconds = now.getSeconds();
    var time = hours + ":" + minutes;
    document.getElementById('time').innerHTML = time;
    display_c();
     }

function loaddata(){
    display_ct();
    data();
}