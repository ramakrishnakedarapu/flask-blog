$("form[name=signup_form").submit(function(e) {

    e.preventDefault(); // prevent form submit (we are doing this for ajax request)

    var $form = $(this);
    var $error =  $form.find(".error");
    var data = $form.serialize();

    $.ajax({
        url:"/user/signup",
        type: "POST",
        data : data,
        success: function(resp){
            console.log(resp);
        },
        error: function(resp){
            console.log(resp)
        }
    })
});