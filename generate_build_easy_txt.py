import os

# input paths
PATH_TO_THOR = "../../../../../../../../../"
COMPONENTS_PATH = PATH_TO_THOR+"/ex/ex/"
TROC_PATH = PATH_TO_THOR + "/Projects/ex/"
projects_paths = [TROC_PATH + "APP/",
            TROC_PATH + "ANM/",
            TROC_PATH + "CFG/",
            TROC_PATH + "ESS/"]


# output paths
OUTPUT_BASE = "-I../../../../../../../../../"

def find_directories_with_extensions(root_dir, extensions):
    # Store directories that contain desired file extensions
    matching_dirs = set()

    # Traverse the directory tree
    for subdir, dirs, files in os.walk(root_dir):
        # Check each file in the current subdirectory
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                matching_dirs.add(subdir)
                break  # No need to check more files in this directory
    
    return list(matching_dirs)

def modify_directories(list_of_directories: list[str], output_path: str) -> list[str]:
    ret_list = []
    for dir in list_of_directories:
        ret_list.append(output_path + dir.split("//")[1].replace('\\', '/'))
    return ret_list

with open("_build_easy_axivion_flags_ARM_AXN.txt", "w") as file:
    file.write("""--flags

flags

flags

-Iinclude paths
""")


    # Example usage:
    required_extensions = ['.h', '.c']

    # Get the list of directories containing the required file extensions
    directories = find_directories_with_extensions(COMPONENTS_PATH, required_extensions)
    directories = modify_directories(directories, OUTPUT_BASE)

    # Print the list of directories
    for directory in directories:
        file.write(directory + "\n")

    for project_path in projects_paths:
        directories = find_directories_with_extensions(project_path, required_extensions)
        
        directories = modify_directories(directories, OUTPUT_BASE)

        # Print the list of directories
        for directory in directories:
            file.write(directory + "\n")