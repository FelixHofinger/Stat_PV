# StatPV project

Represents a Web-FrontEnd for analyzing cross-section vehicle data & air traffic data. 

## Building
- Install Python 3

  **NOTE:** For Windows 10, it is important to check in the Python install the optional feature "tcl/tk and IDLE".

  For Linux, you may install it with something like
  ```
  sudo dnf install python3-tkinter
  ```
  depending on your distribution.


- Install depending libraries (make sure to be in the virtual environment):
  ```
  pip install -r requirements.txt
  ```
  **NOTE:** Especially unter Windows in can be very painful to install (dependent) libraries,
  since they need to be compiled. If you face any errors with the command above (especially
  with GDAL and Fiona), try installing a wheel (aka precompiled binary for your architecture
  and Python version) manually by 
  1. Going to https://www.lfd.uci.edu/~gohlke/pythonlibs/
  2. Downloading the wheel for your architecture and Python version (encoded e.g. in "cp37" for
     Python 3.7)
  3. Installing the wheel with the following command
     ```
     pip install path/to/downloaded/wheel.whl
     ```

## Running
To run:

```
streamlit run main.py
```
