class RemarkableFS {
    constructor(client) {
        this.client = client;
    }

    async find() {
        return (await this.client.getAllItems());
    }

    async opendir(path) {
        if (await this.exists(path, false)) {
            return -1;
        }
        return (await this.client.getAllItems())
            .filter(function (o) {
                return o.Parent === path;
            });
    }

    async open(path) {
        return (await this.client.getItemWithId(path));
    }

    async exists(path, is_directory) {
        if (path === '' && is_directory) {
            return true;
        }
        const items = await this.client.getAllItems();
        return items.filter((o) => o.ID == path && (is_directory ? (o.Type === 'CollectionType') : (o.Type === 'DocumentType'))).length > 0;
    }

    async put(file) {
        // only allow pdf files
        if (file.type === 'application/pdf') {
            const pdf = fs.readFileSync(file.path);
            const filename = file.name.split('.').slice(0, -1).join('.') // trim extension
            const pdfUploadedId = await this.client.uploadPDF(filename, pdf);
        }
    }

    async bookmark(uuid) {

        const item = await this.client.getItemWithId(uuid);
        const url = `${await this.client.getStorageUrl()}/document-storage/json/2/upload/update-status`;
        const body = await this.client.client.put(url, {
            json: [{
                Parent: item.Parent,
                Type: item.Type,
                Version: item.Version + 1,
                ID: uuid,
                VissibleName: item.VissibleName,
                lastModified: new Date().toISOString(),
                ModifiedClient: new Date().toISOString(),
                Bookmarked: !item.Bookmarked,
            },],
        })
        if (!body.body[0].Success) {
            throw body.body[0].Message;
        }
        return body.body[0].Success;
    }

    async remove(uuid) {
        const item = await this.client.getItemWithId(uuid);
        return await this.client.deleteItem(uuid, item.Version);
    }

    async mkdir(name, parent) {
        const uuid = uuidv4();
        const url = `${await this.client.getStorageUrl()}/document-storage/json/2/upload/update-status`;

        const body = await this.client.client.put(url, {
            json: [{
                ID: uuid,
                Parent: parent,
                Type: "CollectionType",
                Version: 1,
                VissibleName: name,
                ModifiedClient: new Date().toISOString(),
            },],
        })
        if (!body.body[0].Success) {
            throw body.body[0].Message;
        }
        return body.body[0].Success;
    }

    async move(uuids, destination) {
        // console.log("move: enter")
        const url = `${await this.client.getStorageUrl()}/document-storage/json/2/upload/update-status`;
        // console.log("move: got target url")
        // console.log("move: check if destination exists as a directory")
        if (!await this.exists(destination, true)) {
            throw "Destination does not exist.";
        }
        // console.log("move: prepare json object to send")
        let json = [];
        for (let id of uuids) {
            const item = await this.client.getItemWithId(id);
            console.log(item);
            console.log(`move: id = ${id}`)
            console.log(`move: parent = ${item.Parent}`)
            console.log(`move: destination = ${destination}`)
            if (item.Parent === destination) {
                continue;
            }
            if (item.ID === destination) {
                throw "Can not move to inside itself.";
            }
            json.push({
                ID: id,
                Parent: destination,
                VissibleName: item.VissibleName,
                Type: item.Type,
                Version: item.Version + 1,
                ModifiedClient: new Date().toISOString(),
            });
        }
        // console.log(`move: ${json}`);
        if (json.length === 0) {
            // no need to move anything
            console.log("no need to move anything")
            return 2;
        }
        // console.log("move: call http put")
        const body = await this.client.client.put(url, { json: json });
        console.log(body.body);
        // console.log("move: call.http put returned")
        if (!body.body[0].Success) {
            throw body.body[0].Message;
        }
        console.log("move: exit")
        return body.body[0].Success;
    }

    async rename(items) {
        console.log(`rename: ${items}`);
        const url = `${await this.client.getStorageUrl()}/document-storage/json/2/upload/update-status`;

        let json = [];
        for (let it of items) {
            const item = await this.client.getItemWithId(it.uuid);
            console.log(item);
            // console.log(`move: id = ${id}`)
            // console.log(`move: parent = ${item.Parent}`)
            // console.log(`move: destination = ${destination}`)
            if (item.VissibleName === it.name) {
                continue;
            }
            json.push({
                ID: item.ID,
                Parent: item.Parent,
                VissibleName: it.name,
                Type: item.Type,
                Version: item.Version + 1,
                ModifiedClient: new Date().toISOString(),
            });
        }
        // console.log(`move: ${json}`);
        console.log(json);
        if (json.length === 0) {
            // no need to move anything
            console.log("no need to rename anything")
            return 2;
        }
        // console.log("move: call http put")
        const body = await this.client.client.put(url, { json: json });
        console.log(body.body);
        // console.log("move: call.http put returned")
        if (!body.body[0].Success) {
            throw body.body[0].Message;
        }
        console.log("rename: exit")
        return body.body[0].Success;
    }
}