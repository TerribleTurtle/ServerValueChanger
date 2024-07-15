"""
tooltip.py

This module provides the Tooltip class, which creates and manages tooltips for Tkinter widgets.

Classes:
    Tooltip: Creates and manages tooltips for Tkinter widgets.

Methods (Tooltip class):
    __init__(self, widget, text): Initialize the Tooltip with a widget and text.
    show_tooltip(self, event=None): Display the tooltip.
    hide_tooltip(self, event=None): Hide the tooltip.
"""

import tkinter as tk

class Tooltip:
    """
    Tooltip class to create and manage tooltips for Tkinter widgets.
    """
    def __init__(self, widget, text):
        """
        Initialize the Tooltip with a widget and text.

        :param widget: The widget to attach the tooltip to.
        :param text: The text to display in the tooltip.
        """
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    # Suppress the Pylint warning for unused arguments
    # pylint: disable=unused-argument
    def show_tooltip(self, event=None):
        """
        Display the tooltip.

        :param event: The event that triggered the tooltip.
        """
        if self.tooltip_window or not self.text:
            return
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(tw, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    # Suppress the Pylint warning for unused arguments
    # pylint: disable=unused-argument
    def hide_tooltip(self, event=None):
        """
        Hide the tooltip.

        :param event: The event that triggered hiding the tooltip.
        """
        tw = self.tooltip_window
        self.tooltip_window = None
        if tw:
            tw.destroy()
