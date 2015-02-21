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
  self.selectedFrameRate = ko.observable();
  self.frameStep = ko.computed(function() {
    return 1.0 / self.selectedFrameRate();
  });
  self.selectedFrameRate.subscribe(function(newValue) {
    console.log(newValue, self.frameStep());
  });
  self.previousFrame = function() {
    $pop.pause();
    $pop.currentTime($pop.currentTime() - self.frameStep());
    self.refresh();
  }
   self.nextFrame = function() {
    $pop.pause();
    $pop.currentTime($pop.currentTime() + self.frameStep());
    self.refresh();
  }

  // Utils
  //
  self.printTime = function() {
    console.log($pop.currentTime());
  }
}


// Apply view model to view
ko.applyBindings(new MomentComposerViewModel());

}());