
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

function functionName(data) {
	var results = data ["results"];
	console.log(JSON.stringify(results, null, "\t"));
	// console.log(data["results"][0]["pid"]);
	var i=0;
	// var categories = [];
	var categories = new StringSet();
	for(i=0; i<results.length; i++) {
		categories.add(results[i]["category"]);
		var str = '          \
			  <a href="#">\
	            <div class="row">\
	              <div class="col-sm-12 well clear-well result-item">\
	                <div class="row">\
	                  <div class="col-sm-3">\
	                    <img src="./resources/1.jpg" class="img img-responsive img-rounded" alt="result-image">\
	                  </div>\
	                  <div class="col-sm-9">\
	                    <blockquote>\
	                      <h4>'+results[i]["name"]+'</h4>\
	                      <p> '+results[i]["description"]+'</p>\
	                      <p> Category: '+results[i]["category"]+'</p>\
	                    </blockquote>\
	                  </div>\
	                </div>\
	              </div>\
	            </div>\
	          </a>';
		$("#result-container").append(str);
	}
console.log(categories.values());
	var cat = categories.values();
	for(i=0; i<cat.length; i++) {
		str='\
               <label class="btn btn-default filter-option">\
                 <input type="checkbox" name="options" autocomplete="off"> '+ cat[i] +'\
               </label>\
		'
		$("#filter-options-container").append(str);

	}
	// $("#result-container").append(JSON.stringify(results, null, "\t"));
}

$.ajax({
  //JSONP API
  url: "http://10.139.243.107:8888/cgi-bin/GetSearchResults.py?query=aweg",
  //the name of the callback function
  jsonp: functionName,
  //tell jQuery to expect JSONP
  dataType: "jsonp",
  //tell YQL what we want and that we want JSON
  data: {
    query: ""
  }
});


// Attach a submit handler to the form
$( "#top_form" ).submit(function( event ) {
// Stop form from submitting normally
event.preventDefault();
// Get some values from elements on the page:
var $form = $( this ),
term = $form.find( "input[name='s']" ).val(),
url = $form.attr( "action" );
// Send the data using post
var posting = $.post( url, { s: term } );
// Put the results in a div
posting.done(function( data ) {
	var content = $( data ).find( "#content" );
	$( "#result" ).empty().append( content );
});
});
