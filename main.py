import os
from terminaltables import AsciiTable

os.system("clear")

Months_Of_The_Year = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def Monthly_Payment_Function(P, r, n):
    M = (P * (r * (1 + r) ** n)) / (((1 + r) ** n) - 1)
    print("Your monthly payments are {:0.2f} dollars.".format(M))
    return M


def Monthly_Interest_Function(Balance, Interest_Rate):
    Interest = (Balance * Interest_Rate)
    return Interest


def Monthly_Principal_Function(Monthly_Payment, Monthly_Interest, Month, Year, Extra1, Extra2, Extra2Month, Extra3, Extra3Month, Extra3Year):
    if Year == Extra3Year:
        if Month == Extra3Month:
            if Month == Extra2Month:
                Principal = (Monthly_Payment - Monthly_Interest + Extra1 + Extra2 + Extra3)
            else:
                Principal = (Monthly_Payment - Monthly_Interest + Extra1 + Extra3)
        else:
            if Month == Extra2Month:
                Principal = (Monthly_Payment - Monthly_Interest + Extra1 + Extra2)
            else:
                Principal = (Monthly_Payment - Monthly_Interest + Extra1)
    else:
        if Month == Extra2Month:
            Principal = (Monthly_Payment - Monthly_Interest + Extra1 + Extra2)
        else:
            Principal = (Monthly_Payment - Monthly_Interest + Extra1)
    return Principal


def Monthly_Balance_Remaining_Function(Previous_Balance, Principal):
    Balance = Previous_Balance - Principal
    return Balance


def Total_Interest_Paid_Function(Previous_Total_Interest, Interest):
    Total_Interest = (Previous_Total_Interest + Interest)
    return Total_Interest


def Extras():
    Extra1 = 0
    Extra2 = 0
    Extra2_Month = None
    Extra3 = 0
    Extra3_Month = None
    Extra3_Year = None
    Extras_Loop = True
    while Extras_Loop:
        print("\nDo you want to add any extra payments??")
        Extra_Payments_Choice = int(input("Options: \n1 = Add money to your monthly mortgage payment \n2 = Add money as an extra yearly mortgage payment occurring in every (month of your choice) \n3 = Add money as a one time mortgage payment in (month and year of your choice) \n4 = No extra payments \nChoose one: "))

        if Extra_Payments_Choice == 1:
            Extra1 = float(input("Add amount of money: "))
            print("Perfect. Every month, you will make an extra payment of", Extra1, "dollars.")

        elif Extra_Payments_Choice == 2:
            Extra2_Month = int(
                input("Which month do you want to make an extra payment every year? \nType the month number: "))
            if Extra2_Month <= 12:
                Extra2 = float(input("Add amount of money: "))
                print("Perfect. Every year in", Months_Of_The_Year[Extra2_Month - 1],", you will make an extra payment of", Extra2, "dollars.")
            else:
                print("The month number should be in the range of 1 to 12.")

        elif Extra_Payments_Choice == 3:
            Extra3_Year = int(input("Which year do you want to make an extra payment? \nType the year: "))
            Extra3_Month = int(input("Which month do you want to make an extra payment? \nType the month number: "))
            if Extra3_Month <= 12:
                Extra3 = float(input("Add amount of money: "))
                print("Perfect. In the year", Extra3_Year, ", and month", Months_Of_The_Year[Extra3_Month - 1],"you will make an extra payment of", Extra3, "dollars.")
            else:
                print("The month number should be in the range of 1 to 12.")

        elif Extra_Payments_Choice == 4:
            Extras_Loop = False

        else:
            print("Please select an option between 1 to 4")
    return Extra1, Extra2, Extra2_Month, Extra3, Extra3_Month, Extra3_Year


amortization_schedule = [["Month", "Year", "Monthly Payment", "Interest", "Principal", "Total Interest Paid", "Balance"],]


def Create_amrt_schedule(Balance_Remaining, Interest_Rate, Monthly_Payment, Total_Interest_Paid, Month, Year, amrt_output):
    Extra1, Extra2, Extra2_Month, Extra3, Extra3_Month, Extra3_Year = Extras()
    while Balance_Remaining > 0.1:
        Monthly_Interest = Monthly_Interest_Function(Balance_Remaining, Interest_Rate)
        Total_Interest_Paid = Total_Interest_Paid_Function(Total_Interest_Paid, Monthly_Interest)
        if Monthly_Payment > Balance_Remaining:
            Monthly_Principal = Balance_Remaining
            Monthly_Payment = Monthly_Principal + Monthly_Interest
        else:
            Monthly_Principal = Monthly_Principal_Function(Monthly_Payment, Monthly_Interest, Month, Year, Extra1, Extra2, Extra2_Month, Extra3, Extra3_Month, Extra3_Year)
        Balance_Remaining = Monthly_Balance_Remaining_Function(Balance_Remaining, Monthly_Principal)

        amortization_schedule.append([Months_Of_The_Year[Month - 1], Year, round(Monthly_Payment, 2), round(Monthly_Interest, 2),round(Monthly_Principal, 2), round(Total_Interest_Paid, 2), round(Balance_Remaining, 2)])
        if Month >= 12:
            Month = 0
            Year += 1
        Month += 1
    print("Your monthly payment amount is:", round(Monthly_Payment, 2), "dollars")
    print("Your total interest to be paid is", round(Total_Interest_Paid, 2), "dollars")
    print("Your estimated payoff date is", Months_Of_The_Year[Month - 2], Year)
    table = AsciiTable(amortization_schedule)
    if amrt_output == 'VIEW':
        print(table.table)
    elif amrt_output == 'SAVE':
        f = open(Name_File + ".txt", "w")
        f.write(table.table)
    else:
        f = open(Name_File + ".txt", "w")
        f.write(table.table)
        print(table.table)


def main():
    global Name_File
    Mortgage_Amount = float(input("Enter the mortgage amount: "))
    Mortgage_Term = (float(input("Enter the mortgage term in years: "))) * 12
    Interest_Rate = (float(input("Enter the annual interest rate percentage (numbers only): "))) / (12 * 100)

    Month = int(input("Enter the month number between 1 to 12 from when your mortgage will start: "))
    Year = int(input('Enter the year from when your mortgage will start: '))

    Monthly_Payment = Monthly_Payment_Function(Mortgage_Amount, Interest_Rate, Mortgage_Term)

    Balance_Remaining = Mortgage_Amount
    Total_Interest_Paid = 0

    print("Do you want to view the amortization schedule, save it in a text file, or do both?")
    Schedule_type = int(input("1 = view, 2 = save, 3 = both \nChoose one: "))
    if Schedule_type == 1:
        Create_amrt_schedule(Balance_Remaining, Interest_Rate, Monthly_Payment, Total_Interest_Paid, Month, Year,"VIEW")
    elif Schedule_type == 2:
        Name_File = input("Type the name of the file you want to save the schedule as: ")
        Create_amrt_schedule(Balance_Remaining, Interest_Rate, Monthly_Payment, Total_Interest_Paid, Month, Year,"SAVE")
    elif Schedule_type == 3:
        Name_File = input("Type the name of the file you want to save the schedule as: ")
        Create_amrt_schedule(Balance_Remaining, Interest_Rate, Monthly_Payment, Total_Interest_Paid, Month, Year,"BOTH")


if __name__ == "__main__":
    main()
