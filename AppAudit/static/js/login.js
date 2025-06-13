var tl = gsap.timeline()


function loginTry(){
    login = $('.identifiant').val()
    mdp = $('.motdepasse').val()
    csrftoken = $('input[name="csrfmiddlewaretoken"]').val()
    console.log(csrftoken)
    var userData = {"login" : login ,"mdp": mdp};
    $.ajax({
        type: "POST",
        url: "/",
        data: JSON.stringify(userData),
        contentType: "application/json",
        dataType: 'json',
        // On envoie le token en header pour que la requête soit validée
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken); // Ajoute CSRF dans le header
        },
        success: function(response,textStatus,jqXHR) {
            $('.loading svg').css({
                "animation" : "none"
            })
            $('.loading circle').css({
                "animation" : "none"
            })
            tl.to($('.loading'), {
                opacity: 0,
                ease: "power1.inOut",
                duration: 0.1
            })
            tl.to($('.connexion-bouton p'), {
                opacity: 1,
                ease: "power1.inOut",
                duration: 0.1
            })
            $('.connexion-bouton').attr("style","")
            $('.connexion-bouton p').attr("style","")

            if(response.success){
                window.location.href = response.redirect_url;
            } 
        },
        error: function(jqXHR){
            if(jqXHR.status === 429){
                alert("Votre compte est temporairement bloqué. Veuillez réessayer plus tard.");
            } else if(jqXHR.status === 401){
                alert("Identifiant et/ou mot de passe erroné(s).");
            } else {
                alert("Erreur serveur ou réseau. Veuillez réessayer.");
        }
        }
    });
    $('.loading svg').css({
        "animation" : "rotate4 2s linear infinite"
    })
    $('.loading circle').css({
        "animation" : "dash4 1.5s ease-in-out infinite"
    })
    gsap.to($('.connexion-bouton'), {
        backgroundColor: "#f4ede4",
        ease: "power1.inOut",
        duration: 0.1
    })
    tl.to($('.connexion-bouton p'), {
        color: "#42181a",
        ease: "power1.inOut",
        duration: 0.1
    })
    tl.to($('.connexion-bouton p'), {
        opacity: 0,
        ease: "power1.inOut",
        duration: 0.1
    })
    tl.to($('.loading'), {
        opacity: 1,
        ease: "power1.inOut",
        duration: 0.1
    })
}

$(document).on('click', '.connexion-bouton', function(){
    loginTry()
})

$(document).on("keydown", function(e){
    if(e.keyCode == 13){
        loginTry()
    }
})
