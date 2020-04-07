
const cloud_settings = new Store({
  configName: 'cloud-settings',
  defaults: {
    token: undefined
  }
});

const rmfs = new RemarkableFS(new Remarkable({ token: cloud_settings.get('token')}));

let tab = new Table("file-list", ['Name', 'Modified', 'Bookmarked'])
let glue = new Glue("move-button", "copy-button", rmfs);
let progressbar = new ProgressBar("progressbar", "progress-label")
let filters_ignore_hierarchy = false;
let current_path = '';
let only_bookmarked = watchableVariable(false);
only_bookmarked.registerListener((v) => {
    document.getElementById('bookmarks-toggle').style.color = v ? 'indigo' : '#737475';
})

let refresh_rate = 5*60;

// list directory --------------------------------------------------------------

function renderTable(path) {
    (async () => {
        try {
            let items; 
            if (typeof(path) == 'string') {
                items = filters_ignore_hierarchy ? 
                    await rmfs.find() : await rmfs.opendir(path)
                if (items === -1) {
                    // can't navigate into files
                    return;
                }
            } else if (Array.isArray(path)) {
                items = path
            } else {
                throw `${path} not a valid list of items or destination to render.`
            }
            let list = [];
            for (let it of items.sort((a, b) => (a.Type < b.Type) ? -1 : +(a.Type > b.Type))){
                if (only_bookmarked.val && !it.Bookmarked)
                {
                    continue;
                }
                list.push({
                    Name: `<span class="icon icon-${ it.Type > 'CollectionType' ? 'doc-text' : 'folder' }"></span> ${ it.VissibleName }`,
                    Modified: `${(new Date(it.ModifiedClient)).toLocaleString('en-GB', {timeZone: 'UTC'})} UTC`, 
                    Bookmarked: `<span class="icon icon-star${ it.Bookmarked ? '' : '-empty' } disabled"></span>`,
                    uuid: it.ID
                });
            }
            tab.loadTable(list);
            progressbar.stopLoading()
        } catch (err) {
            console.log(err)
            showSettings(`${err.name}: try re-connecting the client to the reMarkable Cloud.`);
            progressbar.stopLoading()
        }
    })();
}

function loadPath(path) {
    (async () => {
        // console.log(`loadPath: opening ${path}`);
        progressbar.setLoading()
        if (rmfs.exists(path, true)) {
            // console.log(`loadPath: ${path} exists as a dir`);
            renderTable(path);
            renderPathBar(path);
            current_path = path;
        }
    })();
}

// initial load and refresh of file list ---------------------------------------

loadPath(current_path);
window.setInterval(() => {
    loadPath(current_path);
}, refresh_rate*1000);

// import ----------------------------------------------------------------------

function importFiles(event) {
    (async () => {
        progressbar.setLoading()
        try {
            const files = document.getElementById('import-files').files;
            let wait = document.getElementById('import-files-wait');
            wait.hidden = false;
            for (let file of files) {
                await rmfs.put(file)
            }
            wait.hidden = true;
        } catch (err) {
            showSettings(`${err.name}: try re-connecting the client to the reMarkable Cloud.`);
        }
        loadPath(current_path)
    })();
}

// drag and drop files ---------------------------------------------------------

enableDnD('drop-area');

// bookmarking -----------------------------------------------------------------

function toggleBookmark() {
    (async () => {
        if (tab.getSelected().length > 0){
            progressbar.setLoading()
            for (let uuid of tab.getSelected()) {
                await rmfs.bookmark(uuid);
            }
            loadPath(current_path);
        }
    })();
}

// delete ----------------------------------------------------------------------

function deleteItems() {
    (async () => {
        progressbar.setLoading()
        for (let uuid of tab.getSelected()) {
            await rmfs.remove(uuid);
        }
        loadPath(current_path);
    })();
}

// glue ------------------------------------------------------------------------

function cutItems() {
    (async () => {
        glue.cut(tab.getSelected());
        tab.clearSelected();
    })();
}

function copyItems() {
    (async () => {
        glue.copy(tab.getSelected());
        tab.clearSelected();
    })();
}

function pasteItems() {
    (async () => {
        progressbar.setLoading();
        // console.log("pasteItems: call glue.paste")
        let ret = await glue.paste();
        // console.log("pasteItems: call loadPath")
        if (ret === true) {
            loadPath(current_path);
        } else if (ret === 2) {
            // tried moving into source directory, no need to reload
            progressbar.stopLoading()
        }
    })();
}

// mkdir -----------------------------------------------------------------------

$("#mkdir-dialog").dialog({
    autoOpen: false,
    modal: true,
    resizable: false,
    draggable: false,
    buttons: {
    Create: function () {
        $(this).dialog("close");
        const name = document.getElementById('mkdir-dialog-name').value
        makeDir(name)
        document.getElementById('mkdir-dialog-name').value = "";
    }
    },
    width: 215
});

function makeDir(name) {
    (async () => {
        progressbar.setLoading()
        if (name != "") {
            await rmfs.mkdir(name, current_path);
            loadPath(current_path);
        }
    })();
}


// rename ----------------------------------------------------------------------


$("#rename-dialog").dialog({
    autoOpen: false,
    modal: true,
    resizable: false,
    draggable: false,
    buttons: {
        Rename: function () {
            $(this).dialog("close");
            let items = [];
            for (let el of document.getElementById('rename-dialog').children) {
                items.push({
                    uuid: el.dataset.uuid,
                    name: el.value,
                })
            }
            renameItem(items);
        }
    },
    open: function (event, ui) {
        (async () => {
            let root = document.getElementById("rename-dialog");
            let html = ""
            const selected = tab.getSelected();
            if (selected.length === 0) {
                $(this).dialog("close");
            }
            for (let uuid of tab.getSelected()) {
                const item = await rmfs.open(uuid);
                html += `<input \
                    type="text" \
                    placeholder="New name" \
                    class="text ui-widget-content ui-corner-all" \
                    data-uuid="${uuid}" \
                    value="${item.VissibleName}" \
                    style="margin-bottom: 6px">`;
            }
            root.innerHTML = html;
        })();
    },
    width: 215,
});

function renameItem(items) {
    (async () => {
        // console.log("renameItem: enter")
        if (items.length > 0) {
            progressbar.setLoading()
            let ret = await rmfs.rename(items);
            if (ret === true) {
                loadPath(current_path);
            } else if (ret === 2) {
                // no query was executed
                progressbar.stopLoading()
            }
        }
    })();
}

// search ----------------------------------------------------------------------

enableSearch('search-field', progressbar, () => { loadPath(current_path); });
