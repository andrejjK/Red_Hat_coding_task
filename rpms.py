import sys
import requests
import re
import ijson
from datetime import datetime

RAWHIDE_MAIN_URL = "https://kojipkgs.fedoraproject.org/compose/rawhide"

def get_recent_composes(max_days_ago):
    """Find Rawhide composes built in the last <max_days_ago> days."""

    # Get the list of composes from the main page
    rawhide_page = requests.get(RAWHIDE_MAIN_URL)
    rawhides = re.findall(r'href="Fedora-Rawhide-\d{8}\.n\.0', rawhide_page.text)

    today = datetime.today()

    for i in rawhides:
        # Get build date string
        date = re.search(r'\d{8}', i)
        # Convert to datetime object
        dt_obj = datetime.strptime(date.group(), "%Y%m%d")
        # Calculate the offset from today
        delta = today - dt_obj
        days_ago = abs(delta.days)
        # Print results
        if days_ago >= 0 and days_ago <= max_days_ago:
            print(f"Fedora-Rawhide-{date.group()}.n.0")

def find_changed_packages(old_compose, new_compose):
    """Find packages that were added, removed, or changed between two composes."""

    # Read packages from rpms.json files
    print(f"Reading packages from compose {old_compose}")
    old_rpms = read_packages(old_compose)
    print(f"Reading packages from compose {new_compose}")
    new_rpms = read_packages(new_compose)

    # Find packages added in the new version
    print(f"\nSearching packages added in the new compose\n")
    old_rpm_names = {name for name, _ in old_rpms}
    added_rpms = [rpm for rpm in new_rpms if rpm[0] not in old_rpm_names]

    print(f"\n##### Added packages: #####\n")
    for i in added_rpms:
        print(f"{i[0]}-{i[1]}")

    # Find packages removed in the new version
    print(f"\nSearching packages removed in the new compose\n")
    new_rpm_names = {name for name, _ in new_rpms}
    removed_rpms = [rpm for rpm in old_rpms if rpm[0] not in new_rpm_names]

    print(f"\n##### Removed packages: #####\n")
    for i in removed_rpms:
        print(f"{i[0]}-{i[1]}")

    # Find packages with changed versions
    print(f"\nSearching packages with changed versions\n")
    changed_rpms = [rpm for rpm in new_rpms if rpm[0] in old_rpm_names]

    print(f"\n##### Changed packages: #####\n")
    for i in changed_rpms:
        # Get the old version of the rpm
        old_version = [rpm[1] for rpm in old_rpms if rpm[0] == i[0]][0]
        # Get the new version of the rpm
        new_version = i[1]
        # Print if the version has changed
        if old_version != new_version:
            print(f"{i[0]} {old_version} -> {new_version}")

def read_packages(compose_date):
    """Read packages from rpms.json file and return a list of tuples (name, version)."""

    rpms_url = f"{RAWHIDE_MAIN_URL}/Fedora-Rawhide-{compose_date}.n.0/compose/metadata/rpms.json"
    rpms_stream = requests.get(rpms_url, stream=True)

    # Read packages from rpms.json file stream
    rpms = []
    for rpm, _ in ijson.kvitems(rpms_stream.raw, 'payload.rpms.Everything.x86_64'):
        # Get package name
        rpm_name = rpm.rsplit('-', 2)[0]
        # Get package version
        rpm_version = '-'.join(rpm.rsplit('-', 2)[1:]).rsplit('.', 2)[0]
        # Store name and version tuple in a list
        rpm_item = (rpm_name, rpm_version)
        rpms.append(rpm_item)

    return rpms

# Process CLI arguments
args = sys.argv[1:]

match len(args):
    case 0:
        print("""Usage:
            python3 rpms.py <max_days_ago>
        OR
            python3 rpms.py <old_compose> <new_compose>""")
    case 1:
        get_recent_composes(int(args[0]))
    case 2:
        find_changed_packages(args[0], args[1])
    case _:
        print("Error: Must provide either one (number) or two (compose) arguments.")
        sys.exit(1)
