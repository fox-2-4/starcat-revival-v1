
import * as fflate from './fflate/esm/browser.js'
import { StellarObject } from './stellar_object.js';


const ROOT_DIR = '../'
const DATA_DIR = ROOT_DIR + 'data/';
const PROCESSED_DATA_DIR = DATA_DIR + 'processed/';
const ZIPPED_OBJ_DB_FILE_NAME = 'obj_db.zip';
const ZIPPED_OBJ_DB_FILE_PATH = PROCESSED_DATA_DIR + ZIPPED_OBJ_DB_FILE_NAME;
const OBJ_DB_FN = 'obj_db.json';


const appDataPromise = loadAppData();

document.getElementById('text').textContent =
    JSON.stringify(await appDataPromise, null, 2);



async function loadAppData() {
    const response = await fetch(ZIPPED_OBJ_DB_FILE_PATH);
    if (!response.ok) {
        throw new Error(`Failed to fetch ${ZIPPED_OBJ_DB_FILE_PATH}: ${response.status}`);
    }
    const buffer = await response.arrayBuffer();
    const zipUint8 = new Uint8Array(buffer);
    const files = await unzipAsync(zipUint8);
    const data = files[OBJ_DB_FN];

    if (!data) {
        throw new Error(`${OBJ_DB_FN} not found in ${ZIPPED_OBJ_DB_FILE_NAME}`);
    }

    const text = new TextDecoder('utf-8').decode(data);
    return JSON.parse(text);
}

function unzipAsync(data) {
    return new Promise((resolve, reject) => {
        fflate.unzip(data, (err, files) => {
            if (err) { reject(err); return; }
            resolve(files)
        });
    });
}

