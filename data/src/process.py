# """
# This code doesn't need to be fast or efficient.
# It just needs to run once in a developer environment on a
# very specific set of SIMBAD output to produce the desired data.
# """

import json
import zipfile
from pathlib import Path
from tqdm import tqdm, trange
from prettytable import PrettyTable, TableStyle

from stellar_object import StellarObject as STOB
from process_funcs import *
from vector_math import *


SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent

UNPROCESSED_DATA_DIR = DATA_DIR / "unprocessed"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

UNPROCESSED_DATA_FILE_PATTERN = '*.txt'


OBJ_DB_FILE_NAME = Path('obj_db.json')
OBJ_DB_FILE_PATH = PROCESSED_DATA_DIR / OBJ_DB_FILE_NAME
ZIPPED_OBJ_DB_FILE_NAME = OBJ_DB_FILE_NAME.with_suffix('.zip')
ZIPPED_OBJ_DB_FILE_PATH = PROCESSED_DATA_DIR / ZIPPED_OBJ_DB_FILE_NAME



# The structure of this tuple describes how the data is arranged on the scraped .txt files.
UNPROCESSED_DATA_COLUMN_HEADERS = (
    
    None, STOB.MAIN_ID, STOB.OBJ_TYPE,

    STOB.ICRS_J2000_RA, STOB.ICRS_J2000_DEC,
    STOB.ECLIPTIC_2000_LON, STOB.ECLIPTIC_2000_LAT,
    STOB.GALACTIC_LON, STOB.GALACTIC_LAT,

    STOB.RADIAL_VEL,

    STOB.MAGNITUDE_CAP_U, STOB.MAGNITUDE_CAP_B, STOB.MAGNITUDE_CAP_V,
    STOB.MAGNITUDE_CAP_R, STOB.MAGNITUDE_CAP_G, STOB.MAGNITUDE_CAP_I,
    STOB.MAGNITUDE_CAP_J, STOB.MAGNITUDE_CAP_H, STOB.MAGNITUDE_CAP_K,
    STOB.PHOTOMETRIC_F150W, STOB.PHOTOMETRIC_F200W, STOB.PHOTOMETRIC_F444W,
    STOB.MAGNITUDE_LIL_U, STOB.MAGNITUDE_LIL_G, STOB.MAGNITUDE_LIL_R,
    STOB.MAGNITUDE_LIL_I, STOB.MAGNITUDE_LIL_Z,
    STOB.SPECTRAL_TYPE,

    STOB.PROPER_MOTION_NOF_MES,
    STOB.PROPER_MOTION_RA, STOB.PROPER_MOTION_RA_ERR,
    STOB.PROPER_MOTION_DEC, STOB.PROPER_MOTION_DEC_ERR,
    STOB.PROPER_MOTION_COORD_SYS, STOB.PROPER_MOTION_BIBCODE,

    STOB.PARALLAX_NOF_OF_MES,
    STOB.PARALLAX, STOB.PARALLAX_ERR,
    STOB.PARALLAX_OBS_CODE,
    STOB.PARALLAX_BIBCODE,

    STOB.DISTANCE_NOF_MES,
    STOB.DISTANCE, STOB.DISTANCE_QUALITY, STOB.DISTANCE_UNIT,
    STOB.DISTANCE_MINUS_ERR, STOB.DISTANCE_PLUS_ERR,
    STOB.DISTANCE_METHOD, STOB.DISTANCE_BIBCODE,

    STOB.DIAMETER_NOF_MES,
    STOB.DIAMETER, STOB.DIAMETER_QUALITY, STOB.DIAMETER_UNIT, STOB.DIAMETER_ERR,
    STOB.DIAMETER_FILTER, STOB.DIAMETER_METHOD, STOB.DIAMETER_BIBCODE,

    STOB.FE_H_NOF_MES,
    STOB.EFFECTIVE_TEMP, STOB.LOG_G,
    STOB.FE_H_INDEX, STOB.FE_H_FLAG,
    STOB.FE_H_COMPARISON_STAR,
    STOB.FE_H_CAT_NO, STOB.FE_H_BIBCODE,

    STOB.ROTATION_N,
    STOB.ROTATION_UPPER_VAL, STOB.ROTATION_VEL, STOB.ROTATION_VEL_ERR,
    STOB.ROTATION_NOF_MES, STOB.ROTATION_QUALITY, STOB.ROTATION_BIBCODE

)

NOF_UNRPOCESSED_DATA_COLUMNS = len(UNPROCESSED_DATA_COLUMN_HEADERS)

obj_stack: list[dict] = []
obj_main_id_stack: dict = {}



def check_directory_structure():

    if not DATA_DIR.exists():
        raise FileNotFoundError(f"Main data directory not found: {DATA_DIR}")
    elif not UNPROCESSED_DATA_DIR.exists():
        raise FileNotFoundError(f"Raw data directory not found: {UNPROCESSED_DATA_DIR}")
    elif not PROCESSED_DATA_DIR.exists():
        raise FileNotFoundError(f"Processed data directory not found: {PROCESSED_DATA_DIR}")
    
    print("Identified the following critical directories:",
          '- ' + str(SCRIPT_DIR),
          '- ' + str(DATA_DIR),
          '- ' + str(UNPROCESSED_DATA_DIR),
          '- ' + str(PROCESSED_DATA_DIR),
          '\n',
          sep='\n')



def fetch_unprocessed_files() -> list:
    
    unprocessed_data_file_paths = list(UNPROCESSED_DATA_DIR.rglob(UNPROCESSED_DATA_FILE_PATTERN))

    # no files that fit the file pattern were identified
    if not len(unprocessed_data_file_paths):
        raise FileNotFoundError(f"No files found in unprocessed data directory: {UNPROCESSED_DATA_DIR}")

    # files were identified; log to console
    print(f"Identified the following {len(unprocessed_data_file_paths)} unprocessed files:")
    for unprocessed_data_file_path in unprocessed_data_file_paths:
        print(unprocessed_data_file_path.name)
    print('\n')

    return unprocessed_data_file_paths



def do_preprocess_extraction():

    global obj_stack
    global obj_main_id_stack

    unprocessed_data_file_paths = fetch_unprocessed_files()

    preprocess_stats = {str(unprocessed_data_file_path.name): {}
                        for unprocessed_data_file_path in unprocessed_data_file_paths}

    print('Extracting rows...')

    for unprocessed_data_file_path in tqdm(
        unprocessed_data_file_paths, 
        desc='...', 
        total=len(unprocessed_data_file_paths), 
        ncols=150
    ):
        
        unprocessed_data_file_name = unprocessed_data_file_path.name

        non_data_rows_ct = 0
        completed_rows_ct = 0
        duplicate_data_ct = 0

        try:
            with open(unprocessed_data_file_path, "rt", encoding="utf8") as tsv_file:
                tsv_rows = tsv_file.read().split('\n')
        
        except FileNotFoundError as err:
            print(f"File not processed: {unprocessed_data_file_name}", err, sep='\n')
            continue

        # each TSV row contains all data for one stellar object
        for tsv_row in tsv_rows:
            
            row_data = tsv_row.split('\t')

            if len(row_data) != NOF_UNRPOCESSED_DATA_COLUMNS:
                non_data_rows_ct += 1
                continue
            
            keyed_row_data = {
                UNPROCESSED_DATA_COLUMN_HEADERS[i]: item 
                for i, item in enumerate(row_data)
                if UNPROCESSED_DATA_COLUMN_HEADERS[i] is not None  # 'None' identifies data items we don't care to extract
            }
            
            if keyed_row_data[STOB.MAIN_ID] in obj_main_id_stack.keys():
                duplicate_data_ct += 1
                continue

            obj_stack.append(keyed_row_data)
            obj_main_id_stack[keyed_row_data[STOB.MAIN_ID]] = True  # value doesn't matter
            
            completed_rows_ct += 1
        
        preprocess_stats[unprocessed_data_file_name] = {
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
    for unprocessed_data_file_name in preprocess_stats.keys():
        preprocess_stats_table.add_row([
            unprocessed_data_file_name,
            preprocess_stats[unprocessed_data_file_name]["non_data_rows_ct"],
            preprocess_stats[unprocessed_data_file_name]["completed_rows_ct"],
            preprocess_stats[unprocessed_data_file_name]["duplicate_data_ct"]
        ])
    print(preprocess_stats_table)
    print(f"""Total # of duplicate rows: {sum([
        preprocess_stats[raw_data_file_name]["duplicate_data_ct"] 
        for raw_data_file_name in preprocess_stats.keys()
    ])}""")
    print(f"Total # of unique rows: {len(obj_stack)}")
    print('\n')



def do_basic_type_conversion():

    global obj_stack

    print("Working basic parsing & type conversion over extracted objects...")
    
    for obj_data in tqdm(
        obj_stack, 
        desc="...", 
        total=len(obj_stack),
        ncols=150
    ):
        
        for obj_key in obj_data.keys():

            if obj_key == STOB.MAIN_ID:
                obj_data[STOB.MAIN_ID] = parse_main_id(obj_data[STOB.MAIN_ID])

            # Expected numeric data: attempt to parse. 
            elif obj_key in (

                STOB.RADIAL_VEL,

                STOB.MAGNITUDE_CAP_U, STOB.MAGNITUDE_CAP_B, STOB.MAGNITUDE_CAP_V,
                STOB.MAGNITUDE_CAP_R, STOB.MAGNITUDE_CAP_G, STOB.MAGNITUDE_CAP_I,
                STOB.MAGNITUDE_CAP_J, STOB.MAGNITUDE_CAP_H, STOB.MAGNITUDE_CAP_K,
                STOB.PHOTOMETRIC_F150W, STOB.PHOTOMETRIC_F200W, STOB.PHOTOMETRIC_F444W,
                STOB.MAGNITUDE_LIL_U, STOB.MAGNITUDE_LIL_G, STOB.MAGNITUDE_LIL_R,
                STOB.MAGNITUDE_LIL_I, STOB.MAGNITUDE_LIL_Z,

                STOB.PROPER_MOTION_NOF_MES,
                STOB.PROPER_MOTION_RA, STOB.PROPER_MOTION_RA_ERR,
                STOB.PROPER_MOTION_DEC, STOB.PROPER_MOTION_DEC_ERR,
            
                STOB.PARALLAX_NOF_OF_MES,
                STOB.PARALLAX, STOB.PARALLAX_ERR,
            
                STOB.DISTANCE_NOF_MES,
                STOB.DISTANCE, STOB.DISTANCE_MINUS_ERR, STOB.DISTANCE_PLUS_ERR,
            
                STOB.DIAMETER_NOF_MES,
                STOB.DIAMETER, STOB.DIAMETER_ERR,
            
                STOB.FE_H_NOF_MES,
                STOB.EFFECTIVE_TEMP, STOB.LOG_G,
                STOB.FE_H_INDEX,
            
                STOB.ROTATION_N,
                STOB.ROTATION_VEL, STOB.ROTATION_VEL_ERR,
                STOB.ROTATION_NOF_MES

            ):
                obj_data[obj_key] = parse_numeric_val(obj_data[obj_key])

            # Expected non-numeric value: check for empty data.
            else:
                if obj_data[obj_key].strip() == '':
                    obj_data[obj_key] = None

    print('\n')



def do_coordinate_parsing():

    global obj_stack
    
    print("Checking data integrity, parsing celestial coordinates...")
    
    for obj_data in tqdm(
        obj_stack, 
        desc="...", 
        total=len(obj_stack),
        ncols=150
    ):
        # Bad distance data or object is a Solar System object.
        if obj_data[STOB.DISTANCE] == 0 and obj_data[STOB.MAIN_ID] != "Sol":
            obj_data[STOB.DISTANCE] = None
            obj_data[STOB.DISTANCE_UNIT] = None

        # Numeric parsing failed earlier. Lacking units, distance value is useless and vice versa.
        elif None in (obj_data[STOB.DISTANCE], obj_data[STOB.DISTANCE_UNIT]):
            obj_data[STOB.DISTANCE] = None

        # Distance unit is something other than parsecs; usually extragalactic.
        elif obj_data[STOB.DISTANCE_UNIT] != "pc":
            match obj_data[STOB.DISTANCE_UNIT]:
                case "kpc": obj_data[STOB.DISTANCE] *= 1e3
                case "Mpc": obj_data[STOB.DISTANCE] *= 1e6
                case "Gpc": obj_data[STOB.DISTANCE] *= 1e9
                case _: obj_data[STOB.DISTANCE] = None  # unrecognized distance unit (let's log it)
            obj_data[STOB.DISTANCE_UNIT] = "pc"

        # Attempt to parse celestial coordinates from extracted strings.
        do_strict_coordinate_parsing = False
        obj_data[STOB.ICRS_J2000_RA] = parse_coordinates(obj_data[STOB.ICRS_J2000_RA], fmt='h m s', strict=do_strict_coordinate_parsing)
        obj_data[STOB.ICRS_J2000_DEC] = parse_coordinates(obj_data[STOB.ICRS_J2000_DEC], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[STOB.ECLIPTIC_2000_LON] = parse_coordinates(obj_data[STOB.ECLIPTIC_2000_LON], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[STOB.ECLIPTIC_2000_LAT] = parse_coordinates(obj_data[STOB.ECLIPTIC_2000_LAT], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[STOB.GALACTIC_LON] = parse_coordinates(obj_data[STOB.GALACTIC_LON], fmt='d m s', strict=do_strict_coordinate_parsing)
        obj_data[STOB.GALACTIC_LAT] = parse_coordinates(obj_data[STOB.GALACTIC_LAT], fmt='d m s', strict=do_strict_coordinate_parsing)
    
    print('\n')



def do_coordinate_transformations():

    global obj_stack

    print("Performing coordinate system transformations...")

    # TO-DO: Get stats on # of objects w/o adequate coordinates & positions
    for obj_data in tqdm(
        obj_stack, 
        desc="...", 
        total=len(obj_stack),
        ncols=150
    ):
        
        # Normalize parsed coordinates to radian values.
        if None not in (obj_data[STOB.ICRS_J2000_RA], obj_data[STOB.ICRS_J2000_DEC]):
            obj_data[STOB.ICRS_J2000_RA_RAD] = hms_to_radians(obj_data[STOB.ICRS_J2000_RA])
            obj_data[STOB.ICRS_J2000_DEC_RAD] = dms_to_radians(obj_data[STOB.ICRS_J2000_DEC])
        else:
            obj_data[STOB.ICRS_J2000_RA_RAD] = None
            obj_data[STOB.ICRS_J2000_DEC_RAD] = None     

        if None not in (obj_data[STOB.ECLIPTIC_2000_LON], obj_data[STOB.ECLIPTIC_2000_LAT]):
            obj_data[STOB.ECLIPTIC_2000_LON_RAD] = hms_to_radians(obj_data[STOB.ECLIPTIC_2000_LON])
            obj_data[STOB.ECLIPTIC_2000_LAT_RAD] = dms_to_radians(obj_data[STOB.ECLIPTIC_2000_LAT])
        else:
            obj_data[STOB.ECLIPTIC_2000_LON_RAD] = None
            obj_data[STOB.ECLIPTIC_2000_LAT_RAD] = None

        if None not in (obj_data[STOB.GALACTIC_LON], obj_data[STOB.GALACTIC_LAT]):
            obj_data[STOB.GALACTIC_LON_RAD] = hms_to_radians(obj_data[STOB.GALACTIC_LON])
            obj_data[STOB.GALACTIC_LAT_RAD] = dms_to_radians(obj_data[STOB.GALACTIC_LAT])
        else:
            obj_data[STOB.GALACTIC_LON_RAD] = None
            obj_data[STOB.GALACTIC_LAT_RAD] = None 
        
        # Calculate spherical coordinates from equatorial coordinate system values;
        # then, calculate Cartesian (x, y, z) from spherical coordinates.
        # Ecliptic and galactic coordinates not yet used.
        if None not in (obj_data[STOB.ICRS_J2000_RA_RAD], 
                        obj_data[STOB.ICRS_J2000_DEC_RAD], 
                        obj_data[STOB.DISTANCE]):
            obj_data[STOB.SPHERICAL_COORDS] = equatorial_to_spherical((
                obj_data[STOB.ICRS_J2000_RA_RAD], 
                obj_data[STOB.ICRS_J2000_DEC_RAD], 
                obj_data[STOB.DISTANCE]
            ))
            obj_data[STOB.SPATIAL_COORDS] = spherical_to_cartesian(obj_data[STOB.SPHERICAL_COORDS])

    print('\n')



def do_serialization_and_dumping():

    global obj_stack

    print(f'Serializing object data...')
    
    serial_obj_stack =  []

    for obj_data in tqdm(
        obj_stack, 
        desc="...", 
        total=len(obj_stack),
        ncols=150
    ):
        
        serial_obj_stack.append(STOB.serialize_stellar_obj_data(obj_data))

    print('\n')

    print(f'Dumping serialized object database \"{OBJ_DB_FILE_NAME}\" ...')
    with open(OBJ_DB_FILE_PATH, "w") as file:
        json.dump(serial_obj_stack, file, indent=4)

    print(f"Writing compressed object database \"{ZIPPED_OBJ_DB_FILE_NAME}\" ...")
    with zipfile.ZipFile(ZIPPED_OBJ_DB_FILE_PATH, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        zip_file.write(OBJ_DB_FILE_PATH, arcname=OBJ_DB_FILE_NAME)



def process_raw_data():

    check_directory_structure()
    do_preprocess_extraction()
    do_basic_type_conversion()
    do_coordinate_parsing()
    do_coordinate_transformations()
    do_serialization_and_dumping()



if __name__ == "__main__":
    process_raw_data()
