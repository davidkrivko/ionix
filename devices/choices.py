

# SMART_THERM_STATUSES = [ 
#     ("TST", "Test status")
# ]

ANALOGUE_THERM_STATUSES = [ 
    ("OFF", "Off"),
    ("AUT", "Auto")
]

IONIQ_LOAD_TYPES = [ 
    ("PMP", "Pump"),
    ("ZVL", "Zone Valves"),
]

IONIQ_TYPES = [ 
    ('MX', 'Ioniq Max'),
    ('MN', 'Ioniq Mini')
]

HEATING_SENSOR_TYPES = [ 
    ("TMP", "Temperature"),
    ("PRS", "Pressure"),
    ("CRT", "Current")
]
HEATING_SENSOR_PIPES = [
    ("SPL", "Supply"),
    ("RTN", "Return"),
]

BOILER_TYPES = [ 
    (0, "Steam"),
    (1, "Hydronic"),
    (2, "Combination"),
]

BOILER_SYSHEALTH_STATUSES = [ 
    ("PEN", "Pending"),
    ("EXC", "Excelent"),
    ("ATN", "Attention"),
    ("ERR", "Error!"),
]

# FORCED STATES FOR ENDSWITCH (0 - disabled, 1 - enabled, 2 - auto)
BOILER_FORCED_STATES = [ 
    (0, 'Turned off'),
    (1, 'Turned on'),
    (2, 'Set to auto')
]

PIN_CHOICES =  [ 
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
]

ZONE_PIN_CHOICES =  [ 
    (1, 1),
    (2, 2),
    (3, 3),
]