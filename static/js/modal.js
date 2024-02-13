// function openUpdateModalStudents(name, phone_number, address, bus_number) {
//     document.getElementById('updateName').value = name;
//     document.getElementById('updatePhoneNumber').value = phone_number;
//     document.getElementById('updateAddress').value = address;
//     document.getElementById('updateBusNo').value = bus_number;
//     document.getElementById('updateModal').style.display = 'block';
// }


function openUpdateModalStudents(name, address, bus_number, student_id) {

    document.getElementById(`updateName-${student_id}`).value = name;
    document.getElementById(`updatePhoneNumber-${student_id}`).value = phone_number;
    document.getElementById(`updateAddress-${student_id}`).value = address;
    document.getElementById(`updateBusNo-${student_id}`).value = bus_number;
    document.getElementById(`updateModal-${student_id}`).style.display = 'block';
}

function openUpdateModalParents(name, phone_number, parent_id) {

    document.getElementById(`updateName-${parent_id}`).value = name;
    document.getElementById(`updatePhoneNumber-${parent_id}`).value = phone_number;
    document.getElementById(`updateModal-${parent_id}`).style.display = 'block';
}

function openUpdateModalDrivers(name, phone_number, licExpDt, bus_number, driver_id) {

    document.getElementById(`updateName-${driver_id}`).value = name;
    document.getElementById(`updatePhoneNumber-${driver_id}`).value = phone_number;
    document.getElementById(`updateLicExpDt-${driver_id}`).value = licExpDt;
    document.getElementById(`updateBusNo-${driver_id}`).value = bus_number;
    document.getElementById(`updateModal-${driver_id}`).style.display = 'block';
}

// function closeUpdateModal() {
//     document.getElementById('updateModal').style.display = 'none';
// }

function closeUpdateModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

