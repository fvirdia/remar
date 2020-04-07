
class Glue {
    constructor(idMove, idCopy, rmfs) {
      this.objmove = document.getElementById(`${idMove}`);
      this.objcopy = document.getElementById(`${idCopy}`);
      this.pasting = false;
      this.moving = false;
      this.uuids = [];
      this.rmfs = rmfs;
    }

    cut(uuids) {
        if (this.pasting || uuids.length <= 0) {
            return;
        }
        this.uuids = uuids;
        this.pasting = true;
        this.moving = true;
        this.objmove.setAttribute( "onClick", "javascript: pasteItems();" );
        this.objcopy.classList.add("disabled");
        this.objcopy.disabled = true;
        this.objmove.children[0].classList.remove("icon-logout");
        this.objmove.children[0].classList.add("icon-clipboard");
        this.objmove.children[1].innerText = "Paste";
    }

    copy(uuids) {
        console.log("try copy")
        if (this.pasting || uuids.length <= 0) {
            return;
        }
        console.log("inside copy")
        this.uuids = uuids;
        this.pasting = true;
        this.moving = false;
        this.objcopy.setAttribute( "onClick", "javascript: pasteItems();" );
        this.objmove.classList.add("disabled");
        this.objmove.disabled = true;
        this.objcopy.children[0].classList.remove("icon-docs");
        this.objcopy.children[0].classList.add("icon-clipboard");
        this.objcopy.children[1].innerText = "Paste";
    }

    async paste() {
        // console.log("glue: enter")
        if (!this.pasting || this.uuids.length <= 0) {
            return;
        }
        // do the thing
        // also, check whether the starting and ending locations are the same
        // ...
        let ret = false;
        if (this.moving) {
            // console.log("glue: call move")
            ret = await this.rmfs.move(this.uuids, current_path);
        } else {
            // TODO: copy functionality here
        }
        // console.log(`glue: ${this.uuids}`);
        // cleanup
        this.uuids = [];
        this.pasting = false;
        this.objmove.setAttribute( "onClick", "javascript: cutItems();" );
        // this.objcopy.setAttribute( "onClick", "javascript: copyItems();" );
        this.objmove.classList.remove("disabled");
        // this.objcopy.classList.remove("disabled");
        this.objmove.disabled = false;
        // this.objcopy.disabled = false;
        this.objmove.children[0].classList.remove("icon-clipboard");
        // this.objcopy.children[0].classList.remove("icon-clipboard");
        this.objmove.children[0].classList.add("icon-logout");
        // this.objcopy.children[0].classList.add("icon-docs");
        this.objmove.children[1].innerText = "Move";
        // this.objcopy.children[1].innerText = "Copy";
        console.log(`glue: exit (return value: ${ret})`);
        return ret;
    }
}
