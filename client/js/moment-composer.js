(function() {

// Knockout view model for MomentComposer
//
function MomentComposerViewModel() {
  var self = this;
  var $pop = Popcorn("#video");

  // Keep computed's up to date via refresh
  // seed: call inside computed
  // refresh: refresh all computed's that call seed
  //
  self.seed = ko.observable();
  self.refresh = function() {
    self.seed(Math.random());
  }

  // Play button
  //
  self.playButtonLabel = ko.computed(function() {
    self.seed();
    return $pop.paused() ? "Play" : "Pause";
  })
  self.playButtonClass = ko.computed(function() {
    self.seed();
    return $pop.paused() ? "button-primary" : "";
  })
  self.togglePlay = function() {
    if ($pop.paused()) {
      $pop.play();
      self.refresh();
    } else {
      $pop.pause();
      self.refresh();
    }
  }

  // Frame-by-frame
  //
  var FRAME_RATES = [24, 30, 60, 120]
  self.frameByFrameRates = ko.observableArray(FRAME_RATES);
  self.selectedFrameRate = ko.observable(FRAME_RATES[1]);
  self.frameStep = ko.computed(function() {
    return 1.0 / self.selectedFrameRate();
  });
  self.selectedFrameRate.subscribe(function(newValue) {
    console.log(newValue, self.frameStep());
  });
  self.previousFrame = function(n) {
    self.skipFrames(n, -self.frameStep());
  }
  self.nextFrame = function(n) {
    self.skipFrames(n, self.frameStep());
  }
  self.skipFrames = function(n, delta) {
    $pop.pause();
    self.refresh();
    var skips = isNaN(n) ? 1 : n;
    for (var i = skips; i > 0; i--) {
      $pop.currentTime($pop.currentTime() + delta);
    }
  }

  // Utils
  //
  self.printTime = function() {
    console.log($pop.currentTime());
  }

  // Database
  //
  $.couch.urlPrefix = "http://localhost:5984";
  var db = $.couch.db("mw-test");
  var doc = {text: "sup homie!"};
  self.saved = ko.observable();
  self.saved.subscribe(function (newValue) {
    db.openDoc(newValue.id, {
      success: function(data) {
          console.log("New message saved: '" + data.text + "'");
      },
      error: function(status) {
          console.log(status);
      }
    });
  });

  db.saveDoc(doc, {
      success: function(data) {
          self.saved(data);
      },
      error: function(status) {
          console.log("error");
      }
  });
}

// Apply view model to view
ko.applyBindings(new MomentComposerViewModel());

}());