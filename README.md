# INTRODUCTION:

In-progress library for parsing a vdif .vex file for an e-MERLIN observation.
Author: C. Walker

Currently, this library can take an input .vex file and output a dictionary of
information about each scan within the observation of the .vex file.

# REQUIREMENTS:
- numpy
- astropy

# TO USE:

```
>vex_data = parse_vex(<vexfile>)
>schedule_info = get_vex_sched(vex_data)
```
where `vexfile` is the location of the .vex file to be parsed. The scans within the observation can then be seen with:

```
>schedule_info.keys()
```

For a given scan, e.g. scan number `0001`, the scan information can then be seen with:

```
>schedule_info['0001'].keys()
```


