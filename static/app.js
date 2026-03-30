function confirmDelete(itemType) {
    return confirm("Are you sure you want to delete this " + itemType + "?");
}

function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    sidebar.classList.toggle("open");
}

function openModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.classList.add("visible");
}

function closeModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.classList.remove("visible");
}

function setDepartmentName(selectElement) {
    var selected = selectElement.options[selectElement.selectedIndex];
    var nameField = document.getElementById("department_name");
    nameField.value = selected.getAttribute("data-name") || "";
}

function setLocationName(selectElement) {
    var selected = selectElement.options[selectElement.selectedIndex];
    var nameField = document.getElementById("location_name");
    nameField.value = selected.getAttribute("data-name") || "";
}

function setManagerName(selectElement) {
    var selected = selectElement.options[selectElement.selectedIndex];
    var nameField = document.getElementById("manager_name");
    nameField.value = selected.getAttribute("data-name") || "";
}

function openEditDepartment(deptId, name, description) {
    var form = document.getElementById("edit-department-form");
    form.action = "/departments/" + deptId + "/edit";
    document.getElementById("edit-dept-name").value = name;
    document.getElementById("edit-dept-description").value = description;
    openModal("edit-department-modal");
}

function openEditLocation(locId, name, address, city, state, country) {
    var form = document.getElementById("edit-location-form");
    form.action = "/locations/" + locId + "/edit";
    document.getElementById("edit-loc-name").value = name;
    document.getElementById("edit-loc-address").value = address;
    document.getElementById("edit-loc-city").value = city;
    document.getElementById("edit-loc-state").value = state;
    document.getElementById("edit-loc-country").value = country;
    openModal("edit-location-modal");
}

document.addEventListener("click", function (event) {
    var modals = document.querySelectorAll(".modal-overlay.visible");
    modals.forEach(function (modal) {
        if (event.target === modal) {
            modal.classList.remove("visible");
        }
    });
});

setTimeout(function () {
    var flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach(function (msg) {
        msg.style.opacity = "0";
        msg.style.transition = "opacity 0.5s ease";
        setTimeout(function () { msg.remove(); }, 500);
    });
}, 4000);
