When program starts open the data file
Ask user for a Username
    Check an Account List for Username
    If found:
        Ask user for a Password
        Check the Account List for Password with the Username
            If Password matches:
                Log in successfully
            Else:
                Give an error and ask them to try again
    Else:
        Ask user to enter a Username and Password
            Append Username and Password to the Account List with User class
When program is closed save all the newly inputted information to a data file

If both match a defined Username and Password Log in to the associated account

Extraneous Variables:
    Accounts
        Account #
        Username
        Password
        Permissions
    Permissions
        Administrator
            Can view all user information and delete accounts
        User
            Can log into the account


