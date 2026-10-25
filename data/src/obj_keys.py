
from enum import StrEnum
import json
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent
PROCESSED_DATA_DIR = DATA_DIR / "processed"

OBJ_KEYS_FN = 'obj_db_keys.json'
OBJ_KEYS_FP = PROCESSED_DATA_DIR / OBJ_KEYS_FN



class ObjKey(StrEnum):
    """
    Object keys indexing stellar object database.
    """

    MAIN_ID = 'main_id'
    OBJ_TYPE = 'obj_type'
    ALT_DESIG = 'alt_desig'
    
    ICRS_J2000_RA = 'ICRS_J2000_ra'
    ICRS_J2000_DEC = 'ICRS_J2000_dec'
    ECLIPTIC_2000_LON = 'ecliptic_2000_lon'
    ECLIPTIC_2000_LAT = 'ecliptic_2000_lat'
    GALACTIC_LON = 'galactic_lon'
    GALACTIC_LAT = 'galactic_lat'
    
    ICRS_J2000_RA_RAD = 'ICRS_J2000_ra_rad'
    ICRS_J2000_DEC_RAD = 'ICRS_J2000_dec_rad'
    ECLIPTIC_2000_LON_RAD = 'ecliptic_2000_lon_rad'
    ECLIPTIC_2000_LAT_RAD = 'ecliptic_2000_lat_rad'
    GALACTIC_LON_RAD = 'galactic_lon_rad'
    GALACTIC_LAT_RAD = 'galactic_lat_rad'
    
    SPHERICAL_COORDS = 'spherical_coords'
    SPHERICAL_VEL = 'spherical_vel'
    SPATIAL_COORDS = 'spatial_coords'
    SPATIAL_VEL = 'spatial_vel'
    
    RADIAL_VEL = 'rad_vel'
    
    MAGNITUDE_CAP_U = 'mag_U'
    MAGNITUDE_CAP_B = 'mag_B'
    MAGNITUDE_CAP_V = 'mag_V'
    MAGNITUDE_CAP_R = 'mag_R'
    MAGNITUDE_CAP_G = 'mag_G'
    MAGNITUDE_CAP_I = 'mag_I'
    MAGNITUDE_CAP_J = 'mag_J'
    MAGNITUDE_CAP_H = 'mag_H'
    MAGNITUDE_CAP_K = 'mag_K'
    PHOTOMETRIC_F150W = 'F150W'
    PHOTOMETRIC_F200W = 'F200W'
    PHOTOMETRIC_F444W = 'F444W'
    MAGNITUDE_LIL_U = 'mag_u'
    MAGNITUDE_LIL_G = 'mag_g'
    MAGNITUDE_LIL_R = 'mag_r'
    MAGNITUDE_LIL_I = 'mag_i'
    MAGNITUDE_LIL_Z = 'mag_z'
    SPECTRAL_TYPE = 'sp_type'
    
    PROPER_MOTION_NOF_MES = 'pm_n'
    PROPER_MOTION_RA = 'pm_ra'
    PROPER_MOTION_RA_ERR = 'pm_ra_err'
    PROPER_MOTION_DEC = 'pm_dec'
    PROPER_MOTION_DEC_ERR = 'pm_dec_err'
    PROPER_MOTION_COORD_SYS = 'pm_coord_sys'
    PROPER_MOTION_BIBCODE = 'pm_bibcode'

    PARALLAX_NOF_OF_MES = 'plx_n'
    PARALLAX = 'plx'
    PARALLAX_ERR = 'plx_err'
    PARALLAX_OBS_CODE = 'plx_obs_code'
    PARALLAX_BIBCODE = 'plx_bibcode'

    DISTANCE_NOF_MES = 'dist_n'
    DISTANCE = 'dist'
    DISTANCE_QUALITY = 'dist_q'
    DISTANCE_UNIT = 'dist_unit'
    DISTANCE_MINUS_ERR = 'dist_m_err'
    DISTANCE_PLUS_ERR = 'dist_p_err'
    DISTANCE_METHOD = 'dist_method'
    DISTANCE_BIBCODE = 'dist_bibcode'

    DIAMETER_NOF_MES = 'diam_n'
    DIAMETER = 'diam'
    DIAMETER_QUALITY = 'diam_q'
    DIAMETER_UNIT = 'diam_unit'
    DIAMETER_ERR = 'diam_err'
    DIAMETER_FILTER = 'diam_filter'
    DIAMETER_METHOD = 'diam_method'
    DIAMETER_BIBCODE = 'diam_bibcode'

    FE_H_NOF_MES = 'Fe_H_n'
    EFFECTIVE_TEMP = 'eff_temp'
    LOG_G = 'log_g'
    FE_H_INDEX = 'Fe_H_index'
    FE_H_FLAG = 'Fe_H_flag'  # Expresses calculation method
    # S = result from a spectrum of low signal to noise ratio
    # M = average of several values given in the corresponding article
    # C = in the absence of any indication in the corresponding article, [Fe/H] relative to the Sun was calculated with a solar value of 7.50
    # T = indicates that both M and C apply
    # D = indicates that both S and C apply
    FE_H_COMPARISON_STAR = 'Fe_H_comp_star'
    FE_H_CAT_NO = 'Fe_H_cat_no'
    FE_H_BIBCODE = 'Fe_H_bibcode'

    ROTATION_N = 'rot_n'
    ROTATION_UPPER_VAL = 'rot_up_vel'
    ROTATION_VEL = 'rot_vel'
    ROTATION_VEL_ERR = 'rot_vel_err'
    ROTATION_NOF_MES = 'rot_nof_mes'
    ROTATION_QUALITY = 'rot_q'
    ROTATION_BIBCODE = 'rot_bibcode'


    @staticmethod
    def obj_keys():

        return (
            ObjKey.MAIN_ID, ObjKey.OBJ_TYPE,

            ObjKey.ICRS_J2000_RA, ObjKey.ICRS_J2000_DEC,
            ObjKey.ECLIPTIC_2000_LON, ObjKey.ECLIPTIC_2000_LAT,
            ObjKey.GALACTIC_LON, ObjKey.GALACTIC_LAT,

            ObjKey.ICRS_J2000_RA_RAD, ObjKey.ICRS_J2000_DEC_RAD,
            ObjKey.ECLIPTIC_2000_LON_RAD, ObjKey.ECLIPTIC_2000_LAT_RAD,
            ObjKey.GALACTIC_LON_RAD, ObjKey.GALACTIC_LAT_RAD,

            ObjKey.SPHERICAL_COORDS, ObjKey.SPHERICAL_VEL,
            ObjKey.SPATIAL_COORDS, ObjKey.SPATIAL_VEL,

            ObjKey.RADIAL_VEL,

            ObjKey.MAGNITUDE_CAP_U, ObjKey.MAGNITUDE_CAP_B, ObjKey.MAGNITUDE_CAP_V,
            ObjKey.MAGNITUDE_CAP_R, ObjKey.MAGNITUDE_CAP_G, ObjKey.MAGNITUDE_CAP_I,
            ObjKey.MAGNITUDE_CAP_J, ObjKey.MAGNITUDE_CAP_H, ObjKey.MAGNITUDE_CAP_K,
            ObjKey.PHOTOMETRIC_F150W, ObjKey.PHOTOMETRIC_F200W, ObjKey.PHOTOMETRIC_F444W,
            ObjKey.MAGNITUDE_LIL_U, ObjKey.MAGNITUDE_LIL_G, ObjKey.MAGNITUDE_LIL_R,
            ObjKey.MAGNITUDE_LIL_I, ObjKey.MAGNITUDE_LIL_Z,
            ObjKey.SPECTRAL_TYPE,

            ObjKey.PROPER_MOTION_NOF_MES,
            ObjKey.PROPER_MOTION_RA, ObjKey.PROPER_MOTION_RA_ERR,
            ObjKey.PROPER_MOTION_DEC, ObjKey.PROPER_MOTION_DEC_ERR,
            ObjKey.PROPER_MOTION_COORD_SYS, ObjKey.PROPER_MOTION_BIBCODE,

            ObjKey.PARALLAX_NOF_OF_MES,
            ObjKey.PARALLAX, ObjKey.PARALLAX_ERR,
            ObjKey.PARALLAX_OBS_CODE,
            ObjKey.PARALLAX_BIBCODE,

            ObjKey.DISTANCE_NOF_MES,
            ObjKey.DISTANCE, ObjKey.DISTANCE_QUALITY, ObjKey.DISTANCE_UNIT,
            ObjKey.DISTANCE_MINUS_ERR, ObjKey.DISTANCE_PLUS_ERR,
            ObjKey.DISTANCE_METHOD, ObjKey.DISTANCE_BIBCODE,

            ObjKey.DIAMETER_NOF_MES,
            ObjKey.DIAMETER, ObjKey.DIAMETER_QUALITY, ObjKey.DIAMETER_UNIT, ObjKey.DIAMETER_ERR,
            ObjKey.DIAMETER_FILTER, ObjKey.DIAMETER_METHOD, ObjKey.DIAMETER_BIBCODE,

            ObjKey.FE_H_NOF_MES,
            ObjKey.EFFECTIVE_TEMP, ObjKey.LOG_G,
            ObjKey.FE_H_INDEX, ObjKey.FE_H_FLAG,
            ObjKey.FE_H_COMPARISON_STAR,
            ObjKey.FE_H_CAT_NO, ObjKey.FE_H_BIBCODE,

            ObjKey.ROTATION_N,
            ObjKey.ROTATION_UPPER_VAL, ObjKey.ROTATION_VEL, ObjKey.ROTATION_VEL_ERR,
            ObjKey.ROTATION_NOF_MES, ObjKey.ROTATION_QUALITY, ObjKey.ROTATION_BIBCODE
        )


    @staticmethod
    def serialize_obj_data(obj_data: dict) -> list:
        """
        Maps object data items to key structure of 'obj_keys()'. 
        """
        obj_keys = ObjKey.obj_keys()
        serial_obj_data = [None] * len(obj_keys)
        for obj_key, obj_item in obj_data.items():
            try:
                key_idx = obj_keys.index(obj_key)
            except ValueError:
                raise ValueError(f'Could not index key \"{obj_key}\" and item \"{obj_item}\" with object keys.')
            
            serial_obj_data[key_idx] = obj_item
        
        return serial_obj_data


    @staticmethod
    def deserialize_obj_data(serial_obj_data: list) -> dict:
        ...

    
    @staticmethod
    def dump_obj_keys():
        print(f'Dumping object database keys to {OBJ_KEYS_FP} ...')
        try:
            with open(OBJ_KEYS_FP, 'w') as json_file:
                json.dump(ObjKey.obj_keys(), json_file, indent=4)
        except OSError as err:
            raise OSError(f'Could not write JSON file for object database keys.', err, sep='\n')
        
        print(f'Object database keys dumped.')



if __name__ == '__main__':
    ObjKey.dump_obj_keys()