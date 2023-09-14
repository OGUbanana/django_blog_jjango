document.addEventListener('DOMContentLoaded', function() {
    var writeForm = document.querySelector('#write-form');
    
    if (writeForm) {
        
        // Create a new WebSocket connection when the page is loaded.
        var socket = new WebSocket('ws://' + window.location.host + '/write/');
        
        var autoButton = writeForm.querySelector('.auto');

        if (autoButton) {
            autoButton.addEventListener('click', function(event) {
                event.preventDefault();
                var postTitleElement = writeForm.querySelector('#id_post_title');
                var postTitle = postTitleElement ? postTitleElement.value : '';
                socket.send(JSON.stringify({post_title: postTitle}));
            });

            socket.onmessage = function(e) {
                var data = JSON.parse(e.data);
                console.log(data.content)
                var editorInstanceName = 'id_post_content';
                
                if (CKEDITOR.instances[editorInstanceName]) {
                    CKEDITOR.instances[editorInstanceName].insertText(data.content);
                }
            };
            
            socket.onclose= function(e){
              console.error('WebSocket closed unexpectedly');
           };
       }
   }
});