"""Class to hold information found on an EORI oil well card"""

class Card:
    def __init__(self):
        self.documentID=""
        self.pageNum=""
        # self.status = "" # Do we need this here?
        self.api = ""
        self.well_name = ""
        self.operator = ""
        self.location=""
        self.township = ""
        self.range = ""
        self.section = ""
        self.NS_Footage = ""
        self.EW_Footage = ""
        self.Qtr_Qtr = ""
        self.locationFootage=""
        self.elevation = ""
        self.spud = ""
        self.completion = ""
        self.TD_Formation = ""
        self.total_depth = ""
        self.plug_back = ""
        self.casing = ""
        self.init_prod = ""
        self.card_num = ""
        self.well_status = ""
        self.reissued = ""
        self.DSTS_Cores = ""

    
    def printCardInfo(self):
        print("documentID:", self.documentID)
        print("typeID:", self.typeID)
        print("api:", self.api)
        print("well_name:", self.well_name)
        print("operator:", self.operator)
        print("location:", self.location)
        print("township:", self.township)
        print("range:", self.range)
        print("section:", self.section)
        print("NS_Footage:", self.NS_Footage)
        print("EW_Footage:", self.EW_Footage)
        print("Qtr_Qtr:", self.Qtr_Qtr)
        print("locationFootage:", self.locationFootage)
        print("elevation:", self.elevation)
        print("spud:", self.spud)
        print("completion:", self.completion)
        print("TD_Formation:", self.TD_Formation)
        print("total_depth:", self.total_depth)
        print("plug_back:", self.plug_back)
        print("casing:", self.casing)
        print("init_prod:", self.init_prod)
        print("card_num:", self.card_num)
        print("well_status:", self.well_status)
        print("reissued:", self.reissued)
        print("DSTS_Cores:", self.DSTS_Cores)
        return


    def get_value_list(self):
        return [self.documentID,
        self.typeID,
        '',
        self.api,
        self.well_name,
        self.operator,
        self.location,
        self.township,
        self.range,
        self.section,
        self.NS_Footage,
        self.EW_Footage,
        self.Qtr_Qtr,
        self.locationFootage,
        self.elevation,
        self.spud,
        self.completion,
        self.TD_Formation,
        self.total_depth,
        self.plug_back,
        self.casing,
        self.init_prod,
        self.card_num,
        self.well_status,
        self.reissued,
        self.DSTS_Cores]

    def setLocation(self):
        # Make sure to separate the township, range, and section from the pool
        # and county
        if len(self.location) > 0:
            self.location = ', ' + self.location
        # Set township, range and section
        if self.section:
            self.location = ' sec. ' + self.section + self.location
        if self.range:
            self.location = ' ' + self.range + self.location
        if self.township:
            self.location = self.township + self.location
        
        
        return

    def setLocationFootage(self):
        if self.NS_Footage:
            self.locationFootage += self.NS_Footage
        if self.EW_Footage:
            self.locationFootage += ' ' + self.EW_Footage
        return
