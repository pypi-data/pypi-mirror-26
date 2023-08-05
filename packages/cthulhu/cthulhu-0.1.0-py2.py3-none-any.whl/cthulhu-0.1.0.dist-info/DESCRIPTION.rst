cthulhu
=======

Ionospheric diagnostics and tools. Mostly designed to work with the information provided by RTS calibration logs for EoR analysis, but will work with any other positional data.

Usage
-----
A simple usage of cthulhu is given in "cthulhu_wrapper.py". Alternatively, for integration with another script or somesuch:

        from cthulhu.reconstruct import Obsid
        from cthulhu.plot_tools import generate_diagnostic_figure, raw_and_tec
        obj = Obsid(([ra, dec, ra_shifts, dec_shifts]))
        generate_diagnostic_figure(obj)
        raw_and_tec(obj)

where `ra`, `dec`, `ra_shifts` and `dec_shifts` are lists or numpy arrays containing expected and apparent positions of sources due to ionospheric activity. This will generate plots in the present working directory under "plots" and "raw\_and\_tec".

If interfacing with RTS logs, cthulhu includes scripts to convert RTS logs to pickles, JSONs and YAMLs. These intermediate files are useful because interfacing directly with an RTS log is much slower, and occupy much smaller volumes. Pickles will be approximately one-third the size of a JSON or YAML, but need to be unpacked before being inspected, and are not compatible across all versions of python and computer architectures. In addition, pickles can execute arbitrary code upon opening, so avoid using them whenever possible. YAML is also a lot more readable than JSON, as well as contained in a smaller file size, so use YAML if you can!

Limitations
-----------
Currently, cthulhu expects coordinates to be in a celestial reference frame ($\alpha$, $\delta$). However, no coordinate transformations (or etc.) are performed with common operations, so your resulting plots will simply use the values of your input data's coordinate system with default RA/Dec. labels. Other coordinates could be incorporated in the future, but is beyond the scope of this work.

Modelling and correcting the "ionosphere" from the data is not implemented correctly yet, although this will not involve much work.

Bugs? Inconsistencies?
----------------------
Absolutely! If you find something odd, let me know and I'll attempt to fix it ASAP.

Contact
-------
christopherjordan87 -at- gmail.com

Dependencies
------------
- python 2.7.x or 3.x
- numpy
- scipy
- astropy
- matplotlib
- pyGrad2Surf (available on my [GitHub](https://github.com/cjordan/pyGrad2Surf))

Optional dependencies
---------------------
- PyYAML (human-readable intermediate format, really nice!)


