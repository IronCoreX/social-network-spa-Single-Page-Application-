// Attach to window so HTML 'onclick' can see it
window.edit_post = function(id) {
    const contentDiv = document.querySelector(`#content-${id}`);
    const originalContent = contentDiv.innerText;

    contentDiv.innerHTML = `
        <textarea id="textarea-${id}" class="form-control">${originalContent}</textarea>
        <button class="btn btn-success btn-sm mt-2" onclick="save_post(${id})">Save</button>
    `;
}

window.save_post = function(id) {
    const newContent = document.querySelector(`#textarea-${id}`).value;

    fetch(`/edit/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: newContent
        })
    })
    .then(response => {
        if (response.ok) {
            document.querySelector(`#content-${id}`).innerHTML = newContent;
        }
    });
}

window.toggle_like = function(id) {
    fetch(`/like/${id}`, {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        // Update the heart icon
        const btn = document.querySelector(`#like-btn-${id}`);
        btn.innerHTML = data.liked ? "❤️" : "🤍";
        
        // Update the count number
        document.querySelector(`#like-count-${id}`).innerHTML = data.count;
    });
}