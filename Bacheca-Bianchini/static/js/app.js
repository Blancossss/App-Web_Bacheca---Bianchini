async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/api/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.status === 200)
        location.href = "messages.html";
}


async function registerUser() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const res = await fetch("/api/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({email, password})
    });

    const data = await res.json();
    alert(data.message || data.error);

    if (res.status === 201)
        location.href = "login.html";
}


//va in messages.html
async function logout() {
    await fetch("/api/logout", {method: "POST"});
    location.href = "login.html";
}


async function loadMessages() {
    const res = await fetch("/api/messages");

    if (res.status !== 200) {
        location.href = "login.html";
        return;
    }

    const data = await res.json();
    const currentUser = data.current_user.email;

    const list = document.getElementById("messageList");
    list.innerHTML = "";

    data.items.forEach(t => {
        const li = document.createElement("li");

        // Testo
        const textSpan = document.createElement("span");
        textSpan.textContent = t.email+": "+t.text+" | "+t.time;

        // Area icone
        const actions = document.createElement("div");

        if (t.email === currentUser) {
        // 🗑 icona
        const del = document.createElement("button");
            del.className = "icon-btn";
            del.innerHTML = '<i class="fa-solid fa-trash" title="Elimina"></i>';
            del.onclick = () => deleteMessage(t.id);

            actions.appendChild(del);
        }
        li.appendChild(textSpan);
        li.appendChild(actions);
        list.appendChild(li);
    });
}


async function addMessage() {
    const text = document.getElementById("messageText").value;

    await fetch("/api/messages", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({text})
    });

    loadMessages();
}


async function updateMessage(id, done) {
    await fetch(`/api/messages/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({done})
    });

    loadMessages();
}


async function deleteMessage(id) {
    await fetch(`/api/messages/${id}/delete`, {method: "DELETE"});
    loadMessages();
}


if (location.pathname.endsWith("messages.html"))
    loadMessages();