
function enableSearch(objId, progressbar, failCb) {
    let obj = document.getElementById(objId);
    obj.addEventListener("keyup", function(event) {
    if (event.keyCode === 13) {
      event.preventDefault();
      progressbar.setLoading();
      (async () => {
          const items = await rmfs.find();
          let query = obj.value.toLowerCase();
          if (query.length === 0) {
            failCb();
          } else {
              let matches = [];
              for (let item of items) {
                  if (item.VissibleName.toLowerCase().indexOf(query) !== -1) {
                      matches.push(item);
                    }
                }
                renderTable(matches);
            }
      })();
    }
  });
}