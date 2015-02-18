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

// Knockout view model for MomentComposer
function MomentComposerViewModel() {
    var self = this
    var $pop = Popcorn("#video")
    // self.refresh() triggers computeds that call
    // self.forceEval() to refresh their values
    self.forceEval = ko.observable()
    self.refresh = function() {
        self.forceEval(Math.random())
    }

    self.playButtonLabel = ko.computed(function() {
        self.forceEval()
        return $pop.paused() ? "Play" : "Pause"
    })

    self.togglePlay = function() {
        if ($pop.paused()) {
            $pop.play()
            self.refresh()
        } else {
            $pop.pause()
            self.refresh()
        }
    }

    self.printTime = function() {
        console.log($pop.currentTime())
    }
}

// Apply view model to view
ko.applyBindings(new MomentComposerViewModel())