"""
This code doesn't need to be fast or efficient.
It just needs to run once on a specific set of data to produce the desired JSON.
"""

import json
import zipfile
from pathlib import Path
from tqdm import tqdm, trange
from prettytable import PrettyTable, TableStyle

from obj_keys import ObjKey as OK
from process_funcs import *
from vector_math import *


SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
PROCESSED_DATA_FILE_NAME = "processed.json"
ZIP_ARCHIVE_FILE_NAME = "processed.json.zip"

# The structure of this tuple describes how the data is arranged on the scraped .txt files.
RAW_DATA_COLUMNS = (
    None, OK.MAIN_ID, OK.OBJ_TYPE,

    OK.ICRS_J2000_RA, OK.ICRS_J2000_DEC,
    OK.ECLIPTIC_2000_LON, OK.ECLIPTIC_2000_LAT,
    OK.GALACTIC_LON, OK.GALACTIC_LAT,

    OK.RADIAL_VEL,

    OK.MAGNITUDE_CAP_U, OK.MAGNITUDE_CAP_B, OK.MAGNITUDE_CAP_V,
    OK.MAGNITUDE_CAP_R, OK.MAGNITUDE_CAP_G, OK.MAGNITUDE_CAP_I,
    OK.MAGNITUDE_CAP_J, OK.MAGNITUDE_CAP_H, OK.MAGNITUDE_CAP_K,
    OK.PHOTOMETRIC_F150W, OK.PHOTOMETRIC_F200W, OK.PHOTOMETRIC_F444W,
    OK.MAGNITUDE_LIL_U, OK.MAGNITUDE_LIL_G, OK.MAGNITUDE_LIL_R,
    OK.MAGNITUDE_LIL_I, OK.MAGNITUDE_LIL_Z,
    OK.SPECTRAL_TYPE,

    OK.PROPER_MOTION_NOF_MES,
    OK.PROPER_MOTION_RA, OK.PROPER_MOTION_RA_ERR,
    OK.PROPER_MOTION_DEC, OK.PROPER_MOTION_DEC_ERR,
    OK.PROPER_MOTION_COORD_SYS, OK.PROPER_MOTION_BIBCODE,

    OK.PARALLAX_NOF_OF_MES,
    OK.PARALLAX, OK.PARALLAX_ERR,
    OK.PARALLAX_OBS_CODE,
    OK.PARALLAX_BIBCODE,

    OK.DISTANCE_NOF_MES,
    OK.DISTANCE, OK.DISTANCE_QUALITY, OK.DISTANCE_UNIT,
    OK.DISTANCE_MINUS_ERR, OK.DISTANCE_PLUS_ERR,
    OK.DISTANCE_METHOD, OK.DISTANCE_BIBCODE,

    OK.DIAMETER_NOF_MES,
    OK.DIAMETER, OK.DIAMETER_QUALITY, OK.DIAMETER_UNIT, OK.DIAMETER_ERR,
    OK.DIAMETER_FILTER, OK.DIAMETER_METHOD, OK.DIAMETER_BIBCODE,

    OK.FE_H_NOF_MES,
    OK.EFFECTIVE_TEMP, OK.LOG_G,
    OK.FE_H_INDEX, OK.FE_H_FLAG,
    OK.FE_H_COMPARISON_STAR,
    OK.FE_H_CAT_NO, OK.FE_H_BIBCODE,

    OK.ROTATION_N,
    OK.ROTATION_UPPER_VAL, OK.ROTATION_VEL, OK.ROTATION_VEL_ERR,
    OK.ROTATION_NOF_MES, OK.ROTATION_QUALITY, OK.ROTATION_BIBCODE
)
NOF_RAW_DATA_COLUMNS = len(RAW_DATA_COLUMNS)



def process_raw_data():

    # Check data directory structure.
    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Main data directory not found: {DATA_DIR}")
    elif not RAW_DATA_DIR.exists():
        raise FileNotFoundError(f"Raw data directory not found: {RAW_DATA_DIR}")
    elif not PROCESSED_DATA_DIR.exists():
        raise FileNotFoundError(f"Processed data directory not found: {PROCESSED_DATA_DIR}")
    
    print("Identified the following critical directories:",
          SCRIPT_DIR,
          DATA_DIR,
          RAW_DATA_DIR,
          PROCESSED_DATA_DIR,
          '\n',
          sep='\n')

    # Identify raw data files.
    raw_data_file_pattern = "*.txt"
    raw_data_file_paths = list(RAW_DATA_DIR.rglob(raw_data_file_pattern))
    if len(raw_data_file_paths):
        print(f"Identified the following {len(raw_data_file_paths)} raw data files:")
        for raw_data_file_path in raw_data_file_paths:
            print(raw_data_file_path.name)
        print('\n')
    else:
        raise FileNotFoundError(f"No files not found in raw data directory: {RAW_DATA_DIR}")


    preprocessed_data = {}  # keyed via obj. "main_id"
    preprocess_stats = {str(raw_data_file_path.name): {} for raw_data_file_path in raw_data_file_paths}

    print('Extracting rows...')
    for raw_data_file_path in tqdm(
        raw_data_file_paths, 
        desc='...', 
        total=len(raw_data_file_paths), 
        ncols=150
    ):
        raw_data_file_name = raw_data_file_path.name

        non_data_rows_ct = 0
        completed_rows_ct = 0
        duplicate_data_ct = 0
        
        try:
            with open(raw_data_file_path, "rt", encoding="utf8") as tsv_file:
                tsv_rows = tsv_file.read().split('\n')
        except FileNotFoundError as err:
            print(f"File not processed: {raw_data_file_name}", err, sep='\n')
            continue

        # each TSV row contains all data for one stellar object
        for tsv_row in tsv_rows:
            
            raw_data = tsv_row.split('\t')
            if len(raw_data) != NOF_RAW_DATA_COLUMNS:
                non_data_rows_ct += 1
                continue
            
            keyed_data = {
                RAW_DATA_COLUMNS[i]: item 
                for i, item in enumerate(raw_data)
                if RAW_DATA_COLUMNS[i] is not None  # 'None' identifies data items we don't care to extract
            }
            if keyed_data[OK.MAIN_ID] in preprocessed_data.keys():
                duplicate_data_ct += 1
                continue
            
            # raw data dict index in total_keyed_data via "main_id" (ostensibly UID)
            preprocessed_data[keyed_data[OK.MAIN_ID]] = keyed_data
            completed_rows_ct += 1
        
        preprocess_stats[raw_data_file_name] = {
            "non_data_rows_ct": non_data_rows_ct,
            "completed_rows_ct": completed_rows_ct,
            "duplicate_data_ct": duplicate_data_ct
        }

    print("Preprocessing complete. Stats:")
    preprocess_stats_table = PrettyTable()
    preprocess_stats_table.set_style(TableStyle.PLAIN_COLUMNS)
    preprocess_stats_table.field_names = [
        "File name", 
        "# of non-data rows", 
        "# of preprocessed rows", 
        "# of duplicate data rows"
    ]
    for raw_data_file_name in preprocess_stats.keys():
        preprocess_stats_table.add_row([
            raw_data_file_name,
            preprocess_stats[raw_data_file_name]["non_data_rows_ct"],
            preprocess_stats[raw_data_file_name]["completed_rows_ct"],
            preprocess_stats[raw_data_file_name]["duplicate_data_ct"]
        ])
    print(preprocess_stats_table)
    print(f"""Total # of duplicate rows: {sum([
        preprocess_stats[raw_data_file_name]["duplicate_data_ct"] 
        for raw_data_file_name in preprocess_stats.keys()
    ])}""")
    print(f"Total # of unique rows: {len(preprocessed_data.keys())}")
    print('\n')

    parsed_data: dict = {}
    print("Working basic parsing & type conversion over extracted objects...")
    for main_id, obj_data in tqdm(
        preprocessed_data.items(), 
        desc="...", 
        total=len(preprocessed_data),
        ncols=150
    ):
        for obj_key in obj_data.keys():

            if obj_key == OK.MAIN_ID:
                # obj_data["og_main_id"] = obj_data["main_id"]  # store unprocessed value of main_id for posterity
                obj_data[OK.MAIN_ID] = parse_main_id(obj_data[OK.MAIN_ID])

            elif obj_key in (
                OK.RADIAL_VEL,

                OK.MAGNITUDE_CAP_U, OK.MAGNITUDE_CAP_B, OK.MAGNITUDE_CAP_V,
                OK.MAGNITUDE_CAP_R, OK.MAGNITUDE_CAP_G, OK.MAGNITUDE_CAP_I,
                OK.MAGNITUDE_CAP_J, OK.MAGNITUDE_CAP_H, OK.MAGNITUDE_CAP_K,
                OK.PHOTOMETRIC_F150W, OK.PHOTOMETRIC_F200W, OK.PHOTOMETRIC_F444W,
                OK.MAGNITUDE_LIL_U, OK.MAGNITUDE_LIL_G, OK.MAGNITUDE_LIL_R,
                OK.MAGNITUDE_LIL_I, OK.MAGNITUDE_LIL_Z,

                OK.PROPER_MOTION_NOF_MES,
                OK.PROPER_MOTION_RA, OK.PROPER_MOTION_RA_ERR,
                OK.PROPER_MOTION_DEC, OK.PROPER_MOTION_DEC_ERR,
            
                OK.PARALLAX_NOF_OF_MES,
                OK.PARALLAX, OK.PARALLAX_ERR,
            
                OK.DISTANCE_NOF_MES,
                OK.DISTANCE, OK.DISTANCE_MINUS_ERR, OK.DISTANCE_PLUS_ERR,
            
                OK.DIAMETER_NOF_MES,
                OK.DIAMETER, OK.DIAMETER_ERR,
            
                OK.FE_H_NOF_MES,
                OK.EFFECTIVE_TEMP, OK.LOG_G,
                OK.FE_H_INDEX,
            
                OK.ROTATION_N,
                OK.ROTATION_VEL, OK.ROTATION_VEL_ERR,
                OK.ROTATION_NOF_MES
            ):
                obj_data[obj_key] = parse_numeric_val(obj_data[obj_key])

            else:
                if obj_data[obj_key].strip() == '':
                    obj_data[obj_key] = None

        # re-key by processed main_id.
        # working dict from here on out.
        parsed_data[obj_data[OK.MAIN_ID]] = obj_data

    print('\n')

    print("Checking data integrity, parsing celestial coordinates...")
    for main_id, obj_data in tqdm(
        parsed_data.items(), 
        desc="...", 
        total=len(parsed_data),
        ncols=150
    ):
        if obj_data[OK.DISTANCE] == 0 and obj_data[OK.MAIN_ID] != "Sol":  # bad distance data
            obj_data[OK.DISTANCE] = None
        
        elif None in (obj_data["dist"], obj_data[OK.DISTANCE_UNIT]):  # lacking units, distance value is meaningless
            obj_data[OK.DISTANCE] = None

        elif obj_data[OK.DISTANCE_UNIT] != "pc":  # distance unit something other than parsecs; usually extragalactic
            match obj_data[OK.DISTANCE_UNIT]:
                case "kpc": obj_data[OK.DISTANCE] *= 1e3
                case "Mpc": obj_data[OK.DISTANCE] *= 1e6
                case "Gpc": obj_data[OK.DISTANCE] *= 1e9
                case _: obj_data[OK.DISTANCE] = None  # unrecognized distance unit
            obj_data[OK.DISTANCE_UNIT] = "pc"

        # parse celestial coordinates from exracted strings
        do_strict_coordinate_parsing = False
        obj_data[OK.ICRS_J2000_RA] = parse_coordinates(obj_data[OK.ICRS_J2000_RA], fmt='h m s', strict=do_strict_coordinate_parsing)
        obj_data[OK.ICRS_J2000_DEC] = parse_coordinates(obj_data[OK.ICRS_J2000_DEC], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[OK.ECLIPTIC_2000_LON] = parse_coordinates(obj_data[OK.ECLIPTIC_2000_LON], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[OK.ECLIPTIC_2000_LAT] = parse_coordinates(obj_data[OK.ECLIPTIC_2000_LAT], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[OK.GALACTIC_LON] = parse_coordinates(obj_data[OK.GALACTIC_LON], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[OK.GALACTIC_LAT] = parse_coordinates(obj_data[OK.GALACTIC_LAT], fmt='d m s', strict=do_strict_coordinate_parsing)
    print('\n')


    print("Performing coordinate system transformations...")
    # TO-DO: Get stats on # of objects w/o adequate coordinates & positions
    for main_id, obj_data in tqdm(
        parsed_data.items(), 
        desc="...", 
        total=len(parsed_data),
        ncols=150
    ):
        # normalize to radian values
        if None not in (obj_data[OK.ICRS_J2000_RA], obj_data[OK.ICRS_J2000_DEC]):
            obj_data[OK.ICRS_J2000_RA_RAD] = hms_to_radians(obj_data[OK.ICRS_J2000_RA])
            obj_data[OK.ICRS_J2000_DEC_RAD] = dms_to_radians(obj_data[OK.ICRS_J2000_DEC])
        else:
            obj_data[OK.ICRS_J2000_RA_RAD] = None
            obj_data[OK.ICRS_J2000_DEC_RAD] = None     

        if None not in (obj_data[OK.ECLIPTIC_2000_LON], obj_data[OK.ECLIPTIC_2000_LAT]):
            obj_data[OK.ECLIPTIC_2000_LON_RAD] = hms_to_radians(obj_data[OK.ECLIPTIC_2000_LON])
            obj_data[OK.ECLIPTIC_2000_LAT_RAD] = dms_to_radians(obj_data[OK.ECLIPTIC_2000_LAT])
        else:
            obj_data[OK.ECLIPTIC_2000_LON_RAD] = None
            obj_data[OK.ECLIPTIC_2000_LAT_RAD] = None

        if None not in (obj_data[OK.GALACTIC_LON], obj_data[OK.GALACTIC_LAT]):
            obj_data[OK.GALACTIC_LON_RAD] = hms_to_radians(obj_data[OK.GALACTIC_LON])
            obj_data[OK.GALACTIC_LAT_RAD] = dms_to_radians(obj_data[OK.GALACTIC_LAT])
        else:
            obj_data[OK.GALACTIC_LON_RAD] = None
            obj_data[OK.GALACTIC_LAT_RAD] = None 
        
        # calculate spherical coordinates from equatorial coordinate system values;
        # then, calculate Cartesian (x, y, z) from spherical coordinates;
        # ecliptic and galactic coordinates not yet used.
        if None not in (obj_data[OK.ICRS_J2000_RA_RAD], 
                        obj_data[OK.ICRS_J2000_DEC_RAD], 
                        obj_data[OK.DISTANCE]):
            obj_data[OK.SPHERICAL_COORDS] = equatorial_to_spherical((
                obj_data[OK.ICRS_J2000_RA_RAD], 
                obj_data[OK.ICRS_J2000_DEC_RAD], 
                obj_data[OK.DISTANCE]
            ))
            obj_data[OK.SPATIAL_COORDS] = spherical_to_cartesian(obj_data[OK.SPHERICAL_COORDS])

    print('\n')


    print(f'Serializing object data...')
    for main_id, obj_data in tqdm(
        parsed_data.items(), 
        desc="...", 
        total=len(parsed_data),
        ncols=150
    ):
        


    print(f"Writing uncompressed JSON \"{PROCESSED_DATA_FILE_NAME}\" ...")
    with open(PROCESSED_DATA_DIR / PROCESSED_DATA_FILE_NAME, "w") as file:
        json.dump(parsed_data, file, indent=4)

    print(f"Writing compressed JSON \"{ZIP_ARCHIVE_FILE_NAME}\" ...")
    with zipfile.ZipFile(
        PROCESSED_DATA_DIR / ZIP_ARCHIVE_FILE_NAME, 
        "w", 
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:
        zip_file.write(
            PROCESSED_DATA_DIR / PROCESSED_DATA_FILE_NAME, 
            arcname=PROCESSED_DATA_FILE_NAME)



if __name__ == "__main__":
    process_raw_data()
