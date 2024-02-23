var url = window.location.href;
var sections = url.split('/');
let lastSection = sections.pop() || sections.pop();
var removedElements = [];

var canvas = new fabric.Canvas('canvas');

$.ajax({
    type: 'GET',
    //contentType: 'application/json',
    url: `/audience/get_state/${lastSection}/`,
    success: function (data) {
        if (data != null) {
            canvas.loadFromJSON(data, function() {
                canvas.renderAll(); 
            },
            function(o, figure){
                console.log(figure.figureId)
                figureController(figure);
            })
        }
        else {
            var imgElement = document.getElementById('my-image');

            var imgInstance = new fabric.Image(imgElement, {
                figureId: 'test'
            });
            imgInstance.scale(0.035);

            var imgInstance2 = new fabric.Image(imgElement, {
                figureId: 'test2'
            });
            imgInstance2.scale(0.035);

            canvas.add(imgInstance);
            canvas.add(imgInstance2);
        }
    }
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

document.getElementById('saveState').addEventListener(
    'click',
    function () {
        console.log(canvas);
        var json = JSON.stringify(canvas);

        $.ajax({
            url: '/audience/change_state/',
            type: 'PUT',
            contentType: 'application/json',
            data: json,
            dataType: 'json',
            success: function (data) {
                console.log('Данные успешно отправлены на сервер');
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при отправке данных на сервер:', error);
            }
        })
        
        console.log(json);
    },
    false
);

function figureController(figure)
{
    figure.on('mouseover', function() {
        canvas.hoverCursor = 'pointer';
        canvas.renderAll();
    });
    figure.on('mousedown', function(e) {
        console.log(e.target.figureId);
    });
}

function createNewFigure(id) {
    var image = document.getElementById('my-image');

    var figure = new fabric.Image(image, {
        figureId: id
    });
    figure.scale(0.04);

    canvas.add(figure);
    console.log(canvas._objects);
    updateFigures(id);
    figureController(figure);
}

$('.newComputer').click(function(){
    createNewFigure(this.id);
});

function updateFigures(id) {
    removedElements.push($(`#${id}`).parent());
    console.log(id);
    //console.log(removedElements[0]);
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
            //console.log(id);
            //console.log($($(el).children()[0]).attr('id'));
            $('.audience').append(removedElements[index]);
            removedElements.splice(index, 1);
            $(`#${id}`).click(function(){
                createNewFigure(id);
            });
        })
    }
});