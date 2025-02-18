def extract_and_deduplicate_names(input_file, output_file):
    """
    Extracts names from a file, removes duplicates, and writes them to another file.

    Args:
        input_file: Path to the input text file with full names.
        output_file: Path to the output text file for unique names.
    """

    unique_names = set()  # Use a set to store unique names

    try:
        with open(input_file, 'r', encoding='utf-8') as infile:
            for line in infile:
                parts = line.strip().split()  # Split the line into parts
                if parts:  # Check if the line is not empty
                    name = parts[-1]  # Extract the last part as the name
                    unique_names.add(name)  # Add the name to the set (duplicates are ignored)

        with open(output_file, 'w', encoding='utf-8') as outfile:
            for name in unique_names:
                outfile.write(name + '\n')  # Write each unique name to a new line

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("number of name: ", len(unique_names))



input_file="fullname.txt"
output_file="sample_vi_name.txt"

extract_and_deduplicate_names(input_file, output_file)
print(f"Unique names have been written to '{output_file}'")
