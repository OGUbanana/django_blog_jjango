document.addEventListener('DOMContentLoaded', function() {
    var writeForm = document.querySelector('#write-form');
    
    if (writeForm) {
        var autoButton = writeForm.querySelector('.auto');
        
        if (autoButton) {
            autoButton.addEventListener('click', function(event) {
                event.preventDefault();
                
                var formData = new FormData(writeForm);
                formData.append("csrfmiddlewaretoken", document.querySelector('[name=csrfmiddlewaretoken]').value);
                
                fetch('/write/', {
                    method: 'POST',
                    body: formData,
                    headers: {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
                })
                .then(function(response) {
                    if (!response.ok) {throw new Error('Network response was not ok');}
                    return response.json();
                })
                .then(function(data) {
                    // CKEditor 인스턴스 가져오기
                    var editorInstanceName = 'id_post_content';
                    
                    // 자동완성 결과를 CKEditor 입력 부분에 출력
                    if (CKEDITOR.instances[editorInstanceName]) {
                        CKEDITOR.instances[editorInstanceName].setData(data.completion);
                    }
                })
                .catch(function(error) {console.error(error);});
            });
        }
    }
});