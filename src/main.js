
// const APP_DATA_DIR = '../data/';

// const ARCHIVED_APP_DATA_DIR = APP_DATA_DIR + '/processed/';
// const ARCHIVED_APP_DATA_FN = 'processed.json.zip';
// const ARCHIVED_APP_DATA_FP = ARCHIVED_APP_DATA_DIR + ARCHIVED_APP_DATA_FN;
// const APP_DATA_FN = 'processed.json';

// let app_data = null;


// document.getElementById('check-btn').addEventListener('click', displayData);

// function displayData() {
//     document.getElementById('text').textContent = app_data;
// }


// fetch(ARCHIVED_APP_DATA_FP)
//     .then(response => response.arrayBuffer())
//     .then(buffer => {
//         const zipUint8 = new Uint8Array(buffer);
//         fflate.unzip(zipUint8, (err, unzippedFiles) => {
//             if (err) {
//                 console.error(
//                     `Encountered error while unzipping application file(s) from 
//                     \'${ARCHIVED_APP_DATA_FN}\'`, 
//                     err);
//                 return;
//             }
//             const data = unzippedFiles[APP_DATA_FN]
//             if (data) {
//                 const text = new TextDecoder('utf-8').decode(data);
//                 // console.log(text);
//                 app_data = text;
//             }
//             else {
//                 console.error(
//                     `App data \'${APP_DATA_FN}\' not found in 
//                     ZIP archive \'${ARCHIVED_APP_DATA_FN}\'.`);
//             }
//         });
//     });


// console.log(app_data);


const APP_DATA_DIR = '../data/';
const ARCHIVED_APP_DATA_DIR = APP_DATA_DIR + 'processed/';
const ARCHIVED_APP_DATA_FN = 'processed.json.zip';
const ARCHIVED_APP_DATA_FP = ARCHIVED_APP_DATA_DIR + ARCHIVED_APP_DATA_FN;
const APP_DATA_FN = 'processed.json';


const appDataPromise = loadAppData();

document.getElementById('text').textContent =
    JSON.stringify(await appDataPromise, null, 2);



async function loadAppData() {
    const response = await fetch(ARCHIVED_APP_DATA_FP);
    if (!response.ok) {
        throw new Error(`Failed to fetch ${ARCHIVED_APP_DATA_FP}: ${response.status}`);
    }
    const buffer = await response.arrayBuffer();
    const zipUint8 = new Uint8Array(buffer);
    const files = await unzipAsync(zipUint8);
    const data = files[APP_DATA_FN];

    if (!data) {
        throw new Error(`${APP_DATA_FN} not found in ${ARCHIVED_APP_DATA_FN}`);
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


// document
//     .getElementById('check-btn')
//     .addEventListener('click', displayData);


// async function displayData() {
//     try {
//         const appData = await appDataPromise;
//         document.getElementById('text').textContent =
//             JSON.stringify(appData, null, 2);
//     }
//     catch (err) {
//         console.error('Could not load application data:', err);
//     }
// }