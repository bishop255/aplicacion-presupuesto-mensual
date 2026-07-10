import tkinter as tk
from datetime import date, datetime
from tkinter import messagebox, ttk

from .constants import (
    ACCENT,
    ACCENT_DARK,
    APP_BG,
    CYAN,
    DB_PATH,
    GREEN,
    ICON_PATH,
    MUTED,
    ORANGE,
    PANEL_BG,
    PINK,
    PURPLE,
    RED,
    TEXT,
    YELLOW,
)
from .dialogs import MoneyDialog
from .store import BudgetStore
from .utils import money, month_key, month_label, parse_money


class BudgetApp(tk.Tk):
    """Ventana principal de la aplicacion."""

    def __init__(self):
        super().__init__()
        self.title("Presupuesto mensual")
        self.geometry("1180x760")
        self.minsize(760, 520)
        self.configure(bg=APP_BG)
        self.apply_window_icon()
        self.store = BudgetStore(DB_PATH)
        self.current_month = month_key()
        self.row_ids = {}
        self.metric_cards = []
        self.metric_columns = 0
        self.configure_style()
        self.build()
        self.refresh_all()

    def apply_window_icon(self):
        if ICON_PATH.exists():
            self.iconbitmap(default=str(ICON_PATH))

    def configure_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=APP_BG)
        style.configure("Panel.TFrame", background=PANEL_BG)
        style.configure("TLabel", background=APP_BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Panel.TLabel", background=PANEL_BG, foreground=TEXT, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=PANEL_BG, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Header.TLabel", background=APP_BG, foreground=TEXT, font=("Segoe UI", 22, "bold"))
        style.configure("Subheader.TLabel", background=APP_BG, foreground=MUTED, font=("Segoe UI", 10))
        style.configure("Section.TLabel", background=PANEL_BG, foreground=TEXT, font=("Segoe UI", 13, "bold"))
        style.configure("Metric.TLabel", background=PANEL_BG, foreground=TEXT, font=("Segoe UI", 17, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 8))
        style.configure("Accent.TButton", background=ACCENT, foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", ACCENT_DARK)])
        style.configure("Danger.TButton", foreground=RED)
        style.configure("TNotebook", background=APP_BG, borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=(18, 10))
        style.layout(
            "TNotebook.Tab",
            [
                (
                    "Notebook.tab",
                    {
                        "sticky": "nswe",
                        "children": [
                            (
                                "Notebook.padding",
                                {
                                    "side": "top",
                                    "sticky": "nswe",
                                    "children": [("Notebook.label", {"side": "top", "sticky": ""})],
                                },
                            )
                        ],
                    },
                )
            ],
        )
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=30, background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), padding=8)

    def build(self):
        self.build_header()
        self.tabs = ttk.Notebook(self)
        self.tabs.configure(takefocus=False)
        self.tabs.pack(fill="both", expand=True, padx=14, pady=(0, 14))

        self.summary_page = ttk.Frame(self.tabs)
        self.fixed_tab = ttk.Frame(self.tabs, padding=18)
        self.leisure_tab = ttk.Frame(self.tabs, padding=18)
        self.saving_tab = ttk.Frame(self.tabs, padding=18)
        self.config_tab = ttk.Frame(self.tabs, padding=18)

        self.tabs.add(self.summary_page, text="Dashboard")
        self.tabs.add(self.fixed_tab, text="Gastos fijos")
        self.tabs.add(self.leisure_tab, text="Ocio")
        self.tabs.add(self.saving_tab, text="Ahorro")
        self.tabs.add(self.config_tab, text="Configuracion")
        self.summary_tab = self.make_scrollable_tab(self.summary_page)

        self.build_summary()
        self.build_fixed()
        self.build_leisure()
        self.build_saving()
        self.build_config()

    def build_header(self):
        top = ttk.Frame(self, padding=(20, 18, 20, 10))
        top.pack(fill="x")
        title_box = ttk.Frame(top)
        title_box.pack(side="left", fill="x", expand=True)
        ttk.Label(title_box, text="Presupuesto mensual", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            title_box,
            text="Controla tu sueldo, gastos fijos, ocio y ahorro sin pelearte con una planilla.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        nav = ttk.Frame(top)
        nav.pack(side="right")
        ttk.Label(nav, text="Mes").pack(side="left", padx=(0, 8))
        self.month_combo = ttk.Combobox(top, state="readonly", width=22)
        self.month_combo.pack(in_=nav, side="left")
        self.month_combo.bind("<<ComboboxSelected>>", self.on_month_change)
        ttk.Button(nav, text="Anterior", command=lambda: self.shift_month(-1)).pack(side="left", padx=(12, 4))
        ttk.Button(nav, text="Siguiente", style="Accent.TButton", command=lambda: self.shift_month(1)).pack(
            side="left", padx=4
        )

    def make_scrollable_tab(self, parent):
        canvas = tk.Canvas(parent, bg=APP_BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        content = ttk.Frame(canvas, padding=18)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def update_scrollregion(_event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def fit_width(event):
            canvas.itemconfigure(window_id, width=event.width)
            update_scrollregion()

        def mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        content.bind("<Configure>", update_scrollregion)
        canvas.bind("<Configure>", fit_width)
        canvas.bind_all("<MouseWheel>", mousewheel)
        return content

    def build_summary(self):
        self.metric_frame = ttk.Frame(self.summary_tab)
        self.metric_frame.pack(fill="x")
        self.metrics = {}
        labels = [
            ("income", "Sueldo del mes", "Lo que entra este mes"),
            ("cash_remaining", "Disponible real", "Despues de lo pagado"),
            ("annual_saved", "Ahorro anual", "Todo lo guardado este ano"),
            ("planned_remaining", "Ocio disponible", "Para gustos despues de fijos y ahorro"),
            ("fixed_planned", "Fijos esperados", "Compromisos del mes"),
            ("fixed_paid", "Fijos pagados", "Lo que ya quedo listo"),
            ("savings_target", "Meta de ahorro", "Segun tu porcentaje"),
            ("leisure", "Ocio gastado", "Compras, salidas y gustos"),
        ]
        for _index, (key, text, hint) in enumerate(labels):
            box = tk.Frame(self.metric_frame, bg=PANEL_BG, highlightbackground="#d9e2ec", highlightthickness=1)
            stripe_color = {
                "income": ACCENT,
                "cash_remaining": GREEN,
                "annual_saved": PURPLE,
                "planned_remaining": CYAN,
                "leisure": PINK,
                "savings_target": YELLOW,
            }.get(key, "#94a3b8")
            tk.Frame(box, bg=stripe_color, height=4).pack(fill="x")
            inner = tk.Frame(box, bg=PANEL_BG)
            inner.pack(fill="both", expand=True, padx=14, pady=12)
            tk.Label(inner, text=text, bg=PANEL_BG, fg=MUTED, font=("Segoe UI", 9, "bold")).pack(anchor="w")
            value = tk.Label(inner, text="$ 0", bg=PANEL_BG, fg=TEXT, font=("Segoe UI", 18, "bold"))
            value.pack(anchor="w", pady=(7, 2))
            tk.Label(inner, text=hint, bg=PANEL_BG, fg=MUTED, font=("Segoe UI", 9)).pack(anchor="w")
            self.metrics[key] = value
            self.metric_cards.append(box)
        self.metric_frame.bind("<Configure>", self.arrange_metric_cards)

        progress_panel = ttk.Frame(self.summary_tab, style="Panel.TFrame", padding=16)
        progress_panel.pack(fill="x", pady=(14, 8))
        ttk.Label(progress_panel, text="Pulso del mes", style="Section.TLabel").pack(anchor="w")
        self.fixed_progress_text = ttk.Label(progress_panel, text="", style="Panel.TLabel")
        self.fixed_progress_text.pack(anchor="w", pady=(12, 3))
        self.fixed_progress = self.create_color_progress(progress_panel)
        self.saving_progress_text = ttk.Label(progress_panel, text="", style="Panel.TLabel")
        self.saving_progress_text.pack(anchor="w", pady=(12, 3))
        self.saving_progress = self.create_color_progress(progress_panel)

        ttk.Label(self.summary_tab, text="Movimientos recientes", style="Section.TLabel").pack(anchor="w", pady=(18, 8))
        self.recent_tree = ttk.Treeview(
            self.summary_tab,
            columns=("fecha", "tipo", "detalle", "monto"),
            show="headings",
            height=16,
        )
        self.setup_tree(
            self.recent_tree,
            [("fecha", "Fecha", 120), ("tipo", "Tipo", 120), ("detalle", "Detalle", 420), ("monto", "Monto", 120)],
        )
        self.recent_tree.pack(fill="x")
        self.recent_tree.bind("<Configure>", self.resize_recent_tree)

    def arrange_metric_cards(self, _event=None):
        width = max(self.metric_frame.winfo_width(), 1)
        if width >= 1180:
            columns = 4
        elif width >= 720:
            columns = 2
        else:
            columns = 1
        if columns == self.metric_columns:
            return
        self.metric_columns = columns
        for card in self.metric_cards:
            card.grid_forget()
        for column in range(4):
            self.metric_frame.columnconfigure(column, weight=0)
        for column in range(columns):
            self.metric_frame.columnconfigure(column, weight=1, uniform="metrics")
        for index, card in enumerate(self.metric_cards):
            card.grid(row=index // columns, column=index % columns, sticky="nsew", padx=7, pady=7)

    def resize_recent_tree(self, event):
        width = max(event.width - 8, 500)
        self.recent_tree.column("fecha", width=max(90, int(width * 0.16)), stretch=True)
        self.recent_tree.column("tipo", width=max(90, int(width * 0.18)), stretch=True)
        self.recent_tree.column("detalle", width=max(180, int(width * 0.46)), stretch=True)
        self.recent_tree.column("monto", width=max(100, int(width * 0.20)), stretch=True)

    def create_color_progress(self, parent):
        canvas = tk.Canvas(parent, height=16, bg=PANEL_BG, highlightthickness=0)
        canvas.pack(fill="x")
        canvas.bind("<Configure>", lambda _event: self.redraw_progress(canvas))
        canvas.percent = 0
        canvas.color = ACCENT
        return canvas

    def set_color_progress(self, canvas, percent, color):
        canvas.percent = max(0, min(100, percent))
        canvas.color = color
        self.redraw_progress(canvas)

    def redraw_progress(self, canvas):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 1)
        height = max(canvas.winfo_height(), 16)
        fill_width = width * getattr(canvas, "percent", 0) / 100
        canvas.create_rectangle(0, 0, width, height, fill="#e5e7eb", outline="")
        canvas.create_rectangle(0, 0, fill_width, height, fill=getattr(canvas, "color", ACCENT), outline="")
        canvas.create_text(
            width - 8,
            height / 2,
            text=f"{getattr(canvas, 'percent', 0)}%",
            anchor="e",
            fill="#ffffff" if fill_width > 45 else TEXT,
            font=("Segoe UI", 8, "bold"),
        )

    def build_fixed(self):
        ttk.Label(self.fixed_tab, text="Gastos fijos", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            self.fixed_tab,
            text="Marca lo que ya pagaste y manten tu lista mensual siempre actualizada.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(2, 14))
        actions = ttk.Frame(self.fixed_tab)
        actions.pack(fill="x", pady=(0, 10))
        ttk.Button(actions, text="Marcar pagado", style="Accent.TButton", command=self.mark_fixed_paid).pack(side="left")
        ttk.Button(actions, text="Quitar pago", command=self.clear_fixed_paid).pack(side="left", padx=6)
        ttk.Button(actions, text="Agregar gasto fijo", command=self.add_fixed).pack(side="left", padx=(18, 6))
        ttk.Button(actions, text="Editar gasto fijo", command=self.edit_fixed).pack(side="left", padx=6)
        ttk.Button(actions, text="Eliminar", style="Danger.TButton", command=self.delete_fixed).pack(side="left", padx=6)

        self.fixed_tree = ttk.Treeview(
            self.fixed_tab,
            columns=("nombre", "esperado", "pagado", "restante", "fecha", "estado"),
            show="headings",
        )
        self.setup_tree(
            self.fixed_tree,
            [
                ("nombre", "Gasto", 280),
                ("esperado", "Esperado", 110),
                ("pagado", "Pagado", 110),
                ("restante", "Restante", 110),
                ("fecha", "Fecha pago", 120),
                ("estado", "Estado", 120),
            ],
        )
        self.fixed_tree.pack(fill="both", expand=True)
        self.fixed_tree.bind(
            "<Configure>",
            lambda event: self.resize_tree_columns(
                self.fixed_tree,
                event.width,
                [
                    ("nombre", 0.32, 150),
                    ("esperado", 0.14, 90),
                    ("pagado", 0.14, 90),
                    ("restante", 0.14, 90),
                    ("fecha", 0.14, 95),
                    ("estado", 0.12, 85),
                ],
            ),
        )

    def build_leisure(self):
        ttk.Label(self.leisure_tab, text="Ocio y compras", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            self.leisure_tab,
            text="Anota esos gastos del dia a dia: salidas, regalos, ropa o cualquier gusto del mes.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(2, 14))
        form = ttk.Frame(self.leisure_tab, style="Panel.TFrame", padding=14)
        form.pack(fill="x", pady=(0, 12))
        self.leisure_date = self.add_labeled_entry(form, "Fecha", 0, date.today().isoformat(), 12)
        self.leisure_desc = self.add_labeled_entry(form, "Detalle", 1, "", 34)
        self.leisure_amount = self.add_labeled_entry(form, "Monto", 2, "", 14)
        ttk.Button(form, text="Agregar", style="Accent.TButton", command=self.add_leisure).grid(row=0, column=6, padx=8)
        ttk.Button(form, text="Eliminar seleccionado", command=self.delete_leisure).grid(row=0, column=7, padx=4)

        self.leisure_tree = ttk.Treeview(self.leisure_tab, columns=("fecha", "detalle", "monto"), show="headings")
        self.setup_tree(
            self.leisure_tree,
            [("fecha", "Fecha", 130), ("detalle", "Detalle", 520), ("monto", "Monto", 140)],
        )
        self.leisure_tree.pack(fill="both", expand=True)
        self.leisure_tree.bind(
            "<Configure>",
            lambda event: self.resize_tree_columns(
                self.leisure_tree,
                event.width,
                [("fecha", 0.18, 95), ("detalle", 0.62, 180), ("monto", 0.20, 100)],
            ),
        )

    def build_saving(self):
        ttk.Label(self.saving_tab, text="Ahorro", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            self.saving_tab,
            text="Registra lo que separaste y compara tu avance contra la meta del mes.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(2, 14))
        self.saving_info = ttk.Label(self.saving_tab, text="", style="Section.TLabel")
        self.saving_info.pack(anchor="w", pady=(0, 10))
        self.saving_annual_info = ttk.Label(self.saving_tab, text="", style="Subheader.TLabel")
        self.saving_annual_info.pack(anchor="w", pady=(0, 12))

        form = ttk.Frame(self.saving_tab, style="Panel.TFrame", padding=14)
        form.pack(fill="x", pady=(0, 12))
        self.saving_date = self.add_labeled_entry(form, "Fecha", 0, date.today().isoformat(), 12)
        self.saving_desc = self.add_labeled_entry(form, "Detalle", 1, "Ahorro", 34)
        self.saving_amount = self.add_labeled_entry(form, "Monto", 2, "", 14)
        ttk.Button(form, text="Agregar", style="Accent.TButton", command=self.add_saving).grid(row=0, column=6, padx=8)
        ttk.Button(form, text="Eliminar seleccionado", command=self.delete_saving).grid(row=0, column=7, padx=4)

        self.saving_tree = ttk.Treeview(self.saving_tab, columns=("fecha", "detalle", "monto"), show="headings")
        self.setup_tree(
            self.saving_tree,
            [("fecha", "Fecha", 130), ("detalle", "Detalle", 520), ("monto", "Monto", 140)],
        )
        self.saving_tree.pack(fill="both", expand=True)
        self.saving_tree.bind(
            "<Configure>",
            lambda event: self.resize_tree_columns(
                self.saving_tree,
                event.width,
                [("fecha", 0.18, 95), ("detalle", 0.62, 180), ("monto", 0.20, 100)],
            ),
        )

    def build_config(self):
        ttk.Label(self.config_tab, text="Configuracion del mes", style="Header.TLabel").pack(anchor="w")
        ttk.Label(
            self.config_tab,
            text="Ajusta el sueldo y el porcentaje de ahorro cuando el mes venga distinto.",
            style="Subheader.TLabel",
        ).pack(anchor="w", pady=(2, 14))
        form = ttk.Frame(self.config_tab, style="Panel.TFrame", padding=18)
        form.pack(anchor="w")
        ttk.Label(form, text="Sueldo del mes", style="Panel.TLabel").grid(row=0, column=0, sticky="w", pady=8)
        self.income_entry = ttk.Entry(form, width=20)
        self.income_entry.grid(row=0, column=1, sticky="w", padx=10, pady=8)
        ttk.Label(form, text="Porcentaje de ahorro", style="Panel.TLabel").grid(row=1, column=0, sticky="w", pady=8)
        self.percent_entry = ttk.Entry(form, width=20)
        self.percent_entry.grid(row=1, column=1, sticky="w", padx=10, pady=8)
        ttk.Button(form, text="Guardar cambios", style="Accent.TButton", command=self.save_config).grid(
            row=2, column=1, sticky="w", padx=10, pady=14
        )

    def add_labeled_entry(self, parent, label, col, default, width):
        ttk.Label(parent, text=label, style="Panel.TLabel").grid(row=0, column=col * 2, sticky="w", padx=(0, 5))
        entry = ttk.Entry(parent, width=width)
        entry.insert(0, default)
        entry.grid(row=0, column=col * 2 + 1, sticky="w", padx=(0, 10))
        return entry

    def setup_tree(self, tree, columns):
        for key, label, width in columns:
            tree.heading(key, text=label)
            tree.column(key, width=width, anchor="w", stretch=True)

    def resize_tree_columns(self, tree, width, columns):
        usable_width = max(width - 8, 420)
        minimum_total = sum(min_width for _, _, min_width in columns)
        if usable_width < minimum_total:
            for key, _, min_width in columns:
                tree.column(key, width=min_width, stretch=True)
            return
        for key, ratio, min_width in columns:
            tree.column(key, width=max(min_width, int(usable_width * ratio)), stretch=True)

    def on_month_change(self, _event=None):
        selected = self.month_combo.get()
        for key in self.store.months():
            if month_label(key) == selected:
                self.current_month = key
                self.refresh_all()
                return

    def shift_month(self, step):
        year, month = map(int, self.current_month.split("-"))
        month += step
        if month == 0:
            year -= 1
            month = 12
        elif month == 13:
            year += 1
            month = 1
        self.current_month = f"{year:04d}-{month:02d}"
        self.store.ensure_month(self.current_month)
        self.refresh_all()

    def refresh_month_combo(self):
        months = self.store.months()
        if self.current_month not in months:
            self.store.ensure_month(self.current_month)
            months = self.store.months()
        self.month_combo["values"] = [month_label(key) for key in months]
        self.month_combo.set(month_label(self.current_month))

    def refresh_all(self):
        self.refresh_month_combo()
        self.refresh_config()
        self.refresh_summary()
        self.refresh_fixed()
        self.refresh_leisure()
        self.refresh_saving()

    def refresh_config(self):
        settings = self.store.month_settings(self.current_month)
        self.income_entry.delete(0, tk.END)
        self.income_entry.insert(0, str(settings["income"]))
        self.percent_entry.delete(0, tk.END)
        self.percent_entry.insert(0, str(settings["savings_percent"]))

    def refresh_summary(self):
        data = self.store.summary(self.current_month)
        year = int(self.current_month.split("-")[0])
        annual = self.store.annual_savings(year)
        data["annual_saved"] = annual["total_saved"]
        for key, label in self.metrics.items():
            label.configure(text=money(data[key]))
        self.metrics["cash_remaining"].configure(fg=GREEN if data["cash_remaining"] >= 0 else RED)
        self.metrics["annual_saved"].configure(fg=PURPLE)
        self.metrics["planned_remaining"].configure(fg=GREEN if data["planned_remaining"] >= 0 else ORANGE)

        fixed_percent = min(100, round(data["fixed_paid"] / data["fixed_planned"] * 100)) if data["fixed_planned"] else 0
        saving_percent = min(100, round(data["saved"] / data["savings_target"] * 100)) if data["savings_target"] else 0
        self.set_color_progress(self.fixed_progress, fixed_percent, GREEN if fixed_percent >= 100 else ACCENT if fixed_percent >= 50 else ORANGE)
        self.set_color_progress(self.saving_progress, saving_percent, GREEN if saving_percent >= 100 else CYAN if saving_percent >= 50 else PINK)
        self.fixed_progress_text.configure(
            text=f"Gastos fijos pagados: {fixed_percent}% ({money(data['fixed_paid'])} de {money(data['fixed_planned'])})"
        )
        self.saving_progress_text.configure(
            text=f"Ahorro avanzado: {saving_percent}% ({money(data['saved'])} de {money(data['savings_target'])})"
        )
        for item in self.recent_tree.get_children():
            self.recent_tree.delete(item)
        rows = []
        rows.extend((expense["spent_on"], "Ocio", expense["description"], expense["amount"]) for expense in self.store.expenses(self.current_month))
        rows.extend((saving["saved_on"], "Ahorro", saving["description"], saving["amount"]) for saving in self.store.savings(self.current_month))
        for fixed in self.store.fixed_rows(self.current_month):
            if fixed["paid_amount"]:
                rows.append((fixed["paid_date"] or "", "Gasto fijo", fixed["name"], fixed["paid_amount"]))
        for spent_on, kind, detail, amount in sorted(rows, reverse=True)[:20]:
            self.recent_tree.insert("", tk.END, values=(spent_on, kind, detail, money(amount)))

    def refresh_fixed(self):
        for item in self.fixed_tree.get_children():
            self.fixed_tree.delete(item)
        self.row_ids = {}
        for row in self.store.fixed_rows(self.current_month):
            remaining = row["amount"] - row["paid_amount"]
            status = "Pagado" if remaining <= 0 and row["paid_amount"] else "Pendiente"
            item = self.fixed_tree.insert(
                "",
                tk.END,
                values=(row["name"], money(row["amount"]), money(row["paid_amount"]), money(max(remaining, 0)), row["paid_date"] or "", status),
            )
            self.row_ids[item] = row["id"]

    def refresh_leisure(self):
        for item in self.leisure_tree.get_children():
            self.leisure_tree.delete(item)
        for row in self.store.expenses(self.current_month):
            self.leisure_tree.insert("", tk.END, iid=str(row["id"]), values=(row["spent_on"], row["description"], money(row["amount"])))

    def refresh_saving(self):
        data = self.store.summary(self.current_month)
        year = int(self.current_month.split("-")[0])
        annual = self.store.annual_savings(year)
        self.saving_info.configure(text=f"Meta: {money(data['savings_target'])} | Guardado: {money(data['saved'])}")
        self.saving_annual_info.configure(
            text=f"Acumulado {year}: {money(annual['total_saved'])} | Meta registrada: {money(annual['total_target'])}"
        )
        for item in self.saving_tree.get_children():
            self.saving_tree.delete(item)
        for row in self.store.savings(self.current_month):
            self.saving_tree.insert("", tk.END, iid=str(row["id"]), values=(row["saved_on"], row["description"], money(row["amount"])))

    def selected_fixed_id(self):
        selected = self.fixed_tree.selection()
        if not selected:
            messagebox.showinfo("Seleccion pendiente", "Selecciona un gasto fijo primero.")
            return None
        return self.row_ids[selected[0]]

    def selected_fixed_row(self):
        template_id = self.selected_fixed_id()
        if template_id is None:
            return None
        for row in self.store.fixed_rows(self.current_month):
            if row["id"] == template_id:
                return row
        return None

    def mark_fixed_paid(self):
        row = self.selected_fixed_row()
        if not row:
            return
        dialog = MoneyDialog(
            self,
            "Marcar pagado",
            ["Monto pagado", "Fecha", "Nota"],
            {"Monto pagado": row["amount"], "Fecha": date.today().isoformat(), "Nota": row["notes"]},
        )
        if dialog.result:
            try:
                amount = parse_money(dialog.result["Monto pagado"])
                paid_date = self.clean_date(dialog.result["Fecha"])
            except ValueError as exc:
                messagebox.showerror("Dato invalido", str(exc))
                return
            self.store.set_fixed_payment(self.current_month, row["id"], amount, paid_date, dialog.result["Nota"])
            self.refresh_all()

    def clear_fixed_paid(self):
        template_id = self.selected_fixed_id()
        if template_id is None:
            return
        self.store.clear_fixed_payment(self.current_month, template_id)
        self.refresh_all()

    def add_fixed(self):
        dialog = MoneyDialog(self, "Agregar gasto fijo", ["Nombre", "Monto"])
        if dialog.result:
            name = dialog.result["Nombre"].strip()
            if not name:
                messagebox.showerror("Dato invalido", "Escribe un nombre.")
                return
            self.store.add_fixed_template(name, parse_money(dialog.result["Monto"]))
            self.refresh_all()

    def edit_fixed(self):
        row = self.selected_fixed_row()
        if not row:
            return
        dialog = MoneyDialog(self, "Editar gasto fijo", ["Nombre", "Monto"], {"Nombre": row["name"], "Monto": row["amount"]})
        if dialog.result:
            name = dialog.result["Nombre"].strip()
            if not name:
                messagebox.showerror("Dato invalido", "Escribe un nombre.")
                return
            self.store.edit_fixed_template(row["id"], name, parse_money(dialog.result["Monto"]))
            self.refresh_all()

    def delete_fixed(self):
        template_id = self.selected_fixed_id()
        if template_id is None:
            return
        if messagebox.askyesno("Eliminar", "Este gasto fijo ya no aparecera en meses nuevos."):
            self.store.deactivate_fixed_template(template_id)
            self.refresh_all()

    def add_leisure(self):
        try:
            spent_on = self.clean_date(self.leisure_date.get())
            amount = parse_money(self.leisure_amount.get())
        except ValueError as exc:
            messagebox.showerror("Dato invalido", str(exc))
            return
        description = self.leisure_desc.get().strip()
        if not description:
            messagebox.showerror("Dato invalido", "Escribe un detalle.")
            return
        self.store.add_expense(self.current_month, spent_on, "Ocio", description, amount)
        self.leisure_desc.delete(0, tk.END)
        self.leisure_amount.delete(0, tk.END)
        self.refresh_all()

    def delete_leisure(self):
        selected = self.leisure_tree.selection()
        if selected:
            self.store.delete_expense(int(selected[0]))
            self.refresh_all()

    def add_saving(self):
        try:
            saved_on = self.clean_date(self.saving_date.get())
            amount = parse_money(self.saving_amount.get())
        except ValueError as exc:
            messagebox.showerror("Dato invalido", str(exc))
            return
        description = self.saving_desc.get().strip() or "Ahorro"
        self.store.add_saving(self.current_month, saved_on, description, amount)
        self.saving_amount.delete(0, tk.END)
        self.refresh_all()

    def delete_saving(self):
        selected = self.saving_tree.selection()
        if selected:
            self.store.delete_saving(int(selected[0]))
            self.refresh_all()

    def save_config(self):
        try:
            income = parse_money(self.income_entry.get())
            percent = float(self.percent_entry.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Dato invalido", "Revisa el sueldo y el porcentaje.")
            return
        self.store.save_month_settings(self.current_month, income, percent)
        self.refresh_all()
        messagebox.showinfo("Guardado", "Configuracion del mes guardada.")

    def clean_date(self, value):
        value = value.strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Usa la fecha con formato AAAA-MM-DD.") from exc
        return value
