import common

# get hart id from the line
def get_hartid(line):
    regex = r"C(\d+)*:(\s+)(\d+) \[(\d+)\]"
    match = common.match_regex(regex, line)
    if match is not None:
        return match[0]
    
# get valid bit from the line
def get_valid(line):
    regex = r"C(\d+)*:(\s+)(\d+) \[(\d+)\]"
    match = common.match_regex(regex, line)
    if match is not None:
        return match[3]

# parse cycle count from the line
def get_cycles(line):
    regex = r"C(\d+)*:(\s+)(\d+) \[(\d+)\]"
    match = common.match_regex(regex, line)
    if match is not None:
        return match[2]

# parse instruction (hex) from the line
def get_inst(line):
    regex = r"inst=\[([0-9a-fA-F]+)\]"
    match = common.match_regex(regex, line)
    if match is not None:
        return match