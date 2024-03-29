import re
from pathlib import Path

INSTALL_DIR = Path(__file__).parent


def update_rc(target=Path.home() / ".bashrc"):
    if not target.exists():
        return 0
    contents = target.read_text()
    to_write = (INSTALL_DIR / "templates" / ".bashrc").read_text()

    contents, replacements = re.subn(
        r"\# \<START OF PYBASHRC CODE\>\n(.|\n)*\n\# \<END OF PYBASHRC CODE\>\n",
        to_write,
        contents,
    )
    if replacements == 0:
        contents += "\n" + to_write

    target.write_text(contents.replace("<INSTALL_DIR>", str(INSTALL_DIR.absolute())))
    print(f"Modified {target}")
    return 1


def post_setup():
    # Create pybashrc file if necessary
    pybashrc_file = Path.home() / ".pybashrc.py"
    if not pybashrc_file.exists():
        pybashrc_file.write_text(
            (INSTALL_DIR / "templates" / ".pybashrc.py").read_text()
        )
        print(f"Created pybashrc file at {pybashrc_file}.")

    # Create fresh symlink in install dir
    symlink = INSTALL_DIR / "pybashrc_link.py"
    if symlink.exists():
        symlink.unlink()
    symlink.symlink_to(pybashrc_file)
    print(f"Created pybashrc symlink at {symlink}")

    # Create aliases
    alias_file = INSTALL_DIR / ".pybashrc_aliases"
    alias_file.write_text((INSTALL_DIR / "templates" / ".pybashrc_aliases").read_text())
    print(f"Created pybashrc alias file at {alias_file}.")

    # Include the necessary things in ~/.bashrc and ~/.zshrc, if they exist
    updated = update_rc(target=Path.home() / ".bashrc")
    updated += update_rc(target=Path.home() / ".zshrc")
    if updated == 0:
        raise ValueError("Neither ~/.bashrc nor ~/.zshrc exists!")
    print("pybashrc post-install setup complete. Please restart your shell.")
