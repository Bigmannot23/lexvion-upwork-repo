import subprocess, sys, os
def test_cli_smoke():
    with open("tests/test_job_post.txt","r") as f:
        p = subprocess.run([sys.executable, "app.py", "tests/test_job_post.txt"], capture_output=True, text=True)
    assert p.returncode == 0
    assert os.path.exists("proposal.md")