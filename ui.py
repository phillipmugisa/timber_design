import tkinter as tk
from tkinter import ttk, messagebox
from typing import List

import eurocode

class UI:
    def __init__(self, members: List[tuple[str, int]]) -> None:

        if len(members) < 1:
            raise 

        self.title = 'Mugisa Phillip Timber Design'

        self.root = tk.Tk()
        self.root.config()
        self.root.title(self.title)

        self.members = members
        #self.current_member = self.members[0][0]
        
        self.buildUI()

    def runUI(self):
        self.root.mainloop()

    def buildUI(self):

        # left side with fields
        # for user to enter values
        self.leftArea = ttk.LabelFrame(self.root, text='Controls', padding=(10,10))
        self.leftArea.pack(side=tk.LEFT, anchor=tk.N, fill='y', padx=(10, 5), pady=10)

        self.buildLeftSide()

        self.rightArea = ttk.LabelFrame(self.root, text='Timber Dimensions and Properties:', padding=(10,10))
        self.rightArea.pack(side=tk.RIGHT, fill='both', expand=True, padx=(10,10), pady=10)
        self.rightArea.columnconfigure(0, weight=0)  # labels
        self.rightArea.columnconfigure(1, weight=1) 
        # the user selects the member that they want to design

        if self.members:
            self.getMemberChecks(self.members[0][1])
            self.addInputFieldToUI(self.checks)

    def getMemberChecks(self, option: int):
        from design import get_checks_for_member
        self.checks = get_checks_for_member(option)

    def onMemberSelect(self):
        member = self.member_var.get()
        self.current_member = member

        self.checks = []
        for m in self.members:
            if m[0] == member:
                self.getMemberChecks(m[1])
                break

        for widget in self.rightArea.winfo_children():
            widget.destroy()
        self.addInputFieldToUI(self.checks)

    def showResults(self):
        pass

    def all_fields_filled(self):
        for widget in self.rightArea.winfo_children():
            # Only check Entry or Combobox widgets
            if isinstance(widget, (ttk.Entry, ttk.Combobox)):
                if not widget.get():  # empty
                    return False
        return True

    def designMember(self):
        if not self.all_fields_filled():
            messagebox.showerror("Input Error", "Please fill in all required fields!")
            return

        from design import perform_checks
        results = perform_checks(self.checks, source=self, mode='gui')

        for widget in self.rightArea.winfo_children():
            widget.destroy()

        headers = ["Check", "Status", "Comment"]

        # Headers
        for col, h in enumerate(headers):
            ttk.Label(self.rightArea, text=h, font=("Arial", 10, "bold")).grid(row=0, column=col, padx=5, pady=2)

        # Rows
        for row_idx, r in enumerate(results, start=1):
            ttk.Label(self.rightArea, text=r[0]).grid(row=row_idx, column=0, padx=5, pady=2)
            status_str = "PASS" if r[1] else "FAIL"
            ttk.Label(self.rightArea, text=status_str).grid(row=row_idx, column=1, padx=5, pady=2)
            ttk.Label(self.rightArea, text=r[2]).grid(row=row_idx, column=2, padx=5, pady=2)



    def clearRightArea(self):
        for widget in self.rightArea.winfo_children():
            widget.destroy()
        self.addInputFieldToUI(self.checks)


    def buildLeftSide(self):

        ttk.Label(self.leftArea, text="Member:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        
        self.member_var = tk.StringVar(value=self.members[0][0])
        members = [(m[0], m[0]) for m in self.members]

        for text, member in members:
            ttk.Radiobutton(self.leftArea, text=text.title(), variable=self.member_var, value=member, command=self.onMemberSelect).pack(anchor=tk.W)
        
        ttk.Separator(self.leftArea, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Button(self.leftArea, text='Design', command=self.designMember).pack(fill=tk.X, pady=10)
        ttk.Button(self.leftArea, text='Clear', command=self.clearRightArea).pack(fill=tk.X, pady=10)

    def getEurocodeValue(self, event):
        from eurocode import get_eurocode_value, get_kmod_value

        timber_class = self.timber_class.get()
        service_class = self.service_class.get()
        loading_duration = self.loading_duration.get()


        if all([loading_duration, service_class]):
            Kmod = get_kmod_value(loading_duration, int(service_class))

        if timber_class:
            if getattr(self, 'xTic_tensile_strength', None) and self.xTic_tensile_strength.winfo_exists():
                self.xTic_tensile_strength.delete(0, 'end')
                self.xTic_tensile_strength.insert(0, f"{get_eurocode_value('strength', 'ft0k', timber_class)}")

            if getattr(self, 'E005', None) and self.E005.winfo_exists():
                self.E005.delete(0, 'end')
                self.E005.insert(0, f"{get_eurocode_value('stiffness', 'E005', timber_class)}")

            if getattr(self, 'xTic_compressive_strength', None) and self.xTic_compressive_strength.winfo_exists():
                self.xTic_compressive_strength.delete(0, 'end')
                self.xTic_compressive_strength.insert(0, f"{get_eurocode_value('strength', 'fc0k', timber_class)}")

            if getattr(self, 'xTic_shear_strength', None) and self.xTic_shear_strength.winfo_exists():
                self.xTic_shear_strength.delete(0, 'end')
                self.xTic_shear_strength.insert(0, f"{get_eurocode_value('strength', 'fvk', timber_class)}")

            if getattr(self, 'xTic_bending_strength', None) and self.xTic_bending_strength.winfo_exists():
                self.xTic_bending_strength.delete(0, 'end')
                self.xTic_bending_strength.insert(0, f"{get_eurocode_value('strength', 'fmk', timber_class)}")

            if getattr(self, 'characteristic_compressive_strength_90', None) and self.characteristic_compressive_strength_90.winfo_exists():
                self.characteristic_compressive_strength_90.delete(0, 'end')
                self.characteristic_compressive_strength_90.insert(0, f"{get_eurocode_value('strength', 'fc90k', timber_class)}")

    def addInputFieldToUI(self, checks: List[str]):
        if not checks:
            ttk.Label(self.rightArea, text='Please select a member to design').grid(row=0, column=0, sticky="w", pady=5)
            return

        # Define form fields
        fields = []
        if 'tension' in checks or 'compression' in checks:
            fields = [
                ("Permanent Load (kN)", "permanent_load"),
                ("Variable Load (kN)", "variable_load")
            ]
        fields = [
            *fields,
            ("Width (mm)", "width"),
            ("Depth (mm)", "depth"),
            ("Ksys", "Ksys"),
        ]


        self.entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(self.rightArea, text=label).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(self.rightArea)
            entry.grid(row=i, column=1, pady=5)
            self.entries[key] = entry


        ttk.Label(self.rightArea, text="Service Class").grid(row=5, column=0, sticky="w", pady=5, padx=5)
        self.service_class = ttk.Combobox(self.rightArea, values=[f'{s}' for s in eurocode.service_classes], state="readonly")
        self.service_class.grid(row=5, column=2, pady=5, padx=5)
        self.service_class.bind('<<ComboboxSelected>>', self.getEurocodeValue)

        ttk.Label(self.rightArea, text="Loading Duration").grid(row=6, column=0, sticky="w", pady=5, padx=5)
        self.loading_duration = ttk.Combobox(self.rightArea, values=list(eurocode.Kmod_values.keys()), state="readonly")
        self.loading_duration.grid(row=6, column=2, pady=5, padx=5)
        self.loading_duration.bind('<<ComboboxSelected>>', self.getEurocodeValue)

        ttk.Label(self.rightArea, text="Timber Class").grid(row=7, column=0, sticky="w", pady=5, padx=5)
        self.timber_class = ttk.Combobox(self.rightArea, values=eurocode.timber_classes, state="readonly")
        self.timber_class.grid(row=7, column=2, pady=5, padx=5)
        self.timber_class.bind('<<ComboboxSelected>>', self.getEurocodeValue)


        if ('tension' in checks and not (len(checks) == 1)) or ('tension' not in checks and len(checks) > 0):
            ttk.Label(self.rightArea, text="Length(mm)").grid(row=8, column=0, sticky="w", pady=5, padx=5)
            self.length = ttk.Entry(self.rightArea)
            self.length.grid(row=8, column=1, pady=5, padx=5)

        if 'tension' in checks:
            ttk.Label(self.rightArea, text="Largest Area Reduction").grid(row=9, column=0, sticky="w", pady=5, padx=5)
            self.largest_area_reduction = ttk.Entry(self.rightArea)
            self.largest_area_reduction.grid(row=9, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="xTic Tensile Strength").grid(row=10, column=0, sticky="w", pady=5, padx=5)
            self.xTic_tensile_strength = ttk.Entry(self.rightArea)
            self.xTic_tensile_strength.grid(row=10, column=1, pady=5, padx=5)

        if 'compression' in checks:
            ttk.Label(self.rightArea, text="Support Condition").grid(row=11, column=0, sticky="w", pady=5, padx=5)
            self.support_condition = ttk.Entry(self.rightArea)
            self.support_condition.grid(row=11, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="E005").grid(row=12, column=0, sticky="w", pady=5, padx=5)
            self.E005 = ttk.Entry(self.rightArea)
            self.E005.grid(row=12, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="xTic Compressive Strength").grid(row=13, column=0, sticky="w", pady=5, padx=5)
            self.xTic_compressive_strength = ttk.Entry(self.rightArea)
            self.xTic_compressive_strength.grid(row=13, column=1, pady=5, padx=5)

        if 'shear' in checks or 'flexure' in checks or 'deflection' in checks or 'bearing' in checks:
            ttk.Label(self.rightArea, text="Tributory Width(mm)").grid(row=14, column=0, sticky="w", pady=5, padx=5)
            self.tributory_width = ttk.Entry(self.rightArea)
            self.tributory_width.grid(row=14, column=1, pady=5, padx=5)

        if 'shear' in checks:
            ttk.Label(self.rightArea, text="xTic Shear Strength").grid(row=15, column=0, sticky="w", pady=5, padx=5)
            self.xTic_shear_strength = ttk.Entry(self.rightArea)
            self.xTic_shear_strength.grid(row=15, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="Kv").grid(row=16, column=0, sticky="w", pady=5, padx=5)
            self.Kv = ttk.Entry(self.rightArea)
            self.Kv.grid(row=16, column=1, pady=5, padx=5)

        if 'flexure' in checks:
            ttk.Label(self.rightArea, text="xTic Bending Strength").grid(row=17, column=0, sticky="w", pady=5, padx=5)
            self.xTic_bending_strength = ttk.Entry(self.rightArea)
            self.xTic_bending_strength.grid(row=17, column=1, pady=5, padx=5)

        if 'bearing' in checks:
            ttk.Label(self.rightArea, text="Bearing Length(mm)").grid(row=18, column=0, sticky="w", pady=5, padx=5)
            self.bearing_length = ttk.Entry(self.rightArea)
            self.bearing_length.grid(row=18, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="Characteristic Compressive Strength 90°").grid(row=19, column=0, sticky="w", pady=5, padx=5)
            self.characteristic_compressive_strength_90 = ttk.Entry(self.rightArea)
            self.characteristic_compressive_strength_90.grid(row=19, column=1, pady=5, padx=5)

        if 'deflection' in checks:
            ttk.Label(self.rightArea, text="K_def").grid(row=20, column=0, sticky="w", pady=5, padx=5)
            self.K_def = ttk.Entry(self.rightArea)
            self.K_def.grid(row=20, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="Quasi Permanent Value for Variable Load").grid(row=21, column=0, sticky="w", pady=5, padx=5)
            self.qausi_permanent_value_for_variable_load = ttk.Entry(self.rightArea)
            self.qausi_permanent_value_for_variable_load.grid(row=21, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="Young's Modulus").grid(row=22, column=0, sticky="w", pady=5, padx=5)
            self.youngs_modulus = ttk.Entry(self.rightArea)
            self.youngs_modulus.grid(row=22, column=1, pady=5, padx=5)

        if 'shear' in checks or 'flexure' in checks or 'bearing' in checks or 'deflection' in checks:
            ttk.Label(self.rightArea, text="Permanent Load (KN/m^2)").grid(row=23, column=0, sticky="w", pady=5, padx=5)
            self.permanent_load_per_square_m = ttk.Entry(self.rightArea)
            self.permanent_load_per_square_m.grid(row=23, column=1, pady=5, padx=5)

            ttk.Label(self.rightArea, text="Variable Load (KN/m^2)").grid(row=24, column=0, sticky="w", pady=5, padx=5)
            self.variable_load__per_square_m = ttk.Entry(self.rightArea)
            self.variable_load__per_square_m.grid(row=24, column=1, pady=5, padx=5)

    def get_field_value(self, name: str) -> str:
        """
        Returns the value of a UI field by its name.
        If the widget doesn't exist or is not rendered, returns ''.
        """
        widget = getattr(self, name, None)
        
        # Check if the widget exists and is mapped
        if widget and widget.winfo_exists():
            return widget.get()
        
        # Also check if it's in the entries dictionary
        if hasattr(self, 'entries') and name in self.entries:
            entry = self.entries[name]
            if entry.winfo_exists():
                return entry.get()
        
        return ''


members = [
    ('beam', 1),
    ('column', 2),
    ('ties', 3),
    ('Structs', 4),
    ('Tie Beam', 5),
    ('Studs', 6),
    ('Joists', 7),
    ('Header Plate', 8),
    ('Rafter', 9),
    ('Base Plate', 10)
]
UI(members).runUI()

