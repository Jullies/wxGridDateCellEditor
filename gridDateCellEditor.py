'''
Custom Editted to work with Python3
'''

import wx.grid
class DatePickerEditor(wx.grid.GridCellEditor):
    """
    This GridCellEditor allows you to date pick from a calendar inside the
    cell of a grid.
    """
    Grid = wx.grid
    def __init__(self):
        # Constructor
        Grid = wx.grid
        Grid.GridCellEditor.__init__(self)
    # end __init__
 
    def Create(self, parent, id, evtHandler, *args):
        """
        Called to create the control, which must derive from wx.Control.
        """
        self._picker = wx.adv.DatePickerCtrl(parent, style=wx.adv.DP_DROPDOWN)
        self.startingDate = None
        self.SetControl(self._picker)
 
        if evtHandler:
            self._picker.PushEventHandler(evtHandler)
    # end Create
 
    def SetSize(self, rect, *args):
        """
        Called to position/size the edit control within the cell rectangle.
        If you don't fill the cell (the rect) then be sure to override
        PaintBackground and do something meaningful there.
        """
        self._picker.SetSize(rect.x, rect.y, rect.width+2, rect.height+2,
                               wx.SIZE_ALLOW_MINUS_ONE)
    # end SetSize
 
    def Show(self, show, attr):
        """
        Show or hide the edit control.  You can use the attr (if not None)
        to set colours or fonts for the control.
        """
        super(DatePickerEditor, self).Show(show, attr)
    # end Show
 
    def PaintBackground(self, rect, attr, *args):
        """
        Draws the part of the cell not occupied by the edit control.  The
        base  class version just fills it with background colour from the
        attribute.  In this class the edit control fills the whole cell so
        don't do anything at all in order to reduce flicker.
        """
        pass
    # end PaintBackground
 
    def BeginEdit(self, row, col, grid, *args):
        """
        Fetch the value from the table and prepare the edit control
        to begin editing.  Set the focus to the edit control.
        *Must Override*
        """
        self.startValue = str(grid.GetTable().GetValue(row, col)).strip()
 
        if not self.startValue == '':
            # Split the string up and then insert it in there
            tmpDate = wx.DateTime()
            tmpDate.ParseDate(self.startValue)
            self._picker.SetValue(tmpDate)
            self.startingDate = tmpDate
 
        self._picker.SetFocus()
 
    # end BeginEdit
 
    def EndEdit(self, row, col, grid, *args):
        """
        Complete the editing of the current cell. Returns True if the value
        has changed.  If necessary, the control may be destroyed.
        *Must Override*
        """
        changed = False
 
        val = self._picker.GetValue().GetDateOnly()
 
        if val.Format("%m/%d/%Y") != self.startValue:
            changed = True
            grid.SetCellValue(row, col, str(('%s-%s-%s' %(val.day, val.month, val.year)))) # update the table
            self.startValue = val.Format("%m/%d/%Y")
 
        return changed
    # end EndEdit
 
    def Reset(self, *args):
        """
        Reset the value in the control back to its starting value.
        *Must Override*
        """
        if self.startingDate is not None:
            self._picker.SetValue(self.startingDate)
    # end Reset
 
    def IsAcceptedKey(self, evt, *args):
        """
        Return True to allow the given key to start editing: the base class
        version only checks that the event has no modifiers.  F2 is special
        and will always start the editor.
        """
 
        # or do it ourselves
        return (not (evt.ControlDown() or evt.AltDown()) and
                evt.GetKeyCode() != wx.WXK_SHIFT)
    # end IsAcceptedKey
 
    def StartingKey(self, evt, *args):
        """
        If the editor is enabled by pressing keys on the grid, this will be
        called to let the editor do something about that first key if desired.
        """
        key = evt.GetKeyCode()
        ch = None
        if key in [ wx.WXK_NUMPAD0, wx.WXK_NUMPAD1, wx.WXK_NUMPAD2, wx.WXK_NUMPAD3,
                    wx.WXK_NUMPAD4, wx.WXK_NUMPAD5, wx.WXK_NUMPAD6, wx.WXK_NUMPAD7,
                    wx.WXK_NUMPAD8, wx.WXK_NUMPAD9
                    ]:
 
            ch = ch = chr(ord('0') + key - wx.WXK_NUMPAD0)
 
        else:
            ch = chr(key)
 
        evt.Skip()
    # end StartingKey
 
    def StartingClick(self,*args):
        """
        If the editor is enabled by clicking on the cell, this method will be
        called to allow the editor to simulate the click on the control if
        needed.
        """
 
        pass
    # end StartingClick
    
    def ApplyEdit(self, row, col, grid, *args):
        """
        This function should save the value of the control into the
        grid or grid table. It is called only after EndEdit() returns
        a non-None value.
        *Must Override*
        """
        pass
 
    def Destroy(self,*args):
        """final cleanup"""
        self.base_Destroy()
    # end Destroy
 
    def Clone(self):
        """
        Create a new object which is the copy of this one
        *Must Override*
        """
        return DatePickerEditor()
    # end Clone    

'''
This feature works best with Column attribute

renderer = DatePickerEditor()
attr = wx.grid.GridCellAttr()
attr.SetEditor(renderer)
self.grid.SetColAttr(0, attr)        
'''