"""This file contains code,
by Sungmin Kim, available from sungminkim31

Copyright 2015 Sungmin Kim
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

"""This file contains class definitions for:


"""
import math
import numpy

def ReturnAfterMonth(initial, annualInterestRate, month):
    """This function gives financial returns after months given the
    initial fund and annualInterestRate.
    """
    year = math.floor(month / 12.0)
    monthLeft = month % 12
    monthlyRate = (1 + annualInterestRate)**(1 / 12.0) - 1
    afterYear = initial * (1 + annualInterestRate)**(year)
    final = afterYear * (1 + monthlyRate)**(monthLeft)
    return(final)


def TotalCostAnnualIncrease(initialMonthlyPayment, annualRate, month):
    """This function gives total cost of monthly payment with annual increase rate.
    """
    year = math.floor(month / 12.0)
    monthLeft = month % 12
    upToYear = initialMonthlyPayment * 12 * (1 - (1 + annualRate)**(year)) / (1 - (1 + annualRate))
    lastYear = initialMonthlyPayment * 12 * (1 + annualRate)**(year)
    leftMonthPay = lastYear * (1 + annualRate) / 12 * monthLeft
    return(upToYear + leftMonthPay)


def TotalMonthlySavings(initSavings, monthlyDeposit, annualRate, month):
    """This function computes total savings after months.
    """
    c = (1 + annualRate / 12)
    fromInitSavings = initSavings * c**(month) # Assume monthly compound
    fromMonthlyDeposit = monthlyDeposit * (1 - (c)**month) / (1 - (c))
    return(fromInitSavings + fromMonthlyDeposit)

def TotalRentAndSaving(monthlyAllow, initRent, annualIncreaseRate, initSavings, annualInterest, t):
    """Out of monthly allowance you pay rent and save the rest. After t months how much would you save?
    """
    TotalRent = 0
    TotalSaving = 0
    c = (1 + annualInterest / 12)
    for i in range(0, t):
        year = math.floor(i / 12.0)
        monthLeft = i % 12
        rentIncrease = (1 + annualIncreaseRate)**year
        monthlyRent = initRent * rentIncrease
        monthSaving = monthlyAllow - monthlyRent
        TotalRent += monthlyRent
        TotalSaving += monthSaving * c**(t - i)
    TotalSaving += initSavings * c**t
    return({"TotalRent":TotalRent, "TotalSaving":TotalSaving})
    

class HousePrice:

    def __init__(self, p0, rate):
        self.initPrice = p0
        self.annualIncreaseRate = rate

    def atTime(self, t):
        currentPrice = ReturnAfterMonth(self.initPrice, self.annualIncreaseRate, t)
        return(currentPrice)

class MonthlyRentAndSaving:
    """Given monthly allowance, you pay rent and save the rest. Assume the allowance is greater than rent.
    """
    def __init__(self, initRent, RentIncreaseRate, monthlyAllow, initSavings, interestRate):        
        self.initRent = initRent
        self.annualIncreaseRate = RentIncreaseRate
        self.monthlyAllow = monthlyAllow
        self.initSavings = initSavings
        self.annualInterest = interestRate

    def RentAndSavingAtTime(self, t):
        total = TotalRentAndSaving(self.monthlyAllow, self.initRent, self.annualIncreaseRate, self.initSavings, self.annualInterest, t)
        return(total)

class MonthlySavings:
    def __init__(self, initSavings, monthly, rate):
        self.initSavings = initSavings
        self.monthlySavings = monthly
        self.annualRate = rate

    def atTime(self, t):
        totalSavings = TotalMonthlySavings(self.initSavings, self.monthlySavings, self.annualRate, t)
        return(totalSavings)
    
class MortgagePaymentPrincipal:
    """Mortgage formula
    source: http://www.mtgprofessor.com/formulas.htm
    """
    def __init__(self, initPrincipal, rate, n_payment):
        self.initPrincipal = initPrincipal
        self.annualRate = rate
        self.n_payment = n_payment
        c = self.annualRate / 12
        self.p = self.initPrincipal * (c * (1 + c) * self.n_payment) / ((1 + c) * self.n_payment - 1)

    def MonthlyPayment(self):
        return(self.p)
        
    def TotalPaymentAfterTime(self, k):
        """Total mortgage payments after k monthly payment of mortgage.
        Monthly payment: P = L[c(1 + c)n]/[(1 + c)n - 1]
        """
        return(self.p * k) 

    def RemainingPrincipalAfterTime(self, k):
        """Remaining Principal after paying k monthly mortgage.
        Remaning Loan Balance: B = L[(1 + c)n - (1 + c)k]/[(1 + c)n - 1]
        """
        c = self.annualRate / 12
        b = self.initPrincipal * ((1 + c) * self.n_payment - (1 + c) * k) / ((1+c) * self.n_payment - 1)
        return(b) 
        
        
def main():
    HOUSE_PRICE_INCREASE_RATE = 0.00
    HOUSE_CURRENT_PRICE = 800 # unit is $1000
    MONTH_AFTER = 12 * 5 # 

    print("Your target house is priced at ${}k and you expect the price would increase at the rate of {} annually. You want to evaluate your bottom line after {} months".format(HOUSE_CURRENT_PRICE, HOUSE_PRICE_INCREASE_RATE, MONTH_AFTER))
          
    MONTHLY_ALLOW = 8 # unit is $1000
    INIT_RENT = 2.8
    RENT_INCREASE_RATE = 0.04
    INIT_SAVINGS = 70
    SAVING_INTEREST_RATE = 0.02

    print("Your monthly budget for housing is ${}k. You are currently paying ${}k for your rent and you expect the rent would increase {} annually. Currently you hae savings of ${}k and your expected interest rate for the savings is {}.".format(MONTHLY_ALLOW, INIT_RENT, RENT_INCREASE_RATE, INIT_SAVINGS, SAVING_INTEREST_RATE))

    MORTGAGE_RATE = 0.05
    MORTGAGE_N = 12 * 30 # 30 years monthly payment
    CLOSING_COST = HOUSE_CURRENT_PRICE * 0.01 # Assume 1% of house price. http://www.zillow.com/mortgage-rates/buying-a-home/closing-costs/

    print("You plan to have {} years mortgage with the rate {}. And you set aside ${}k for the extra cost of your moving.".format(math.floor(MORTGAGE_N/12), MORTGAGE_RATE, CLOSING_COST))
    
    MONTHLY_MAINTENANCE = 0.3 # $300 monthly maintenance cost
    MONTHLY_INSURANCE = 0.1

    print("Your expected monthly maintenance cost is about ${}k and monthly insurance is ${}k.".format(MONTHLY_MAINTENANCE, MONTHLY_INSURANCE))

    # initialize
    myRentAndSaving = MonthlyRentAndSaving(INIT_RENT, RENT_INCREASE_RATE, MONTHLY_ALLOW, INIT_SAVINGS, SAVING_INTEREST_RATE)
    myHouse = HousePrice(HOUSE_CURRENT_PRICE, HOUSE_PRICE_INCREASE_RATE)

    totalRent = []
    totalSavingBefore = []
    principal = []
    housePurchasePrice = []
    monthlyMortgage = []
    totalSavingAfter = []
    remainingPrincipal = []
    totalMortgage = []

    # compute required components
    for t in range(0, MONTH_AFTER):
        # Before buying a house
        temp = myRentAndSaving.RentAndSavingAtTime(t)
        totalRent.append(temp["TotalRent"])
        totalSavingBefore.append(temp["TotalSaving"])
        # At the purchase
        initPrincipal = myHouse.atTime(t) - temp["TotalSaving"] + CLOSING_COST
        principal.append(initPrincipal)
        housePurchasePrice.append(myHouse.atTime(t))
        
        # At the evaluation time
        myMortgage = MortgagePaymentPrincipal(initPrincipal, MORTGAGE_RATE, MORTGAGE_N)
        monthlyMortgage.append(myMortgage.MonthlyPayment())
        totalMortgage.append(myMortgage.TotalPaymentAfterTime(MONTH_AFTER - t))
        remainingPrincipal.append(myMortgage.RemainingPrincipalAfterTime(MONTH_AFTER - t))
        property_tax = 0.01 * housePurchasePrice[t]
        mySavingsAfter = MonthlySavings(0, MONTHLY_ALLOW - myMortgage.MonthlyPayment() - MONTHLY_MAINTENANCE - MONTHLY_INSURANCE - property_tax/12, SAVING_INTEREST_RATE)
        totalSavingAfter.append(mySavingsAfter.atTime(MONTH_AFTER - t))


    # compute bottom line for each t
    moneyAtHand = []
    for t in range(0, MONTH_AFTER):
        # Assume transanction cost 15% of the house price
        moneyAtHand.append(myHouse.atTime(MONTH_AFTER) * 0.85 - remainingPrincipal[t] + totalSavingAfter[t])

    moneyAtHand = numpy.array(moneyAtHand)

    print("Your bottom lines: The optimal purchase time is after month {} whose expected bottom line is ${:.2f}k and the worst purchase time is after {} month whose expected bottom line is ${:.2f}k.".format(numpy.argmax(moneyAtHand), numpy.max(moneyAtHand), numpy.argmin(moneyAtHand), numpy.min(moneyAtHand)))

    #for t in range(0, MONTH_AFTER):    
    #   print("After {} month you have {}.".format(t, moneyAtHand[t]))

           
        
    
