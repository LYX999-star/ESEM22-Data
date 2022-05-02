# Read bug-fix related files from the specified path
def get_bug_fixed_files(path):
    bug_fixed_files = []

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            bug_fixed_files.append(line.split('\n')[0])

    return bug_fixed_files
