function openUpdateModalStudents(name, address, bus_number, student_id) {

    document.getElementById(`updateName-${student_id}`).value = name;
    document.getElementById(`updatePhoneNumber-${student_id}`).value = phone_number;
    document.getElementById(`updateAddress-${student_id}`).value = address;
    document.getElementById(`updateBusNo-${student_id}`).value = bus_number;
    document.getElementById(`updateModal-${student_id}`).style.display = 'block';
}


function openUpdateModalParents(name, address,parent_id ) {
    document.getElementById(`updateName-${parent_id}`).value = name;
    document.getElementById(`updateAddress-${parent_id}`).value = address;

    // Fetch the students for the parent
    fetch(`/get_students_by_parent_phone/${parent_id}`)
        .then(response => response.json())
        .then(data => {
            const studentList = document.getElementById(`studentList-${parent_id}`);
            studentList.innerHTML = '';

            data.forEach(student => {
                const listItem = document.createElement('li');
                listItem.textContent = `${student.name} - Bus No. ${student.bus_number}`;

                const editButton = document.createElement('button');
                editButton.textContent = 'Edit';
                editButton.onclick = () => openUpdateModalStudents(student.name, student.bus_number, student.id);
                listItem.appendChild(editButton);

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.onclick = () => deleteStudent(student.id);
                listItem.appendChild(deleteButton);

                studentList.appendChild(listItem);
            });
        });

    document.getElementById(`updateModal-${parent_id}`).style.display = 'block';
}



function openUpdateModalDrivers(name, phone_number, licExpDt, bus_number, driver_id) {

    document.getElementById(`updateName-${driver_id}`).value = name;
    document.getElementById(`updatePhoneNumber-${driver_id}`).value = phone_number;
    document.getElementById(`updateLicExpDt-${driver_id}`).value = licExpDt;
    document.getElementById(`updateBusNo-${driver_id}`).value = bus_number;
    document.getElementById(`updateModal-${driver_id}`).style.display = 'block';
}

function openUpdateModalBuses(number, district, bus_id) {
    document.getElementById(`updateNumber-${bus_id}`).value = number;
    document.getElementById(`updateDistrict-${bus_id}`).value = district;
    document.getElementById(`updateModal-${bus_id}`).style.display = 'block';
}


function closeUpdateModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

//TAKFA


//---------Edit Profile Modal----------
function openProfileModal() {
    var modal = document.getElementById('profile-modal');
    modal.style.display = 'block';
}

function closeProfileModal() {
    var modal = document.getElementById('profile-modal');
    modal.style.display = 'none';
}
