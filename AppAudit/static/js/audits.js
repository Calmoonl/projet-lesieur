feather.replace();

$(document).on('click', '.connexion-bouton', function(){
    /*
    machine = $('.machine').val()
    csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
    var userData = {"designation" : designation ,"valeur_attendue": valeur_attendue,"unite" : unite ,"machine": machine};
    $.ajax({
        type: "POST",
        url: "/standards",
        data: JSON.stringify(userData),
        contentType: "application/json",
        dataType: 'json',
        // On envoie le token en header pour que la requête soit validée
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken); // Ajoute CSRF dans le header
        },
        success: function(response) {
            if(response.success){
                window.location.href = response.redirect_url;
            } else {
                alert(response.message)
            }
        }
    });
    */
})
