# CRM Day - UI Prototype Collection

## Project Overview
**CRM Day** is a comprehensive collection of high-fidelity UI prototypes for a Customer Relationship Management (CRM) system. The project showcases various screens including member dashboards, reward marketplaces, mission details, and E-store interfaces, primarily designed for mobile-first or responsive experiences.

The project serves as a visual and functional gallery to demonstrate the user interface and user experience (UI/UX) flow for a loyalty-based CRM platform.

## Key Technologies
- **Styling:** [Tailwind CSS](https://tailwindcss.com/) (loaded via CDN).
- **Typography:** Google Fonts ([Prompt](https://fonts.google.com/specimen/Prompt) for headings, [Sarabun](https://fonts.google.com/specimen/Sarabun) for body text).
- **Icons:** [Material Symbols Outlined](https://fonts.google.com/icons).
- **Layout:** Responsive design with mobile, tablet, and desktop preview modes.

## Directory Structure
- `index.html`: The main entry point and gallery viewer. It features a sidebar for navigation and an iframe-based previewer with device mode toggles.
- `html/`: Contains subdirectories for each screen or feature.
  - Each subdirectory (e.g., `html/member_dashboard_home/`) typically contains:
    - `code.html`: The source code for the specific UI screen.
    - `screen.png`: A static preview image of the screen.

## Available Screens
The collection includes, but is not limited to:
- **Onboarding:** Login and initial setup screens.
- **Dashboard:** Member home view with point tracking and virtual cards.
- **Rewards:** Marketplace, detail views, and checkout flows.
- **Missions:** Play-to-earn mission lists and details.
- **E-Store:** Click-and-collect shopping interface.
- **Account:** History, wallet, and notification center.
- **Support:** News, promotions, and help center.

## Usage
To view the prototype:
1. Open `index.html` in any modern web browser.
2. Use the sidebar to navigate between different UI screens.
3. Use the top bar controls to toggle between **Mobile**, **Tablet**, and **Desktop** viewports.

## Development Conventions
- **Tailwind CSS:** Most screens use Tailwind utility classes for rapid prototyping.
- **Thai Language Support:** All screens are localized for the Thai language.
- **Custom Fonts:** Fonts are injected into the preview iframe via `index.html` to ensure consistent typography across all prototypes.

## TODO / Future Improvements
- [ ] Transition to a local Tailwind build if the project grows.
- [ ] Add interactive links between the `code.html` files to simulate a real application flow.
- [ ] Implement a search or filter feature in the sidebar for easier navigation.
