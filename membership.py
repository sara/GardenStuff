import pandas as pd
# this needs to produce CSVs that can be uploaded to drive as sheets so they can be resorted as necessary

# for now, payments are going to have to be an input file of emails from which the payments came. worry about all the payment details later

# input = existing membership records and google responses

# output = CSV matching format of membership records

class Person:
    first_name
    last_name
    cell_phone
    address
    spouse_first_name
    spouse__last_name
    spouse_email
    special_skills
    special_interests
    has_paid
    email (primary id)
    join_date_time
    renewal_date_time
    membership_problems
    waitlist_position
    plot_name
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


def main():





if __name__ == "__main__":
    main()
