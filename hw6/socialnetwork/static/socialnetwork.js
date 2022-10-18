function pageUpdate(xhr) {
    if (xhr.status === 200) {
        let response = JSON.parse(xhr.responseText)
        commentUpdate(response)
        return
    }
    if (xhr.status === 0) {
        errorMsg("Unable to connect")
        return
    }
    if (!xhr.getResponseHeader('content-type') === 'application/json') {
        errorMsg("Received status=" + xhr.status)
        return
    }
    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        errorMsg(response.error)
        return
    }
    errorMsg(response)
}

function errorMsg(message) {
    let errorElement = document.getElementsByClassName("error")
    errorElement.innerHTML = message
}

function commentUpdate(response) {
    // Removes the post items
    let posts = document.getElementById("post_list")
    console.log(posts)
    for (let i = 0;i<posts.children.length;i++) {
        let post = posts.children[i]
        let isPostDelete = true
        for(let j=0;j<response.length;j++) {
            if(post.id === "post_list_" + response[j].id) {
                isPostDelete = false
                break;
            }
        }
        if(isPostDelete) {
            posts.removeChild(post)
            continue
        }
        let comment = post.children[1];
        if(comment.id.startsWith("id_comment_input_div")) continue;
        for (let j =0;j<comment.children.length;j++) {

            let comment_id = comment.children[j].children[0].id
            let isDelete = true
            for(let k=0;k<response.length;k++) {
                let comments = response[k].comments
                for(let l=0;l< comments.length;l++) {
                    if(comment_id === ("id_comment_div_" + comments[l].id )) {
                        isDelete = false
                    }
                }
            }
            if(isDelete) comment.removeChild(comment.childNodes[j])
        }
    }
    // add new posts and new comments
    for(let i=response.length - 1;i>=0;i--) {

        let post = response[i];
        let element;
        let isExistPost = true
        element = document.getElementById("post_list_" + post.id)

        if(element == null) {
            isExistPost = false
            console.log(response[i].id, false)
            element = document.createElement("li")
            element.id = "post_list_" + post.id
            element.innerHTML = '<div id="id_post_div_'+post.id +'" class="post">' +
                "Post by" +
                '<a id="id_post_profile_' + post.id +'" href="personal_profile/' + post.author_id + '">' +
                post.first_name + " " + post.last_name +
                '</a>' +
                " - " +
                '<span id="id_post_text_' + post.id + '" class="text">' +
                post.texts +
                '</span> – <span id="id_post_date_time_' + post.id + '" class="time">' +
                dateFormat(post.date) +
                "</span></div>";
        }

        let isExistComments = true
        let comments = document.getElementById("comment_list_" + post.id)
        if(comments == null) {
            isExistComments = false
            comments = document.createElement("ul")
        }
        comments.id = "comment_list_" + post.id
        let tab = 0
        if(document.getElementById("tab_type").className === 'follower') {
            tab = 1
        }
        if(post.comments.length === 0) {
            if(isExistPost) continue
            element.innerHTML += '<div id="id_comment_input_div_' + post.id + '">' +
            '    <label for="item">New Comment:</label>' +
            '    <input id="id_comment_input_text_' + post.id + '" type="text" name="new_comment">' +
            '    <button id="id_comment_button_' + post.id + '" type="submit" onclick="addComment(' + post.id+ ',' + tab + ')">Submit</button>' +
            '    <span class="error"></span>' +
            '</div>';
            posts.insertBefore(element, posts.firstChild)
            continue
        }


        let temp = post.comments
        for(let j = temp.length-1;j>=0;j--) {
            let comment = temp[j]
            if(document.getElementById("id_comment_div_" + comment.id) != null) {
                continue
            }
            let comment_element = document.createElement("li")
            comment_element.innerHTML = '<div id="id_comment_div_' + comment.id+ '" class="comment">' +
            "Comment by" +
            '<a id="id_comment_profile_' + comment.id + '" href="personal_profile/' + comment.author_id + '">' +
            comment.comment_first_name + " " + comment.comment_last_name +
            '</a>' +
            " - " +
            '<span id="id_comment_text_' + comment.id + '" class="text">' +
            comment.texts +
            '</span> – <span id="id_comment_date_time_' + comment.id + '" class="time">' +
            dateFormat(comment.date) +
            "</span></div>"

            if(comments.firstChild != null) {
                comments.insertBefore(comment_element, comments.firstChild)
            } else {
                comments.appendChild(comment_element)
            }
        }
        if(!isExistComments) element.appendChild(comments)
        if(!isExistPost) {
            element.innerHTML += '<div id="id_comment_input_div_' + post.id + '">' +
            '    <label for="item">New Comment:</label>' +
            '    <input id="id_comment_input_text_' + post.id + '" type="text" name="new_comment">' +
            '    <button id="id_comment_button_' + post.id + '" type="submit" onclick="addComment(' + post.id + ',' + tab + ')">Submit</button>' +
            '    <span class="error"></span>' +
            '</div>';
            posts.insertBefore(element, posts.firstChild)
        }
        if(post.id === 9) {
            console.log(posts)
        }
    }
    console.log(posts)
}

function getGlobalComment() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) {
            return
        }
        pageUpdate(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-global", true)
    xhr.send()
}

function getFollowerComment() {
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (this.readyState !== 4) return
        pageUpdate(xhr)
    }

    xhr.open("GET", "/socialnetwork/get-follower", true)
    xhr.send()
}

function addComment(id, tab) {
    let itemTextElement = document.getElementById("id_comment_input_text_" + id)
    let itemTextValue   = itemTextElement.value

    itemTextElement.value = ''
    errorMsg('')

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState !== 4) return
        pageUpdate(xhr)
    }

    xhr.open("POST", addCommentURL, true)
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
    xhr.send("req_type=" + tab + "&post_id=" + id + "&comment_text=" + itemTextValue + "&csrfmiddlewaretoken="+CSRFToken())
}

function CSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()
        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}

function dateFormat(date){
    var now = new Date(date);
    var y = now.getFullYear();
    var m = now.getMonth();
    m = m + 1;
    var d = now.getDate();
    var h = now.getHours();
    var mm = now.getMinutes();
    var s = now.getSeconds();
    var str;
    if(h>12) {
        h -= 12;
        str = " PM";
    }else{
        str = " AM";
    }
    h = h < 10 ? "0" + h : h;
    d = d < 10 ? "0" + d : d;
    m = m < 10 ? "0" + m : m;
    mm = mm < 10 ? "0" + mm : mm;
    s = s < 10 ? "0" + s : s;
    var xy = m + "/" + d + "/" + y + " " + h + ":" + mm + " ";
    xy += str;
    return xy;
}