(function (window) {
    var URL = window.URL || window.webkitURL;
    var inputNode = $('input');
    var $pop = Popcorn("#video");

    var playSelectedFile = function(event) {
        var file = this.files[0];
        console.log(file);
        var type = file.type;

        var fileURL = URL.createObjectURL(file);
        $("#video").attr("src", fileURL);
    };

    $("#play-button").on("click", function() {
        console.log($pop);
        console.log($pop.readyState());
        $pop.play();
    });

    if (!URL) {
        displayMessage('Your browser is not ' + '<a href="http://caniuse.com/bloburls">supported</a>!', true);
        return;
    }

    inputNode.on('change', playSelectedFile);
}(window));