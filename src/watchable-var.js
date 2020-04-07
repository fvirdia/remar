watchableVariable = function (init_value)
{
  return {
    aInternal: init_value,
    aListener: function(val) {},
    set val(val) {
      this.aInternal = val;
      this.aListener(val);
    },
    get val() {
      return this.aInternal;
    },
    registerListener: function(listener) {
      this.aListener = listener;
    }
  }
}