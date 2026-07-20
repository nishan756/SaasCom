function openDeleteModal(appName, deleteUrl) {

        document.getElementById('deleteAppName').innerText = appName;
        

        document.getElementById('deleteAppForm').action = deleteUrl;
        

        var myModal = new bootstrap.Modal(document.getElementById('deleteConfirmModal'));
        myModal.show();
    }