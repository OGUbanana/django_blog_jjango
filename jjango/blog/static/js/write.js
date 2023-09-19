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
                var editorInstanceName = 'id_post_content';
                
                if (CKEDITOR.instances[editorInstanceName]) {
                    CKEDITOR.instances[editorInstanceName].insertText(data.content);
                }
            };
            
            socket.onclose= function(e){
              console.error('웹 소켓이 닫혔습니다');
           };
       }
   }
});


document.addEventListener('DOMContentLoaded', function() {
    var tempBtn = document.getElementById('temporary-btn');
    var maxContentLength = 160;
    var dateOptions = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };

    if (tempBtn) { 
        tempBtn.addEventListener('click', function() {
            fetch('/api/posts/unpublished/')
                .then(response => response.json())
                .then(data => {
                    for (let post of data) {
                        let date = new Date(post.post_created_at);
                        let formattedDate = new Intl.DateTimeFormat('ko-KR', dateOptions).format(date);
                        let ImgTags = post.post_content.replace(/<img[^>]*>/g, "");
                        let PTags = ImgTags.replace(/<\/?p[^>]*>/g, "");
                        let maxContent = PTags.length > maxContentLength ? PTags.substring(0, maxContentLength) + '...' : PTags;
                        let html = '';
                        html += '<div class="temp-post" data-id="' + post.post_id + '">';
                        html += '<p class="temp-title">' + post.post_title + '</p>';
                        html += '<p class="temp-content">' + maxContent + '</p>';
                        html += '<p class="temp-created">' + formattedDate + '</p>';
                        html += '</div>';
                        var modalBackground = document.getElementById('modal-background');
                        var popup = document.getElementById('temp-popup');

                        if (popup) {
                            modalBackground.style.display = 'block';
                            popup.insertAdjacentHTML('beforeend', html);
                            popup.style.display = 'flex';

                            var closeButton = document.getElementById('close-button');

                            if (closeButton) {
                                closeButton.addEventListener('click', function() {
                                    popup.style.display = 'none';
                                    modalBackground.style.display = 'none';
                                    var postsDivs = popup.querySelectorAll('.temp-post');
                                    for (let div of postsDivs) {
                                        div.remove();
                                    }
                                });
                            }

                            var postadd=popup.querySelectorAll('.temp-post:not(.event-added)');
                            
                            for(let div of postadd){
                                div.classList.add("event-added");
                                div.addEventListener("click",function(){
                                  let postId=this.getAttribute("data-id");
                                  let select=data.find(post=>post.post_id==postId);
                                  
                                  if(select){
                                      document.getElementById("id_post_title").value=select.post_title;
                                      CKEDITOR.instances.id_post_content.setData(select.post_content);

                                      let topic=document.querySelector(`input[name="post_topic"][value="${select.post_topic}"]`);
                                      
                                      if(topic)
                                          topic.checked=true;
                                  }
                              });
                          }
                      }
                  }
              });
          });
      }
});
