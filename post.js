var categories = [];
var results = [];
var sortsentiment = 0;
var order = 1;


function clickfilter(el)
{
	// alert(jQuery(el).attr('value'));
	if(jQuery(el).hasClass('active'))
	{
		categories.remove(jQuery(el).attr('value'));
	}
	else
	{
		categories.add(jQuery(el).attr('value'));
	}
	loadResults();
}

$("#sortbtn").click(function(){
    if(order==1)
    {
        order = -1;
        $("#sortbtn").html("Ascending");
    }
    else
    {
        order = 1;
        $("#sortbtn").html("Descending");
    }
    loadResults();
})
function StringSet() {
	var setObj = {}, val = {};

	this.add = function(str) {
		setObj[str] = val;
	};

	this.contains = function(str) {
		return setObj[str] === val;
	};

	this.remove = function(str) {
		delete setObj[str];
	};

	this.values = function() {
		var values = [];
		for (var i in setObj) {
			if (setObj[i] === val) {
				values.push(i);
			}
		}
		return values;
	};
}

function search_result_click(pid) {
    
    // console.log(elem);
    // alert(pid);
    request_data(pid);
   // generate_modal(pid);
}

function generatemodal(result) {
	$("#pname").html(result['name']);
	$("#plink").attr('href',result['link']);
	$("#pdesc").html(result['description']);
	if(result["rating"]!='-1.0') result["rating"] = result["rating"]+'/5';
	else result["rating"] = "N/A";
	$("#prating").html(result['rating']);
	$("#pimg").attr('src',result['imgsrc']);
	$("#pcateg").html(result['category']);
	var reviews = result['reviews'];
	for (var i = 0; i <reviews.length; i++) {
		var revstr = '<div id="review-container" class="col-sm-12">';
		revstr += '<div class="row">';
		revstr += '<div class="col-sm-10 col-sm-offset-1 review-item well clear-well">';
		revstr += '<blockquote>';	
		revstr += '<h4>'+reviews[i]['title']+'</h4>';
		revstr += '<small>'+reviews[i]['nick']+'</small>';
		revstr += '<div style="color:';
		if(reviews[i]['sentiment_score']<0) revstr+='red';
		else revstr += 'green';
		revstr += '"> SA Score:'+reviews[i]['sentiment_score']+'</div>';
		revstr += '<br>';
		revstr += '<p>Date: '+reviews[i]['date']+'</p>';
		revstr += '<i><p id="review-text">'+reviews[i]['text']+'</p></i>';
		revstr += '</blockquote>';
		revstr += '</div>';
		revstr += '</div>';
		revstr += '</div>';
		$("#previews").append(revstr);
	};
	
}

function request_data(pid) {
	// alert('Hola'+term);
	$.get( "http://10.139.243.107:8888/cgi-bin/GetProductDetails.py?pid="+pid, function( data ) {
		// alert('in');
	  	generate_modal(data);
	}, "jsonp" );
 //    $.ajax({
 //        //JSONP API
 //        url: "http://10.139.243.107:8888/cgi-bin/GetProductDetails.py?pid="+pid,
 //        //the name of the callback function
 //        //tell jQuery to expect JSONP
	//     dataType: "jsonp"
	// }).done(function(data, textStatus,jqXHR) {
	// //work on data
	// generate_modal(data);
	// });
}


function loadResults(){
	if(sortsentiment==1) results.sort(function(a,b) { return order*(parseFloat(b["avg_score"]) - parseFloat(a["avg_score"])) } );
	else results.sort(function(a,b) { return order*(parseFloat(b["solr_score"]) - parseFloat(a["solr_score"])) } );

	var i=0;
    // var categories = [];
    $("#result-container").html("");
    for(i=0; i<results.length; i++) {
    	if(categories.contains(results[i]["category"])!=true) continue;
    	var str = '\
    	<a onclick = "search_result_click(\''+results[i]["pid"]+'\')" data-toggle="modal" data-target="#modalpid" href="#">\
    	<div class="row">\
    	<div class="col-sm-12 well clear-well result-item">\
    	<div class="row">\
    	<div class="col-sm-3">\
    	<img src="'+results[i]["img_src"]+'" alt="result-image">\
    	</div>\
    	<div class="col-sm-9">\
    	<blockquote>\
    	<h4>'+results[i]["name"]+'</h4>\
    	<div style="color:black;"> Rating: '+results[i]["rating"]+'</div>\
    	<p style="font-size:15px; font-weight:500;"> '+results[i]["description"]+'</p>';
    	if(sortsentiment==1) str += '<div>Raw Score:'+results[i]["solr_score"]+', SA Score:'+results[i]["avg_senti"]+', Avg. Score:'+results[i]["avg_score"]+'</div>';
    	else str+= '<div>Score:'+results[i]["solr_score"]+'</div>';
    	str+= '<strong><p>'+results[i]["category"]+'</p></strong>\
    	</blockquote>\
    	</div>\
    	</div>\
    	</div>\
    	</div>\
    	</a>\
    	';
    	$("#result-container").append(str);
    }
    
}
function functionName(data) {
	// alert('hola');
	results = data ["results"];
	results.sort(function(a,b) { return order*(parseFloat(b["solr_score"]) - parseFloat(a["solr_score"])) } );
	// console.log(JSON.stringify(results, null, "\t"));
	// console.log(data["results"][0]["pid"]);
	var i=0;
    // var categories = [];
    categories = new StringSet();
    $("#result-container").html("");
    for(i=0; i<results.length; i++) {
    	results[i]["avg_score"] = Math.round(results[i]["avg_score"]*100)/100;
        var x = results[i]["avg_sentiment_score"];
        var mult = 1;
        if(x<0) mult = -1;
        x *= mult;
    	results[i]["avg_senti"] = mult* Math.round(x*100)/100;
    	results[i]["solr_score"] = Math.round(results[i]["solr_score"]*100)/100;
    	results[i]["category"] = results[i]["category"].replace('quot;','');
    	results[i]["category"] = results[i]["category"].replace('"','');
    	results[i]["category"] = results[i]["category"].replace('&','');
    	if(results[i]["rating"]!='-1.0') results[i]["rating"] = results[i]["rating"]+'/5';
    	else results[i]["rating"] = "N/A";
    	categories.add(results[i]["category"]);
    	// var str = '\
    	// <a onclick = "search_result_click(\''+results[i]["pid"]+'\')" data-toggle="modal" data-target="#modalpid" href="#">\
    	// <div class="row">\
    	// <div class="col-sm-12 well clear-well result-item">\
    	// <div class="row">\
    	// <div class="col-sm-3">\
    	// <img src="'+results[i]["img_src"]+'" alt="result-image">\
    	// </div>\
    	// <div class="col-sm-9">\
    	// <blockquote>\
    	// <h4>'+results[i]["name"]+'</h4>\
    	// <div style="color:black;"> Rating: '+results[i]["rating"]+'</div>\
    	// <p style="font-size:15px; font-weight:500;"> '+results[i]["description"]+'</p>\
    	// <div>Score:'+results[i]["solr_score"]+'</div>\
    	// <strong><p>'+results[i]["category"]+'</p></strong>\
    	// </blockquote>\
    	// </div>\
    	// </div>\
    	// </div>\
    	// </div>\
    	// </a>\
    	// ';
    	// $("#result-container").append(str);
    }
    //console.log(categories.values());
    var cat = categories.values();
    for(i=0; i<cat.length; i++) {
    	str='\
    	<label class="btn btn-default filter-option" value="'+cat[i]+'" onclick="clickfilter(this)">\
    	'+ cat[i] +'\
    	</label>\
    	'
    	$("#filter-options-container").append(str);
    }
    $('.filter-option').addClass('active');
    loadResults();
}

function getdata(term) {
	// alert('Hola'+term);
	$.get( "http://10.139.243.107:8888/cgi-bin/GetSearchResults.py?query="+term, function( data ) {
		// alert('out');
	  	// functionName(data);
	}, "jsonp" );
	
// 	$.ajax({
//         //JSONP API
//         url: "http://10.139.243.107:8888/cgi-bin/GetSearchResults.py?query="+term,
//     	//the name of the callback function
// 	    //tell jQuery to expect JSONP
// 	    dataType: "jsonp"
// 	}).done(function(data, textStatus,jqXHR) {
// 	//work on data
	
// });
}

// Attach a submit handler to the form
$("#top_form").submit(function( event ) {
    // Stop form from submitting normally
    event.preventDefault();
    // Get some values from elements on the page:
    var $form = $( this ),
    term = $form.find( "input[name='s']" ).val(),

    sa = $form.find( "input[name='sa']" ).val(),

    url = $form.attr( "action" );
    console.log(term);
    console.log(sa);
    // Send the data using post
    $("#result-container").html("<h2>Searching...</h2>");
    getdata(term);
	// var posting = $.post( url, { s: term } );
	// Put the results in a div
	// posting.done(function( data ) {
	//    var content = $( data ).find( "#content" );
	//    $( "#result" ).empty().append( content );
	//});
});
