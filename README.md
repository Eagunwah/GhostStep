# GhostStep
A 2D puzzle-platformer built in **Python** using **Pygame**, where your previous failed attempts become solid platforms to help you reach the goal.

## Overview
In **GhostStep**, every time you hit a spike, your movement from that run is recorded and replayed by a "ghost" on subsequent attempts. Once a ghost finishes replaying its path, it solidifies into a platform—allowing you to climb higher, bridge deadly spike pits, and reach otherwise inaccessible areas across 5 handcrafted levels.

## Key Features & Mechanics
* **Frame-by-Frame Ghost Recording & Playback:** Records player `(x, y)` coordinates at 60 FPS and replays up to 3 recent runs simultaneously with dynamic opacity scaling before turning them into solid, collidable platforms.
* **Custom Triangle Collision Detection:** Uses barycentric coordinate point-in-triangle math and line-segment intersection checks to match triangular spike hitboxes accurately rather than relying on oversized bounding boxes.
* **5 Progressive Levels:** Includes multi-tier platforming, spike hazards, and high-velocity bounce pads (`1.5x` jump multiplier) in later stages.
* **Complete UI & Audio System:** Features a main menu, level select screen, settings and credits views, interactive button press states, instant level reset (`R` key or HUD icon), and dynamic background music switching via `pygame.mixer`.

## Controls
* **Move Left / Right:** `A` / `D` or `Left` / `Right` Arrow Keys
* **Jump:** `W`, `Up` Arrow, or `Spacebar`
* **Restart Level:** `R` or click the top-left restart icon

## Tech Stack
* **Language:** Python 3
* **Library:** Pygame

## How to Run Locally
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/](https://github.com/)<your-username>/<your-repo-name>.git
   cd <your-repo-name>
