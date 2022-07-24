from piazza_api import Piazza, exceptions
import json
import pathlib
import os
import time

FILEPATH = os.path.dirname(os.path.realpath(__file__))

class color:
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    NC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Takes in a string like '3-5, 9-10' and returns a set like (3, 4, 5, 9, 10)
def process_selection(selection):
    result = set()
    ranges = selection.split(',')
    for r in ranges:
        t = r.split('-')
        if len(t) == 1:
            i = int(t[0])
            if i < 1 or i > len(classes):
                raise ValueError(f'Invalid selection {i}')
            result.add(i)
        else:
            first, last = t
            for i in range(int(first), int(last)+1):
                if i < 1 or i > len(classes):
                    raise ValueError(f'Invalid selection {i}')
                result.add(i)

    return result

def prettify(c):
    return f"{c['num']} {c['term']} ({c['id']})"


print(f'{color.MAGENTA}Welcome to the Piazza Archiver!{color.NC}')
p = Piazza()
email, password = None, None
try:
    sf = open('SECRETS', 'r')
    secrets = json.load(sf)
    sf.close()
    email, password = secrets['email'], secrets['password']
    print(f'{color.CYAN}Authenticating as {email}{color.NC}')
except:
    print(f'{color.WARNING}SECRETS file missing or invalid. Please enter your credentials below.{color.NC}')

try:    
    p.user_login(email=email, password=password)
except exceptions.AuthenticationError as e:
    print(f'{color.FAIL}Authentication Error: {e}{color.NC}')
    exit(1)
profile = p.get_user_profile()
# f = open('user.json', 'w')
# f.write(json.dumps(profile))

# f.close()
classes = []
ctr = 1
for c in profile['all_classes'].values():
    print(f"{ctr}: {prettify(c)}")
    classes.append(c)
    ctr += 1
print(f'\n{color.MAGENTA}Choose the classes you want to archive.\nExamples:\t1\t2-5\t3-5,9-10{color.NC}')
selection = input('> ')
try:
    selection = process_selection(selection)
except Exception as e:
    print(f'{color.FAIL}Invalid selection: {selection}\n{e}{color.NC}')
    exit(1)

for i in selection:
    c = classes[i-1]
    print(f'{color.BLUE}Archiving {prettify(c)}{color.NC}')
    curr_path = f"{FILEPATH}/{prettify(c)}"
    pathlib.Path(curr_path).mkdir(parents=True, exist_ok=True)
    network = p.network(c['id'])
    info_file = open(f"{curr_path}/info.json", "w")
    info_file.write(json.dumps(c, indent=2))
    info_file.close()
    try:
        print(f"{color.CYAN}Fetching course statistics...{color.NC}")
        stats_file = open(f"{curr_path}/stats.json", "w")
        stats_file.write(json.dumps(network.get_statistics(), indent=2))
        stats_file.close()
        print(f"{color.GREEN}Course stats saved to stats.json. Fetching posts...{color.NC}")
    except Exception as e:
        print(f"{color.FAIL}Failed to fetch stats: {e}{color.NC}")
    posts_file = open(f"{curr_path}/posts.json", "w")
    posts = network.iter_all_posts()
    posts_file.write('{"posts": [\n')
    curr_count = 0
    for post in posts:
        posts_file.write(json.dumps(post, indent=2))
        last = posts_file.tell()
        posts_file.write(",\n")
        curr_count += 1
        print(f"Current progress: {curr_count} posts")
        time.sleep(1)
        # if curr_count % 50 == 0:
        #     print(f"{color.WARNING}Taking a break to avoid timeout...{color.NC}")
        #     time.sleep(60)
    posts_file.seek(last)
    posts_file.write('\n]}\n')
    print(f"{color.GREEN}Successfully archived {curr_count} posts{color.NC}")


    posts_file.close()

print(f"{color.GREEN}All done!{color.NC}")
    