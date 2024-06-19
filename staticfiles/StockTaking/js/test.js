// document.getElementById('rr').addEventListener('click', function() {
//     console.log("ky");
// });

var requestType = 'computers';

$('#rr').on('click', function() {
    // Получение значений полей ввода
    console.log('aa');
    var flRamValue = $('#ramsInput').val().match(/\d+/);
    var flVideoRamValue = $('#videoMemoryInput').val().match(/\d+/);
    var ramValue = parseFloat(flRamValue) * 1024.0;
    var coresValue = parseInt($('#coresInput').val());
    var withVideocard = $('#videocardCheckbox').is(":checked");
    var osValue = $('#osInput').val();
    console.log($('#softwaresInput').val());
    var softwares = $('#softwaresInput').val();
    var computers = parseInt($('#computersInput').val());
    var maxPlaces = parseInt($('#placesInput').val());
    var withProjector = $('#projectorCheckbox').is(":checked");
    var requestData = {};
    var videoMemoryValue = parseFloat(flVideoRamValue) * 1024.0;
    console.log(videoMemoryValue);
    //var freeMemoryValue = $('#freeMemoryInput').val();

    // Формирование тела запроса
    if (requestType == 'computers')
        requestData = {
            "ram": ramValue,
            "cores": coresValue,
            "with_videocard": withVideocard,
            "os_name": osValue,
            "softwares": softwares,
            "video_memory": videoMemoryValue,
            //"videoMemory": videoMemoryValue,
            //"freeMemory": freeMemoryValue
        };
    else if (requestType == 'audiences')
        requestData = {
            "max_computers": computers,
            "max_places": maxPlaces,
            "with_projector": withProjector,
        };

    console.log(requestData);
    var csrftoken = getCookie('csrftoken');
    var insertedElements = "";
    // Отправка AJAX-запроса
    $.ajax({
        type: "POST",
        url: `/api/analyze/?analizing_type=${requestType}`,
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        data: JSON.stringify(requestData),
        contentType: "application/json",
        success: function(response) {
            //console.log("good");
            // Обработка успешного ответа
            var result = response.result;
            // console.log(result.length);
            // Проходим по каждому элементу массива result
            // for (var key in result) {
                
            // }
            
            if (result != undefined) {
                //result.forEach(function(element) {
                for (var key in result) {
                    if (requestType == 'computers') {
                        insertedElements += `<div class="accordion accordion-flush" id="${key}">`;
                        insertedElements += `<div class="accordion-item">`;
                        insertedElements += `<h2 class="accordion-header" id="${key}-heading">`;
                        insertedElements += `<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-${key == 'Без аудитории' ? 'withoutAudience' : key}" aria-expanded="false" aria-controls="flush-${key == 'Без аудитории' ? 'withoutAudience' : key}">${key} ${result[key].count}/${result[key].total_count}</button>`;
                        insertedElements += `</h2><div id="flush-${key == 'Без аудитории' ? 'withoutAudience' : key}" class="accordion-collapse collapse" aria-labelledby="${key == 'Без аудитории' ? 'withoutAudience' : key}-heading" data-bs-parent="#${key == 'Без аудитории' ? 'withoutAudience' : key}"><div class="accordion-body">`;
                        
                        result[key].computers.forEach(function(computer) {
                            insertedElements += `<div><a href="/computer/${computer}/">${computer}</a></div>`;
                        });

                        insertedElements += `</div></div></div>`;
                    }
                    else if (requestType == 'audiences') {
                        insertedElements += `<div class="accordion accordion-flush" id="${key}">`;
                        insertedElements += `<div class="accordion-item">`;
                        insertedElements += `<h2 class="accordion-header" id="${key}-heading">`;
                        insertedElements += `<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#flush-${key}" aria-expanded="false" aria-controls="flush-${key}">Корпус ${key}</button>`;
                        insertedElements += `</h2><div id="flush-${key}" class="accordion-collapse collapse" aria-labelledby="${key}-heading" data-bs-parent="#${key}"><div class="accordion-body">`;
                        
                        result[key].audiences.forEach(function(audience) {
                            insertedElements += `<div><a href="/audience/${audience.id}/">${audience.name}</a></div>`;
                        });
                        
                        insertedElements += `</div></div></div>`;
                    }
                }
                insertedElements += `</div>`;
            }
            else
                insertedElements = "<div>Компьютеров с такими характеристиками не найдено</div>"
            //console.log(insertedElements);
            $('#result').html(insertedElements);
        },
        error: function(xhr, status, error) {
            // Обработка ошибки
            console.error(error);
        }
    });
});

function openFields(evt, settingName) {
    // Declare all variables
    if (settingName == 'Computers')
        requestType = 'computers'
    else if (settingName == 'Audiences')
        requestType = 'audiences'

    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = $(".tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = $(".nav-link");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the button that opened the tab
    document.getElementById(settingName).style.display = "block";
    evt.currentTarget.className += " active";
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}