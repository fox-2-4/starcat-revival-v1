
import { StellarObject } from './stellar_object.js';
import { Cmatrix } from './cmatrix.js';


const ROOT_DIR = '../'
const DATA_DIR = ROOT_DIR + 'data/';
const PROCESSED_DATA_DIR = DATA_DIR + 'processed/';
const ZIPPED_OBJ_DB_FILE_NAME = 'obj_db.zip';
const ZIPPED_OBJ_DB_FILE_PATH = PROCESSED_DATA_DIR + ZIPPED_OBJ_DB_FILE_NAME;
const OBJ_DB_FN = 'obj_db.json';


const cmatrixMain = new Cmatrix('#main-cmatrix', 120, 60, ' ');
const cmatrixSub = new Cmatrix('#sub-cmatrix', 40, 30, ' ');

