import subprocess

subprocess.run([
    "sudo", "docker", "run",
    "--rm",
    "-it",
    "-v", "/home/iris/work:/data",
    "poppler"
])
