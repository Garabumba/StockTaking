var url = window.location.href;
var sections = url.split('/');
let lastSection = sections.pop() || sections.pop();
var removedElements = [];

var canvas = new fabric.Canvas('canvas');

$.ajax({
    type: 'GET',
    url: `/api/get_audience_state/${lastSection}/`,
    success: function (data) {
        if (data.state != null) {
            canvas.loadFromJSON(data.state, function() {
                canvas.renderAll();
                if (data.photo != null)
                    if (canvas.backgroundImage == null) {
                        var imgElement = new Image();
                        imgElement.src = "/media/home/audiences/E325.png";//data.photo;
                        imgElement.onload = function() {
                            canvas.setBackgroundImage(imgElement.src, canvas.renderAll.bind(canvas), {
                                scaleX: 300.0 / imgElement.width,
                            scaleY: 150.0 / imgElement.height,
                            });
                        };
                    }
            },
            function(o, figure){
                figureController(figure, false);
                updateFigures(figure.figureId);
            })
        }
    }
});

var switchInput = document.getElementById('flexSwitchCheckDefault');

if (switchInput.checked) {
    $(".tools").css("display", "block");
    $(".t").css("display", "grid");
    const contentDiv = document.querySelector('#main');
    const resizeObserver = new ResizeObserver(() => {
        resizeCanvas();
    });
    resizeObserver.observe(contentDiv);
}
else {
    $(".tools").css("display", "none");
    $(".t").css("display", "block");
    const contentDiv = document.querySelector('#main');
    const resizeObserver = new ResizeObserver(() => {
        resizeCanvas();
    });
    resizeObserver.observe(contentDiv);
}

    
switchInput.addEventListener('change', function() {
    checked = this.checked;
    if (checked) {
        $(".tools").css("display", "block");
        $(".t").css("display", "grid");
        const contentDiv = document.querySelector('#main');
        const resizeObserver = new ResizeObserver(() => {
            resizeCanvas();
        });
        resizeObserver.observe(contentDiv);
    }
    else {
        $(".tools").css("display", "none");
        $(".t").css("display", "block");
        const contentDiv = document.querySelector('#main');
        const resizeObserver = new ResizeObserver(() => {
            resizeCanvas();
        });
        resizeObserver.observe(contentDiv);
    }

    canvas.discardActiveObject();
    canvas.requestRenderAll();
    canvas.forEachObject(function(obj) {  
        obj.__eventListeners["mousedown"] = [];
        figureController(obj, checked);
    });
});

function resizeCanvas() {
    const outerCanvasContainer = document.getElementById('stage-parent');
    const ratio          = canvas.getWidth() / canvas.getHeight();
    const containerWidth = outerCanvasContainer.offsetWidth - 30;
    const scale          = containerWidth / canvas.getWidth();
    const zoom           = canvas.getZoom() * scale;
    canvas.setDimensions({width: containerWidth, height: containerWidth / ratio});
    canvas.setViewportTransform([zoom, 0, 0, zoom, 0, 0]);
}

resizeCanvas();

window.addEventListener('resize', resizeCanvas);

const contentDiv = document.querySelector('#main');
const resizeObserver = new ResizeObserver(() => {
    resizeCanvas();
});

resizeObserver.observe(contentDiv);

document.getElementById('saveState').addEventListener(
    'click',
    function () {
        console.log(canvas);
        var json = JSON.stringify(canvas);
        console.log(json);
        audienceId = $("#saveState").attr('data-id');
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: `/api/change_audience_state/${audienceId}/`,
            type: 'PUT',
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            contentType: 'application/json',
            data: json,
            dataType: 'json',
        })
    },
    false
);

function sendNewRequest()
{
    const title = $('#titleInput').val();
    const message = $('#messageInput').val();
    const inventoryNumber = $('#sendButton').attr('data-id');
    const requestObject = {
        request: {
            title: title,
            message: message,
            inventory_number: inventoryNumber,
            users: []
        }
    };
    
    const json = JSON.stringify(requestObject);
    
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/api/create_request/',
        type: 'POST',
        beforeSend: function(xhr) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        contentType: 'application/json',
        data: json,
        dataType: 'json',
        success: function (data) {
            console.log('Данные успешно отправлены на сервер');
            $('.modal-body').html('Успешно создано');
        },
        error: function (xhr, status, error) {
            console.error('Ошибка при отправке данных на сервер:', error);
            $('.modal-body').html('Ошибка создания');
        }
    })
}

function testClick()
{
    const inventoryNumber = $('#createRequest').attr('data-id');
    const insert_elements = `
    <div class="form-group">
        <label for="titleInput">Заголовок</label>
        <input type="text" class="form-control" id="titleInput" maxlength="50">
    </div>
    <div class="form-group">
        <label for="messageInput">Сообщение</label>
        <textarea class="form-control" id="messageInput" rows="4" maxlength="255"></textarea>
    </div>
    <button type="button" class="btn btn-primary" id="sendButton" onclick="sendNewRequest()" data-id="${inventoryNumber}">Создать</button>
`;

    $('#exampleModalLabel').html(`Создание обращения`);

    $('.modal-body').html(insert_elements);
}

function figureController(figure, isEdit = true)
{
    figure.on('mouseover', function() {
        canvas.hoverCursor = 'pointer';
        canvas.renderAll();
    });
    if (!isEdit)
    {
        figure.selectable = false;
        figure.on('mousedown', function(e) {
            var url = "";
            url = `/api/get_technique_info/?inventory_number=${figure.figureId}`;
            $.ajax({
                type: 'GET',
                url: url,
                success: function (data) {
                    if (data != null) {
                        $('#exampleModalLabel').html(figure.figureId);
                        if (figure.techniqueId == 1) {
                            insert_elements = `<h1>Компьютер</h1><div><b>Имя компьютера: </b>${data.name}</div>`;
                            insert_elements += `<div><b>Инвентарный номер компьютера: </b>${data.inventory_number}</div>`;
                            insert_elements += `<div><b>Ядра: </b>${data.cpu.model.cores}</div>`;
                            insert_elements += `<div><b>Потоки: </b>${data.cpu.model.threads}</div>`;
                            insert_elements += `<div><b>Объём памяти: </b>${data.rams.reduce((sum, ram) => sum + ram.model.memory / 1024, 0)} ГБ</div>`;
                            insert_elements += `<div><b>Объём видеопамяти: </b>${data.videocards.reduce((sum, videocard) => sum + videocard.model.memory / 1024, 0)} ГБ</div>`;
                            insert_elements += `<div><b>Статус: </b>${data.status.name}</div>`;
                            insert_elements += `<button class="createReuqest btn btn-primary text-end" id="createRequest", data-id=${figure.figureId} onclick="testClick()">Создать обращение</button>`;
                        }
                        else if (figure.techniqueId == 2) {
                            insert_elements = `<h1>Проектор</h1><div><b>Имя проектора: </b>${data.name}</div>`;
                            insert_elements += `<div><b>Инвентарный номер проектора: </b>${data.inventory_number}</div>`;
                            insert_elements += `<button class="createReuqest btn btn-primary text-end" id="createRequest", data-id=${figure.figureId} onclick="testClick()">Создать обращение</button>`;
                        }
                        else if (figure.techniqueId == 3) {
                            insert_elements = `<h1>Принтер</h1><div><b>Имя принтера: </b>${data.name}</div>`;
                            insert_elements += `<div><b>Инвентарный номер принтера: </b>${data.inventory_number}</div>`;
                            insert_elements += `<button class="createReuqest btn btn-primary text-end" id="createRequest", data-id=${figure.figureId} onclick="testClick()">Создать обращение</button>`;
                        }
                        else if (figure.techniqueId == 4) {
                            insert_elements = `<h1>МФУ</h1><div><b>Имя МФУ: </b>${data.name}</div>`;
                            insert_elements += `<div><b>Инвентарный номер МФУ: </b>${data.inventory_number}</div>`;
                            insert_elements += `<button class="createReuqest btn btn-primary text-end" id="createRequest", data-id=${figure.figureId} onclick="testClick()">Создать обращение</button>`;
                        }
                        else if (figure.techniqueId == 5) {
                            insert_elements = `<h1>Телевизор</h1><div><b>Имя телевизора: </b>${data.name}</div>`;
                            insert_elements += `<div><b>Инвентарный номер телевизора: </b>${data.inventory_number}</div>`;
                            insert_elements += `<button class="createReuqest btn btn-primary text-end" id="createRequest", data-id=${figure.figureId} onclick="testClick()">Создать обращение</button>`;
                        }
                        $('.modal-body').html(insert_elements);
                        
                    }
                    else {
                        console.log("Беда");
                    }
                }
            });
            $('#exampleModal').modal('show');
        });
    }
    else
    {
        figure.selectable = true;
    }
}

function createNewFigure(id, typeId) {
    console.log(id);
    console.log(typeId);
    var statusId = 0;
    var url = "";
    url = `/api/get_technique_info/?inventory_number=${id}`;
    $.ajax({
        type: 'GET',
        url: url,
        success: function (data) {
            if (data != null) {
                console.log(data);
                statusId = data.status.id;
                techniqueId = data.technique_type_id;
                tt(id, statusId, techniqueId);
            }
            else {
                console.log("Беда");
            }
        }
    });
}

function tt(id, statusId, techniqueId) {
    var image = document.getElementById('my-image');
    console.log(techniqueId);
    console.log(statusId);

    if (techniqueId == 1 && statusId == 1)
        image = document.getElementById('my-image');
    else if (techniqueId == 1 && statusId == 2)
        image = document.getElementById('my-image2');
    else if (techniqueId == 2 && statusId == 1)
        image = document.getElementById('my-image3');
    else if (techniqueId == 2 && statusId == 2)
        image = document.getElementById('my-image4');
    else if (techniqueId == 3 && statusId == 1)
        image = document.getElementById('my-image5');
    else if (techniqueId == 3 && statusId == 2)
        image = document.getElementById('my-image6');
    else if (techniqueId == 4 && statusId == 1)
        image = document.getElementById('my-image7');
    else if (techniqueId == 4 && statusId == 2)
        image = document.getElementById('my-image8');
    else if (techniqueId == 5 && statusId == 1)
        image = document.getElementById('my-image9');
    else if (techniqueId == 5 && statusId == 2)
        image = document.getElementById('my-image10');

    var figure = new fabric.Image(image, {
        figureId: id,
        statusId: statusId,
        techniqueId: techniqueId
    });
    figure.scale(0.04);

    canvas.add(figure);
    
    updateFigures(id);
    figureController(figure);
}

$('.newComputer').click(function(){
    createNewFigure(this.id, $(this).attr('data-id'));
});

function updateFigures(id) {
    removedElements.push($(`#${id}`).parent());
    $(`#${id}`).parent().remove();
}

document.addEventListener('keydown', function (e) {
    if (e.keyCode === 46) {
        var ids = [];
        var array = [];
        
        if (canvas.getActiveObject()._objects != undefined)
            for (let i = 0; i < canvas.getActiveObject()._objects.length; i++)
            {
                ids.push(canvas.getActiveObject()._objects[i].figureId);
                canvas.remove(canvas.getActiveObject()._objects[i]);
            }
        else
        {
            ids.push(canvas.getActiveObject().figureId);
            canvas.remove(canvas.getActiveObject());
        }
        
        ids.forEach((id) => {
            removedElements.forEach((removedElement) => {
                if ($($(removedElement).children()[0]).attr('id') == id) {
                    array.push(removedElement);
                }
            })
        })
        
        array.forEach((el) => {
            var index = removedElements.indexOf(el);
            let id = $($(el).children()[0]).attr('id');
            let dataId = $($(el).children()[0]).attr('data-id');
            $(`#tech${dataId}`).append(removedElements[index]);
            removedElements.splice(index, 1);
            $(`#${id}`).click(function(){
                createNewFigure(id, $(this).attr('data-id'));
            });
        })
    }
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}