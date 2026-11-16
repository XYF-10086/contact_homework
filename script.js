let contactList = [];
let currentEditContactId = null;
let currentAddType = "";

const contactModal = document.getElementById("contactModal");
const addItemModal = document.getElementById("addItemModal");
const contactListEl = document.getElementById("contactList");
const showFavOnlyCheckbox = document.getElementById("showFavOnly");
const searchInput = document.getElementById("searchNameInput");
const itemModalTitle = document.getElementById("itemModalTitle");
const itemInputLabel = document.getElementById("itemInputLabel");
const newItemInput = document.getElementById("newItemInput");

// Open new contact popup
document.getElementById("addContactBtn").onclick = function () {
    contactModal.style.display = "flex";
    // 清空新建弹窗
    document.getElementById("contactName").value = "";
    document.getElementById("contactAddress").value = "";
    document.getElementById("initialPhone").value = "";
    document.getElementById("initialEmail").value = "";
    document.getElementById("initialQQ").value = "";
    currentEditContactId = null;
};
document.querySelector(".close").onclick = function () {
    contactModal.style.display = "none";
};
document.querySelector(".closeItem").onclick = function () {
    addItemModal.style.display = "none";
};

// Save new contact OR edit existing contact
document.getElementById("saveContactBtn").onclick = function () {
    const name = document.getElementById("contactName").value.trim();
    const address = document.getElementById("contactAddress").value.trim();
    const phone = document.getElementById("initialPhone").value.trim();
    const email = document.getElementById("initialEmail").value.trim();
    const qq = document.getElementById("initialQQ").value.trim();
    if (!name) return;

    if (currentEditContactId === null) {
        // 新建联系人
        const newContact = {
            id: Date.now(),
            name: name,
            addresses: address ? [address] : [],
            phones: phone ? [phone] : [],
            emails: email ? [email] : [],
            qqs: qq ? [qq] : [],
            favorite: false
        };
        contactList.push(newContact);
    } else {
        // 编辑已有联系人
        const target = contactList.find(c => c.id === currentEditContactId);
        if (target) {
            target.name = name;
            target.addresses = address ? [address] : [];
            target.phones = phone ? [phone] : [];
            target.emails = email ? [email] : [];
            target.qqs = qq ? [qq] : [];
        }
    }

    contactModal.style.display = "none";
    renderContactList();
};

// 打开编辑弹窗
function openEditContactModal(contactId) {
    const target = contactList.find(c => c.id === contactId);
    if (!target) return;
    currentEditContactId = contactId;
    // 把现有数据填充进弹窗
    document.getElementById("contactName").value = target.name;
    document.getElementById("contactAddress").value = target.addresses[0] || "";
    document.getElementById("initialPhone").value = target.phones[0] || "";
    document.getElementById("initialEmail").value = target.emails[0] || "";
    document.getElementById("initialQQ").value = target.qqs[0] || "";
    contactModal.style.display = "flex";
}

// Open add different type item modal
function openAddItemModal(contactId, type) {
    currentEditContactId = contactId;
    currentAddType = type;
    switch (type) {
        case "phone":
            itemModalTitle.innerText = "Add New Phone Number";
            itemInputLabel.innerText = "Phone Number";
            break;
        case "address":
            itemModalTitle.innerText = "Add New Address";
            itemInputLabel.innerText = "Address";
            break;
        case "email":
            itemModalTitle.innerText = "Add New Email";
            itemInputLabel.innerText = "Email";
            break;
        case "qq":
            itemModalTitle.innerText = "Add New QQ";
            itemInputLabel.innerText = "QQ";
            break;
    }
    newItemInput.value = "";
    addItemModal.style.display = "flex";
}

// Save new item
document.getElementById("saveItemBtn").onclick = function () {
    const val = newItemInput.value.trim();
    if (!val) return;
    const target = contactList.find(c => c.id === currentEditContactId);
    if (!target) return;
    switch (currentAddType) {
        case "phone": target.phones.push(val); break;
        case "address": target.addresses.push(val); break;
        case "email": target.emails.push(val); break;
        case "qq": target.qqs.push(val); break;
    }
    addItemModal.style.display = "none";
    renderContactList();
};

// Delete single item
function deleteItem(contactId, type, index) {
    const target = contactList.find(c => c.id === contactId);
    if (!target) return;
    switch (type) {
        case "phone": target.phones.splice(index, 1); break;
        case "address": target.addresses.splice(index, 1); break;
        case "email": target.emails.splice(index, 1); break;
        case "qq": target.qqs.splice(index, 1); break;
    }
    renderContactList();
}

// Delete whole contact
function deleteWholeContact(contactId) {
    contactList = contactList.filter(c => c.id !== contactId);
    renderContactList();
}

// Toggle SAVE favorite
function toggleFavorite(contactId) {
    const target = contactList.find(c => c.id === contactId);
    if (target) {
        target.favorite = !target.favorite;
        renderContactList();
    }
}

// Filter trigger
showFavOnlyCheckbox.onchange = renderContactList;
searchInput.oninput = renderContactList;

// Render cards
function renderContactList() {
    const showFavOnly = showFavOnlyCheckbox.checked;
    const keyword = searchInput.value.trim().toLowerCase();
    let displayList = [...contactList];

    if (showFavOnly) displayList = displayList.filter(item => item.favorite);
    if (keyword) displayList = displayList.filter(item => item.name.toLowerCase().includes(keyword));

    contactListEl.innerHTML = "";
    if (displayList.length === 0) {
        contactListEl.innerHTML = `<div class="empty-tip">No contacts yet, click "New Contact" to add.</div>`;
        return;
    }

    displayList.forEach(contact => {
        const card = document.createElement("div");
        card.className = "contact-card";

        let addrHtml = "";
        contact.addresses.forEach((item, idx) => {
            addrHtml += `<div class="info-item"><span>${item}</span><button class="info-del-btn" onclick="deleteItem(${contact.id},'address',${idx})">Delete</button></div>`;
        });
        let phoneHtml = "";
        contact.phones.forEach((item, idx) => {
            phoneHtml += `<div class="info-item"><span>${item}</span><button class="info-del-btn" onclick="deleteItem(${contact.id},'phone',${idx})">Delete</button></div>`;
        });
        let emailHtml = "";
        contact.emails.forEach((item, idx) => {
            emailHtml += `<div class="info-item"><span>${item}</span><button class="info-del-btn" onclick="deleteItem(${contact.id},'email',${idx})">Delete</button></div>`;
        });
        let qqHtml = "";
        contact.qqs.forEach((item, idx) => {
            qqHtml += `<div class="info-item"><span>${item}</span><button class="info-del-btn" onclick="deleteItem(${contact.id},'qq',${idx})">Delete</button></div>`;
        });

        card.innerHTML = `
            <div class="card-header">
                <h3>${contact.name}</h3>
                <div style="display:flex;gap:8px;">
                    <button onclick="openEditContactModal(${contact.id})">Edit</button>
                    <button class="save-toggle ${contact.favorite ? "active" : ""}" onclick="toggleFavorite(${contact.id})">FAVORITE</button>
                </div>
            </div>
            <div class="info-group">
                <div class="info-title">Address</div>
                ${addrHtml || "<div>No address</div>"}
            </div>
            <div class="info-group">
                <div class="info-title">Phone</div>
                ${phoneHtml || "<div>No phone</div>"}
            </div>
            <div class="info-group">
                <div class="info-title">Email</div>
                ${emailHtml || "<div>No email</div>"}
            </div>
            <div class="info-group">
                <div class="info-title">QQ</div>
                ${qqHtml || "<div>No QQ</div>"}
            </div>
            <div class="card-footer">
                <button class="add-phone-btn" onclick="openAddItemModal(${contact.id},'phone')">Add Phone</button>
                <button class="add-address-btn" onclick="openAddItemModal(${contact.id},'address')">Add Address</button>
                <button class="add-email-btn" onclick="openAddItemModal(${contact.id},'email')">Add Email</button>
                <button class="add-qq-btn" onclick="openAddItemModal(${contact.id},'qq')">Add QQ</button>
                <button class="del-contact-btn" onclick="deleteWholeContact(${contact.id})">Delete Contact</button>
            </div>
        `;
        contactListEl.appendChild(card);
    });
}