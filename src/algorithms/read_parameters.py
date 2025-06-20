import yaml
import os


def yaml_to_list(filepath):
    """
    Reads a YAML file and converts its content into a plain Python list.
    This function expects the YAML file to contain a simple list (no nested structures).
    Args:
        filepath (str): The path to the YAML file.

    Returns:
        list: A plain Python list containing the data from the YAML file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        yaml.YAMLError: If there is an error parsing the YAML file.
        TypeError: If the YAML content is not a list.
        Exception: For any other unexpected errors during file reading.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"The file '{filepath}' was not found.")

    try:
        with open(filepath, "r") as file:
            data = yaml.safe_load(file)
        if not isinstance(data, list):
            raise TypeError(
                f"YAML content is not a plain list. Found type: {type(data)}. "
                "Expected a list at the root of the YAML file."
            )
        return data
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file '{filepath}': {e}")
    except Exception as e:
        raise Exception(f"An unexpected error occurred while reading '{filepath}': {e}")
