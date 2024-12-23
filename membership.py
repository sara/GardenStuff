import pandas as pd
from datetime import datetime
import heapq
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
        self.skills = None if pd.isna(data['skills']) else data['skills']
        self.special_interests = None if pd.isna(data['special_interests']) else data['special_interests']
        self.notes = [] if pd.isna(data['notes']) else [data['notes']]
        self.spouse = None
        self.spouse_email = None
        self.waitlist_date = None
        self.has_paid = False
        self.waitlist_position = None
        self.plot_name = None
        self.last_renewed = datetime.now().year -1
        self.membership_problems = []
        self.paid_up = True

        if not pd.isna(data['spouse']) and not data['spouse'].lower() == 'n/a':
            self.spouse = data['spouse']
            self.spouse_email = data['spouse_email']
        if self.is_on_waitlist:
            self.waitlist_date = data['waitlist_date']
        if self.is_plot_holder:
            self.plot_name = data['waitlist_date']

    def update(self, updated_data):
        if not pd.isna(updated_data['address']):
            self.address = updated_data['address']
        if not pd.isna(updated_data['notes']):
            self.notes.append(updated_data['notes'])
        self.last_renewed = datetime.now().year
        self.paid_up = False

    def quick_str(self):
        return f"{self.first_name} {self.last_name}: {self.email}"
   

def make_people_from_doc(members_doc="data.xlsx"):
    people_df = pd.read_excel(members_doc, sheet_name="MasterSheet")
    keys = ["id_on_file", "is_on_waitlist", "has_mini_plot", "waitlist_date", "email", "first_name", "last_name", "phone", "address", "spouse", "spouse_email", "skills", "special_interests", "notes"]
    people = {}
    for index, row in people_df.iterrows():
        values = row.tolist()
        data = {}
        for key, value in zip(keys, values):
            data[key] = value
        person = Person(data)
        people[person.email] = person
    
    waitlist = [person for person in people.values() if person.is_on_waitlist]
    heapq.heapify(waitlist, key=lambda person:person.waitlist_date)
    return (people, waitlist)

def get_renewal_data(people, renewal_doc="renewals.xlsx"):
    renewals_df = pd.read_excel("renewals.xlsx", sheet_name="Form Responses 1")
    raw_to_keys = {'Timestamp':'timestamp', 'Email Address':'email', 'LAST NAME':'last_name', 'FIRST NAME':'first_name', 'Questions, Concerns or Requests':'notes', 'If your address has changed what is your NEW address (same ? leave blank)':'address', 'Go to this link and pay the $30 General member or $50 plot fee -\n\nhttps://www.paypal.com/donate/?hosted_button_id=595WNG5MULXEN\n\nDON\'T FORGET TO \n***Submit this form****':'paypal'}
    renewals = {}
    for index, row in renewals_df.iterrows():
        raw_dict = row.to_dict()
        updated_data = {}
        for key, value in raw_dict.items():
            updated_data[raw_to_keys[key]] = value
        del(updated_data['timestamp'])
        del(updated_data['paypal'])
        renewals[updated_data['email']] = updated_data
    return renewals

def update_members(people, renewal_data):
    for renewal, updated_data in renewal_data.items():
            email = updated_data['email']
            person = people[email]
            person.first_name = updated_data['first_name']
            person.last_name = updated_data['last_name']
            person.update(updated_data)

# this needs to be converted into docs
def show_nonrenewed_members(people):
    print("The following members have not yet renewed their membership:")
    for person in people.values():
        if person.last_renewed != datetime.now().year:
            print(person.quick_str)

# this needs to be converted into docs
def show_members_with_problems(people):
    unpaid = []
    missing_id = []
    # figure out how you're going to manage work party issues
    for person in people.values():
        if not person.paid_up:
            unpaid.append(person)
        if not person.id_on_file:
            missing_id.append(person)
    if unpaid:
        print("The following people are not paid up:")
        for person in unpaid:
            print(person.quick_str())
    if missing_id:
        print("The following people are missing IDs:")
        for person in missing_id:
            print(person.quick_str())

def show_waitlist(waitlist):
    while waitlist:
        person = heapq.heappop(waitlist)
        print(f"{person.first_name} {person.last_name}: {person.waitlist_date}")

def set_waitlist_positions(waitlist, people):
    position = 1
    while waitlist:
        person = waitlist.heappop()
        person.waitlist_position = position
        position += 1

    

def main():
    people, waitlist = make_people_from_doc()
    renewal_data = get_renewal_data(people)
    update_members(people, renewal_data)
    show_waitlist(waitlist)
    #show_nonrenewed_members(people)
    #show_members_with_problems(people)

    show_waitlist(waitlist)
    # TODO if there's a name with a changed email address, issue a warning
        
    


if __name__ == "__main__":
    main()
