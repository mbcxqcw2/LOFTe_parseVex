# INTRODUCTION:

In-progress library for parsing a vdif .vex file for an e-MERLIN observation.
Author: C. Walker

Currently, this library can take an input .vex file and output a dictionary of
information about each scan within the observation of the .vex file.

On Charlie's machine, this git repo is stored at /Users/c.walker/LOFTe_parseVex/

# REQUIREMENTS:
- numpy
- astropy

# TO USE:
After git cloning this repository and adding it to your python path do:
```
>from LOFTe_parseVex_lib import parse_vex, get_vex_sched
>vex_data = parse_vex(<vexfile.vex>)
>schedule_info = get_vex_sched(vex_data)
```
where `<vexfile.vex>` is the location of the .vex file to be parsed. The scans within the observation can then be seen with:

```
>schedule_info.keys()
```

For a given scan, e.g. scan number `0001`, the scan information can then be seen with:

```
>schedule_info['0001'].keys()
```


