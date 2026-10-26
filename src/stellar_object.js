
import * as fflate from './fflate/esm/browser.js'

const ROOT_DIR = '../'
const DATA_DIR = ROOT_DIR + 'data/';
const PROCESSED_DATA_DIR = DATA_DIR + 'processed/';
const ZIPPED_OBJ_DB_FILE_NAME = 'obj_db.zip';
const ZIPPED_OBJ_DB_FILE_PATH = PROCESSED_DATA_DIR + ZIPPED_OBJ_DB_FILE_NAME;
const OBJ_DB_FN = 'obj_db.json';


export const StellarObject = Object.freeze({

    MAIN_ID: 'main_id',
    OBJ_TYPE: 'obj_type',
    ALT_DESIG: 'alt_desig',
    
    ICRS_J2000_RA: 'ICRS_J2000_ra',
    ICRS_J2000_DEC: 'ICRS_J2000_dec',
    ECLIPTIC_2000_LON: 'ecliptic_2000_lon',
    ECLIPTIC_2000_LAT: 'ecliptic_2000_lat',
    GALACTIC_LON: 'galactic_lon',
    GALACTIC_LAT: 'galactic_lat',
    
    ICRS_J2000_RA_RAD: 'ICRS_J2000_ra_rad',
    ICRS_J2000_DEC_RAD: 'ICRS_J2000_dec_rad',
    ECLIPTIC_2000_LON_RAD: 'ecliptic_2000_lon_rad',
    ECLIPTIC_2000_LAT_RAD: 'ecliptic_2000_lat_rad',
    GALACTIC_LON_RAD: 'galactic_lon_rad',
    GALACTIC_LAT_RAD: 'galactic_lat_rad',
    
    SPHERICAL_COORDS: 'spherical_coords',
    SPHERICAL_VEL: 'spherical_vel',
    SPATIAL_COORDS: 'spatial_coords',
    SPATIAL_VEL: 'spatial_vel',
    
    RADIAL_VEL: 'rad_vel',
    
    MAGNITUDE_CAP_U: 'mag_U',
    MAGNITUDE_CAP_B: 'mag_B',
    MAGNITUDE_CAP_V: 'mag_V',
    MAGNITUDE_CAP_R: 'mag_R',
    MAGNITUDE_CAP_G: 'mag_G',
    MAGNITUDE_CAP_I: 'mag_I',
    MAGNITUDE_CAP_J: 'mag_J',
    MAGNITUDE_CAP_H: 'mag_H',
    MAGNITUDE_CAP_K: 'mag_K',
    PHOTOMETRIC_F150W: 'F150W',
    PHOTOMETRIC_F200W: 'F200W',
    PHOTOMETRIC_F444W: 'F444W',
    MAGNITUDE_LIL_U: 'mag_u',
    MAGNITUDE_LIL_G: 'mag_g',
    MAGNITUDE_LIL_R: 'mag_r',
    MAGNITUDE_LIL_I: 'mag_i',
    MAGNITUDE_LIL_Z: 'mag_z',
    SPECTRAL_TYPE: 'sp_type',
    
    PROPER_MOTION_NOF_MES: 'pm_n',
    PROPER_MOTION_RA: 'pm_ra',
    PROPER_MOTION_RA_ERR: 'pm_ra_err',
    PROPER_MOTION_DEC: 'pm_dec',
    PROPER_MOTION_DEC_ERR: 'pm_dec_err',
    PROPER_MOTION_COORD_SYS: 'pm_coord_sys',
    PROPER_MOTION_BIBCODE: 'pm_bibcode',

    PARALLAX_NOF_OF_MES: 'plx_n',
    PARALLAX: 'plx',
    PARALLAX_ERR: 'plx_err',
    PARALLAX_OBS_CODE: 'plx_obs_code',
    PARALLAX_BIBCODE: 'plx_bibcode',

    DISTANCE_NOF_MES: 'dist_n',
    DISTANCE: 'dist',
    DISTANCE_QUALITY: 'dist_q',
    DISTANCE_UNIT: 'dist_unit',
    DISTANCE_MINUS_ERR: 'dist_m_err',
    DISTANCE_PLUS_ERR: 'dist_p_err',
    DISTANCE_METHOD: 'dist_method',
    DISTANCE_BIBCODE: 'dist_bibcode',

    DIAMETER_NOF_MES: 'diam_n',
    DIAMETER: 'diam',
    DIAMETER_QUALITY: 'diam_q',
    DIAMETER_UNIT: 'diam_unit',
    DIAMETER_ERR: 'diam_err',
    DIAMETER_FILTER: 'diam_filter',
    DIAMETER_METHOD: 'diam_method',
    DIAMETER_BIBCODE: 'diam_bibcode',

    FE_H_NOF_MES: 'Fe_H_n',
    EFFECTIVE_TEMP: 'eff_temp',
    LOG_G: 'log_g',
    FE_H_INDEX: 'Fe_H_index',
    FE_H_FLAG: 'Fe_H_flag',
    FE_H_COMPARISON_STAR: 'Fe_H_comp_star',
    FE_H_CAT_NO: 'Fe_H_cat_no',
    FE_H_BIBCODE: 'Fe_H_bibcode',

    ROTATION_N: 'rot_n',
    ROTATION_UPPER_VAL: 'rot_up_vel',
    ROTATION_VEL: 'rot_vel',
    ROTATION_VEL_ERR: 'rot_vel_err',
    ROTATION_NOF_MES: 'rot_nof_mes',
    ROTATION_QUALITY: 'rot_q',
    ROTATION_BIBCODE: 'rot_bibcode',


    stellarObjKeys() {

        return [

            StellarObject.MAIN_ID, StellarObject.OBJ_TYPE, StellarObject.ALT_DESIG,

            StellarObject.ICRS_J2000_RA, StellarObject.ICRS_J2000_DEC,
            StellarObject.ECLIPTIC_2000_LON, StellarObject.ECLIPTIC_2000_LAT,
            StellarObject.GALACTIC_LON, StellarObject.GALACTIC_LAT,

            StellarObject.ICRS_J2000_RA_RAD, StellarObject.ICRS_J2000_DEC_RAD,
            StellarObject.ECLIPTIC_2000_LON_RAD, StellarObject.ECLIPTIC_2000_LAT_RAD,
            StellarObject.GALACTIC_LON_RAD, StellarObject.GALACTIC_LAT_RAD,

            StellarObject.SPHERICAL_COORDS, StellarObject.SPHERICAL_VEL,
            StellarObject.SPATIAL_COORDS, StellarObject.SPATIAL_VEL,

            StellarObject.RADIAL_VEL,

            StellarObject.MAGNITUDE_CAP_U, StellarObject.MAGNITUDE_CAP_B, StellarObject.MAGNITUDE_CAP_V,
            StellarObject.MAGNITUDE_CAP_R, StellarObject.MAGNITUDE_CAP_G, StellarObject.MAGNITUDE_CAP_I,
            StellarObject.MAGNITUDE_CAP_J, StellarObject.MAGNITUDE_CAP_H, StellarObject.MAGNITUDE_CAP_K,
            StellarObject.PHOTOMETRIC_F150W, StellarObject.PHOTOMETRIC_F200W, StellarObject.PHOTOMETRIC_F444W,
            StellarObject.MAGNITUDE_LIL_U, StellarObject.MAGNITUDE_LIL_G, StellarObject.MAGNITUDE_LIL_R,
            StellarObject.MAGNITUDE_LIL_I, StellarObject.MAGNITUDE_LIL_Z,
            StellarObject.SPECTRAL_TYPE,

            StellarObject.PROPER_MOTION_NOF_MES,
            StellarObject.PROPER_MOTION_RA, StellarObject.PROPER_MOTION_RA_ERR,
            StellarObject.PROPER_MOTION_DEC, StellarObject.PROPER_MOTION_DEC_ERR,
            StellarObject.PROPER_MOTION_COORD_SYS, StellarObject.PROPER_MOTION_BIBCODE,

            StellarObject.PARALLAX_NOF_OF_MES,
            StellarObject.PARALLAX, StellarObject.PARALLAX_ERR,
            StellarObject.PARALLAX_OBS_CODE,
            StellarObject.PARALLAX_BIBCODE,

            StellarObject.DISTANCE_NOF_MES,
            StellarObject.DISTANCE, StellarObject.DISTANCE_QUALITY, StellarObject.DISTANCE_UNIT,
            StellarObject.DISTANCE_MINUS_ERR, StellarObject.DISTANCE_PLUS_ERR,
            StellarObject.DISTANCE_METHOD, StellarObject.DISTANCE_BIBCODE,

            StellarObject.DIAMETER_NOF_MES,
            StellarObject.DIAMETER, StellarObject.DIAMETER_QUALITY, StellarObject.DIAMETER_UNIT, StellarObject.DIAMETER_ERR,
            StellarObject.DIAMETER_FILTER, StellarObject.DIAMETER_METHOD, StellarObject.DIAMETER_BIBCODE,

            StellarObject.FE_H_NOF_MES,
            StellarObject.EFFECTIVE_TEMP, StellarObject.LOG_G,
            StellarObject.FE_H_INDEX, StellarObject.FE_H_FLAG,
            StellarObject.FE_H_COMPARISON_STAR,
            StellarObject.FE_H_CAT_NO, StellarObject.FE_H_BIBCODE,

            StellarObject.ROTATION_N,
            StellarObject.ROTATION_UPPER_VAL, StellarObject.ROTATION_VEL, StellarObject.ROTATION_VEL_ERR,
            StellarObject.ROTATION_NOF_MES, StellarObject.ROTATION_QUALITY, StellarObject.ROTATION_BIBCODE

        ];

    },


    /**
     * 
     * @param {Array} serialObjData 
     */
    deserializeStellarObjData(serialObjData) {
    },


    async fetchStellarObjDatabase() {

        function unzip(data) {
            return new Promise((resolve, reject) => {
                fflate.unzip(data, (err, files) => {
                    if (err) { reject(err); return; }
                    resolve(files)
                });
            });
        }

        const response = await fetch(ZIPPED_OBJ_DB_FILE_PATH);

        if (!response.ok) { throw new Error(`Failed to fetch ${ZIPPED_OBJ_DB_FILE_PATH}: ${response.status}`); }

        const buffer = await response.arrayBuffer();
        const uint8Arr = new Uint8Array(buffer);
        const files = await unzip(uint8Arr);
        const data = files[OBJ_DB_FN];

        if (!data) { throw new Error(`${OBJ_DB_FN} not found in ${ZIPPED_OBJ_DB_FILE_NAME}`); }

        const text = new TextDecoder('utf-8').decode(data);

        return JSON.parse(text);
    }

});