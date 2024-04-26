BUGS_PROMPT = """Act as a programmer to fix this bug
There is a bug in this codebase fix it provided to you
Here is a quick description: {description}
Here is the code: {code}
"""

CLEANER_CODE_PROMPT = """Act as a programmer to clean that code and 
write it in a better way and more pythonic one
Here is the code: {code}"""

POSSIBLE_BUGS_PROMPT = """
Act as a programmer to find possible bug that could occurr in runtime
Here is the code: {code}
"""

DOC_STRING_PROMPT = """
Generate a doc string to that code
Here is the code: {code}
"""

description_needed_commands = [BUGS_PROMPT]