from behave import given, then, when
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


WAIT_SECONDS = 10


def wait_for_element(context, by, value):
    return WebDriverWait(context.driver, WAIT_SECONDS).until(
        ec.visibility_of_element_located((by, value))
    )


def wait_for_text(context, text):
    return WebDriverWait(context.driver, WAIT_SECONDS).until(
        ec.visibility_of_element_located((By.XPATH, f"//*[contains(normalize-space(), \"{text}\")]"))
    )


def fill_input(context, by, value, text):
    element = wait_for_element(context, by, value)
    element.clear()
    element.send_keys(text)


@given("the blog home page is open")
def step_open_home_page(context):
    context.driver.get(context.base_url)
    wait_for_text(context, "All Posts")


@when("the user opens the login page")
def step_open_login_page(context):
    context.driver.get(f"{context.base_url}accounts/login/")
    wait_for_element(context, By.ID, "id_username")


@when('the user logs in with username "{username}" and password "{password}"')
def step_log_in(context, username, password):
    fill_input(context, By.ID, "id_username", username)
    fill_input(context, By.ID, "id_password", password)
    wait_for_element(context, By.ID, "login-submit-button").click()
    wait_for_text(context, "Logout")


@then("the user should see that they are logged in")
def step_verify_logged_in(context):
    wait_for_text(context, "Logout")


@when("the user opens the create post page")
def step_open_create_post_page(context):
    context.driver.get(f"{context.base_url}post/new/")
    wait_for_element(context, By.ID, "post-form")


@when('the user creates a post with title "{title}" and content "{content}"')
def step_create_post(context, title, content):
    fill_input(context, By.ID, "id_title", title)
    fill_input(context, By.ID, "id_content", content)
    submit_button = wait_for_element(context, By.ID, "post-submit-button")
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", submit_button
    )
    context.driver.execute_script("arguments[0].click();", submit_button)
    wait_for_element(context, By.ID, "post-title")


@when('the user adds a comment "{comment_text}"')
def step_add_comment(context, comment_text):
    fill_input(context, By.ID, "id_content", comment_text)
    submit_button = wait_for_element(context, By.ID, "comment-submit-button")
    context.driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", submit_button
    )
    context.driver.execute_script("arguments[0].click();", submit_button)
    wait_for_text(context, "Comment added successfully.")


@then('the page should show the post title "{title}"')
def step_verify_post_title(context, title):
    post_title = wait_for_element(context, By.ID, "post-title")
    assert post_title.text == title


@then('the page should show the text "{text}"')
def step_verify_text(context, text):
    wait_for_text(context, text)


@then('the page should show the comment "{comment_text}"')
def step_verify_comment(context, comment_text):
    try:
        wait_for_text(context, comment_text)
    except TimeoutException as exc:
        raise AssertionError(f'Comment "{comment_text}" was not found on the page.') from exc
