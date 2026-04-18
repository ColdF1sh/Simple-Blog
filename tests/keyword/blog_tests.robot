*** Settings ***
Library    SeleniumLibrary
Test Teardown    Close All Browsers

*** Variables ***
${URL}             http://127.0.0.1:8000/
${BROWSER}         chrome
${USERNAME}        newuser
${PASSWORD}        simplepassword67
${POST_TITLE}      Created in test
${POST_CONTENT}    post test
${COMMENT_TEXT}    Nice comment from robot

*** Keywords ***
Start Clean Browser
    Close All Browsers
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Wait Until Page Contains    Simple Blog    10s

Login As Existing User
    Start Clean Browser
    Click Link    Login
    Wait Until Element Is Visible    id=id_username    10s
    Input Text    id=id_username    ${USERNAME}
    Input Password    id=id_password    ${PASSWORD}
    Click Button    css:.btn-primary
    Wait Until Page Contains    Logout    10s
    Page Should Contain    Hello, ${USERNAME}

*** Test Cases ***
Login User
    Login As Existing User
    Page Should Contain    Logout

Create Post
    Login As Existing User
    Click Link    New Post
    Wait Until Element Is Visible    id=id_title    10s
    Input Text    id=id_title    ${POST_TITLE}
    Input Text    id=id_content    ${POST_CONTENT}
    Click Button    css:.btn-primary
    Wait Until Page Contains    ${POST_TITLE}    10s
    Page Should Contain    ${POST_CONTENT}

Add Comment
    Login As Existing User
    Go To    ${URL}
    Wait Until Page Contains    ${POST_TITLE}    10s
    Click Link    ${POST_TITLE}
    Wait Until Element Is Visible    name=content    10s
    Input Text    name=content    ${COMMENT_TEXT}
    Click Button    css:.btn-primary
    Wait Until Page Contains    ${COMMENT_TEXT}    10s
    Page Should Contain    ${COMMENT_TEXT}