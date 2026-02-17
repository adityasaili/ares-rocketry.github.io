import os
import shutil


def restructure():
    # Define moves: Source -> (DestDir, DestFile)
    # Note: 'about', 'team', 'projects' are ALREADY moved.
    # We need to move the rest.
    moves = {
        "sponsors.html": ("sponsors", "index.html"),
        "application-guide.html": ("apply", "index.html"),
        "join.html": ("join", "index.html"),
        "gallery.html": ("gallery", "index.html"),
        "news.html": ("news", "index.html"),
        # 'achievements.html': ('achievements', 'index.html')  <-- User didn't ask for this, but to be safe I'll leave it in root?
        # Actually, if I move everything else, achievements.html links might look odd if inconsistent.
        # But I'll stick to the requested list to avoid unexpected changes.
    }

    # Ensure directories exist and move files
    for src, (dest_dir, dest_file) in moves.items():
        if os.path.exists(src):
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
                print(f"Created directory: {dest_dir}")

            shutil.move(src, os.path.join(dest_dir, dest_file))
            print(f"Moved {src} to {dest_dir}/{dest_file}")
        elif os.path.exists(os.path.join(dest_dir, dest_file)):
            print(f"{dest_dir}/{dest_file} already exists, skipping move.")
        else:
            print(f"Warning: Source {src} not found!")

    # Now we need to update links in ALL HTML files across the tree.
    # We have files in root (index.html, achievements.html, team.html?)
    # And files in subdirs (about/, team/, projects/, sponsors/, apply/, join/, gallery/, news/).

    # We need a robust replacement strategy.
    # Mapping old hrefs to new hrefs.

    # "about.html" -> "about/"
    # "subteams.html" -> "team/"
    # "projects.html" -> "projects/"
    # "sponsors.html" -> "sponsors/"
    # "application-guide.html" -> "apply/"
    # "join.html" -> "join/"
    # "gallery.html" -> "gallery/"
    # "news.html" -> "news/"
    # "team.html" -> "team.html" or "team/"?
    #   If user wants "team" -> "team/", then "team.html" in root is likely deprecated or should forward?
    #   I'll assume links to "team.html" should now point to "team/" IF the user intended "team" page.
    #   "subteams.html" was the one moved to "team/index.html".
    #   So "subteams.html" links -> "team/".
    #   What about existing "team.html" links?
    #   In `index.html`, the link was `href="team/"` (from my previous edit).
    #   In `team.html` (the file), it links to `subteams.html` as "Team" (or "View Sub-teams").
    #   I will map `team.html` links to `team/` as well if they meant the main team page?
    #   Actually, `team.html` (the file) has "Leadership" content.
    #   If I don't move it, it stays `team.html`.
    #   If I move it to `leadership/index.html`? User didn't ask.
    #   I'll leave `team.html` alone but update its links.

    replacements = {
        'href="about.html"': ('href="about/"', 'href="../about/"'),
        'href="about/"': (
            'href="about/"',
            'href="../about/"',
        ),  # Handle already updated ones if needed? No, logic handles depth.
        'href="subteams.html"': ('href="team/"', 'href="../team/"'),
        'href="team/"': ('href="team/"', 'href="../team/"'),
        'href="projects.html"': ('href="projects/"', 'href="../projects/"'),
        'href="projects/"': ('href="projects/"', 'href="../projects/"'),
        'href="sponsors.html"': ('href="sponsors/"', 'href="../sponsors/"'),
        'href="sponsors/"': ('href="sponsors/"', 'href="../sponsors/"'),
        'href="application-guide.html"': ('href="apply/"', 'href="../apply/"'),
        'href="apply/"': ('href="apply/"', 'href="../apply/"'),
        'href="join.html"': ('href="join/"', 'href="../join/"'),
        'href="join/"': ('href="join/"', 'href="../join/"'),
        'href="gallery.html"': ('href="gallery/"', 'href="../gallery/"'),
        'href="gallery/"': ('href="gallery/"', 'href="../gallery/"'),
        'href="news.html"': ('href="news/"', 'href="../news/"'),
        'href="news/"': ('href="news/"', 'href="../news/"'),
        # Static files/root files
        'href="index.html"': ('href="index.html"', 'href="../index.html"'),
        'href="../index.html"': (
            'href="index.html"',
            'href="../index.html"',
        ),  # normalization
        'href="achievements.html"': (
            'href="achievements.html"',
            'href="../achievements.html"',
        ),
        'href="../achievements.html"': (
            'href="achievements.html"',
            'href="../achievements.html"',
        ),
        'href="team.html"': ('href="team.html"', 'href="../team.html"'),
        'href="../team.html"': ('href="team.html"', 'href="../team.html"'),
        # Assets
        'src="assets/': ('src="assets/', 'src="../assets/'),
        'src="../assets/': ('src="assets/', 'src="../assets/'),
        'href="assets/': ('href="assets/', 'href="../assets/'),
        'href="../assets/': ('href="assets/', 'href="../assets/'),
        'href="styles.css"': ('href="styles.css"', 'href="../styles.css"'),
        'href="../styles.css"': ('href="styles.css"', 'href="../styles.css"'),
        'src="script.js"': ('src="script.js"', 'src="../script.js"'),
        'src="../script.js"': ('src="script.js"', 'src="../script.js"'),
    }

    files_to_update = []
    for root, dirs, files in os.walk("."):
        if ".git" in root or ".gemini" in root:
            continue
        for file in files:
            if file.endswith(".html"):
                files_to_update.append(os.path.join(root, file))

    print(f"Found {len(files_to_update)} HTML files to update.")

    for file_path in files_to_update:
        with open(file_path, "r") as f:
            content = f.read()

        # Determine depth
        # ./index.html -> depth 0
        # ./about/index.html -> depth 1
        rel_path = os.path.relpath(file_path, ".")
        # If rel_path is "index.html", depth is 0.
        # If rel_path is "about/index.html", depth is 1.
        depth = rel_path.count(os.path.sep)

        new_content = content

        # Apply replacements
        for key, (root_repl, subdir_repl) in replacements.items():
            # key is the target string currently in file (e.g. 'href="about.html"')
            # BUT wait, the file might ALREADY have 'href="../about/"' if I ran script before?
            # Yes. So I need to be careful not to double replace 'href="../about/"' -> 'href="../../about/"'.
            # My logic:
            # If depth 0: replace key with root_repl.
            # If depth 1: replace key with subdir_repl.

            # AND I need to handle existing "correct" links too?
            # e.g. if file has 'href="../about/"' and it's depth 1, it stays 'href="../about/"'.
            # The mappings above for 'href="../about/"' -> (..., 'href="../about/"') handle this.

            # However, string replacement is dumb. 'href="about/"' matches 'href="about/"'.
            # I should iterate over KEYS which are POTENTIAL patterns in the file.

            # Issue: 'href="about.html"' vs 'href="about/"'.
            # If I replace 'href="about.html"' with 'href="../about/"', good.
            # If I then replace 'href="about/"' (which might be the NEW string) with 'href="../about/"'?
            # No, 'href="about/"' key maps to 'href="../about/"'.
            # So if I replace 'href="about.html"' -> 'href="../about/"',
            # and later try to replace 'href="about/"' -> 'href="../about/"',
            # it might match 'href="../about/"' as 'href="..[href="about/"]"'? No.
            # But 'href="about/"' is a substring of 'href="../about/"'.
            # So I must be careful with order or check boundaries.

            # Strategy: Two pass? Or just precise strings.
            # The keys must be unique enough.

            # To avoid doing double replacement:
            # 1. We should list all KEYS we want to find.
            # 2. Re-construct the file? No, too hard.

            # Simple approach:
            # Revert everything to "canonical root form" first?
            # e.g. change ALL 'href="../about/"', 'href="about.html"', etc. to 'href="ABOUT_PLACEHOLDER"'.
            # Then resolve placeholders based on depth.
            pass

        # Better strategy:
        # Use regex to find attributes and replace logic.
        pass

    # RE-IMPLEMENTING WITH REGEX FOR SAFETY
    import re

    def replacer(match, depth):
        # path is the URL inside quotes
        # e.g. "about.html", "../styles.css", "assets/logo.png"
        path = match.group(2)
        quote = match.group(1)  # " or '

        # Normalize path to ROOT relative first
        # logic:
        # if path starts with http: return match (ignore)
        # if path starts with #: return match
        # if path is "about.html" -> "about/"
        # if path is "../about/" -> "about/"
        # if path is "assets/..." -> "assets/..."
        # if path is "../assets/..." -> "assets/..."

        clean_path = path
        if clean_path.startswith(("http", "#", "mailto:")):
            return match.group(0)

        # Remove leading ../
        while clean_path.startswith("../"):
            clean_path = clean_path[3:]

        # Map filenames to directories
        # "about.html" -> "about/"
        # "subteams.html" -> "team/"
        # "projects.html" -> "projects/"
        # "sponsors.html" -> "sponsors/"
        # "application-guide.html" -> "apply/"
        # "join.html" -> "join/"
        # "gallery.html" -> "gallery/"
        # "news.html" -> "news/"

        # Handle directory-like paths if they exist
        # "about/" -> "about/"

        # Mappings (Clean Path -> Clean Target)
        path_map = {
            "about.html": "about/",
            "subteams.html": "team/",
            "projects.html": "projects/",
            "sponsors.html": "sponsors/",
            "application-guide.html": "apply/",
            "join.html": "join/",
            "gallery.html": "gallery/",
            "news.html": "news/",
            # 'achievements.html' -> 'achievements.html' (unchanged)
        }

        # Handle index.html in subdirs?
        # "about/index.html" -> "about/" usually

        if clean_path in path_map:
            target_root = path_map[clean_path]
        else:
            target_root = clean_path

        # Also need to handle "about/" -> "about/"
        # But if it's "about/index.html", we might want "about/"
        if target_root.endswith("index.html") and "/" in target_root:
            # e.g. about/index.html -> about/
            target_root = target_root.replace("index.html", "")

        # Now convert target_root to relative path based on DEPTH
        if depth == 0:
            final_path = target_root
        else:
            # If deeper, we prepend ../
            # But logic depends on target.
            # If target is "about/", in depth 1: "../about/"
            # If target is "index.html", in depth 1: "../index.html"
            # If target is "assets/...", in depth 1: "../assets/..."

            # Special case: "projects/index.html" maps to "projects/"

            final_path = "../" + target_root

        return f"{quote}{final_path}{quote}"

    for file_path in files_to_update:
        with open(file_path, "r") as f:
            content = f.read()

        rel_path = os.path.relpath(file_path, ".")
        depth = rel_path.count(os.path.sep)

        # Find href="..." and src="..."
        # Regex: (href|src)=["'](.*?)["']
        # We need to pass depth to callback.

        callback = lambda m: m.group(1) + "=" + replacer(m.group(3) and m or m, depth)
        # Regex complexity: handling group numbering.
        # simpler: re.sub(pattern, func, string)

        def sub_callback(m):
            attr = m.group(1)  # href or src
            quote = m.group(2)  # " or '
            val = m.group(3)

            # Reconstruct match group for replacer
            # My replacer expects full match with group 1=quote, group 2=path
            # Let's adjust replacer logic inline here.

            path = val
            if path.startswith(("http", "#", "mailto:", "javascript:")):
                return m.group(0)

            clean = path
            while clean.startswith("../"):
                clean = clean[3:]

            # Mappings for clean paths
            mapping = {
                "about.html": "about/",
                "subteams.html": "team/",
                "projects.html": "projects/",
                "sponsors.html": "sponsors/",
                "application-guide.html": "apply/",
                "join.html": "join/",
                "gallery.html": "gallery/",
                "news.html": "news/",
                "about/": "about/",
                "team/": "team/",
                "projects/": "projects/",
                "sponsors/": "sponsors/",
                "apply/": "apply/",
                "join/": "join/",
                "gallery/": "gallery/",
                "news/": "news/",
            }

            target = mapping.get(clean, clean)

            # Convert to relative
            if depth == 0:
                final = target
            else:
                final = "../" + target

            return f"{attr}={quote}{final}{quote}"

        new_content = re.sub(r'(href|src)=(["\'])(.*?)\2', sub_callback, content)

        if new_content != content:
            with open(file_path, "w") as f:
                f.write(new_content)
            print(f"Updated {file_path}")

    # Update script
    with open("optimize_gallery_images.py", "r") as f:
        sc = f.read()

    # Simple replace for list
    # regex to find GALLERY_HTML_PATHS = [...]
    sc = re.sub(
        r"GALLERY_HTML_PATHS = \[.*?\]",
        'GALLERY_HTML_PATHS = ["gallery/index.html", "projects/index.html", "about/index.html", "team/index.html", "sponsors/index.html", "apply/index.html", "join/index.html", "news/index.html"]',
        sc,
        flags=re.DOTALL,
    )

    with open("optimize_gallery_images.py", "w") as f:
        f.write(sc)
    print("Updated optimize script")


if __name__ == "__main__":
    restructure()
