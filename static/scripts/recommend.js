document.addEventListener('DOMContentLoaded', function () {
    const infoContent = {
        'number': 'Please enter a positive number. This field requires a positive numeric value.',
        'dropdown': 'Please choose an option from the dropdown. Make sure to select the most appropriate one for your situation.',
        'number1': 'Isi yang beter atuh kang'
    };

    // Get all input elements
    const inputs = document.querySelectorAll('input[type="number"], select');

    // Attach focus and blur event listeners to each input
    inputs.forEach(function (input) {
        input.addEventListener('focus', function () {
            // Show the corresponding info div when focused
            const infoDiv = document.getElementById(input.id + '-info');
            if (infoDiv) {
                // Retrieve the content based on the input's ID
                const customContent = infoContent[input.id] || 'Please enter valid information.';
                infoDiv.innerHTML = customContent;

                infoDiv.style.display = 'block';
            }
        });

        input.addEventListener('blur', function () {
            // Hide the corresponding info div when focus is lost
            const infoDiv = document.getElementById(input.id + '-info');
            if (infoDiv) {
                infoDiv.style.display = 'none';
            }
        });
    });
});