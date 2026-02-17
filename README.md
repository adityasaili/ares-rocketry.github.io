# ARES Rocketry Website

Welcome to the ARES Rocketry website repository! This is the source code for the team's public website, live at [www.aresrocketry.com](https://www.aresrocketry.com).

The site is built as a modern, static website using HTML5, CSS3, and Vanilla JavaScript. It is designed to be lightweight, responsive, and easy to maintain without complex build tools or frameworks.

### Running Locally
To test changes before pushing, run a local web server in the root directory:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000` in your browser.

> **Note**: Because the site uses directory-based routing (e.g., `/about/`), opening files directly (double-clicking `index.html`) may break links. Always use a local server for testing.

---

## Project Structure

Each page is located in its own directory as an `index.html` file. This allows users to visit `aresrocketry.com/about/` instead of `aresrocketry.com/about.html`.

```
ares-rocketry.github.io/
├── index.html              # Homepage
├── styles.css              # Main stylesheet (global styles, variables)
├── script.js               # Global logic (navigation, scroll effects)
├── optimize_gallery_images.py # Script to Auto-generate thumbnails
├── assets/                 # Images, icons, and logos
│   ├── thumbnails/         # Auto-generated optimized images
│   └── ...
├── about/                  # About Us page
│   └── index.html
├── team/                   # Team & Sub-teams page
│   └── index.html
├── projects/               # Projects Portfolio
│   └── index.html
├── gallery/                # Photo Gallery
│   └── index.html
├── join/                   # Join Us / Recruitment page
│   └── index.html
├── apply/                  # "How to Apply" Guide
│   └── index.html
├── news/                   # News & Updates
│   └── index.html
└── sponsors/               # Sponsors page
    └── index.html
```

---

## Design & Styling

All styles are located in `styles.css`. We use CSS variables for consistent branding.

### Key Colors
- **Primary (Deep Navy)**: `var(--color-primary)` (`#000f46`)
- **Secondary (Cyan/Blue)**: `var(--color-secondary)` (`#46c8f0`)
- **Background (White)**: `var(--color-white)` (`#ffffff`)
- **Light BG (for sections)**: `var(--color-bg-light)` (`#f5f7fa`)

### Typography
- **Headings**: `Fraunces` (Serif)
- **Body**: `Source Sans Pro` (Sans-serif)

---

## Common Tasks

### 1. Editing Content
Navigate to the directory of the page you want to edit (e.g., `about/`) and modify `index.html`. 
- **Links**: Use relative paths. From a sub-page, link to home as `../index.html` or assets as `../assets/image.png`.
- **Header/Footer**: these are manually repeated in each `index.html` file. If you change a menu item, you must update it in **every** `index.html` file... sorry xx

### 2. Adding a New Page
1.  Create a new folder (e.g., `new-page/`).
2.  Create an `index.html` inside it.
3.  Copy the `<head>`, `<header>`, and `<footer>` from an existing page (like `about/index.html`) to ensure consistent styling and navigation.
4.  Update the **Navigation Menu** in `index.html` and **all other pages** to link to your new page.

---

## Deployment

The site is hosted on **GitHub Pages**.

1.  **Commit your changes**:
    ```bash
    git add .
    git commit -m "Description of changes"
    ```
2.  **Push to main**:
    ```bash
    git push origin main
    ```
3.  GitHub Actions will automatically deploy the updates to the live site. Changes typically appear within 1-2 minutes.