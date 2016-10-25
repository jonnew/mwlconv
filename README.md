### mwlconv
Utility for converting between various data file formats used in the MWL@MIT.

  - Oat position files
  - AD position files
  - Open Ephys spike files
  - etc.

Most are aimed at converting more modern (but not nessesarly improved...)
formates back to formats compatible with the MWL's analysis suite

https://github.com/wilsonlab/mwsoft64

This project is not even close to exhaustive, but is aimed at fulfilling
the author's processing requirements and desire to make use, especially,
of the xclust cluster cutting program. 


#### Installation
Assuming all dependencies are met, simply navigate to the root directory and
```
python setup.py install
```

#### Usage
To get help, 
```
mwlconv --help
```

Each conversion routine is specified by the first position argument:

```
mwlconv routine [OPTIONS]
```

Some routines are:

 1. __oat2xpos__
    Create `xpos` file from Oat's json format. Output is a simple position table
    that is readable by several tools in the MWLsoft suite (notably, spikeparms2,
    which allows the creation of .xparms files by those who are using legacy
    recording equipment in the MWL instead of Open Ephys tools).
    
    Example:

    ```
    mwlconv oat2xpos -i pos.json -o pos.xpos # "Single Diode" position
    oat2xpos front.json back.json -o pos.xpos # "Dual Diode"
    ```

 1. __oe2tt__
    Convert Open Ephys `.spike` format to the `.tt` format which results from
    `adextract` and is is readable by several tools in the MWLsoft suite
    (notably, spikeparms2, which allows the creation of .xparms files by those
    who are using legacy recording equipment in the MWL instead of Open Ephys
    tools).
    
    Example:

    ```
    mwlconv oe2tt -i TT0.spike -o TT0.tt 
    ```
