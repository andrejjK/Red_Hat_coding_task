# Red_Hat_coding_task
## Usage:
Output a list of Rawhide composes built in the past N days:
`python3 rpms.py N`
> Note: N must be a number

Output a change-set of packages for the x86_64 architecture between two specified
Rawhide composes (`C1`, `C2`):
`python3 rpms.py C1 C2`
> Note: C1 and C2 must be specified as build date in the format `YYYYMMDD`.
