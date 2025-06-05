
feather.replace();
const csrftoken = document.querySelector('meta[name="csrf-token"]').content;

$.each($('td.valeur'), function (indexInArray, valueOfElement) { 
    $(this).find('div').css('display', "none")
    $(this).find('div').eq(0).css('display', "block")
});

$(document).ready(function () {
    tl = gsap.timeline()
    $('tr').each(function(index, element) {
        gsap.to($(element), {x: 0, opacity: 1, duration: 0.1, delay: 0.02*index+0.2, ease: 'ease-in-out'});
    });
});


$('.ajouter-standard').on('click', function(){
    $('.ajout-standard').css('display', 'flex')
    $('main').addClass('inactive');
    $('aside').addClass('inactive');
    gsap.to('.ajout-standard', {
        opacity: 1,
        duration: 0.2,
        ease: 'ease-in-out'
    })
    gsap.to('.ajout-standard-fenetre', {
        y: 0,
        duration: 0.2,
        ease: 'ease-in-out'
    })
})

$('.ajouter-machine').on('click', function(){
    
    $('.ajout-machine').css({
        'display': 'block',
        'top': $('.ajouter-machine').offset().top - $('.ajout-machine').height() - 15 + "px",
        'left' : $('.ajouter-machine').offset().left
    })
    gsap.to('.ajout-machine', {
        opacity: 1,
        y: 0,
        duration: 0.2,
        ease: 'ease-in-out'
    })
})

$('.ajouter-ligne').on('click', function(){
    
    $('.ajout-ligne').css({
        'display': 'block',
        'top': $('.ajouter-ligne').offset().top - $('.ajout-ligne').height() - 15 + "px",
        'left' : $('.ajouter-ligne').offset().left
    })
    gsap.to('.ajout-ligne', {
        opacity: 1,
        y: 0,
        duration: 0.2,
        ease: 'ease-in-out'
    })
})

function fermerFenetreAjoutStandard(){
    $('main').removeClass('inactive');
    $('aside').removeClass('inactive');
    gsap.to('.ajout-standard', {
        opacity: 0,
        duration: 0.2,
        ease: 'ease-in-out'
    })
    gsap.to('.ajout-standard-fenetre', {
        y: 10,
        duration: 0.2,
        ease: 'ease-in-out'
    })
    setTimeout(function(){
        $('.ajout-standard').css('display', 'none')
    }, 300)
}

function fermerAjoutLigne(){
    gsap.to('.ajout-ligne', {
        opacity: 0,
        y: 5,
        duration: 0.2,
        ease: 'ease-in-out'
    })
    setTimeout(function(){
        $('.ajout-ligne').css('display', 'none')
    }, 300)
}

function fermerAjoutMachine(){
    gsap.to('.ajout-machine', {
        opacity: 0,
        y: 5,
        duration: 0.2,
        ease: 'ease-in-out'
    })
    setTimeout(function(){
        $('.ajout-machine').css('display', 'none')
    }, 300)
}

$('.ajout-standard-fermer').on('click', function(){
    fermerFenetreAjoutStandard()
})

$('.ajout-ligne-fermer').on('click', function(){
    fermerAjoutLigne()
})

$('.ajout-machine-fermer').on('click', function(){
    fermerAjoutMachine()
})

$(window).click(function() {
    fermerFenetreAjoutStandard()
    fermerAjoutLigne()
    fermerAjoutMachine()
});

$('.ajout-standard-fenetre, .ajout-ligne, .ajout-machine, .ajouter-standard, .ajouter-ligne, .ajouter-machine').click(function(event){
    if ($(event.target).attr('class') != "validation-ajout-standard-bouton" || $(event.target).attr('class') != "validation-ajout-ligne-bouton" || $(event.target).attr('class') != "validation-ajout-machine-bouton") {
        event.stopPropagation();
    }
});

$('.format-designation-add').on('click', function(){
    $('<div class="format-designation"><input type="text" placeholder="Désignation" class="format-designation-input"></div>').insertBefore('.format-designation-add')
    $('.format-valeurs').append('<div class="format-valeur"><input type="text" placeholder="Valeur" class="format-valeur-input"></div>')
})

// Détecte l'upload de l'image pour l'ajout de standard
$('.ajout-standard-image-upload').on('change', function(e){ 
    console.log($(this).val());
})

$(document).on('click', '.validation-ajout-standard-bouton', function(){
    console.log("test");
    
    ligne = $('.ajout-standard-ligne-select').val()
    machine = $('.ajout-standard-vmachine-select').val()
    repere = $('.ajout-standard-repere-input').val()
    designation = $('.ajout-standard-designation-input').val()
    unite = $('.ajout-standard-unite-input').val()
    // mettre le code pour récup les données de l'image jsplus comment on fait
    photo = $('.ajout-standard-image-upload').val()

    formats = {}
    $('.format-designation-input').each(function (indexInArray, valueOfElement) { 
        console.log($(this).val(), $('.format-valeur-input').eq(indexInArray).val());
        
         formats[$(this).val()] = $('.format-valeur-input').eq(indexInArray).val()
    });

    var userData = {
        "ligne": ligne,
        "machine": machine,
        "repere": repere,
        "designation": designation,
        "unite": unite,
        "formats": formats,
        "photo": photo
    };

    console.log(userData);
    
    // $.ajax({
    //     type: "POST",
    //     url: "/standards",
    //     data: JSON.stringify(userData),
    //     contentType: "application/json",
    //     dataType: 'json',
    //     // On envoie le token en header pour que la requête soit validée
    //     beforeSend: function(xhr) {
    //         xhr.setRequestHeader("X-CSRFToken", csrftoken); // Ajoute CSRF dans le header
    //     },
    //     success: function(response) {
    //         if(response.success){
    //             window.location.href = response.redirect_url;
    //         } else {
    //             alert(response.message)
    //         }
    //     }
    // });
})

$(document).on('click', '.validation-ajout-ligne-bouton', function(){
    ligne = $('.ajout-ligne input').val()

    dataUser = {
        'ligne' : ligne
    }
})

$(document).on('click', '.validation-ajout-machine-bouton', function(){
    machine = $('.ajout-machine input').val()

    dataUser = {
        'machine' : machine
    }
})

vuePage = 1
standardsParPage = 30
nombreDeStandard = $('tr').length 
nombreDePage = Math.ceil(nombreDeStandard/standardsParPage)
console.log(vuePage, standardsParPage, nombreDeStandard, nombreDePage);

function updateStandardVue() {
    if(vuePage == 1){
        $('.standard-vue svg.feather-chevron-left').css({
            'opacity': '0',
            'pointer-events' : 'none'
        })
        $('.standard-vue svg.feather-chevron-right').css({
            'opacity': '1',
            'pointer-events' : 'all'
        })
    }else if(vuePage == nombreDePage){
        $('.standard-vue svg.feather-chevron-left').css({
            'opacity': '1',
            'pointer-events' : 'all'
        })
        $('.standard-vue svg.feather-chevron-right').css({
            'opacity': '0',
            'pointer-events' : 'none'
        })
    }
    $('.standard-vue p').text("Page " + vuePage + " sur " + nombreDePage)
}

updateStandardVue()

$('.standard-vue svg.feather-chevron-left').on('click', function(){
    if(vuePage == 1){
        return
    }else{
        vuePage--
        updateStandardVue()
    }
})

$('.standard-vue svg.feather-chevron-right').on('click', function(){
    if(vuePage == nombreDePage){
        return
    }else{
        vuePage++
        updateStandardVue()
    }
})

var data = {"fonction":"filtre_standard","recherche": "a","filtre_ligne": "GE","page": 1};
$.ajax({
    csrftoken : csrftoken,
    type: "POST",
    url: "/standards",
    data: JSON.stringify(data),
    beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken); // Ajoute CSRF dans le header
    },
    success: function (response) {
        console.log(response);
        
        $.each(response['lignes'], function (indexInArray, valueOfElement) { 
            ligne = valueOfElement
            console.log(ligne);
            $.each(ligne['machines'], function (indexInArray, valueOfElement) { 
                machine = valueOfElement
                console.log(machine);
                $.each(machine['standards'], function (indexInArray, valueOfElement) { 
                    standard = valueOfElement
                    console.log(standard);
                    tableLigne = '<tr style="opacity: 0; transform: translateX(-5px);"><td>' + machine['designation']
                    tableLigne += '</td><td>' + ligne['num_ligne'] + '</td><td>' + standard['rep']
                    tableLigne += '</td><td>' + standard['designation'] + '</td><td>'
                    if(standard['formats'].length == 0){
                        tableLigne += '<i style="opacity: 0.8;">Aucun format renseigné</i>'
                    }else if(standard['formats'].length == 1){
                        tableLigne += '<div>' + standard['formats']['0']['nom'] + '</div>'
                    }else{
                        tableLigne += '<select name="format" class="format-input">'
                        $.each(standard['formats'], function (indexInArray, valueOfElement) { 
                            format = valueOfElement
                            tableLigne += '<option value="' + format['nom'] + '">' + format['nom'] + '</option>'
                        });
                        tableLigne += '</select>'
                    }
                    tableLigne += '</td><td>'
                    $.each(standard['formats'], function (indexInArray, valueOfElement) { 
                        format = valueOfElement
                        tableLigne += '<div>' + format['valeur_attendue'] + '</div>'
                    });
                    tableLigne += '</td><td>' + standard['photo']['url'] + '</td></tr>'
                    $('table').append(tableLigne)
                    $('tr').each(function(index, element) {
                        gsap.to($(element), {x: 0, opacity: 1, duration: 0.1, delay: 0.02*index+0.2, ease: 'ease-in-out'});
                    });
                });
            });
        });
    }
});