import datetime
import json
from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass


# -------------------------------------------
# Modify the holiday class to
# 1. Only accept Datetime objects for date.
# 2. You may need to add additional functions
# 3. You may drop the init if you are using @dataclasses
# --------------------------------------------
class Holiday:
    def __init__(self, name, date):
        self.name = name
        # check to see if date is a datetime object
        if isinstance(date, datetime.datetime):
            self.date = date
        else:
            raise TypeError("Date must be a datetime object")

    def __str__(self):
        # String output
        # Holiday output when printed.
        return f"{self.name} ({self.date.strftime('%Y-%m-%d')})"


# -------------------------------------------
# The HolidayList class acts as a wrapper and container
# For the list of holidays
# Each method has pseudo-code instructions
# --------------------------------------------


class HolidayList:
    def __init__(self):
        self.innerHolidays = []
        self.saved = False

    def addHoliday(self, holidayObj):
        # Make sure holidayObj is an Holiday Object by checking the type
        if isinstance(holidayObj, Holiday):
            # check if holiday already exists
            if self.findHoliday(holidayObj.name, holidayObj.date) is not None:
                print("Holiday already exists, not added.")
                return False
            # Use innerHolidays.append(holidayObj) to add holiday
            self.innerHolidays.append(holidayObj)
            self.saved = False
            return True
        else:
            print("Holiday Object must be of type Holiday")
            return False

    def findHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays
        for holiday in self.innerHolidays:
            if holiday.name == HolidayName:
                # Check to see if year, month, and day are the same
                if (
                    holiday.date.year == Date.year
                    and holiday.date.month == Date.month
                    and holiday.date.day == Date.day
                ):

                    # Return Holiday
                    return holiday
        # If not found, return None
        return None

    def findHolidayByName(self, HolidayName):
        # Find Holiday in innerHolidays
        for holiday in self.innerHolidays:
            if holiday.name == HolidayName:
                # Return Holiday
                return holiday
        # If not found, return None
        return None

    def removeHoliday(self, HolidayName, Date):
        # Find Holiday in innerHolidays by searching the name and date combination.
        for holiday in self.innerHolidays:
            if holiday.name == HolidayName and holiday.date == Date:
                # Remove Holiday from innerHolidays
                self.innerHolidays.remove(holiday)
                # Inform user you deleted the holiday
                print("Holiday Deleted")
                return
        # If not found, inform user that the holiday was not found.
        print("Holiday not found")

    def read_json(self, filelocation):
        # Read in things from json file location
        with open(filelocation, "r") as file:
            data = json.load(file)
            for holiday in data["holidays"]:
                # Create Holiday Object
                date = datetime.datetime.strptime(holiday["date"], "%Y-%m-%d")
                holidayObj = Holiday(holiday["name"], date)
                # Use addHoliday function to add holidays to inner list.
                self.addHoliday(holidayObj)
        self.saved = True

    def save_to_json(self, filelocation):
        # Write out json file to selected file.
        with open(filelocation, "w") as file:
            # Create a list of dictionaries
            data = []
            for holiday in self.innerHolidays:
                # Create a dictionary for each holiday
                date = holiday.date.strftime("%Y-%m-%d")
                holidayDict = {"name": holiday.name, "date": date}
                # Add dictionary to data list
                data.append(holidayDict)
            # Write data to file
            json.dump({"holidays": data}, file)
        self.saved = True

    def scrapeHolidays(self):
        # Scrape Holidays from https://www.timeanddate.com/holidays/us/
        url = "https://www.timeanddate.com/holidays/us/"
        # Remember, 2 previous years, current year, and 2  years into the future. You can scrape multiple years by adding year to the timeanddate URL. For example https://www.timeanddate.com/holidays/us/2022
        # get current year
        current_year = datetime.datetime.now().year
        # get 2 years before current year
        two_years_before = current_year - 2
        # get 2 years after current year
        two_years_after = current_year + 2
        for year in range(two_years_before, two_years_after + 1):
            # add year to url
            url = f"https://www.timeanddate.com/holidays/us/{year}"
            # get html
            res = requests.get(url)
            if res.status_code != 200:
                print(f"Error getting HTML for {url} - Status Code: {res.status_code}")
                return
            # parse html
            soup = BeautifulSoup(res.text, "html.parser")
            # find table
            holidays_table = soup.find("table", {"id": "holidays-table"})
            # get rows with attribute data-date
            rows = holidays_table.find_all("tr", {"data-date": True})
            # loop through rows
            for row in rows:
                # get holiday name
                holiday_name = row.find("a").text
                # get holiday date from the data-date attribute
                holiday_date = row.get("data-date")
                # convert holiday date from timestamp to datetime object
                holiday_date = datetime.datetime.fromtimestamp(int(holiday_date) / 1000)
                #  Check to see if name and date of holiday is in innerHolidays array
                if self.findHoliday(holiday_name, holiday_date) is None:
                    # create holiday object
                    holiday = Holiday(holiday_name, holiday_date)
                    # Add non-duplicates to innerHolidays
                    self.addHoliday(holiday)

    def numHolidays(self):
        # Return the total number of holidays in innerHolidays
        return len(self.innerHolidays)

    def filter_holidays_by_week(self, year, week_number):
        # Use a Lambda function to filter by week number and save this as holidays, use the filter on innerHolidays
        # Week number is part of the the Datetime object
        filter_by_wy = (
            lambda holiday: holiday.date.isocalendar()[1] == week_number
            and holiday.date.isocalendar()[0] == year
        )

        # Cast filter results as list
        holidays = list(filter(filter_by_wy, self.innerHolidays))
        # return your holidays
        return holidays

    def displayHolidaysInWeek(self, holidayList):
        # Use your filter_holidays_by_week to get list of holidays within a week as a parameter
        # Output formated holidays in the week.
        # * Remember to use the holiday __str__ method.
        for holiday in holidayList:
            print(holiday.__str__())
        pass

    def getWeather(self, weekNum):
        # Convert weekNum to range between two days
        # Use Try / Except to catch problems
        # Query API for weather in that week range
        # Format weather information and return weather string.
        pass

    def viewCurrentWeek(self):
        # Use the Datetime Module to look up current week and year
        # Use your filter_holidays_by_week function to get the list of holidays
        # for the current week/year
        # Use your displayHolidaysInWeek function to display the holidays in the week
        # Ask user if they want to get the weather
        # If yes, use your getWeather function and display results
        pass


def main():
    # Large Pseudo Code steps
    # -------------------------------------
    # 1. Initialize HolidayList Object
    holiday_list = HolidayList()
    # 2. Load JSON file via HolidayList read_json function
    holiday_list.read_json("holiday.json")
    # 3. Scrape additional holidays using your HolidayList scrapeHolidays function.
    holiday_list.scrapeHolidays()

    # Startup Menu
    print("Holiday Management")
    print("===================")
    print(f"There are {holiday_list.numHolidays()} holidays stored in the system.")

    # 3. Create while loop for user to keep adding or working with the Calender
    while True:
        # 4. Display User Menu (Print the menu)
        print("Holiday Menu")
        print("================")
        print("1. Add a Holiday")
        print("2. Remove a Holiday")
        print("3. Save Holiday List")
        print("4. View Holidays")
        print("5. Exit")
        print("================")
        # 5. Take user input for their action based on Menu and check the user input for errors
        while True:
            try:
                user_input = int(input("> "))
                if user_input < 1 or user_input > 5:
                    raise ValueError
                break
            except ValueError:
                print("Please enter a number between 1 and 5")
        # 6. Run appropriate method from the HolidayList object depending on what the user input is
        if user_input == 1:
            # add holiday
            print("Add a Holiday")
            print("================")
            # Ask the user for the name of the holiday
            holiday_name = input("Holiday: ")
            # Ask the user for the date of the holiday
            while True:
                try:
                    holiday_date = input("Date (YYYY-MM-DD): ")
                    holiday_date = datetime.datetime.strptime(holiday_date, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Error:")
                    print("Invalid date. Please try again.")
            # Create a Holiday object
            holiday = Holiday(holiday_name, holiday_date)
            # Add the Holiday object to the HolidayList object
            if holiday_list.addHoliday(holiday):
                print("Success:")
                print(f"{holiday} has been added to the holiday list.")
            # print current number of holidays
            print(
                f"There are now {holiday_list.numHolidays()} holidays stored in the system."
            )
        elif user_input == 2:
            # delete holiday
            print("Remove a Holiday")
            print("================")
            # Ask the user for the name of the holiday
            holiday_name = input("Holiday: ")
            # Check if the holiday exists
            holiday = holiday_list.findHolidayByName(holiday_name)
            if holiday is None:
                print("Error:")
                print(f"{holiday_name} is not in the holiday list.")
            else:
                # Remove the holiday
                holiday_list.removeHoliday(holiday.name, holiday.date)
                print("Success:")
                print(f"{holiday_name} has been removed from the holiday list.")
                # print current number of holidays
                print(
                    f"There are now {holiday_list.numHolidays()} holidays stored in the system."
                )

        elif user_input == 3:
            # save holidays
            print("Saving Holiday List")
            print("================")
            choice = input("Are you sure you want to save your changes? [y/n]: ")
            if choice.lower() == "y":
                holiday_list.save_to_json("holiday.json")
                print("Success:")
                print("Your changes have been saved.")
                # print current number of holidays
                print(
                    f"There are now {holiday_list.numHolidays()} holidays stored in the system."
                )
            else:
                print("Canceled:")
                print("No changes have been made.")
        elif user_input == 4:
            # view holidays in week
            print("View Holidays")
            print("================")
            # Ask the user for the year
            while True:
                try:
                    year = int(input("Which year?: "))
                    break
                except ValueError:
                    print("Error:")
                    print("Invalid year. Please try again.")
            # Ask the user for the week number
            while True:
                try:
                    week_number = input(
                        "Which week? #[1-52, Leave blank for the current week]: "
                    )
                    if week_number == "":
                        # Get the current week
                        week_number = datetime.datetime.now().isocalendar()[1]
                    else:
                        week_number = int(week_number)
                        if week_number < 1 or week_number > 52:
                            raise ValueError
                    break
                except ValueError:
                    print("Error:")
                    print("Invalid week number. Please try again.")
            # Get the holidays in the week
            holidays = holiday_list.filter_holidays_by_week(year, week_number)

            print(f"These are the holidays for {year} week #{week_number}:")
            # Display the holidays in the week
            holiday_list.displayHolidaysInWeek(holidays)
        elif user_input == 5:
            #  exit
            print("Exit:")
            print("================")
            if holiday_list.saved:
                choice = input("Are you sure you want to exit? [y/n]: ")
            else:
                choice = input(
                    "You have unsaved changes. Are you sure you want to exit? [y/n]: "
                )
            if choice.lower() == "y":
                print("Goodbye!")
                break
            else:
                print("Canceled:")
                print("No changes have been made.")
        # 7. Ask the User if they would like to Continue, if not, end the while loop, ending the program.  If they do wish to continue, keep the program going.


if __name__ == "__main__":
    main()


# Additional Hints:
# ---------------------------------------------
# You may need additional helper functions both in and out of the classes, add functions as you need to.
#
# No one function should be more then 50 lines of code, if you need more then 50 lines of code
# excluding comments, break the function into multiple functions.
#
# You can store your raw menu text, and other blocks of texts as raw text files
# and use placeholder values with the format option.
# Example:
# In the file test.txt is "My name is {fname}, I'm {age}"
# Then you later can read the file into a string "filetxt"
# and substitute the placeholders
# for example: filetxt.format(fname = "John", age = 36)
# This will make your code far more readable, by seperating text from code.
