from bs4 import BeautifulSoup
from selectolax.parser import HTMLParser
import re
import pandas as pd

def scaner_file(url):
    file = os.listdir(url)
    for f in file:
        real_url = path.join(url, f)
        if path.isfile(real_url):
            print(path.abspath(real_url))
            Str = str(path.abspath(real_url))
            if Str[-3:]=="txt":
                Url_list.append(Str)
            else:
                Str = '0'
            # 如果是文件，则以绝度路径的方式输出
        elif path.isdir(real_url):
            # 如果是目录，则是地柜调研自定义函数 scaner_file (url)进行多次
            scaner_file(real_url)
        else:
            print("其他情况")
            pass
        #print(real_url)

def get_item1(x):
    number = int(x[x.rindex('-') - 2:x.rindex('-')])
    if number<6 or number>93:
        try:
            fp = open(x, 'r', encoding='utf-8')
            soup = BeautifulSoup(fp, 'lxml')
            TenKtext = soup.text
            matches = re.compile(r'(item\s*(1[\.*\s*]|2[\.*\s*])|'
                                 'business?|'
                                 'properties?)',
                                 re.IGNORECASE)

            matches_array = pd.DataFrame(
                [(match.group(), match.start()) for match in matches.finditer(TenKtext)])

            # Set columns in the dataframe
            matches_array.columns = ['SearchTerm', 'Start']

            # Get the number of rows in the dataframe
            Rows = matches_array['SearchTerm'].count()

            # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
            count = 0  # Counter to help with row location and iteration
            while count < (Rows - 1):  # Can only iterate to the second last row
                matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                    count + 1, 0]).lower()  # Convert to lower case
                count += 1

            # Set up 'Item 7/8 Search Pattern' regex patterns
            matches_item7 = re.compile(r'(item\s*1\.*\s*business\s*[a-z]*)')
            matches_item8 = re.compile(r'(item\s*2\.*\s*properties\s*[a-z]*)')

            # Lists to store the locations of Item 7/8 Search Pattern matches
            Start_Loc = []
            End_Loc = []

            # Find and store the locations of Item 7/8 Search Pattern matches
            count = 0  # Set up counter

            while count < (Rows - 1):  # Can only iterate to the second last row

                # Match Item 7 Search Pattern
                if re.match(matches_item7, matches_array.at[count, 'Selection']):
                    # Column 1 = 'Start' columnn in 'matches_array'
                    Start_Loc.append(matches_array.iloc[
                                         count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                # Match Item 8 Search Pattern
                if re.match(matches_item8, matches_array.at[count, 'Selection']):
                    End_Loc.append(matches_array.iloc[count, 1])

                count += 1
            if len(Start_Loc) == 1:
                Start_Loc.insert(1, Start_Loc[0])
            if len(End_Loc) == 1:
                End_Loc.insert(1, End_Loc[0])

            End_Loc[0] = End_Loc[-2]
            End_Loc[1] = End_Loc[-1]

            if (End_Loc[1] - Start_Loc[1]) <= (End_Loc[0] - Start_Loc[0]):
                End_Loc[1] = End_Loc[0]
                Start_Loc[1] = Start_Loc[0]

            # Extract section of text and store in 'TenKItem7'
            TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

            # Clean newly extracted text
            TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
            TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
            TenKItem7 = TenKItem7.replace('\r',
                                          '')  # Replace \r (carriage returns-if you're on windows) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            while '  ' in TenKItem7:
                TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

            # Print first 500 characters of newly extracted text
            return (TenKItem7)

                   
        except:
            return ("False")

    else:
        try:
            fp = open(x, 'r', encoding='utf-8')
            soup = BeautifulSoup(fp, 'lxml')
            # Grab and store the 10K text body
            TenKtext = soup.text

            # Set up the regex pattern
            matches = re.compile(r'(item\s*(1a[\.*\s*]|1[\.*\s*]|I[\.*\s*])|'
                                 'risk\sfactors?|'
                                 'business)',
                                 re.IGNORECASE)

            matches_array = pd.DataFrame(
                [(match.group(), match.start()) for match in matches.finditer(TenKtext)])

            # Set columns in the dataframe
            matches_array.columns = ['SearchTerm', 'Start']

            # Get the number of rows in the dataframe
            Rows = matches_array['SearchTerm'].count()

            # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
            count = 0  # Counter to help with row location and iteration
            while count < (Rows - 1):  # Can only iterate to the second last row
                matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                    count + 1, 0]).lower()  # Convert to lower case
                count += 1

            # Set up 'Item 7/8 Search Pattern' regex patterns
            matches_item7 = re.compile(r'(item\s*1\.*\s*business)')
            matches_item8 = re.compile(r'(item\s*1*a\.*\s*risk\s*[a-z]*)')

            # Lists to store the locations of Item 7/8 Search Pattern matches
            Start_Loc = []
            End_Loc = []

            # Find and store the locations of Item 7/8 Search Pattern matches
            count = 0  # Set up counter

            while count < (Rows - 1):  # Can only iterate to the second last row

                # Match Item 7 Search Pattern
                if re.match(matches_item7, matches_array.at[count, 'Selection']):
                    # Column 1 = 'Start' columnn in 'matches_array'
                    Start_Loc.append(matches_array.iloc[
                                         count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                # Match Item 8 Search Pattern
                if re.match(matches_item8, matches_array.at[count, 'Selection']):
                    End_Loc.append(matches_array.iloc[count, 1])

                count += 1
            if len(Start_Loc) == 1:
                Start_Loc.insert(1, Start_Loc[0])
            if len(End_Loc) == 1:
                End_Loc.insert(1, End_Loc[0])

            End_Loc[0] = End_Loc[-2]
            End_Loc[1] = End_Loc[-1]

            if (End_Loc[1] - Start_Loc[1]) <= (End_Loc[0] - Start_Loc[0]):
                End_Loc[1] = End_Loc[0]
                Start_Loc[1] = Start_Loc[0]

            # Extract section of text and store in 'TenKItem7'
            TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

            # Clean newly extracted text
            TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
            TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
            TenKItem7 = TenKItem7.replace('\r',
                                          '')  # Replace \r (carriage returns-if you're on windows) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            while '  ' in TenKItem7:
                TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

            # Print first 500 characters of newly extracted text
            return (TenKItem7)

        except:
            return ("False")
def get_item1a(x):
    try:
        fp = open(x, 'r', encoding='utf-8')
        soup = BeautifulSoup(fp, 'lxml')
        # Grab and store the 10K text body
        TenKtext = soup.text

        # Set up the regex pattern
        matches = re.compile(r'(item\s*(1？a[\.*\s*]|1？b[\.*\s*])|'
                             'risk\sfactors?|'
                             'Unresolved\sStaff\sComments)',
                             re.IGNORECASE)

        matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])

        # Set columns in the dataframe
        matches_array.columns = ['SearchTerm', 'Start']

        # Get the number of rows in the dataframe
        Rows = matches_array['SearchTerm'].count()

        # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
        count = 0  # Counter to help with row location and iteration
        while count < (Rows - 1):  # Can only iterate to the second last row
            matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                count + 1, 0]).lower()  # Convert to lower case
            count += 1

        # Set up 'Item 7/8 Search Pattern' regex patterns
        matches_item7 = re.compile(r'(item\s*1*a\.*\s*risk\s[a-z]*)')
        matches_item8 = re.compile(r'(item\s*1b\.*\s*unresolved\s[a-z]*)')

        # Lists to store the locations of Item 7/8 Search Pattern matches
        Start_Loc = []
        End_Loc = []

        # Find and store the locations of Item 7/8 Search Pattern matches
        count = 0  # Set up counter

        while count < (Rows - 1):  # Can only iterate to the second last row

            # Match Item 7 Search Pattern
            if re.match(matches_item7, matches_array.at[count, 'Selection']):
                # Column 1 = 'Start' columnn in 'matches_array'
                Start_Loc.append(matches_array.iloc[
                                     count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

            # Match Item 8 Search Pattern
            if re.match(matches_item8, matches_array.at[count, 'Selection']):
                End_Loc.append(matches_array.iloc[count, 1])

            count += 1
        if len(Start_Loc) == 1:
            Start_Loc.insert(1, Start_Loc[0])
        if len(End_Loc) == 1:
            End_Loc.insert(1, End_Loc[0])

        End_Loc[0] = End_Loc[-2]
        End_Loc[1] = End_Loc[-1]

        if (End_Loc[1] - Start_Loc[1]) <= (End_Loc[0] - Start_Loc[0]):
            End_Loc[1] = End_Loc[0]
            Start_Loc[1] = Start_Loc[0]
        # Extract section of text and store in 'TenKItem7'
        TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

        # Clean newly extracted text
        TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
        TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
        TenKItem7 = TenKItem7.replace('\r', '')  # Replace \r (carriage returns-if you're on windows) with space
        TenKItem7 = TenKItem7.replace(' ',
                                      ' ')  # Replace " " (a special character for space in HTML) with space
        TenKItem7 = TenKItem7.replace(' ',
                                      ' ')  # Replace " " (a special character for space in HTML) with space
        while '  ' in TenKItem7:
            TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

        # Print first 500 characters of newly extracted text
        return (TenKItem7)
    except:
        return("False")
def get_item1b(x):
    try:
        fp = open(x, 'r', encoding='utf-8')
        soup = BeautifulSoup(fp, 'lxml')
        TenKtext = soup.text

        # Set up the regex pattern
        matches = re.compile(r'(item\s*(2[\.*\s*]|1？b[\.*\s*])|'
                             'properties|'
                             'Unresolved\sStaff\sComments)',
                             re.IGNORECASE)

        matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])

        # Set columns in the dataframe
        matches_array.columns = ['SearchTerm', 'Start']

        # Get the number of rows in the dataframe
        Rows = matches_array['SearchTerm'].count()

        # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
        count = 0  # Counter to help with row location and iteration
        while count < (Rows - 1):  # Can only iterate to the second last row
            matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                count + 1, 0]).lower()  # Convert to lower case
            count += 1

        # Set up 'Item 7/8 Search Pattern' regex patterns
        matches_item7 = re.compile(r'(item\s*1*b\.*\s*unresolved\s[a-z]*)')
        matches_item8 = re.compile(r'(item\s*2\.*\s*properties)')

        # Lists to store the locations of Item 7/8 Search Pattern matches
        Start_Loc = []
        End_Loc = []

        # Find and store the locations of Item 7/8 Search Pattern matches
        count = 0  # Set up counter

        while count < (Rows - 1):  # Can only iterate to the second last row

            # Match Item 7 Search Pattern
            if re.match(matches_item7, matches_array.at[count, 'Selection']):
                # Column 1 = 'Start' columnn in 'matches_array'
                Start_Loc.append(matches_array.iloc[
                                     count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

            # Match Item 8 Search Pattern
            if re.match(matches_item8, matches_array.at[count, 'Selection']):
                End_Loc.append(matches_array.iloc[count, 1])

            count += 1
        if len(Start_Loc) == 1:
            Start_Loc.insert(1, Start_Loc[0])
        if len(End_Loc) == 1:
            End_Loc.insert(1, End_Loc[0])
        End_Loc[0] = End_Loc[-2]
        End_Loc[1] = End_Loc[-1]

        if (End_Loc[1] - Start_Loc[1]) <= (End_Loc[0] - Start_Loc[0]):
            End_Loc[1] = End_Loc[0]
            Start_Loc[1] = Start_Loc[0]
        # Extract section of text and store in 'TenKItem7'
        TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

        # Clean newly extracted text
        TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
        TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
        TenKItem7 = TenKItem7.replace('\r', '')  # Replace \r (carriage returns-if you're on windows) with space
        TenKItem7 = TenKItem7.replace(' ',
                                      ' ')  # Replace " " (a special character for space in HTML) with space
        TenKItem7 = TenKItem7.replace(' ',
                                      ' ')  # Replace " " (a special character for space in HTML) with space
        while '  ' in TenKItem7:
            TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

        # Print first 500 characters of newly extracted text
        return (TenKItem7)
    except:
        return("False")
def get_item2(x):
    try:
        fp = open(x, 'r', encoding='utf-8')
        soup = BeautifulSoup(fp, 'lxml')
        TenKtext = soup.text

        # Set up the regex pattern
        matches = re.compile(r'(item\s*(2[\.\s]|3[\.\s])|'
                             'properties|'
                             'legal\sproceedings?)',
                             re.IGNORECASE)

        matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])

        # Set columns in the dataframe
        matches_array.columns = ['SearchTerm', 'Start']

        # Get the number of rows in the dataframe
        Rows = matches_array['SearchTerm'].count()

        # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
        count = 0  # Counter to help with row location and iteration
        while count < (Rows - 1):  # Can only iterate to the second last row
            matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                count + 1, 0]).lower()  # Convert to lower case
            count += 1

        # Set up 'Item 7/8 Search Pattern' regex patterns
        matches_item7 = re.compile(r'(item\s*2\.*\s*properties)')
        matches_item8 = re.compile(r'(item\s*3\.*\s*legal\s[a-z]*)')

        # Lists to store the locations of Item 7/8 Search Pattern matches
        Start_Loc = []
        End_Loc = []

        # Find and store the locations of Item 7/8 Search Pattern matches
        count = 0  # Set up counter

        while count < (Rows - 1):  # Can only iterate to the second last row

            # Match Item 7 Search Pattern
            if re.match(matches_item7, matches_array.at[count, 'Selection']):
                # Column 1 = 'Start' columnn in 'matches_array'
                Start_Loc.append(matches_array.iloc[
                                     count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

            # Match Item 8 Search Pattern
            if re.match(matches_item8, matches_array.at[count, 'Selection']):
                End_Loc.append(matches_array.iloc[count, 1])

            count += 1
        if len(Start_Loc) == 1:
            Start_Loc.insert(1, Start_Loc[0])
        if len(End_Loc) == 1:
            End_Loc.insert(1, End_Loc[0])

        End_Loc[0] = End_Loc[-2]
        End_Loc[1] = End_Loc[-1]

        if (End_Loc[1] - Start_Loc[1]) <= (End_Loc[0] - Start_Loc[0]):
            End_Loc[1] = End_Loc[0]
            Start_Loc[1] = Start_Loc[0]
        # Extract section of text and store in 'TenKItem7'
        TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

        # Clean newly extracted text
        TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
        TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
        TenKItem7 = TenKItem7.replace('\r', '')  # Replace \r (carriage returns-if you're on windows) with space
        TenKItem7 = TenKItem7.replace(' ',
                                      ' ')  # Replace " " (a special character for space in HTML) with space
        TenKItem7 = TenKItem7.replace(' ',
                                      ' ')  # Replace " " (a special character for space in HTML) with space
        while '  ' in TenKItem7:
            TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

        # Print first 500 characters of newly extracted text
        return (TenKItem7)
    except:
        return("False")
def get_item3(x):
    number = int(x[x.rindex('-') - 2:x.rindex('-')])
    if number>=6 and number<=93:
        try:
            fp = open(x, 'r', encoding='utf-8')
            soup = BeautifulSoup(fp, 'lxml')
            # Grab and store the 10K text body
            TenKtext = soup.text

            # Set up the regex pattern
            matches = re.compile(r'(item\s*(3[\.\s]|4[\.\s])|'
                                 'legal\sproceedings?|'
                                 'mine\ssafety\sdisclosures?)',
                                 re.IGNORECASE)

            matches_array = pd.DataFrame(
                [(match.group(), match.start()) for match in matches.finditer(TenKtext)])

            # Set columns in the dataframe
            matches_array.columns = ['SearchTerm', 'Start']

            # Get the number of rows in the dataframe
            Rows = matches_array['SearchTerm'].count()

            # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
            count = 0  # Counter to help with row location and iteration
            while count < (Rows - 1):  # Can only iterate to the second last row
                matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                    count + 1, 0]).lower()  # Convert to lower case
                count += 1

            # Set up 'Item 7/8 Search Pattern' regex patterns
            matches_item7 = re.compile(r'(item\s*3\.*\s*legal\s*[a-z]*)')
            matches_item8 = re.compile(r'(item\s*4\.*\s*mine\s*[a-z]*)')

            # Lists to store the locations of Item 7/8 Search Pattern matches
            Start_Loc = []
            End_Loc = []

            # Find and store the locations of Item 7/8 Search Pattern matches
            count = 0  # Set up counter

            while count < (Rows - 1):  # Can only iterate to the second last row

                # Match Item 7 Search Pattern
                if re.match(matches_item7, matches_array.at[count, 'Selection']):
                    # Column 1 = 'Start' columnn in 'matches_array'
                    Start_Loc.append(matches_array.iloc[
                                         count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                # Match Item 8 Search Pattern
                if re.match(matches_item8, matches_array.at[count, 'Selection']):
                    End_Loc.append(matches_array.iloc[count, 1])

                count += 1
            if len(Start_Loc) == 1:
                Start_Loc.insert(1, Start_Loc[0])
            if len(End_Loc) == 1:
                End_Loc.insert(1, End_Loc[0])
            End_Loc[0] = End_Loc[-2]
            End_Loc[1] = End_Loc[-1]
            if (End_Loc[1] - Start_Loc[1]) <= (End_Loc[0] - Start_Loc[0]):
                End_Loc[1] = End_Loc[0]
                Start_Loc[1] = Start_Loc[0]
            # Extract section of text and store in 'TenKItem7'
            TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

            # Clean newly extracted text
            TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
            TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
            TenKItem7 = TenKItem7.replace('\r',
                                          '')  # Replace \r (carriage returns-if you're on windows) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            while '  ' in TenKItem7:
                TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

            # Print first 500 characters of newly extracted text
            return (TenKItem7)

                   
        except:
            return ("False")
    else:
        try:
            fp = open(x, 'r', encoding='utf-8')
            soup = BeautifulSoup(fp, 'lxml')
            TenKtext = soup.text

            # Set up the regex pattern
            matches = re.compile(r'(item\s*(3[\.\s]|4[\.\s])|'
                                 'legal\sproceedings?|'
                                 'Submission\sof\sMatters?)',
                                 re.IGNORECASE)

            matches_array = pd.DataFrame(
                [(match.group(), match.start()) for match in matches.finditer(TenKtext)])

            # Set columns in the dataframe
            matches_array.columns = ['SearchTerm', 'Start']

            # Get the number of rows in the dataframe
            Rows = matches_array['SearchTerm'].count()

            # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
            count = 0  # Counter to help with row location and iteration
            while count < (Rows - 1):  # Can only iterate to the second last row
                matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                    count + 1, 0]).lower()  # Convert to lower case
                count += 1

            # Set up 'Item 7/8 Search Pattern' regex patterns
            matches_item7 = re.compile(r'(item\s*3\.*\s*legal\s*[a-z]*)')
            matches_item8 = re.compile(r'(item\s*4\.*\s*submission\s*[a-z]*)')

            # Lists to store the locations of Item 7/8 Search Pattern matches
            Start_Loc = []
            End_Loc = []

            # Find and store the locations of Item 7/8 Search Pattern matches
            count = 0  # Set up counter

            while count < (Rows - 1):  # Can only iterate to the second last row

                # Match Item 7 Search Pattern
                if re.match(matches_item7, matches_array.at[count, 'Selection']):
                    # Column 1 = 'Start' columnn in 'matches_array'
                    Start_Loc.append(matches_array.iloc[
                                         count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                # Match Item 8 Search Pattern
                if re.match(matches_item8, matches_array.at[count, 'Selection']):
                    End_Loc.append(matches_array.iloc[count, 1])

                count += 1
            if len(Start_Loc) == 1:
                Start_Loc.insert(1, Start_Loc[0])
            if len(End_Loc) == 1:
                End_Loc.insert(1, End_Loc[0])

            End_Loc[0] = End_Loc[-2]
            End_Loc[1] = End_Loc[-1]

            if (End_Loc[1] - Start_Loc[1]) <= (End_Loc[0] - Start_Loc[0]):
                End_Loc[1] = End_Loc[0]
                Start_Loc[1] = Start_Loc[0]
            # Extract section of text and store in 'TenKItem7'
            TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

            # Clean newly extracted text
            TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
            TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
            TenKItem7 = TenKItem7.replace('\r',
                                          '')  # Replace \r (carriage returns-if you're on windows) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            TenKItem7 = TenKItem7.replace(' ',
                                          ' ')  # Replace " " (a special character for space in HTML) with space
            while '  ' in TenKItem7:
                TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

            # Print first 500 characters of newly extracted text
            return (TenKItem7)

                   
        except:
            return ("False")

def get_item5(x):
    try:
        fp = open(x, 'r', encoding='utf-8')
        soup = BeautifulSoup(fp, 'lxml')
        for filing_document in soup.find_all(
                'document'):  # The document tags contain the various components of the total 10K filing pack

            # The 'type' tag contains the document type
            document_type = filing_document.type.find(text=True, recursive=False).strip()

            if document_type == "10-K":  # Once the 10K text body is found

                # Grab and store the 10K text body
                TenKtext = filing_document.find('text').extract().text

                # Set up the regex pattern
                matches = re.compile(r'(item\s(5[\.\s]|6[\.\s])|'
                                     'market\sfor(\sthe)?\sregistrant?|'
                                     'selected\sfinancial\sdata)',
                                     re.IGNORECASE)

                matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])

                # Set columns in the dataframe
                matches_array.columns = ['SearchTerm', 'Start']

                # Get the number of rows in the dataframe
                Rows = matches_array['SearchTerm'].count()

                # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
                count = 0  # Counter to help with row location and iteration
                while count < (Rows - 1):  # Can only iterate to the second last row
                    matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                        count + 1, 0]).lower()  # Convert to lower case
                    count += 1

                # Set up 'Item 7/8 Search Pattern' regex patterns
                matches_item7 = re.compile(r'(item\s5\.*\s*market\s[a-z]*)')
                matches_item8 = re.compile(r'(item\s6\.*\s*selected\s[a-z]*)')

                # Lists to store the locations of Item 7/8 Search Pattern matches
                Start_Loc = []
                End_Loc = []

                # Find and store the locations of Item 7/8 Search Pattern matches
                count = 0  # Set up counter

                while count < (Rows - 1):  # Can only iterate to the second last row

                    # Match Item 7 Search Pattern
                    if re.match(matches_item7, matches_array.at[count, 'Selection']):
                        # Column 1 = 'Start' columnn in 'matches_array'
                        Start_Loc.append(matches_array.iloc[
                                             count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                    # Match Item 8 Search Pattern
                    if re.match(matches_item8, matches_array.at[count, 'Selection']):
                        End_Loc.append(matches_array.iloc[count, 1])

                    count += 1
                if len(Start_Loc) == 1:
                    Start_Loc.insert(1, Start_Loc[0])
                if len(End_Loc) == 1:
                    End_Loc.insert(1, End_Loc[0])
                i_1 = 0
                while Start_Loc[1] > End_Loc[1]:
                    End_Loc[1] = End_Loc[1 + i_1]
                    i_1 = i_1 + 1

                # Extract section of text and store in 'TenKItem7'
                TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

                # Clean newly extracted text
                TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
                TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
                TenKItem7 = TenKItem7.replace('\r', '')  # Replace \r (carriage returns-if you're on windows) with space
                TenKItem7 = TenKItem7.replace(' ',
                                              ' ')  # Replace " " (a special character for space in HTML) with space
                TenKItem7 = TenKItem7.replace(' ',
                                              ' ')  # Replace " " (a special character for space in HTML) with space
                while '  ' in TenKItem7:
                    TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

                # Print first 500 characters of newly extracted text
                return (TenKItem7)
    except:
        return("False")
def get_item6(x):
    try:
        fp = open(x, 'r', encoding='utf-8')
        soup = BeautifulSoup(fp, 'lxml')
        for filing_document in soup.find_all(
                'document'):  # The document tags contain the various components of the total 10K filing pack

            # The 'type' tag contains the document type
            document_type = filing_document.type.find(text=True, recursive=False).strip()

            if document_type == "10-K":  # Once the 10K text body is found

                # Grab and store the 10K text body
                TenKtext = filing_document.find('text').extract().text

                # Set up the regex pattern
                matches = re.compile(r'(item\s(5[\.\s]|6[\.\s])|'
                                     'market\sfor(\sthe)?\sregistrant?|'
                                     'selected\sfinancial\sdata)',
                                     re.IGNORECASE)

                matches_array = pd.DataFrame([(match.group(), match.start()) for match in matches.finditer(TenKtext)])

                # Set columns in the dataframe
                matches_array.columns = ['SearchTerm', 'Start']

                # Get the number of rows in the dataframe
                Rows = matches_array['SearchTerm'].count()

                # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
                count = 0  # Counter to help with row location and iteration
                while count < (Rows - 1):  # Can only iterate to the second last row
                    matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                        count + 1, 0]).lower()  # Convert to lower case
                    count += 1

                # Set up 'Item 7/8 Search Pattern' regex patterns
                matches_item7 = re.compile(r'(item\s5\.*\s*market\s[a-z]*)')
                matches_item8 = re.compile(r'(item\s6\.*\s*selected\s[a-z]*)')

                # Lists to store the locations of Item 7/8 Search Pattern matches
                Start_Loc = []
                End_Loc = []

                # Find and store the locations of Item 7/8 Search Pattern matches
                count = 0  # Set up counter

                while count < (Rows - 1):  # Can only iterate to the second last row

                    # Match Item 7 Search Pattern
                    if re.match(matches_item7, matches_array.at[count, 'Selection']):
                        # Column 1 = 'Start' columnn in 'matches_array'
                        Start_Loc.append(matches_array.iloc[
                                             count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                    # Match Item 8 Search Pattern
                    if re.match(matches_item8, matches_array.at[count, 'Selection']):
                        End_Loc.append(matches_array.iloc[count, 1])

                    count += 1
                if len(Start_Loc) == 1:
                    Start_Loc.insert(1, Start_Loc[0])
                if len(End_Loc) == 1:
                    End_Loc.insert(1, End_Loc[0])
                i_1 = 0
                while Start_Loc[1] > End_Loc[1]:
                    End_Loc[1] = End_Loc[1 + i_1]
                    i_1 = i_1 + 1

                # Extract section of text and store in 'TenKItem7'
                TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

                # Clean newly extracted text
                TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
                TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
                TenKItem7 = TenKItem7.replace('\r', '')  # Replace \r (carriage returns-if you're on windows) with space
                TenKItem7 = TenKItem7.replace(' ',
                                              ' ')  # Replace " " (a special character for space in HTML) with space
                TenKItem7 = TenKItem7.replace(' ',
                                              ' ')  # Replace " " (a special character for space in HTML) with space
                while '  ' in TenKItem7:
                    TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

                # Print first 500 characters of newly extracted text
                return (TenKItem7)
    except:
        return("False")
def get_item7(x):
    number = int(x[x.rindex('-') - 2:x.rindex('-')])
    if number<6 or number>93:
        try:
            fp = open(x, 'r', encoding='utf-8')
            soup = BeautifulSoup(fp, 'lxml')
            for filing_document in soup.find_all(
                    'document'):  # The document tags contain the various components of the total 10K filing pack

                # The 'type' tag contains the document type
                document_type = filing_document.type.find(text=True, recursive=False).strip()

                if document_type == "10-K":  # Once the 10K text body is found

                    # Grab and store the 10K text body
                    TenKtext = filing_document.find('text').extract().text

                    # Set up the regex pattern
                    matches = re.compile(r'(item\s(7[\.\s]|8[\.\s])|'
                                         'management.s?\sdiscussion\sand\sanalysis|'
                                         'financial\sstatements?\sand\ssupplementary?)',
                                         re.IGNORECASE)

                    matches_array = pd.DataFrame(
                        [(match.group(), match.start()) for match in matches.finditer(TenKtext)])

                    # Set columns in the dataframe
                    matches_array.columns = ['SearchTerm', 'Start']

                    # Get the number of rows in the dataframe
                    Rows = matches_array['SearchTerm'].count()

                    # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
                    count = 0  # Counter to help with row location and iteration
                    while count < (Rows - 1):  # Can only iterate to the second last row
                        matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                            count + 1, 0]).lower()  # Convert to lower case
                        count += 1

                    # Set up 'Item 7/8 Search Pattern' regex patterns
                    matches_item7 = re.compile(r'(item\s7\.*\s*management.s\s*[a-z]*)')
                    matches_item8 = re.compile(r'(item\s8\.*\s*financial\s*[a-z]*)')

                    # Lists to store the locations of Item 7/8 Search Pattern matches
                    Start_Loc = []
                    End_Loc = []

                    # Find and store the locations of Item 7/8 Search Pattern matches
                    count = 0  # Set up counter

                    while count < (Rows - 1):  # Can only iterate to the second last row

                        # Match Item 7 Search Pattern
                        if re.match(matches_item7, matches_array.at[count, 'Selection']):
                            # Column 1 = 'Start' columnn in 'matches_array'
                            Start_Loc.append(matches_array.iloc[
                                                 count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                        # Match Item 8 Search Pattern
                        if re.match(matches_item8, matches_array.at[count, 'Selection']):
                            End_Loc.append(matches_array.iloc[count, 1])

                        count += 1
                    if len(Start_Loc) == 1:
                        Start_Loc.insert(1, Start_Loc[0])
                    if len(End_Loc) == 1:
                        End_Loc.insert(1, End_Loc[0])

                    # Extract section of text and store in 'TenKItem7'
                    TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

                    # Clean newly extracted text
                    TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
                    TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
                    TenKItem7 = TenKItem7.replace('\r',
                                                  '')  # Replace \r (carriage returns-if you're on windows) with space
                    TenKItem7 = TenKItem7.replace(' ',
                                                  ' ')  # Replace " " (a special character for space in HTML) with space
                    TenKItem7 = TenKItem7.replace(' ',
                                                  ' ')  # Replace " " (a special character for space in HTML) with space
                    while '  ' in TenKItem7:
                        TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

                    # Print first 500 characters of newly extracted text
                    return (TenKItem7)
        except:
            return ("False")
    else:
        try:
            fp = open(x, 'r', encoding='utf-8')
            soup = BeautifulSoup(fp, 'lxml')
            for filing_document in soup.find_all(
                    'document'):  # The document tags contain the various components of the total 10K filing pack

                # The 'type' tag contains the document type
                document_type = filing_document.type.find(text=True, recursive=False).strip()

                if document_type == "10-K":  # Once the 10K text body is found

                    # Grab and store the 10K text body
                    TenKtext = filing_document.find('text').extract().text

                    # Set up the regex pattern
                    matches = re.compile(r'(item\s(7[\.\s]|7a[\.\s])|'
                                         'management.s?\sdiscussion\sand\sanalysis|'
                                         'quantitative\sand\squantitative\sdisclosures?)',
                                         re.IGNORECASE)

                    matches_array = pd.DataFrame(
                        [(match.group(), match.start()) for match in matches.finditer(TenKtext)])

                    # Set columns in the dataframe
                    matches_array.columns = ['SearchTerm', 'Start']

                    # Get the number of rows in the dataframe
                    Rows = matches_array['SearchTerm'].count()

                    # Create a new column in 'matches_array' called 'Selection' and add adjacent 'SearchTerm' (i and i+1 rows) text concatenated
                    count = 0  # Counter to help with row location and iteration
                    while count < (Rows - 1):  # Can only iterate to the second last row
                        matches_array.at[count, 'Selection'] = (matches_array.iloc[count, 0] + matches_array.iloc[
                            count + 1, 0]).lower()  # Convert to lower case
                        count += 1

                    # Set up 'Item 7/8 Search Pattern' regex patterns
                    matches_item7 = re.compile(r'(item\s7\.*\s*management.s\s*[a-z]*)')
                    matches_item8 = re.compile(r'(item\s7a\.*\s*quantitative\s*[a-z]*)')

                    # Lists to store the locations of Item 7/8 Search Pattern matches
                    Start_Loc = []
                    End_Loc = []

                    # Find and store the locations of Item 7/8 Search Pattern matches
                    count = 0  # Set up counter

                    while count < (Rows - 1):  # Can only iterate to the second last row

                        # Match Item 7 Search Pattern
                        if re.match(matches_item7, matches_array.at[count, 'Selection']):
                            # Column 1 = 'Start' columnn in 'matches_array'
                            Start_Loc.append(matches_array.iloc[count, 1])  # Store in list => Item 7 will be the starting location (column '1' = 'Start' column)

                        # Match Item 8 Search Pattern
                        if re.match(matches_item8, matches_array.at[count, 'Selection']):
                            End_Loc.append(matches_array.iloc[count, 1])

                        count += 1
                    if len(Start_Loc) == 1:
                        Start_Loc.insert(1, Start_Loc[0])
                    if len(End_Loc) == 1:
                        End_Loc.insert(1, End_Loc[0])

                    i_1 = 0
                    while Start_Loc[1]>End_Loc[1]:
                        End_Loc[1]=End_Loc[1+i_1]
                        i_1 = i_1+1

                    # Extract section of text and store in 'TenKItem7'
                    TenKItem7 = TenKtext[Start_Loc[1]:End_Loc[1]]

                    # Clean newly extracted text
                    TenKItem7 = TenKItem7.strip()  # Remove starting/ending white spaces
                    TenKItem7 = TenKItem7.replace('\n', ' ')  # Replace \n (new line) with space
                    TenKItem7 = TenKItem7.replace('\r',
                                                  '')  # Replace \r (carriage returns-if you're on windows) with space
                    TenKItem7 = TenKItem7.replace(' ',
                                                  ' ')  # Replace " " (a special character for space in HTML) with space
                    TenKItem7 = TenKItem7.replace(' ',
                                                  ' ')  # Replace " " (a special character for space in HTML) with space
                    while '  ' in TenKItem7:
                        TenKItem7 = TenKItem7.replace('  ', ' ')  # Remove extra spaces

                    # Print first 500 characters of newly extracted text
                    return (TenKItem7)
        except:
            return ("False")


import os
from os import path
Url_list = []


scaner_file("/Volumes/12321/Data10K1")
df1 = pd.DataFrame(Url_list)
df1.columns = ['url']

df1 = df1.head(10)

df1['item1']=df1['url'].apply(get_item1)#can use pandarallel with pandas
df1['item1a']=df1['url'].apply(get_item1a)
df1['item1b']=df1['url'].apply(get_item1b)
df1['item2']=df1['url'].apply(get_item2)
df1['item3']=df1['url'].apply(get_item3)

df1.to_csv("/Volumes/12321/Data10K1")