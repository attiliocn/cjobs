import os
import shutil 
import pathlib
import sys
import configparser

def compare_config_keys(config1, config2, key_path=""):
    keys1 = set(config1.keys())
    keys2 = set(config2.keys())
    unmatched_keys = []

    # Find keys in config1 that are not in config2
    unmatched_keys += [key_path + key for key in keys1.difference(keys2)]

    # Recursively compare subkeys
    for key in keys1.intersection(keys2):
        if isinstance(config1[key], configparser.SectionProxy):
            sub_keys = compare_config_keys(config1[key], config2[key], key_path + key + ".")
            unmatched_keys += sub_keys

    return unmatched_keys

def config_cjobs_defaults(config_dir, config_file):
    CJOBS_DIR = pathlib.Path(sys.argv[0]).parent

    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"Directory created: {config_dir}")
        shutil.copy2(f"{CJOBS_DIR}/cjobsrc", config_dir)
        print(f"File copied to directory: cjobsrc -> {config_dir}")
    else:
        print(f"Directory already exists: {config_dir}")

        if os.path.isfile(config_file):
            print(f"Configuration file already exists: {config_file}\n")

            with open(config_file) as f:
                current_config = configparser.ConfigParser()
                current_config.read_file(f)

            with open(f"{CJOBS_DIR}/cjobsrc") as f:
                default_config = configparser.ConfigParser()
                default_config.read_file(f)

            # Compare the keys
            unmatched_keys = compare_config_keys(default_config, current_config)

            if not unmatched_keys:
                    print("Your configuration matches the current version of the cjobsrc file.")
                    print("Check if the current settings are correct for this cluster")
            else:
                print("Your configuration does not match the current version of the cjobsrc file.")
                print("Unmatched settings:")
                for key in unmatched_keys:
                    print(f"\t{key}")

                print()    
                print("Check your cjobsrc for any typos.")
                print("Please refer to the documentation for the recommended values for these settings")
                print("depending on the cluster you are configuring.")
                

