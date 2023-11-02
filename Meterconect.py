s = "eui-8cf95720000b7813"

meter_map ={"8CF95720000B778E": "SCALL 2",
            "8CF95720000B7813": "SIAPA  ",
            "8CF95720000B8A57": "SCALL 3",
            "8CF95720000B8C4C": "SCALL 1"}

s_transformed = s.replace('eui-', '').upper()
print(meter_map[s_transformed])