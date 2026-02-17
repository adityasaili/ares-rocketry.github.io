import os


def update_logo_links():
    files_to_update = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".gemini" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                files_to_update.append(os.path.join(root, file))

    print(f"Scanning {len(files_to_update)} HTML files...")

    count = 0
    for file_path in files_to_update:
        with open(file_path, "r") as f:
            content = f.read()

        # Replacement strategy
        # Case 1: Root file (href="index.html")
        new_content = content.replace(
            'href="index.html" class="logo"', 'href="/" class="logo"'
        )
        # Case 2: Subdirectory file (href="../index.html")
        new_content = new_content.replace(
            'href="../index.html" class="logo"', 'href="/" class="logo"'
        )

        if new_content != content:
            with open(file_path, "w") as f:
                f.write(new_content)
            print(f"Updated {file_path}")
            count += 1

    print(f"Updated {count} files.")


if __name__ == "__main__":
    update_logo_links()
