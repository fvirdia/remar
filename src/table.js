class Table {
  constructor(id, header, entries) {
    this.obj = document.getElementById(id)
    this.obj.className = "table-striped";
    this.header = header;
    this.loadHead();
    if (entries) {
      this.loadTable(entries);
    }
  }

  loadHead() {
    let thead = this.obj.createTHead();
    let row = thead.insertRow();
    for (let key of this.header) {
      let th = document.createElement("th");
      let text = document.createTextNode(key);
      th.appendChild(text);
      row.appendChild(th);
    }
  }

  clear() {
    this.tbody.innerHTML = "";
  }

  addRow(entry) {
    if (!this.tbody) {
      this.tbody = this.obj.createTBody();
    }
    let row = this.tbody.insertRow();
    row.dataset.selected = "0"
    row.dataset.uuid = entry['uuid'];
    for (let key of this.header) {
      if (key === 'uuid') {
        continue;
      }
      let cell = row.insertCell();
      cell.innerHTML = entry[key];
      cell.onclick = function (event) {
        window.E = event;
        if (event.target.parentElement.dataset.selected === "0") {
          event.target.parentElement.dataset.selected = "1"
          event.target.parentElement.style.backgroundColor = "powderblue"
        } else {
          event.target.parentElement.dataset.selected = "0"
          event.target.parentElement.style.backgroundColor = ""
        }
      }
      if (key === 'Name') {
        // cell.dataset.uuid = entry['uuid'];
        cell.ondblclick = function (event) {
          loadPath(event.target.parentElement.dataset.uuid);
        }
      // } else if (key === 'Bookmarked') {
      //   cell.dataset.uuid = entry['uuid'];
      //   cell.onclick = function (event) {
      //     console.log(event);
      //   }
      }
    }
  }

  loadTable(data) {
    if (this.tbody) {
      this.clear()
    } else {
      this.tbody = this.obj.createTBody();
    }
    for (let element of data) {
      this.addRow(element);
    }
  }

  getSelected() {
    let selected = [];
    for (let el of this.tbody.children) {
      if (el.dataset.selected === "1") {
        selected.push(el.dataset.uuid);
      }
    }
    return selected;
  }

  clearSelected() {
    for (let el of this.tbody.children) {
      el.dataset.selected = "0";
      el.style.backgroundColor = "";
    }
  }
}