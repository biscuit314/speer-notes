Feature: Users can post and share notes

  Scenario: Authenticated users can add notes
    Given a user named alice is signed up
    When alice adds notes
      | title        | body         |
      | Alice note 1 | Alice body 1 |
    Then the notes are added


  Scenario: Non-authenticated users cannot see any note
    Given a user named alice is signed up
    And alice adds notes
      | title        | body         |
      | Alice note 1 | Alice body 1 |
    And someone named mallory who is not signed up
    When mallory requests all notes
    Then no notes are fetched


  Scenario: Non-authenticated users cannot add notes
    Given someone named mallory who is not signed up
    When mallory adds notes
      | title          | body           |
      | Mallory note 1 | Mallory body 1 |
      | Mallory note 2 | Mallory body 2 |
    Then the notes are not added


  Scenario: Authenticated users see only their own list of notes
    Given a user named alice is signed up
    And a user named bob is signed up
    And alice adds notes
      | title        | body         |
      | Alice note 1 | Alice body 1 |
      | Alice note 2 | Alice body 2 |
      | Alice note 3 | Alice body 3 |
    And bob adds notes
      | title      | body       |
      | Bob note 1 | Bob body 1 |
    When alice requests all notes
    Then the response contains only the notes alice added


  Scenario Outline: Fetching a single note is only successful when an authenticated user fetches her own note
    Given a user named alice is signed up
    And a user named bob is signed up
    And someone named mallory who is not signed up
    And alice adds notes
      | title        | body         |
      | Alice note 1 | Alice body 1 |
    And bob adds notes
      | title      | body       |
      | Bob note 1 | Bob body 1 |
    When <requester> requests a single note that <poster> added
    Then the request <requester> made results in a <status_code>

    Examples:
      | requester | poster | status_code |
      | alice     | alice  | 200         |
      | alice     | bob    | 404         |
      | mallory     | alice  | 401         |


  Scenario Outline: Updating a single note is only successful when an authenticated user updates her own note
    Given a user named alice is signed up
    And a user named bob is signed up
    And someone named mallory who is not signed up
    And alice adds notes
      | title        | body         |
      | Alice note 1 | Alice body 1 |
    And bob adds notes
      | title      | body       |
      | Bob note 1 | Bob body 1 |
    When <requester> updates a single note that <poster> added
    Then the request <requester> made results in a <status_code>

    Examples:
      | requester | poster | status_code |
      | alice     | alice  | 200             |
      | alice     | bob    | 409             |
      | mallory     | alice  | 401             |


  Scenario Outline: Deleting a single note is only successful when an authenticated user deletes her own note
    Given a user named alice is signed up
    And a user named bob is signed up
    And someone named mallory who is not signed up
    And alice adds notes
      | title        | body         |
      | Alice note 1 | Alice body 1 |
    And bob adds notes
      | title      | body       |
      | Bob note 1 | Bob body 1 |
    When <requester> deletes a single note that <poster> added
    Then the request <requester> made results in a <status_code>

    Examples:
      | requester | poster | status_code |
      | alice     | alice  | 404         |
      | alice     | bob    | 200         |
      | mallory     | alice  | 401         |


  Scenario Outline: Sharing a single note is only successful when an authenticated user shares her own note
    Given a user named alice is signed up
    And a user named bob is signed up
    And someone named mallory who is not signed up
    And alice adds notes
      | title        | body         |
      | Alice note 1 | Alice body 1 |
    And bob adds notes
      | title      | body       |
      | Bob note 1 | Bob body 1 |
    When <requester> shares a single note with <share_with> that <poster> added
    Then the request <requester> made results in a <status_code>

    Examples:
      | requester | poster | share_with | status_code |
      | alice     | alice  | bob        | 200         |
      | alice     | bob    | bob        | 404         |
      | mallory     | alice  | bob        | 401         |


  Scenario: Authenticated user can see notes posted by others shared with her
    Given a user named alice is signed up
      And a user named bob is signed up
      And someone named mallory who is not signed up
      And alice adds notes
        | title        | body         |
        | Alice note 1 | Alice body 1 |
      And bob adds notes
        | title      | body       |
        | Bob note 1 | Bob body 1 |
      When alice shares a single note with bob that alice added
      And bob requests all notes
      Then the result is all notes added by bob plus the one that was shared by alice



  Scenario: Authenticated user can search amongst their own notes based on keywords
    Given a user named alice is signed up
      And alice adds notes
        | title                          | body                                     |
        | Keyword                        | Body 1                                   |
        | Note 1                         | Body 2 contains keyword                  |
        | Note 1                         | Body 3                                   |
        | Note with keyword in the title | Note 4 also contains keyword in the body |
    When alice searches all notes for keyword
    Then the result is 3 notes are found

  Scenario: Authenticated user's search results do not include matching notes posted by others
    Given a user named alice is signed up
      And a user named bob is signed up
      And alice adds notes
        | title           | body                               |
        | keyword         | Alice body 1                       |
        | Alice note 1    | Alice body 2 contains keyword      |
        | Alice note 1    | Alice body 3                       |
        | Alice keyword 1 | Alice body 4 also contains keyword |
      And bob adds notes
        | title                          | body                                     |
        | Keyword                        | Body 1                                   |
        | Note 1                         | Body 2 contains keyword                  |
        | Note 1                         | Body 3                                   |
        | Note with keyword in the title | Note 4 also contains keyword in the body |
    When alice searches all notes for keyword
    Then the result is 3 notes are found

  Scenario: Non-authenticated user cannot search for notes
    Given a user named alice is signed up
      And someone named mallory who is not signed up
      And alice adds notes
        | title                          | body                                     |
        | Keyword                        | Body 1                                   |
        | Note 1                         | Body 2 contains keyword                  |
        | Note 1                         | Body 3                                   |
        | Note with keyword in the title | Note 4 also contains keyword in the body |
    When mallory searches all notes for keyword
    Then the result is 0 notes are found
