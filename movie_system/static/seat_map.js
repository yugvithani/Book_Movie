// JavaScript code to handle seat selection

document.addEventListener("DOMContentLoaded", function() {
    // Get all seat elements
    var seats = document.querySelectorAll('.seat');

    // Add click event listener to each seat
    seats.forEach(function(seat) {
        seat.addEventListener('click', function() {
            // Toggle class based on current class
            if (seat.classList.contains('not_selected')) {
                seat.classList.remove('not_selected');
                seat.classList.add('selected');
            } else if (seat.classList.contains('selected')) {
                seat.classList.remove('selected');
                seat.classList.add('not_selected');
            }
        });
    });
});

function change(id){
    var ele=document.getElementById(id);
    if (ele.classList.contains('not_selected')) {
        ele.classList.remove('not_selected');
        ele.classList.add('selected');
    } else if (ele.classList.contains('selected')) {
        ele.classList.remove('selected');
        ele.classList.add('not_selected');
    }
}