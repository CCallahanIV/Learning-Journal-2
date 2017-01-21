$(document).ready(function(){
    $("#homeSubmitButton").on("click", function(e){
        e.preventDefault()
        entry = $(this).parent().serializeArray()
        $.ajax({
            method: 'POST',
            url: '/journal/new-entry',
            data: {
                "csrf_token": entry[0]["value"],
                "title": entry[1]["value"],
                "body": entry[2]["value"]
            }, 
            success: function(result){
                new_id = parseInt($(".entryListItem a").first().attr('href').split('/')[4]) + 1
                $(".entryListItem").first().prepend(
                    "<li class='entryListItem'>" +
                    "<h3><a href=\"journal/" + new_id + "\">" + entry[1]["value"] + "</a></h3>" +
                    "<p class='date'>Created " + Date.now() + " </p>" +
                    "<hr />" +
                    "</li>"
                )
            }
        });        
    });
});
