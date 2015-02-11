function call() {
    $('#cityResults').empty();
    cl.show();
    searchNews();
};

function searchNews() {
    var msg = $('#cityForm').serialize();
    $.ajax({
	type: 'POST',
        url: '/ajax/ajax_news_by_city/',
        async: true,
        data: msg,
        dataType: "json",
        success: gotPost,
        error:  function(){
    	    $('#cityResults').append("<div class='bs-callout bs-callout-warning'><p allign='center'>Я устал, я больше найти не могу, попробуйте позже</p></div>");
    	    $('#id_startFrom').val('0');
    	    cl.hide();
    	}
    });    
};

function gotPost (data) {
    printNews(data)
    searchNews()
};


function printNews(data) {
    $.each(data[0].news, function(i,data)
    {
	var results_text = "<div class='bs-callout bs-callout-info news-text' name='" + data.user_id + "'>";
	results_text += "<div class='thumbnail author'>";
	results_text += "<img src=" + data.photo_link + " />";
	results_text += "<p class='time'>" + data.news_time + "</p>"
	results_text += "<p class='spam'><label><input type='checkbox' name='spammers' onclick='collectSpammers()'  value='" + data.user_id + "'> спам?</label></p>";
	results_text += "</div><div>";
	results_text +=  "<a href='" + data.news_link + "' target='_blank'>" + data.news_text + "</a>";
	results_text += "</div></div>";
	$(results_text).hide().appendTo('#cityResults').fadeIn(1000);
    });
	
$('#id_startFrom').val(data[1].next_from);
};
          
          
$('#id_cityText').autocomplete({    
    source: function( request, response ) {
    $.ajax({
	type: 'POST',
    	url: '/ajax/citysearch/',
    	dataType: "json",
    	data: $('#cityForm').serialize(),
    	success: function(data) {
    	    response($.map(data, function(item) {
    		return {
    		    label: item.city,
    		    value: item.city,
    		    key: item.cid
    		};
    	    }));
    	}
    });
    }, 
    minLength: 2,
    select: function(event, ui) {
	$('#id_cityID').val(ui.item.key);
    }
});

var areSpammers = new Array();
     
function collectSpammers() {
    areSpammers = [];
    $.each($("input[name='spammers']:checked"), function() {
	    areSpammers.push($(this).val());
    })
    if (areSpammers.length > 0) {
        document.getElementById('hideSpam').style.display = 'block'
	document.getElementById('eraseSpam').style.display = 'none';
    }
    else  {
        document.getElementById('hideSpam').style.display = 'none'
    }
};


function hideSpamF() {
    areSpammers=GetUnique(areSpammers);
    for (var i=0,  tot=areSpammers.length; i < tot; i++) {
	    var spamElements=document.getElementsByName(areSpammers[i]);
	    for (var n=0, len=spamElements.length; n < len; n++) {
	        spamElements[n].style.display = 'none';
	    };
    };
    document.getElementById('hideSpam').style.display = 'none';
    document.getElementById('eraseSpam').style.display = 'block';
};


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}


function eraseSpamF() {
    document.getElementById('eraseSpam').style.display = 'none';
    var jAreSpammers = JSON.stringify(areSpammers);

    $.ajaxSetup({
	crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
    	    if (!csrfSafeMethod(settings.type)) {
        	xhr.setRequestHeader("X-CSRFToken", token);
            }
        }
    });    
    
    $.ajax({
	type: 'POST',
	url: '/ajax/erasespam/',
	async: false,
	data: {'spammers': areSpammers},
	dataType: "html",
	success: myEraseResult,
	error: myEraseError,
    });
};


function myEraseResult(data) {
    $('#divEraseSpamResult').html("");
    document.getElementById('divEraseSpamResult').style.display = 'block';
    var hintText = "<p class='hint bg-success'>" + $.trim(data) + "</p>"
    $(hintText).hide().appendTo('#divEraseSpamResult').fadeIn(1000);
    $('#divEraseSpamResult').fadeOut(10000);
};

function myEraseError(data) {
    $('#divEraseSpamResult').html("");
    document.getElementById('divEraseSpamResult').style.display = 'block';
    var hintText="<p class='hint bg-danger'> Кажется, что-то пошло не так. Перелогиньтесь и попробуйте еще раз</p>";
    $('hintText').hide().appendTo('#divEraseSpamResult').fadeIn(1000);
    $('#divEraseSpamResult').fadeOut(10000);
};

function GetUnique(inputArray) {
    var outputArray = [];
    for (var i = 0; i < inputArray.length; i++) {
        if ((jQuery.inArray(inputArray[i], outputArray)) == -1) {
            outputArray.push(inputArray[i]);
        }
    }
   return outputArray;
};