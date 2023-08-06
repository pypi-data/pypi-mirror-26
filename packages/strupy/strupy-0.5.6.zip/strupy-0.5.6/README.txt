*************************************************************************
*                                                                       *
*                            StruPy 0.5                                 *
*            Structural engineering design Python package               *
*                                                                       *
*        (c) 2015-2017 Lukasz Laba  (e-mail : lukaszlab@o2.pl)          *
*                                                                       *
*************************************************************************

StruPy is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

StruPy is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar; if not, write to the Free Software
Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

-------------------------------------------------------------------------
* Visible changes:
-------------------------------------------------------------------------
  StruPy 0.5.6
  - concrete.SteelSection added
  StruPy 0.5.5
  - concrete.RcPanelDataLoader upgraded for Robot2016
  StruPy 0.5.4
  - concrete.RcPanelDataLoader upgraded to Mecway7
  StruPy 0.5.3
  - strupy.x_graphic package updated (caused by dxfstructure)
  StruPy 0.5.2
  - concrete.RcPanelToolbox added (cut_peak, smooth and anchore inside)
  - concrete.RcPanel family updated
  - steel.SectionBase optimized (speedmode paremeter added)
  - steel profile class acc. EC3 implemented
  StruPy 0.5.1
  - strupy.steel.Bolt modules created
  - strupy.x_graphic package updated
  StruPy 0.4.7
  - strupy.concrete.RcRecSectSolver corrected
  StruPy 0.4.6
  - concrete.RcPanelDataLoader upgraded (Mecway input interface)  
  StruPy 0.4.5
  - concrete.RcPanel modules upgraded  
  StruPy 0.4.4
  - concrete.RcPanelDataLoader upgraded  
  StruPy 0.4.3
  - concrete.RcPanelDataLoader upgraded  
  StruPy 0.4.2
  - concrete.RcPanel modules upgraded  
  StruPy 0.4.1
  - some strupy.concrete modules optimized
  - concrete.RcPanel modules created  
  StruPy 0.3.4
  - strupy.concrete.RcRecSectSolver corrected
  StruPy 0.3.3
  - some strupy.concrete modules optimized  
  StruPy 0.3.2
  - some strupy.concrete modules optimized  
  StruPy 0.3.1
  - strupy.steel package upgraded
  - strupy.x_graphic package created  
  StruPy 0.2
  - steel section database created (SectionBase class in strupy.steel)  
  StruPy 0.1
  - some functionality for conncrete deisgn was added  

-------------------------------------------------------------------------
* Prerequisites: 
-------------------------------------------------------------------------
  
Python 2.7.
  Non-standard Python library needed (tested version):
  - Unum 4.1
  - matplotlib 1.4.2 (not necessary - only for a few ploting function needed)
  - PyQt4 1.4.2 (not necessary - only for strupy.x_graphic package needed)
  - numpy 1.8.2 (not necessary - for concret.RcPanel and steel.Bolt family needed)
  - xlrd 0.9.4 (not necessary - only for Concrete.RcPanelDataLoader needed)  
  - dxfwrite 1.2.0 (not necessary - only for Concrete.RcPanelViewer needed)
  - easygui (not necessary - only for Concrete.RcPanelDataLoader)
  - pyautocad 0.2.0 (not necessary - only for strupy.x_graphic package needed)
  
-------------------------------------------------------------------------
* To install StruPy:
-------------------------------------------------------------------------

  After the Python and needed library was installed, install StruPy 
  by typing "pip install strupy".
  
  Windows and Linux tested.
  
-------------------------------------------------------------------------
* Other information :
-------------------------------------------------------------------------

  - Project website: http://struthon.org
  - Git repo: https://bitbucket.org/struthonteam/strupy
  - E-mail : lukaszlab@o2.pl, struthon@gmail.com

=========================================================================