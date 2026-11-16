let contacts = [];
let showOnlyFavorite = false;

const contactListDom = document.getElementById("contactList");
const addModal = document.getElementById("addModal");
const addContactBtn = document.getElementById("addContactBtn");
const closeModal = document.querySelector(".close");
const saveBtn = document.getElementById("saveBtn");
const filterFavBtn = document.getElementById("filterFavBtn");

addContactBtn.onclick = () => {
    addModal.style.display = "block";
}
closeModal.onclick = () => {
    addModal.style.display = "none";
}

saveBtn.onclick = () => {
    const name = document.getElementById("nameInput").value;
    const phone = document.getElementById("phoneInput").value;
    const email = document.getElementById("emailInput").value;
    const addr = document.getElementById("addrInput").value;
    if (!name) {
        alert("Name cannot be empty");
        return;
    }
    contacts.push({
        name: name,
        phone: phone,
        email: email,
        addr: addr,
        isFavorite: false
    })
    renderList();
    addModal.style.display = "none";
    document.getElementById("nameInput").value = "";
    document.getElementById("phoneInput").value = "";
    document.getElementById("emailInput").value = "";
    document.getElementById("addrInput").value = "";
}

function renderList() {
    contactListDom.innerHTML = "";
    let list = showOnlyFavorite ? contacts.filter(c => c.isFavorite) : contacts;
    list.forEach((item, index) => {
        const div = document.createElement("div");
        div.className = "contact-item";
        div.innerHTML = `
            <div>
                <div>Name: ${item.name}</div>
                <div>Phone: ${item.phone}</div>
                <div>Email: ${item.email}</div>
                <div>Address: ${item.addr}</div>
            </div>
            <div class="star ${item.isFavorite ? 'favorite' : ''}" data-idx="${index}">[SAVE]</div>
        `
        contactListDom.appendChild(div);
    })
    document.querySelectorAll(".star").forEach(star => {
        star.onclick = function () {
            const idx = this.dataset.idx;
            contacts[idx].isFavorite = !contacts[idx].isFavorite;
            renderList();
        }
    })
}

filterFavBtn.onclick = function () {
    showOnlyFavorite = !showOnlyFavorite;
    this.innerText = showOnlyFavorite ? "Show All Contacts" : "Show Favorites Only";
    renderList();
}

renderList();