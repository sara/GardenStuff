import pandas as pd
from datetime import datetime
# this needs to produce CSVs that can be uploaded to drive as sheets so they can be resorted as necessary

# for now, payments are going to have to be an input file of emails from which the payments came. worry about all the payment details later

# input = existing membership records and google responses

# output = CSV matching format of membership records


class Person:

    def __init__(self, data):
        self.id_on_file = False if (pd.isna(data['id_on_file']) or data['id_on_file'].lower() == 'no') else True
        self.is_on_waitlist = True if data['is_on_waitlist'].lower() == 'plot waitlist' else False
        self.is_plot_holder = True if data['is_on_waitlist'].lower() == "plot holder" else False
        self.is_general_member = True if data['is_on_waitlist'].lower() == "member only" else False
        self.has_mini_plot = False if pd.isna(data['has_mini_plot']) else True
        self.email = data['email']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.phone = data['phone']
        self.address = data['address']
        self.spouse_email = None if pd.isna(data['spouse_email']) else data['spouse_email']
        self.skills = data['skills']
        self.special_interests = None if pd.isna(data['special_interests']) else data['special_interests']
        self.notes = None if pd.isna(data['notes']) else data['notes']
        self.spouse = None
        self.spouse_email = None
        self.waitlist_date = None
        self.has_paid = False
        self.waitlist_position = None
        self.plot_name = None
        self.last_renewed = datetime.now().year -1
        self.membership_problems = []

        if not pd.isna(data['spouse']) and not data['spouse'].lower() == 'n/a':
            self.spouse = data['spouse']
            self.spouse_email = data['spouse_email']
        if self.is_on_waitlist:
            # todo convert this into a datetime
            self.waitlist_date = data['waitlist_date']
        if self.is_plot_holder:
            self.plot_name = data['waitlist_date']
"""
    is_general_member
    plot_holder
    mini_plot (there are six mini plots)

class membership_problems:
    missing_payment
    work_party
    missing_id

class Plots:
    {plot:Person}

class PlotWaitList:
    {plot:Person}
"""

def main():
    df = pd.read_excel("data.xlsx", sheet_name="MasterSheet")
    keys = ["id_on_file", "is_on_waitlist", "has_mini_plot", "waitlist_date", "email", "first_name", "last_name", "phone", "address", "spouse", "spouse_email", "skills", "special_interests", "notes"]
    people = []
    for index, row in df.iterrows():
        values = row.tolist()
        data = {}
        for key, value in zip(keys, values):
            data[key] = value
        people.append(Person(data))
#        for column, value in row.items():
#            print(f"  Column: {column}, Value: {value}")
    for person in people:
        print(vars(person))
        print("-"*40)


if __name__ == "__main__":
    main()
