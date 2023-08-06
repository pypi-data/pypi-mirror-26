# resswitch 


<img src="https://github.com/danieljosesilva/resSwitch/blob/master/resswitch/ico/resSwitch.ico" height="30"> resswitch v0.1.4

GUI for analyzing resistive switching data. Useful for analyzing experiments involving memristor
transport measurements. This program treats raw data of resistive switching measurements and generates several key statistical values.
It can save treated data with the extension .rs and export data for plotting with other software.

author: Daniel Silva (djsilva99@gmail.com) <br> current version: v0.1.4

![resSwitch-screenshot](https://github.com/danieljosesilva/resSwitch/blob/master/img/resswitch.gif)

## Installation

### Linux

To install simply use the pip package manager:

```bash
pip install resswitch
```

To open the GUI type in the bash shell:

```bash
$ resswitch
```

#### windows

The latest version compatible with windows is v0.1.3.

##### Pre-installation

Python and pip package manager must be installed beforehand. Go directly to installation if already installed.

install the latest version of <a href='https://www.python.org/downloads/windows/'>python2.7</a>.

Download get-pip.py from <a href='https://pip.pypa.io/en/stable/installing/'>https://pip.pypa.io/en/stable/installing/</a> and execute the file.

##### Installation

Open the command line and type:

```bash
pip install resswitch==0.1.3
```

To open the resswitch window you can either open the python shell and type

```python
import resswitch
resswitch.resSwitch.ResSwitch().mainloop()
```

or you can download the resswitch-windows.py file and double click it.