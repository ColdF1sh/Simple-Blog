Feature: Blog user actions
  As a blog user
  I want to use the main blog features through the browser
  So that the core workflows are validated with BDD tests

  Background:
    Given the blog home page is open

  Scenario: User logs in successfully
    When the user opens the login page
    And the user logs in with username "newuser" and password "simplepassword67"
    Then the user should see that they are logged in

  Scenario: Logged-in user creates a post
    When the user opens the login page
    And the user logs in with username "newuser" and password "simplepassword67"
    And the user opens the create post page
    And the user creates a post with title "BDD Test Post" and content "BDD post content"
    Then the page should show the post title "BDD Test Post"
    And the page should show the text "BDD post content"

  Scenario: Logged-in user adds a comment to a post
    When the user opens the login page
    And the user logs in with username "newuser" and password "simplepassword67"
    And the user opens the create post page
    And the user creates a post with title "BDD Test Post" and content "BDD post content"
    And the user adds a comment "BDD comment"
    Then the page should show the comment "BDD comment"
