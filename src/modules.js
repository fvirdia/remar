const { v4: uuidv4 } = require('uuid');
const fs = require('fs');
const Store = require('./src/storage.js');
const { Remarkable, ItemResponse } = require('remarkable-typescript');
const { ipcRenderer } = require('electron');
window.$ = window.jQuery = require('jquery');
