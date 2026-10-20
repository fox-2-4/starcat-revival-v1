"""
This code doesn't need to be fast or efficient.
It just needs to run once on a specific set of data to produce the desired JSON.
"""


from tqdm import tqdm, trange
from pathlib import Path
from prettytable import PrettyTable, TableStyle

from process_funcs import *
from vector_math import *


SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

RAW_DATA_COLUMNS = (
    None, 'main_id', 'obj_type',

    'ICRS_J2000_ra', 'ICRS_J2000_dec',
    'ecliptic_2000_lon', 'ecliptic_2000_lat',
    'galactic_lon', 'galactic_lat',

    'rad_vel',

    'mag_U', 'mag_B', 'mag_V', 'mag_R', 'mag_G', 'mag_I',
    'mag_J', 'mag_H', 'mag_K', 'F150W', 'F200W', 'F444W',
    'mag_u', 'mag_g', 'mag_r', 'mag_i', 'mag_z',
    'sp_type',

    'pm_n', 'pm_ra', 'pm_ra_err', 'pm_dec', 'pm_dec_err',
    'pm_coord_sys', 'pm_bibcode',

    'plx_n', 'plx', 'plx_err',
    'plx_obs_code', 'plx_bibcode',

    'dist_n', 'dist', 'dist_q', 'dist_unit',
    'dist_m_err', 'dist_p_err',
    'dist_method', 'dist_bibcode',

    'diam_n', 'diam', 'diam_q', 'diam_unit', 'diam_err',
    'diam_filter', 'diam_method', 'diam_bibcode',

    'Fe_H_n', 'eff_temp', 'log_g', 'Fe_H_index', 'Fe_H_flag',
    'Fe_H_comp_star', 'Fe_H_cat_no', 'Fe_H_bibcode',

    'rot_n', 'rot_up_vel', 'rot_vel', 'rot_vel_err',
    'rot_nof_mes', 'rot_q', 'rot_bibcode'
)
NOF_RAW_DATA_COLUMNS = len(RAW_DATA_COLUMNS)



def process_raw_data():

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

    for i in trange(len(raw_data_file_paths), desc="Extracting rows...", ncols=150):
        raw_data_file_path = raw_data_file_paths[i]
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
                if RAW_DATA_COLUMNS[i] is not None
            }
            if keyed_data["main_id"] in preprocessed_data.keys():
                duplicate_data_ct += 1
                continue
            
            # raw data dict index in total_keyed_data via "main_id" (ostensibly UID)
            preprocessed_data[keyed_data["main_id"]] = keyed_data
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


    print("Working basic parsing & type conversion over extracted objects...")
    for main_id, obj_data in tqdm(
        preprocessed_data.items(), 
        desc="Working...", 
        total=len(preprocessed_data)
    ):
        for attr_id in obj_data.keys():

            if attr_id == "main_id":
                obj_data["main_id"] = process_main_id(obj_data["mmain_id"])

            elif attr_id in (
                'pm', 'rad_vel',
                'mag_U', 'mag_B', 'mag_V', 'mag_R', 'mag_G', 'mag_I',
                'mag_J', 'mag_H', 'mag_K', 'F150W', 'F200W', 'F444W',
                'mag_u', 'mag_g', 'mag_r', 'mag_i', 'mag_z',
                'pm_n', 'pm_ra', 'pm_ra_err', 'pm_dec', 'pm_dec_err',
                'plx_n', 'plx', 'plx_err',
                'dist_n', 'dist', 'dist_m_err', 'dist_p_err',
                'diam_n', 'diam', 'diam_err',
                'Fe_H_n', 'eff_temp', 'log_g', 'Fe_H_index',
                'rot_n', 'rot_vel', 'rot_vel_err'
            ):
                obj_data[attr_id] = process_numeric_val(obj_data[attr_id])

            else:
                if obj_data[attr_id].strip() == '':
                    obj_data[attr_id] = None
    print('\n')


    print("Checking data integrity, parsing celestial coordinates...")
    for main_id, obj_data in tqdm(
        preprocessed_data.items(), 
        desc="...", 
        total=len(preprocessed_data)
    ):
        if obj_data["dist"] == 0 and obj_data["main_id"] != "Sol":  # bad distance data
            obj_data["dist"] = None
        
        elif None in (obj_data["dist"], obj_data["dist_unit"]):  # lacking units, distance value is meaningless
            obj_data["dist"] = None

        elif obj_data["dist_unit"] != "pc":  # distance unit something other than parsecs; usually extragalactic
            match obj_data["dist_unit"]:
                case "kpc": obj_data["dist"] *= 1e3
                case "Mpc": obj_data["dist"] *= 1e6
                case "Gpc": obj_data["dist"] *= 1e9
                case _: obj_data["dist"] = None  # unrecognized distance unit

        # parse celestial coordinates from exracted strings
        obj_data['equ_ra'] = process_coordinates(obj_data['ICRS_J2000_ra'], fmt='h m s')
        obj_data['equ_dec'] = process_coordinates(obj_data['ICRS_J2000_dec'], fmt='d m s')
        obj_data['ecl_ra'] = process_coordinates(obj_data['ecliptic_2000_lon'], fmt='d m s')
        obj_data['ecl_dec'] = process_coordinates(obj_data['ecliptic_2000_lat'], fmt='d m s')
        obj_data['gal_ra'] = process_coordinates(obj_data['galactic_lon'], fmt='d m s')
        obj_data['gal_dec'] = process_coordinates(obj_data['galactic_lat'], fmt='d m s')
    print('\n')


    print("Performing coordinate calculations...")
    for main_id, obj_data in tqdm(
        preprocessed_data.items(), 
        desc="...", 
        total=len(preprocessed_data)
    ):
        # normalize to radian values
        if obj_data["equ_ra"] is not None: obj_data['equ_ra_rad'] = hms_to_radians(obj_data['equ_ra'])
        if obj_data["equ_dec"] is not None: obj_data['equ_dec_rad'] = dms_to_radians(obj_data['equ_dec'])
        if obj_data["ecl_ra"] is not None: obj_data['ecl_ra_rad'] = dms_to_radians(obj_data['ecl_ra'])
        if obj_data["ecl_dec"] is not None: obj_data['ecl_dec_rad'] = dms_to_radians(obj_data['ecl_dec'])
        if obj_data["gal_ra"] is not None: obj_data['gal_ra_rad'] = dms_to_radians(obj_data['gal_ra'])
        if obj_data["gal_dec"] is not None: obj_data['gal_dec_rad'] = dms_to_radians(obj_data['gal_dec'])

        # calculate spherical coordinates from equatorial coordinate system values;
        # then, calculate Cartesian (x, y, z) from spherical coordinates;
        # ecliptic and galactic coordinates not yet used.
        if None not in (obj_data['equ_ra_rad'], obj_data['equ_dec_rad'], obj_data['dist']):
            obj_data['pos_sph'] = equatorial_to_spherical(
                tuple(obj_data['equ_ra_rad'], obj_data['equ_dec_rad'], obj_data['dist']))
            obj_data['pos_xyz'] = spherical_to_cartesian(obj_data['pos_sph'])



if __name__ == "__main__":
    process_raw_data()
