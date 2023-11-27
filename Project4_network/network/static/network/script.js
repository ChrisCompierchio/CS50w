function edit(post_id, onProfile){

    post_text = document.getElementById(`post-textt${post_id}`).innerHTML;

    document.getElementById(`${post_id}`).innerHTML = `
        <textarea name="new-text" id="new-text" placeholder="Edit Post" style="width: 400px; height: 300px;"> ${post_text} </textarea>
        <br/>
        <input type="button" name="make-edit" id="make-edit" value="Confirm">
    `;

    document.querySelector("#make-edit").addEventListener('click', function(){
        fetch(`/posts/${post_id}`)
        .then(response => response.json())
        .then(post => {
            fetch(`/posts/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    text: document.querySelector("#new-text").value
                })
            })

            document.getElementById(`${post_id}`).innerHTML = `
                <a id = edit${post.id}><h2 id="author">${ post.author }</h2></a>
                <br/>
                <br/>
                <p id="post-textt">${ document.querySelector("#new-text").value }</p>
                <br/>
                <p id="time">${ post.timestamp }</p>
                <br/>
                <p id=likes${post.id}>Likes: ${ post.likes }</p>
                <br/>
                <br/>
                <button name="edit" id="edit" class="${ post.id }" onclick="edit(${ post.id })">Edit</button>
            `;

            if (onProfile == false){
                document.getElementById(`edit${post.id}`).href = `profile/${ post.author }`
            }


        });
    })
}

function likeControl(post_id, currentLiker){

    if (document.querySelector(`#like-button${post_id}`).innerHTML === "Like"){

        fetch(`/posts/${post_id}`)
        .then(response => response.json())
        .then(post => {
            fetch(`/posts/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likes: post.likes + 1
                })
            })

            fetch(`/newLike/${post_id}`)
            .then(response => response.json)
            .then(result => {
                document.querySelector(`#likes${post_id}`).innerHTML = `Likes: ${post.likes + 1}`;
                document.querySelector(`#like-button${post_id}`).innerHTML = "Unlike";
            })
        });
    }
    else{
        fetch(`/posts/${post_id}`)
        .then(response => response.json())
        .then(post => {
            fetch(`/posts/${post_id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    likes: post.likes - 1
                })
            })

            fetch(`/unlike/${post_id}`)
            .then(response => response.json)
            .then(result => {
                document.querySelector(`#likes${post_id}`).innerHTML = `Likes: ${post.likes - 1}`;
                document.querySelector(`#like-button${post_id}`).innerHTML = "Like";
            })

        })
    }

}

function follow(clickedUserId){
    if (document.querySelector("#follow")){
        if (document.querySelector("#follow").innerHTML == "Follow"){
            fetch(`/newFollow/${clickedUserId}`)
            .then(response => response.json)
            .then(result => {
                document.querySelector(`#numFollowers`).innerHTML = parseInt(document.querySelector(`#numFollowers`).innerHTML) + 1;
                document.querySelector(`#follow`).innerHTML = "Unfollow";
            })
        }
        else{
            fetch(`/deleteFollow/${clickedUserId}`)
            .then(response => response.json)
            .then(result => {
                document.querySelector(`#numFollowers`).innerHTML = parseInt(document.querySelector(`#numFollowers`).innerHTML) - 1;
                document.querySelector(`#follow`).innerHTML = "Follow";
            })
        }
    }

}
