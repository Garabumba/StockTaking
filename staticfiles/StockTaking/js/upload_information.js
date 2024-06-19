function setupDropZone(dropZoneId, fileInputId, uploadBtnId, url, messageContainerId) {
    const dropZone = document.getElementById(dropZoneId);
    const fileInput = document.getElementById(fileInputId);
    const uploadBtn = document.getElementById(uploadBtnId);
    const messageContainer = document.getElementById(messageContainerId);

    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (e) => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        fileInput.files = e.dataTransfer.files;
        dropZone.textContent = fileInput.files[0].name;
    });

    dropZone.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            dropZone.textContent = fileInput.files[0].name;
        }
    });

    uploadBtn.addEventListener('click', () => {
        uploadFile(fileInput, url, messageContainer);
    });
}

function uploadFile(fileInput, url, messageContainer) {
    const file = fileInput.files[0];
    var csrftoken = getCookie('csrftoken');
    if (file) {
        const formData = new FormData();
        formData.append('file', file);

        $.ajax({
            url: url,
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            },
            type: 'PUT',
            data: formData,
            processData: false,
            contentType: false,
            success: function(data) {
                console.log(data);
                if (data.created.length > 0 && data.errors === undefined) {
                    showMessage(messageContainer, 'success', 'Файл успешно загружен.');
                } else if (data.created.length == 0 && data.errors === undefined) {
                    showMessage(messageContainer, 'success', 'Новых записей в файле не содержится');
                } else if (data.errors.length > 0 && data.created.length > 0) {
                    showMessage(messageContainer, 'warning', 'Загружено с ошибками', data);
                } else if (data.errors.length > 0 && data.created.length === 0) {
                    showMessage(messageContainer, 'error', 'Не удалось загрузить файл', data);
                }
                //console.log(`File uploaded successfully to ${url}`, data);
                //alert(`Файл успешно загружен на ${url}`);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.error(`Error uploading file to ${url}`, errorThrown);
                //alert(`Ошибка при загрузке файла на ${url}`);
            }
        });
    } else {
        //alert('Пожалуйста, выберите файл для загрузки.');
    }
}

function uploadAllFiles() {
    const vendorsFileInput = document.getElementById('file-input-vendors');
    const attachTechniqueFileInput = document.getElementById('file-input-attachTechnique');
    const usersFileInput = document.getElementById('file-input-users');

    uploadFile(vendorsFileInput, '/api/upload_vendors/');
    uploadFile(attachTechniqueFileInput, '/api/upload_users_technique/');
    uploadFile(usersFileInput, '/api/upload_groups/');
    uploadFile(usersFileInput, '/api/upload_audiences/');
}

//setupDropZone('drop-zone-vendors', 'file-input-vendors', 'upload-btn-vendors', '/api/upload_vendors/');
//setupDropZone('drop-zone-attachTechnique', 'file-input-attachTechnique', 'upload-btn-attachTechnique', '/api/upload_attachTechnique/');
//setupDropZone('drop-zone-users', 'file-input-users', 'upload-btn-users', '/api/upload_users/');

setupDropZone('drop-zone-vendors', 'file-input-vendors', 'upload-btn-vendors', '/api/upload_vendors/', 'message-vendors');
setupDropZone('drop-zone-attachTechnique', 'file-input-attachTechnique', 'upload-btn-attachTechnique', '/api/upload_attachTechnique/', 'message-attachTechnique');
setupDropZone('drop-zone-users', 'file-input-users', 'upload-btn-users', '/api/upload_users/', 'message-users');
setupDropZone('drop-zone-audiences', 'file-input-audiences', 'upload-btn-audiences', '/api/upload_audiences/', 'message-audiences');

document.getElementById('upload-all-btn').addEventListener('click', uploadAllFiles);

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

function showMessage(container, type, message, data = null) {
    container.innerHTML = '';
    //statusIcon.innerHTML = '';
    //statusIcon.className = '';

    const messageDiv = document.createElement('div');
    messageDiv.className = `alert alert-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'success'} alert-dismissible fade show`;
    messageDiv.role = 'alert';
    messageDiv.innerText = message;

    var infoButton = undefined;

    if (type != 'success') {
        infoButton = document.createElement('button');
        infoButton.type = 'button';
        infoButton.className = `btn btn-${type === 'error' ? 'danger' : type === 'warning' ? 'warning' : 'success'}`;
        infoButton.textContent = 'Подробнее';
        // infoButton.dataset.dismiss = 'alert';
        // infoButton.ariaLabel = 'Close';
        // infoButton.innerHTML = '<span aria-hidden="true">&times;</span>';
        messageDiv.appendChild(infoButton);
    }

    container.appendChild(messageDiv);

    if (type === 'error') {
        //statusIcon.innerHTML = '&#9888;';
        //statusIcon.className = 'status-icon error';
        console.log("i'm here");
        infoButton.addEventListener('click', () => {
           document.getElementById('error-modal-body').innerText = data.errors.join('\n');
           $('#errorModal').modal('show');
        });
    } else if (type === 'warning') {
        //statusIcon.innerHTML = '&#9888;';
        //statusIcon.className = 'status-icon warning';
        infoButton.addEventListener('click', () => {
           document.getElementById('error-modal-body').innerText = 'Загружено:\n' + data.created.join('\n') + '\n\nОшибки:\n' + data.errors.join('\n');
           $('#errorModal').modal('show');
        });
    }
}