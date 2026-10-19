
from tqdm import trange
from pathlib import Path
from prettytable import PrettyTable, TableStyle

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



def parse_raw_data():

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
    print(f"Total # of rows: {len(preprocessed_data.keys())}")



if __name__ == "__main__":
    parse_raw_data()
