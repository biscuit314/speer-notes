Feature: Users can be added to the system and can exchange credentials for a token

  Scenario: New user signs up
    Given that alice wants to sign up
    When an administrator enrolls the new user
    Then the user can start using the system

  Scenario: User gets a token
    Given a user named alice is signed up
    When alice requests a token
    Then a token is issued


  Scenario: User does not get a token if credentials are incorrect
    Given a user named alice is signed up
    When alice requests a token with the wrong password
    Then a token is not issued

  Scenario: Only admins can sign up a user
    Given a user named alice is signed up
    When alice enrolls a new user
    Then the attempt fails

  Scenario: Only admins can manage user accounts
    Given a user named alice is signed up
    When alice tries to access user accounts
    Then the attempt fails


  Scenario: Plain-text passwords are not saved in the database

  Scenario: Two users with the same password have different values saved in the database

  Scenario: Copying one user's password hash to a different user does not grant that user the same password
