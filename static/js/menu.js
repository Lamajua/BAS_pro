
document.addEventListener('DOMContentLoaded', function() {
    // Get the current path or URL of the page
    var currentPath = window.location.pathname;

    // Highlight the active menu item based on the current page
    var activeMenuItem = document.querySelector('#menu-items li a[href="' + currentPath + '"]');
    if (activeMenuItem) {
        activeMenuItem.parentNode.classList.add('active');
    }

    // For the Users expansion & collapsed behavior
    const usersMenuItem = document.getElementById('users');
    const submenu = usersMenuItem.querySelector('.submenu');

    // Check if the current path matches the Parents or Drivers page
    if (currentPath.includes("parents") || currentPath.includes("drivers")) {
        submenu.classList.add('expanded'); // Expand the submenu if on Parents or Drivers page
    }

    usersMenuItem.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default behavior of the anchor tag
        submenu.classList.toggle('expanded');
    });

    // Prevent collapsing the submenu when clicking on its items
    submenu.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent the event from bubbling up to the parent
    });
});




// -----------------------  Saving Profile Info To Firestore -----------------
// Function to save profile information to Firestore
function saveProfileInfoFirestore(name, role, schoolName, schoolAddress) {
    var user = firebase.auth().currentUser;
    var db = firebase.firestore();
    db.collection("school_managers").doc(user.uid).set({
        name: name,
        role: role,
        school_name: schoolName,
        school_address: schoolAddress
    })
    .then(() => {
        console.log("Profile information saved to Firestore");
    })
    .catch((error) => {
        console.error("Error saving profile information to Firestore: ", error);
    });
}

// Function to handle saving profile information
function saveProfile() {
    var name = document.getElementById('name').value;
    var role = document.getElementById('role').value;
    var schoolName = document.getElementById('schoolName').value;
    var schoolAddress = document.getElementById('schoolAddress').value;

    // Save profile information to Firestore
    saveProfileInfoFirestore(name, role, schoolName, schoolAddress);

    // Update profile information in the menu
    displayProfileInfo(name, role);

    // Close the profile modal
    closeProfileModal();
}





//-------------------- Saving & Retrieving Users' Profile Info -------------------
// Retrieve saved profile information from local storage
document.addEventListener('DOMContentLoaded', function() {
    var profileInfo = localStorage.getItem('profileInfo');
    if (profileInfo) {
        var parsedProfileInfo = JSON.parse(profileInfo);
        displayProfileInfo(parsedProfileInfo.name, parsedProfileInfo.role);
    }
});

// Function to display profile information in the menu
function displayProfileInfo(name, role) {
    var profileInfoElement = document.getElementById('profile-info');
    profileInfoElement.innerHTML = name + "<br><span style='font-size: smaller;'>" + role + "</span>";
}

// Function to save profile information to local storage
function saveProfileInfo(name, role) {
    var profileInfo = { name: name, role: role };
    localStorage.setItem('profileInfo', JSON.stringify(profileInfo));
}

// Function to open the profile modal
function openProfileModal() {
    var modal = document.getElementById('profile-modal');
    modal.style.display = 'block';
}

// Function to close the profile modal
function closeProfileModal() {
    var modal = document.getElementById('profile-modal');
    modal.style.display = 'none';
}

// Function to handle saving profile information
function saveProfile() {
    var name = document.getElementById('name').value;
    var role = document.getElementById('role').value;

    // Save profile information to local storage
    saveProfileInfo(name, role);

    // Update profile information in the menu
    displayProfileInfo(name, role);

    // Close the profile modal
    closeProfileModal();
}
