feather.replace();
const json = {
    1: {
        "machine": "Etiqueteuse",
        "standard": "Selettes",
        "Valeurs": {
            "isio41l": "Cyan",
            "isio42l": "Magenta"
        },
        "Instruction": "Situé à la base des bouteilles dans les machines.",
        "photo": "Aucune"
    },
    2: {
        "machine": "Etiqueteuse",
        "standard": "Selettes",
        "Valeurs": {
            "isio41l": "Cyan",
            "isio42l": "Magenta"
        },
        "Instruction": "Situé à la base des bouteilles dans les machines.",
        "photo": "Aucune"
    },
    3: {
        "machine": "Etiqueteuse",
        "standard": "Selettes",
        "Valeurs": {
            "isio41l": "Cyan",
            "isio42l": "Magenta"
        },
        "Instruction": "Situé à la base des bouteilles dans les machines.",
        "photo": "Aucune"
    }
};

function DynamicContent() {
    return React.createElement(
        React.Fragment,
        null,
        Object.entries(json).map(([key, item]) =>
            React.createElement("div", { key, className: "standardform-item" },
                React.createElement("div", { className: "leftside" },
                    React.createElement("p", null, `${item.machine} - ${item.standard}`),
                    React.createElement("div", {className: "wtht-img"}, "Pas de photo renseignée"),
                    React.createElement("div", { className: "comment" }, "Ajouter un commentaire")
                ),
                React.createElement("div", { className: "rightside" },
                    React.createElement("div", { className: "form-format" },
                        React.createElement("p", null, "Format:"),
                        React.createElement("select", { name: "format", className: "formatSelect" },
                            Object.keys(item.Valeurs).map((valKey) =>
                                React.createElement("option", { key: valKey, value: valKey }, valKey)
                            )
                        )
                    ),
                    React.createElement("div", { className: "form-valeur" },
                        React.createElement("p", null, "Valeur:"),
                        React.createElement("p", { className: "valeur" }, Object.values(item.Valeurs)[0])
                    ),
                    React.createElement("i", { className: "form-indication" }, item.Instruction),
                    React.createElement("div", { className: "form-conformite" },
                        React.createElement("div", { className: "conforme conformite-active" },
                            React.createElement("p", null, "Conforme"),
                            React.createElement("div", { className: "conformite-radio" })
                        ),
                        React.createElement("div", { className: "non-conforme" },
                            React.createElement("p", null, "Non Conforme"),
                            React.createElement("div", { className: "conformite-radio" })
                        ),
                        React.createElement("div", { className: "non-verifiable" },
                            React.createElement("p", null, "Non vérifiable"),
                            React.createElement("div", { className: "conformite-radio" })
                        )
                    )
                )
            )
        )
    );
}

const container = document.querySelector(".standardform-list");
document.addEventListener("DOMContentLoaded", function () {
    if (container) {
        ReactDOM.render(React.createElement(DynamicContent), container);
    }
});


$(document).on('click', '.conformite-radio', function(){
    console.log($(this).parent().parent().find('.conformite-radio'));
    $(this).parent().parent().find('.conformite-radio').parent().removeClass('conformite-active')
    $(this).parent().addClass('conformite-active')
})


$(document).on('change', '.formatSelect', function(e){
    const indexValeur = $(this).prop("selectedIndex")
    const indexform = $(this).parent().parent().parent().index();
    
    console.log(indexValeur, indexform);
    console.log();
    
    
    $(this).parent().parent().find('.valeur').html(Object.values(json[indexform+1]['Valeurs'])[indexValeur])
})

$(document).on('click', '.comment', function(){
    $('.fenetre-commentaire').css({
        "opacity": "1",
        "pointer-events": "all"
    })
    $('main').css({
        "filter": "brightness(0.5)"
    })
})

$(document).on('click', '.close', function(){
    $('.fenetre-commentaire').css({
        "opacity": "0",
        "pointer-events": "none"
    })
    $('main').css({
        "filter": "brightness(1)"
    })
})


$(document).on('click', '.valider-commentaire', function(){
    $('.fenetre-commentaire').css({
        "opacity": "0",
        "pointer-events": "none"
    })
    $('main').css({
        "filter": "brightness(1)"
    })
})