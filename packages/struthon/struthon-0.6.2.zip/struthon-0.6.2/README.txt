*************************************************************************
*                                                                       *
*                           Struthon 0.6                                *
*           Structural engineering design Python applications           *
*                                                                       *
*         (c) 2015-2017 Lukasz Laba  (e-mail : lukaszlab@o2.pl)         *
*                                                                       *
*************************************************************************

Struthon is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

Struthon is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

-------------------------------------------------------------------------
* Visible changes:
-------------------------------------------------------------------------
  Struthon 0.6.2
  - new application StruthonSteelMember (buckling analysis available)
  - StruthonSteelMonoSection application removed
  Struthon 0.5.4
  - ConcretePanel to Mecway7 upgraded
  Struthon 0.5.3
  - DxfStructure integrated
  Struthon 0.5.2
  - StruthonMainPanel - check for updates option added
  - ConcretePanel new features (cut_peak and smooth for reinforcement)
  - SteelMonoSection - profile class acc. EC3 included
  - SteelBrowser and SteelBoltedConnection updated
  Struthon 0.5.1
  - StruthonSteelBoltedConnection added
  - SeePy and Py4Structure integrated
  Struthon 0.4.5.2
  - StruthonConcretePanel save-open corrected
  Struthon 0.4.5
  - StruthonConcretePanel Mecway integrated  
  Struthon 0.4.4
  - StruthonConcretePanel new features (dxf export, multi loadcase, save/open 
  project file)  
  Struthon 0.4.2
  - StruthonConcretePanel upgraded  
  Struthon 0.4.1
  - StruthonConcretePanel application added  
  Struthon 0.3.3
  - StruthonConcreteMonoSection user interface upgraded
  - StruthonConcreteMonoSection M-N chart creating speed improved  
  Struthon 0.3.2
  - no changes  
  Struthon 0.3.1
  - StruthonSteelSectionBrowser application upgraded (section drawing, 
    section groups filter)
  - StruthonSteelMonoSection application added
  Struthon 0.2
  - StruthonSteelSectionBrowser application added
  Struthon 0.1
  - the first working version with StruthonConcreteMonoSection application
  
-------------------------------------------------------------------------
* Prerequisites:
-------------------------------------------------------------------------

  Python 2.7.
  Non-standard Python library list
   Minimal:
    Struthon (https://pypi.python.org/pypi/struthon)
    StruPy (https://pypi.python.org/pypi/strupy)
    NumPy (http://www.numpy.org)
    PyQt4 (https://www.riverbankcomputing.com/software/pyqt)
    Matplotlib (http://matplotlib.org)
    Unum (https://pypi.python.org/pypi/Unum)
    xlrd (https://pypi.python.org/pypi/xlrd)
    dxfwrite (https://pypi.python.org/pypi/dxfwrite)
    easygui (https://pypi.python.org/pypi/easygui)
    pyautocad (https://pypi.python.org/pypi/pyautocad)
   Extra packages to make SeePy available:
    SeePy (https://pypi.python.org/pypi/seepy)
    mistune (https://pypi.python.org/pypi/mistune)
    pillow (https://pillow.readthedocs.io)
    svgwrite (https://pypi.python.org/pypi/svgwrite)
    Extra packages to make py4structure available:
    py4structure (https://pypi.python.org/pypi/py4structure)
   Extra packages to make DxfStructure available:
    dxfstructure (https://pypi.python.org/pypi/dxfstructure)
    ezdxf (https://pypi.python.org/pypi/ezdxf)
    tabulate (https://pypi.python.org/pypi/tabulate)
    mistune (https://pypi.python.org/pypi/mistune)

-------------------------------------------------------------------------
* To install struthon:
-------------------------------------------------------------------------
  
  After the Python and needed library was installed, install Struthon 
  by typing "pip install struthon".

  To run struthon GUI execute the file struthon.py from installed struthon
  package folder - probabiliit is "C:\Python27\Lib\site-packages\struthon"
  For easy run make shortcut on your system pulpit to this file.
  
  There is install instruction on project website, go to:
  https://bitbucket.org/struthonteam/struthon/wiki/installing
  
  Windows and Linux tested.
   
-------------------------------------------------------------------------
* Other information :
-------------------------------------------------------------------------
    
  - Project website: http://struthon.org
  - Git repo: https://bitbucket.org/struthonteam/struthon
  - E-mail : lukaszlab@o2.pl, struthon@gmail.com

=========================================================================