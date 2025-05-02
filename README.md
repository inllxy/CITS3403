# SF6 Spotlight Project Summary (Click 'Edit File' to read)

Main Page
Overview: The main page primarily displays competition results and includes a navigation bar for quick access.

Requirements: • Tournament categorization by year: o A dropdown menu appears upon clicking the competition button, listing years (e.g., 2023, 2024, 2025). o Clicking a year automatically scrolls the page to that year's competition results.

• Match Information Section: Each match includes: o Match name o Match image o Start date o Three functional buttons:  Result: Purpose currently undecided; currently displays the champion player's image.  Detail: Opens a pannable Offcanvas panel displaying the detailed SF6bracket.html.  Comp: Currently redirects to the official competition website; purpose is subject to further decisions.

Navbar: • Competition: As described above. • Player: Dedicated page listing all participants, displaying basic player information (detailed requirements described below). • News: Intended to directly embed the official X (formerly Twitter) feed; subject to future clarification. • Schedule (Optional): Lists upcoming matches. • Quiz (Optional): o Admin Qualification Quiz: Presents 50 random questions out of a 300-question database. Users scoring at least 90% within the time limit gain editing permissions (match results, player information, etc.). o Level-Up Quiz: Offers 20 random level-specific questions. Users achieving 80% accuracy earn a visible badge beside their comments.

Competition Result Display: • Results cards are currently manually duplicated from a template. • Future goal: Automate card generation via JavaScript templates, allowing customizable parameters (e.g., Card(Name, Date, Image)).

Bracket (Critical Requirement):
Requirements: • Bracket structure clearly shows each pairing: o Player names (clickable links directing to the player's profile, scrolling to relevant information or opening a modal directly). o Scores and nationalities.

• Framework to be auto-generated using JavaScript for ease of replication.

• Automatic highlighting of match winners: o Highlighting can include markers, font style, or background colors based on scores.

• Top three players highlighted distinctly with gold, silver, and bronze borders. o The players' information pages dynamically update to reflect achievements.

• Under each match block: o Comment button: Opens a modal displaying match video at the top and comments below, with an input field at the bottom to post comments. Comments themselves require no further interactive features (likes, replies). o Like button: Single-click action with an optional visible counter. Matches with the top three most likes labelled "Hot" or "Popular." o Match Video button: YouTube icon linking directly to match video or timestamped video segment if available.

• All bracket details (player names, scores, nationalities, comments, video links) must be fully editable, via either a dedicated submission table or inline editing fields.

• Provided bracket style requires readability improvements and adaptive resizing for better user experience.

User Login System (Initial Concept): • Users register and log in through the navbar (positioned on the right side).
• Logged-in users can comment, like, and interact normally. • Logged-in users have access to an "Edit Mode" option (similar to the position of the "+Create" button): o Enables editing player info, match scores, names, and other bracket-related elements. o While in Edit Mode, regular interactive features (likes, comments) can be temporarily disabled.

• Additional common login system functionalities to be incorporated progressively.
# SF6 Spotlight — Flask Backend Quick-Start Guide

> **Goal**  
> Spin the project up locally and open `http://127.0.0.1:5000/` with just a few commands.

---

## Steps

```bash
# 1. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS / Linux
# .\venv\Scripts\activate       # Windows PowerShell

# 2. Install dependencies
python -m pip install --upgrade pip
python -m pip install Flask Flask-SQLAlchemy Flask-Login email-validator

# 3. Initialize the database (run once)
python -m flask --app app.py init-db

# 4. Start the development server
python -m flask --app app.py run

