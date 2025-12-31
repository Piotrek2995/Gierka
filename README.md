# Fast Jumps - Game Mechanics

This document describes the technical aspects of the game, including level generation algorithms and object interactions.

## 1. Platform Generation

The game uses a procedural generation system for an infinite level.

*   **Initialization**: A starting list of platforms is created at the beginning.
*   **Procedural Addition**: When the number of platforms drops below 6 (e.g., when old ones fall off-screen), the game generates new ones.
*   **Algorithm**:
    1.  The rightmost platform is identified (excluding the ground platform to ensure vertical progression).
    2.  A new platform is created at a random distance (`delta_x`) and random height (`delta_y`) relative to the previous one.
    3.  This ensures platforms form a "path" leading right and (usually) up, simulating climbing.
*   **Crumbling Platforms**: Every newly generated platform gets a random lifetime (starting at 4-7 seconds). As time passes, the platform changes color from Green to Red, and upon expiration, it is removed form the game (`kill()`).

## 2. Trampolines (Blue)

*   **Generation**: There is a 10% chance a trampoline will appear on a newly created platform.
*   **Function**: Trampolines boost the player upwards with increased force (1.3x jump strength).
*   **Collision Logic**: Trampoline collisions are checked **before** platform collisions. This ensures the player bounces immediately instead of sticking to the platform underneath.
*   **Culling Tweaks**: Platforms with trampolines (and generally all platforms) now persist even if they fall slightly below the screen bottom (pixel buffer), fixing usage in edge cases.

## 3. Obstacles (Red)

*   **Generation**: There is a 15% chance an obstacle will appear on a newly created platform.
*   **Restrictions**: Obstacles now ONLY spawn on platforms wider than 60px, ensuring the player always has space to land.
*   **Function**: Touching an obstacle results in Game Over.
*   **Positioning**: Obstacles are always centered on the platform they spawn on.

## 4. Coins (Yellow)

*   **Generation**: There is a 10% chance a Coin will appear on a newly created platform.
*   **Function**: Collecting a coin adds **+100 Points** to the score.
*   **Feedback**: A floating text animation ("+100") appears at the collection point.

## 5. Powerups (Cyan/Light Blue)

*   **Generation**: There is a 10% chance a Powerup will appear on a newly created platform.
*   **Function**: **Time Freeze**. Collecting a powerup momentarily stops the decay timer for ALL platforms.
*   **Duration**: The freeze effect lasts for 5 seconds.
*   **UI**: A Cyan bar appears at the top of the screen indicating the remaining freeze time.

## 6. Progressive Difficulty

*   **Scaling**: The game becomes harder as the player scores more points.
*   **Decay Rate**: For every 1000 points obtained, the lifetime of newly generated platforms is reduced by 0.5 seconds.
*   **Limit**: The lifetime is clamped to a minimum ensuring the game remains theoretically playable but very fast-paced at high scores.

## 7. Camera Scrolling

The game doesn't use a traditional camera but moves the entire game world relative to the player:

*   **Right**: When the player crosses half the screen width, all objects (platforms, obstacles, trampolines) shift left.
*   **Up**: When the player is in the top quarter of the screen (height < HEIGHT / 4), the world shifts down, giving the illusion of climbing.
*   **Scoring**: The horizontal shift of the world is added to the player's score.

## 8. Physics and Collisions

*   **Gravity**: A constant gravity force pulls the player down.
*   **Jumping**: Jumping is only possible when standing on a platform, unless bouncing off a trampoline.
*   **Collisions**: Detected only when the player is falling (downward velocity > 0), allowing for one-way platforms (jumping through them from below).
