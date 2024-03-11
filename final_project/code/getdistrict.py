def get_district(address):
        if "中正區" in address:
            return 100
        elif "大同區" in address:
            return 103
        elif "中山區" in address:
            return 104
        elif "松山區" in address:
            return 105
        elif "大安區" in address:
            return 106
        elif "萬華區" in address:
            return 108
        elif "信義區" in address:
            return 110
        elif "士林區" in address:
            return 111
        elif "北投區" in address:
            return 112
        elif "內湖區" in address:
            return 114
        elif "南港區" in address:
            return 115
        elif "文山區" in address:
            return 116
        else:
            return None

   