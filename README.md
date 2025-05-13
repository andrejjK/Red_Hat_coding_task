# Red_Hat_coding_task

## Usage:
1. Output a list of Rawhide composes built in the past N days:

`python3 rpms.py N`

> Note: N must be a number
> 
> Example: `python3 rpms.py 10`

2. Output a change-set of packages for the x86_64 architecture between two specified
Rawhide composes (`C1`, `C2`):

`python3 rpms.py C1 C2`

> Note: C1 and C2 must be specified as build date in the format `YYYYMMDD`.
> 
> Example: `python3 rpms.py 20250501 20250509`

## Remarks:
- For faster task progress, exceptions and error cases are not handled (i.e. invalid inputs, type checks and value checks). Only the behavior specified in the assignment is implemented.
