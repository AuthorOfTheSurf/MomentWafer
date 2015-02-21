//
// Allows a video file to be specified and attached
// to a <video> element as a source
//
(function (window) {
    var URL = window.URL || window.webkitURL
    var inputNode = $('input')

    var playSelectedFile = function(event) {
        var file = this.files[0]
        var type = file.type

        var fileURL = URL.createObjectURL(file)
        $("#video").attr("src", fileURL)
    }

    inputNode.on('change', playSelectedFile)
}(window));