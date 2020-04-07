
function enableDnD(element_id) {
    let dropArea = document.getElementById(element_id);

    dropArea.addEventListener('dragenter', () => {dropArea.style.color = "#888";}, false)
    dropArea.addEventListener('dragleave', () => {dropArea.style.color = "#eee";}, false)
    dropArea.addEventListener('dragover', (e) => { e.preventDefault();}, false)
    dropArea.addEventListener('drop', (e) => {
        e.preventDefault(); // matters on browser, maybe not in electron
        dropArea.style.color = "#eee";
        console.log(e.dataTransfer.files); 
        let wait = document.getElementById(`${element_id}-wait`);
        wait.hidden = false;
        (async () => {
            for (let file of e.dataTransfer.files) {
                await rmfs.put(file)
            }
            wait.hidden = true;
            loadPath(current_path)
        })();
    }, false)
}
