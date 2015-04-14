
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
    results.sort(function(a,b) { return parseFloat(b["avg_score"]) - parseFloat(a["avg_score"]) } );
    console.log(JSON.stringify(results, null, "\t"));
     console.log(data["results"][0]["pid"]);
    var i=0;
    // var categories = [];
    var categories = new StringSet();
    $("#result-container").html("");
    for(i=0; i<results.length; i++) {
        categories.add(results[i]["category"]);
        var str = '\
                  <a data-toggle="modal" data-target="#'+results[i]["pid"]+'" href="#">\
                  <div class="row">\
                  <div class="col-sm-12 well clear-well result-item">\
                  <div class="row">\
                  <div class="col-sm-3">\
                  <img src="'+results[i]["img_src"]+'" alt="result-image">\
                  </div>\
                  <div class="col-sm-9">\
                  <blockquote>\
                  <h4>'+results[i]["name"]+'</h4>\
                  <div class="rating-box">'+results[i]["avg_score"]+'</div>\
                  <strong><p>'+results[i]["category"]+'</p></strong>\
                  <p> '+results[i]["description"]+'</p>\
                  </blockquote>\
                  </div>\
                  </div>\
                  </div>\
                  </div>\
                  </a>\
                  ';
        $("#result-container").append(str);
        var str = '\
                  <div class="modal fade" id="'+results[i]["pid"] +'" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
                  <div class="modal-dialog">\
                  <div class="modal-content">\
                  <div class="modal-header text-center">\
                  <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>\
                  <h4 class="modal-title" id="myModalLabel">Product Details</h4>\
                  </div>\
                  <div class="modal-body">\
                  <div class="row">\
                  <div class="col-sm-3">\
                  <img src="'+results[i]["img_src"]+'" class="img img-responsive img-rounded" alt="result-image">\
                  </div>\
                  <div class="col-sm-9">\
                  <blockquote>\
                  <h1>'+results[i]["name"]+'</h1>\
                  <a href="#">Go to official website</a><br>\
                  <div class="rating-box">'+results[i]["avg_score"]+'</div>\
                  <strong><p>'+results[i]["category"]+'</p></strong>\
                  <p> '+results[i]["description"]+'</p>\
                  </blockquote>\
                  </div>\
                  </div>\
                  <hr>\
                  <div class="row text-center">\
                  <div class="col-sm-12">\
                  <h2>Reviews</h2>\
                  </div>\
                  </div>\
                  <br>\
                  <div class="row">\
                  <div id="review-container" class="col-sm-12">\
                  <div class="row">\
                  <div class="col-sm-10 col-sm-offset-1 review-item well clear-well">\
                  <blockquote>\
                  <h4>Review title</h4>\
                  <small>username</small>\
                  <div class="rating-box">5</div>\
                  <br>\
                  <br>\
                  <i><p id="review-text"> This is the review text</p></i>\
                  </blockquote>\
                  </div>\
                  </div>\
                  </div>\
                  </div>\
                  </div>\
                  <div class="modal-footer">\
                  </div>\
                  </div>\
                  </div>\
                  </div>';
        $("#modals").append(str);
    }
    //console.log(categories.values());
    var cat = categories.values();
    for(i=0; i<cat.length; i++) {
        str='\
            <label class="btn btn-default filter-option">\
            <input type="checkbox" name="options" autocomplete="off" class="check_box"> '+ cat[i] +'\
            </label>\
            '
            $("#filter-options-container").append(str);
        }
}

$(".check_box").change(function whenClick(){
    alert ("clicked");
//    selected = ('.filter-option activ > inpute');
    //thing = $('.filter-option > input');
//    $(selected).each(function (e) {
  //      console.log(e.text());
   // })
});


function get_selected_list() {
    $("#filter-options-container")

}

function getdata(term) {
    //alert(term);
    $.ajax({
        //JSONP API
        url: "http://10.139.243.107:8888/cgi-bin/GetSearchResults.py?query="+term,
    //the name of the callback function
    jsonp: functionName,
    //tell jQuery to expect JSONP
    dataType: "jsonp"
    //tell YQL what we want and that we want JSON
        });
}

// Attach a submit handler to the form
$( "#top_form" ).submit(function( event ) {
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
getdata(term);
// var posting = $.post( url, { s: term } );
// Put the results in a div
// posting.done(function( data ) {
//    var content = $( data ).find( "#content" );
//    $( "#result" ).empty().append( content );
//});
});
