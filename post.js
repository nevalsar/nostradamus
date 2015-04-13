
function functionName(data) {
	console.log(JSON.stringify(data, null, "\t"));
	console.log(data[0]["pid"]);
	alert("done");
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
  },
  //work with the response
  success: function(data) {
    console.log(data); //formatted JSON data
	alert ("received");
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
