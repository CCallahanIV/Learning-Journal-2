$(document).ready(function(){
    $("#submitButton").on("click", function(e){
        e.preventDefault()
        entry = $(this).parent().serializeArray()
        console.log(entry)
        $.ajax({
            method: 'POST',
            url: '/journal/new-entry',
            data: {
                "csrf_token": entry[0]["value"],
                "title": entry[1]["value"],
                "body": entry[2]["value"]
            }, 
            success: function(result){
                console.log($(".entryListItem a").first().attr('href').split('/')[4])
                $(".entryListItem").first().prepend(
                    "<li class='entryListItem'>" +
                    "<h3><a href=" +  + ">{{ entry.title }}</a></h3>" +
                    "<p class='date'>Created {{ entry.creation_date }}</p>" +
                    "<hr />" +
                    "</li>"
                )
            }
        });        
    });
});
