// Messages in Chat
function sendMessage(event, id){
    event.preventDefault()
    let body = $("#input_message").val()
    if(body == '' || urlMessageAjaxDisplay !== "/inbox/ajax-display"){
        return alert('no')
    }
    jqrx = $.ajax({
        url : urlMessageAjaxDisplay,
        type : 'POST',
        dataType :'json',
        data : {
            to_user : to_user,
            body : body,
        }
    })
    .done(function(result){
        if(result.status == false){
            alert('error')
        }
        else{
            $('#send-message')[0].reset()
            let newMessage = `<div class="send-message">
                              <img src="${result.imagen}">
                              <p>${result.body}</p>
                              </div>
                             ` 
            $(".messages-chat").prepend(newMessage)
 
        }
        
    })
}


//chat displyaed (lo comento porque es demasiado codigo innecesario)
// function chatDisplayed(id){
//     url = 'messanger?id=' + id;
//     $.ajax({
//         url: url,

//     })
//     .done(function(result){
//         //For de right side of the page (Chat)
//         $(".right-side-content").css('display', 'none')
//         $(".chat-inbox").css('display', '')

//         //for de displayed menu:
//         $(".background-displayed").css('display', 'none')

//         let x = result.messageFromChat
//         let userChatter = $("#user-chat").text()


//         for(let i = 0; x.length > i; ++i ){
            
//             if(x[i][0].users == result.to_user && userChatter != result.to_user ){
//                 let hisMessage = 
//                     `
//                     <div class="message-received">
//                         <strong id="from_user">${result.to_user}</strong>
//                         <p>${x[i][1].body}</p>
//                     </div>
//                     `
//                 if(x[i][0].users != $("#user-chat").text()){
//                     $(".messages-chat").empty()
//                     $(".messages-chat").append(hisMessage)
//                     $("#user-chat").text(result.to_user)
//                 }
//                 else{
//                     $(".messages-chat").append(hisMessage)
//                 }
//             }
//             else if(x[i][0].users == result.from_user && userChatter != result.to_user){

//                 let myMessage =
//                 `
//                 <div class="send-message">
//                         <strong id="from_user">${result.from_user}</strong>
//                         <p>${x[i][1].body}</p>
//                 </div>
//                 `
//                 if($("#user-chat").text() != result.to_user){
//                     $(".messages-chat").empty()
//                     $(".messages-chat").append(myMessage)
//                     $("#user-chat").text(result.to_user)
//                 }
//                 else{
//                     $(".messages-chat").append(myMessage)
//                 }
//             }
//         }
       
//     })
// }


function followOrUnfollow(action, id){
    $.ajax({
        type : 'POST',
        url : '/profile/' + id,
        dataType : 'json',
        data : {
            id : id,
            action : action
        }
    })
    .done(function(result){
        type = $(".profile-title").children("h2").text()
        if(type == result.user){
            $(".profile-followers").text(result.followers)
            $(".profile-title").children("button").remove();
            if(result.type == 'Follow'){
                let newButton = `<button onmouseover="changeBtn(true)" class="settings-btn-profile">Siguiendo</button>
                                 <button onmouseout="changeBtn(false)" class="unFollow-btn" onclick="followOrUnfollow('unFollow', '{{user.id}}')" style="display: none;">Dejar de Seguir</button> 
                                `
                                $(".profile-title").append(newButton)
            } else {
                let newButton = `<button class="follow-btn" onclick="followOrUnfollow('Follow', '${result.id}')">Seguir</button>`
                $(".profile-title").append(newButton)
            }
        }
        
    })
    .fail(function(){
        window.location.href = 'session-login'
    })

}

function savePost(el, id, type){
    $.ajax({
        url : ' /save-post',
        type : 'POST',
        dataType: 'JSON',
        data: {
            id : id,
            type: type
        }
    })
    .done(function(result){
        if (result.type == 'guardar'){
            let div = `<i class='bi bi-bookmark-fill logo-mini' onclick="savePost(this, ${result.id} , 'eliminar')"></i>`
            $(el).replaceWith(div)
        }
        else{
            let div = `<i class='bi bi-bookmark logo-mini' onclick="savePost(this, '${result.id}' , 'guardar')"></i>`
            $(el).replaceWith(div)
        }

    })
}

function likePost(el, id, type){
    $.ajax({
        url : ' /like-post',
        type : 'POST',
        dataType: 'JSON',
        data: {
            id : id,
            type: type
        }
    })
    .done(function(result){
        if (result.type == 'like'){
            let div = `<i class="bi bi-heart-fill logo-mini"  style="color: red;" onclick="likePost(this,'${result.id}', 'eliminar')"></i>`
            $(el).replaceWith(div)
        }
        else{
            let div = `<i class="bi bi-heart logo-mini" onclick="likePost(this,'${result.id}', 'like')"></i>`
            $(el).replaceWith(div)
        }

    })
}



// DESPLEGAR EL MENU 
function displayMenu(display){
    if(display == true){
        $(".drop-menu-messenger").css('display', '')    
    }
    else{
        $(".drop-menu-messenger").css('display', 'none')
    }
}


// DESPLEGAR HISTORIAS
function storyDisplay(id){
        $.ajax({
        url : ' /historyJson?id=' + id,
        type : 'GET'
    })
    .done(function(result){
        $(".story-displayed").empty()
        showStory = 
                `
                <div class="story-open-background">
                    <i class="bi bi-x-lg close-story" onclick="cerrar()"></i>
                    <div class="slideshow-container">
                        <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
                        <a class="next" onclick="plusSlides(1)">&#10095;</a>
                    </div>  
                </div>
                `
        $(".story-displayed").append(showStory)
            for(let x in result.historiesImg){
                histories = 
                `<div class="mySlides fade">
                    <div class="numbertext">
                    <img src="/static/images/meowed.png" style="width: 25px;">
                    <p style="font-size: 17px; color:white;">${result.historiesUser[0]}</p>  
                    <small style="color:white;">${result.historiesTimes[x]}</small>
                    </div>
                    <img src="/static${result.historiesImg[x]}" >
                    <div class="story-description-display">${result.historiesDes[x]}</div>
                </div>
                `
                $(".slideshow-container").prepend(histories)
            } 
        slideIndex = 1
        showSlides(slideIndex);
                      
    })
    }

    let slideIndex; 
function plusSlides(n) {
    showSlides(slideIndex += n);
}

function showSlides(n) {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}

  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}

function cerrar(){
    $('.story-open-background').css('display', 'none')
}

function postComment(id, type){
    let comment = $("#newComment" + id).val()
    $.ajax({
        url : ' /create-Comment',
        type : 'POST',
        datatype : 'json',
        data : {
            id : id,
            comment : comment,
            type : type,
        }
    })
    .done(function(result){
        if(result.status == 'mal')return window.location.href = 'profile/ session-login';

        if (type == 'redirect')return window.location.href = 'post/' + id;
        
        message = 
        `
        <div>
            <div style="display: flex; gap: 10px;">
                <img src="${result.avatar}">
                <p><strong>${result.host}</strong> ${result.comment}</p> 
            </div>
            <div style="cursor: pointer;">
                <p onclick="deleteComment(this, '${result.pk}')">✖</p>
            </div>
        </div>
        `
        $(".comments").append(message);
        $(".newComment").val('')
    })
}

function deleteComment(el, id){
    $.ajax({
        url : ' /delete-Comment?id=' + id,
        type : 'GET'
    })
    .done(function(result){
        $(el).parent().parent().fadeOut('slow')
    })
}