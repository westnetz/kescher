KESCHER_DB = "kescher.db"
KESCHER_LOG = "kescher.log"


def test_init_creates_db_and_log(initialized_path):
    assert initialized_path.joinpath(KESCHER_DB).is_file()
    assert initialized_path.joinpath(KESCHER_LOG).is_file()


def test_init_debug_writes_to_log(initialized_path):
    with open(initialized_path / KESCHER_LOG) as logfile:
        log_content = logfile.read()
        assert "kescher - DEBUG - Debug mode is on" in log_content
