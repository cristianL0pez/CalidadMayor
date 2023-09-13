document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("dropdown-toggle");
    const dropdownMenu = document.getElementById("dropdown-menu");

    toggleButton.addEventListener("click", function() {
        dropdownMenu.classList.toggle("hidden");
    });
});