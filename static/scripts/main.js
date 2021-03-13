function showHideConfig() {
    var isShown = $('#overlay').is(':visible');

    if (isShown) {
        $('#overlay').css('display', 'none')
    } else {
        $('#overlay').css('display', 'block')
    }
}




$(document).ready(function() {
    $('#closeConfigButton').click(showHideConfig);
    $('#configButton').click(showHideConfig);
});