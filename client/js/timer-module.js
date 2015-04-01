function TimerModuleViewModel() {
  var self = this;
  console.log(moment().format());
  self.millis = ko.observable(moment().format());
}

ko.applyBindings(TimerModuleViewModel);
