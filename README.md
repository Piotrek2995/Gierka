# Fast Jumps - Game Mechanics

This document describes the technical aspects of the game, including level generation algorithms and object interactions.

## 1. Platform Generation

The game uses a procedural generation system for an infinite level.

*   **Initialization**: A starting list of platforms is created at the beginning.
*   **Procedural Addition**: When the number of platforms drops below 6 (e.g., when old ones fall off-screen), the game generates new ones.
*   **Algorithm**:
    1.  The rightmost platform is identified.
    2.  A new platform is created at a random distance (`delta_x`) and random height (`delta_y`) relative to the previous one.
    3.  This ensures platforms form a "path" leading right and (usually) up, simulating climbing.
*   **Crumbling Platforms**: Every newly generated platform gets a random lifetime (from 4 to 7 seconds). As time passes, the platform changes color from Green to Red, and upon expiration, it is removed from the game (`kill()`).

## 2. Trampolines (Blue)

*   **Generation**: There is a 10% chance a trampoline will appear on a newly created platform.
*   **Function**: Trampolines boost the player upwards with increased force (1.3x jump strength).
*   **Collision Logic**: Trampoline collisions are checked **before** platform collisions. This ensures the player bounces immediately instead of sticking to the platform underneath.

## 3. Obstacles (Red)

*   **Generation**: There is a 15% chance an obstacle will appear on a newly created platform.
*   **Function**: Touching an obstacle results in Game Over.
*   **Positioning**: Obstacles are always centered on the platform they spawn on.

## 4. Camera Scrolling

The game doesn't use a traditional camera but moves the entire game world relative to the player:

*   **Right**: When the player crosses half the screen width, all objects (platforms, obstacles, trampolines) shift left.
*   **Up**: When the player is in the top quarter of the screen (height < HEIGHT / 4), the world shifts down, giving the illusion of climbing.
*   **Scoring**: The horizontal shift of the world is added to the player's score.

## 5. Physics and Collisions

*   **Gravity**: A constant gravity force pulls the player down.
*   **Jumping**: Jumping is only possible when standing on a platform, unless bouncing off a trampoline.
*   **Collisions**: Detected only when the player is falling (downward velocity > 0), allowing for one-way platforms (jumping through them from below).
