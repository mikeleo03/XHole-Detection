document.addEventListener('DOMContentLoaded', function () {
    const infoContent = {
        'rock': 'Please select the considered rock type!',
        'explosives': 'Please choose appropriate explosive you use.',
        'expdensity': 'Reference Value <br></br> ANFO : 0.8 - 0.85 gr/cc <br></br> TNT : 1.65 - 1.75 gr/cc',
        'detspeed': 'Reference Value <br></br> ANFO :  8202.5 - 14764.5 ft/s <br></br> TNT : > 22967 ft/s',
        'level': 'Input the high level in meter.',
        'rows': 'Input the number of rows in the blast hole',
        'stdevdrill': 'Input the standard deviation of drilling accuracy'
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