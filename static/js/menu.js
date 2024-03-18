// document.addEventListener('DOMContentLoaded', function() {
//     // Get the current path or URL of the page
//     var currentPath = window.location.pathname;

//     // Highlight the active menu item based on the current page
//     var activeMenuItem = document.querySelector('#menu-items li a[href="' + currentPath + '"]');
//     if (activeMenuItem) {
//         activeMenuItem.parentNode.classList.add('active');
//     }
// });


// // For the USers axpansion & Collapsed behaviours 
// document.addEventListener('DOMContentLoaded', function() {
//     const usersMenuItem = document.getElementById('users');
//     const submenu = usersMenuItem.querySelector('.submenu');

//     usersMenuItem.addEventListener('click', function(event) {
//         event.preventDefault(); // Prevent the default behavior of the anchor tag
//         submenu.classList.toggle('expanded');
//     });

//     // Prevent collapsing the submenu when clicking on its items
//     submenu.addEventListener('click', function(event) {
//         event.stopPropagation(); // Prevent the event from bubbling up to the parent
//     });
// });


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
