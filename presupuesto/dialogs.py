from tkinter import simpledialog, ttk


class MoneyDialog(simpledialog.Dialog):
    """Dialogo reutilizable para pedir texto, fechas y montos."""

    def __init__(self, parent, title, labels, values=None):
        self.labels = labels
        self.values = values or {}
        self.entries = {}
        self.result = None
        super().__init__(parent, title)

    def body(self, master):
        for row, label in enumerate(self.labels):
            ttk.Label(master, text=label).grid(row=row, column=0, sticky="w", padx=8, pady=6)
            entry = ttk.Entry(master, width=36)
            entry.grid(row=row, column=1, sticky="ew", padx=8, pady=6)
            entry.insert(0, str(self.values.get(label, "")))
            self.entries[label] = entry
        return next(iter(self.entries.values()))

    def apply(self):
        self.result = {label: entry.get().strip() for label, entry in self.entries.items()}

