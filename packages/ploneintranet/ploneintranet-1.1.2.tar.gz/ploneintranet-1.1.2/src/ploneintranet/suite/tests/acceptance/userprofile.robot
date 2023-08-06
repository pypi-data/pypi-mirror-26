*** Settings ***

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot
Resource  ../lib/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote
Library  DebugLibrary

Variables  variables.py

Test Setup  Prepare test browser
Test Teardown  Close all browsers

*** Test Cases ***

Alice can view her own profile
    Given I am logged in as the user alice_lindstrom
    Then I can open the personal tools menu
    And I can follow the link to my profile
    And I can see details for Alice Lindström

# This is disabled at the moment, see:
# https://github.com/ploneintranet/ploneintranet/pull/530#issuecomment-121600509
# Alice can view her own personal settings
#     Given I am logged in as the user alice_lindstrom
#     Then I can open the personal tools menu
#     And I can follow the link to my personal settings
#     And I can see details for Alice Lindström

Alice can logout
    Given I am logged in as the user alice_lindstrom
    Then I can open the personal tools menu
    Then I can follow the link to logout

Alice cannot view her personal preferences
    Given I am logged in as the user alice_lindstrom
    When I open the personal preferences page
    Then The page is not found

Alice can view her documents
    Given I am logged in as the user alice_lindstrom
    Then I can view the profile for user alice_lindstrom
    Then Click Link  Documents
    Then Click Link  Human Resources

Alice can view her documents sorted by date
    Given I am logged in as the user alice_lindstrom
    Then I can view the profile for user alice_lindstrom
    Then I can see my documents grouped  by_date

Alice can search her documents
    Given I am logged in as the user alice_lindstrom
     Then I can search in my documents for  Human

Alice cannot open the password reset form
    Given I am logged in as the user alice_lindstrom
    When I open the password reset form
    Then The page is not found

Allan can view Alice's profile
    Given I am logged in as the user allan_neece
    Then I can view the profile for user alice_lindstrom
    And I can see details for Alice Lindström

Allan can follow Christian
    Given I am logged in as the user allan_neece
    Then I can view the profile for user christian_stoney
    And I can follow Christian Stoney
    Then I can open the personal tools menu
    And I can follow the link to my profile
    And I can see Christian Stoney in the list of users being followed

Dollie can unfollow Guy
    Given I am logged in as the user dollie_nocera
    Then I can view the profile for user guy_hackey
    And I can unfollow Guy Hackey
    Then I can open the personal tools menu
    And I can follow the link to my profile
    And I cannot see Guy Hackey in the list of users being followed

Dollie can change her details
    Given I am logged in as the user dollie_nocera
    And I can view the profile for user dollie_nocera
    Then I can change my name to Mickey

Dollie cannot change Guy's details
    Given I am logged in as the user dollie_nocera
    And I can view the profile for user guy_hackey
    Then I cannot edit personal details

Dollie can change her avatar from the menu
    Given I am logged in as the user dollie_nocera
    And I can open the personal tools menu
    Then I can upload a new avatar from the menu

# This doesn't work because the input form element isn't visible
# Dollie can change her avatar from her profile page
#     Given I am logged in as the user dollie_nocera
#     And I can view the profile for user dollie_nocera
#     Then I can upload a new avatar from my profile

*** Keywords ***

I can open the personal tools menu
    Click Element  css=header #user-avatar
    Wait Until Element Is Visible  css=.tooltip-container .menu

I open the personal preferences page
    Go To  ${PLONE_URL}/@@personal-preferences

I can follow the link to my profile
    Click Element  css=.tooltip-container .menu a.icon-user

I can see my documents grouped
    [arguments]  ${VALUE}
    # BBB: fix the Go To when this one is closed:
    # - https://github.com/quaive/ploneintranet.prototype/issues/262
    # we should use the select
    Go To  ${PLONE_URL}/profiles/alice_lindstrom?${VALUE}=1#person-documents
    Wait until element is visible  jquery=.group:last a:contains("Human Resources")

I can search in my documents for
    [arguments]  ${VALUE}
    I can open the personal tools menu
    I can follow the link to my profile
    Click Link  Documents
    Input Text  jquery=#person-documents [name=SearchableText]  ${VALUE}
    Wait Until Page Does Not Contain Element  css=.injecting-content
    Click Element  jquery=.preview img[alt~="${VALUE}"]

# This is disabled at the moment, see:
# https://github.com/ploneintranet/ploneintranet/pull/530#issuecomment-121600509
# I can follow the link to my personal settings
#     Click Element  css=.tooltip-container .menu a.icon-cog

I can follow the link to logout
    Click Element  css=.tooltip-container .menu a.icon-exit

I can view the profile for user ${USERID}
    Go To  ${PLONE_URL}/profiles/${USERID}

I can see details for ${NAME}
    Element should contain  css=#person-timeline .sidebar .user-info-header figcaption a  ${NAME}

I can follow ${NAME}
    Wait Until Page Contains Element  css=button[title="Click to follow ${NAME}"]
    Click Element  css=button[title="Click to follow ${NAME}"]
    Wait Until Page Contains Element  css=button[title="You are now following ${NAME}. Click to unfollow."]

I can unfollow ${NAME}
    Wait Until Page Contains Element  css=button[title="You are now following ${NAME}. Click to unfollow."]
    Click Element  css=button[title="You are now following ${NAME}. Click to unfollow."]
    Wait Until Page Contains Element  css=button[title="Click to follow ${NAME}"]

I can see ${NAME} in the list of users being followed
    Click Element  css=nav.tabs a.link-following
    Page should contain Element  jquery=#person-following a strong:contains("${NAME}")

I cannot see ${NAME} in the list of users being followed
    Click Element  css=nav.tabs a.link-following
    Page should not contain Element  jquery=#person-following a strong:contains("${NAME}")

I can change my name to ${NAME}
    Click Element  link=Info
    Wait Until Page Contains Element  css=#user-edit-form
    Input Text  name=form.widgets.first_name  Mickey
    Click button  name=form.buttons.save
    Page should contain Element  xpath=//figcaption//a[contains(text(), "Mickey")]

I cannot edit personal details
    Click Element  link=Info
    Page Should Contain Element  css=dt.icon-user

I can upload a new avatar from the menu
    Choose File  xpath=(//input[@name='portrait'])[2]  ${UPLOADS}/new-profile.jpg
    Wait until page contains   Personal image updated

# This doesn't work because the input form element isn't visible
# It is possible to click on the label to get the file dialog, but that doesn't work for
# the Choose File keyword
# I can upload a new avatar from my profile
#     Choose File  css=#change-personal-image label.icon-pencil  ${UPLOADS}/new-profile.jpg
#     Submit form  css=#change-personal-image
#     Wait until page contains   Personal image updated
