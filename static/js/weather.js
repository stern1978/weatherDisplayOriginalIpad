fetch('http://192.168.1.200:8000/data')
    .then(function(response) {
		return response.json();
	})
	.then(function(data) {
		console.log(data);
		//var outsidetemp = data.outsidetemp;
		//var feels_like = data.feels_like;
		//var icon = data.icon;
		//var alerts = data.alerts;
		//var avgtemp = data.avgtemp;
		//var high = data.high;
		//var low = data.low;
		//var forcast = data.forcastlst;
		//var sunrise = data.sunrise;

		//document.getElementById("sunrise").innerHTML = sunrise;
		//document.getElementById("sunset").innerHTML = sunset;
		//document.getElementById("sunrisetomorrow").innerHTML = sunrisetomorrow;
		//document.getElementById("outsidetemp").innerHTML = outsidetemp + '&#8457;';
		//document.getElementById("realfeel").innerHTML = 'Feels Like ' + feels_like + '&#8457;';
		//document.getElementById("icon").src = icon;
		//document.getElementById("alerts").innerHTML = alerts;
		//document.getElementById("high").innerHTML = high;
		//document.getElementById("low").innerHTML = low;
		//document.getElementById("avgtemp").innerHTML = avgtemp + '&#8457;';
	});