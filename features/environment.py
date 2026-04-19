import os
import socket
import tempfile
import time
import urllib.request
import shutil
from pathlib import Path
from threading import Thread
from wsgiref.simple_server import make_server

import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application
from django.db import connections
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


RUNTIME_DIR = Path(__file__).resolve().parent / "reports"


def _get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _wait_for_server(base_url, timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base_url, timeout=2) as response:
                if response.status < 500:
                    return
        except Exception:
            time.sleep(1)
    raise RuntimeError(f"Django server did not start at {base_url}")


def _ensure_test_user():
    user_model = get_user_model()
    user, created = user_model.objects.get_or_create(username="newuser")
    user.set_password("simplepassword67")
    if created or not user.is_active:
        user.is_active = True
    user.save()


def _get_chromedriver_path():
    try:
        return ChromeDriverManager().install()
    except Exception:
        cache_root = Path.home() / ".wdm"
        cached_drivers = sorted(cache_root.rglob("chromedriver.exe"), key=lambda path: path.stat().st_mtime, reverse=True)
        if cached_drivers:
            return str(cached_drivers[0])
        raise


def before_all(context):
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
    context.db_path = Path(tempfile.gettempdir()) / "blog_behave.sqlite3"
    settings.DATABASES["default"]["NAME"] = str(context.db_path)
    settings.ALLOWED_HOSTS = ["127.0.0.1", "localhost", "testserver"]
    django.setup()

    call_command("migrate", interactive=False, verbosity=0)
    _ensure_test_user()

    port = _get_free_port()
    context.base_url = f"http://127.0.0.1:{port}/"
    context.server = make_server("127.0.0.1", port, get_wsgi_application())
    context.server_thread = Thread(target=context.server.serve_forever, daemon=True)
    context.server_thread.start()
    _wait_for_server(context.base_url)


def before_scenario(context, scenario):
    RUNTIME_DIR.mkdir(parents=True, exist_ok=True)
    context.chrome_profile_dir = Path(
        tempfile.mkdtemp(prefix="chrome-profile-", dir=RUNTIME_DIR)
    )
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-extensions")
    options.add_argument(f"--user-data-dir={context.chrome_profile_dir}")
    options.add_argument("--remote-debugging-port=0")
    options.add_argument("--start-maximized")

    service = Service(_get_chromedriver_path())
    context.driver = webdriver.Chrome(service=service, options=options)
    context.driver.maximize_window()


def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        context.driver.quit()
    if hasattr(context, "chrome_profile_dir"):
        shutil.rmtree(context.chrome_profile_dir, ignore_errors=True)


def after_all(context):
    if hasattr(context, "server"):
        context.server.shutdown()
        context.server.server_close()
    if hasattr(context, "server_thread"):
        context.server_thread.join(timeout=10)
    connections.close_all()
    if hasattr(context, "db_path"):
        for suffix in ("", "-shm", "-wal"):
            db_file = Path(f"{context.db_path}{suffix}")
            if db_file.exists():
                try:
                    db_file.unlink()
                except PermissionError:
                    pass
