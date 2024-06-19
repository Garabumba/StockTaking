$(document).ready(function () {
    var deleteButtons = $('.btn-delete');
    var deleteComputerButtons = $('.btn-delete-computer');
    var modal = $('#deleteModal');
    var confirmDeleteButton = $('#confirmDelete');
    var confirmDeleteButtonComputer = $('#confirmDeleteComputer');
    var confirmDeleteButtonAll = $('#confirmDeleteAll');
    var modalBodyContent = $('#modalBodyContent');
    var cancelButton = $('#cancel');
    var cancelDeleteButton = $('#cancelDelete');
    var deleteRow = null;
    var deleteEndpoint = null;

    deleteButtons.each(function () {
        $(this).on('click', function () {
            deleteEndpoint = $(this).data('url');
            var objectName = $(this).data('id');
            deleteRow = $(this).closest('tr'); // or $(this).closest('.card') for mobile view
            deleteRowMobile = $(this).closest('.card');
            modalBodyContent.text(`Вы действительно хотите удалить "${objectName}"?`);
            confirmDeleteButton.show();
            cancelButton.text('Нет');
            modal.modal('show');
        });
    });

    deleteComputerButtons.each(function () {
        $(this).on('click', function () {
            var objectName = $(this).data('id');
            deleteEndpoint = $(this).data('url');
            deleteRow = $(this).closest('tr'); // or $(this).closest('.card') for mobile view
            deleteRowMobile = $(this).closest('.card');
            modalBodyContent.text(`Выберите вариант удаления:\nУдалить только компьютер - удалит компьютер, но все его комплектующие останутся в справочниках.\nУдалить всё - удалит компьютер вместе со всеми комплектующими.?`);
            confirmDeleteButton.hide();
            cancelButton.hide();
            confirmDeleteButtonComputer.show();
            confirmDeleteButtonAll.show();
            modal.modal('show');
        });
    });

    confirmDeleteButtonComputer.on('click', function () {
        if (deleteEndpoint) {
            $.ajax({
                url: deleteEndpoint + '?delete_related=false',
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function (response, status, xhr) {
                    if (xhr.status === 204) {
                        //modalBodyContent.text('Удаление прошло успешно');
                        modal.modal('hide');
                        deleteRow.remove();
                        deleteRowMobile.remove();
                    } else {
                        modalBodyContent.text('Неизвестная ошибка');
                    }
                    confirmDeleteButton.hide();
                    cancelButton.text('Закрыть');
                },
                error: function (xhr) {
                    if (xhr.status === 400) {
                        var errors = JSON.parse(xhr.responseText);
                        modalBodyContent.text(errors[0]);
                    } else {
                        modalBodyContent.text('Неизвестная ошибка');
                    }
                    confirmDeleteButton.hide();
                    cancelButton.text('Закрыть');
                }
            });
        }
    });

    confirmDeleteButtonAll.on('click', function () {
        if (deleteEndpoint) {
            $.ajax({
                url: deleteEndpoint + '?delete_related=true',
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function (response, status, xhr) {
                    if (xhr.status === 204) {
                        //modalBodyContent.text('Удаление прошло успешно');
                        modal.modal('hide');
                        deleteRow.remove();
                        deleteRowMobile.remove();
                    } else {
                        modalBodyContent.text('Неизвестная ошибка');
                    }
                    confirmDeleteButton.hide();
                    cancelButton.text('Закрыть');
                },
                error: function (xhr) {
                    if (xhr.status === 400) {
                        var errors = JSON.parse(xhr.responseText);
                        modalBodyContent.text(errors[0]);
                    } else {
                        modalBodyContent.text('Неизвестная ошибка');
                    }
                    confirmDeleteButton.hide();
                    cancelButton.text('Закрыть');
                }
            });
        }
    });

    confirmDeleteButton.on('click', function () {
        if (deleteEndpoint) {
            $.ajax({
                url: deleteEndpoint,
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                success: function (response, status, xhr) {
                    if (xhr.status === 204) {
                        //modalBodyContent.text('Удаление прошло успешно');
                        modal.modal('hide');
                        deleteRow.remove();
                        deleteRowMobile.remove();
                    } else {
                        modalBodyContent.text('Неизвестная ошибка');
                    }
                    confirmDeleteButton.hide();
                    cancelButton.text('Закрыть');
                },
                error: function (xhr) {
                    if (xhr.status === 400) {
                        var errors = JSON.parse(xhr.responseText);
                        modalBodyContent.text(errors[0]);
                    } else {
                        modalBodyContent.text('Неизвестная ошибка');
                    }
                    confirmDeleteButton.hide();
                    cancelButton.text('Закрыть');
                }
            });
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = $.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
