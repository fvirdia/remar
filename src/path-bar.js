/*
<div id="path-bar" class="btn-group">
    <button class="btn btn-default">
    <span class="icon icon-home"></span>
    </button>
    <button class="btn btn-default">
    subdir1
    </button>
    <button class="btn btn-default active">
    subdir2
    </button>
</div>
*/

function renderPathBar(path) {
    (async () => {
        if (await rmfs.exists(path, true)) {
            let trail = [ ];
            cur_path = path;
            while (cur_path !== '') {
                let item = await rmfs.open(cur_path);
                trail.push({'name': item.VissibleName, 'uuid': item.ID})
                cur_path = item.Parent;
            }

            let obj = document.getElementById('path-bar');
            obj.innerHTML = '\
            <button class="btn btn-default" onclick="loadPath(\'\')">\
                <span class="icon icon-home"></span>\
            </button>';

            for (let item of trail) {
                let btn = document.createElement('button');
                btn.className = "btn btn-default";
                btn.innerText = item.name;
                btn.dataset.uuid = item.uuid;
                btn.onclick = function (event) {
                    loadPath(event.target.dataset.uuid);
                }
                obj.appendChild(btn);
            }
        }
    })();
}