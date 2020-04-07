
class ProgressBar {
    constructor(idBar, idLabel) {
      this.bar = $(`#${idBar}`);
      this.label = $(`#${idLabel}`);

      this.bar.progressbar({
        value: 100,
        change: function () {
            // this.label.text(this.bar.progressbar("value") + "%");
        },
        complete: function () {
            // this.label.text( "Complete!" );
        }
      });
    }
  
    setLoading() {
        this.bar.progressbar("value", false)
        document.getElementById('overlay').style.display = "block";
    }

    stopLoading() {
        this.bar.progressbar("value", 100)
        document.getElementById('overlay').style.display = "none";
    }
}