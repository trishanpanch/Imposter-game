# Imposter

**Imposter** is a modern, mobile-first party game inspired by "Spyfall." It's designed to be played in person with a group of friends using a single device (pass-and-play).

Players are assigned roles: most are "Innocents" who know a secret word, while one (or more) is the "Imposter" who must blend in without knowing the secret. The goal is for the Innocents to find the Imposter, and for the Imposter to figure out the secret word.

## Features

*   **Pass-and-Play:** Designed for a single phone passed around the group.
*   **AI-Powered Content:** Uses Google's **Gemini AI** to dynamically generate infinite categories and secret words, ensuring no two games are alike.
*   **Mobile-First UI:** A sleek, "glassmorphism" aesthetic built with Tailwind CSS, optimized for mobile screens and dark mode.
*   **Secure Role Reveal:** "Hold-to-reveal" style mechanics ensure role secrecy.
*   **User Persistence:** Remembers your player list for quick game setup on return visits.

## Technology Stack

This project is built using a lightweight, serverless architecture:

*   **Frontend:**
    *   Standard **HTML5**.
    *   **Tailwind CSS** (via CDN) for rapid, responsive styling.
    *   **Vanilla JavaScript** for game logic and DOM manipulation.
*   **Backend:**
    *   **Python** (Flask) running on **Google Cloud Functions** (accessed via Cloud Run).
    *   Functions Framework for serverless routing.
*   **AI Integration:**
    *   **Google Gemini API** (Gemini 1.5 Flash) for generating game topics and words.
*   **Deployment:**
    *   Deployed to **Google Cloud Run** as a containerized service.

## How to Play

1.  **Login:** Enter your name to access your saved player groups.
2.  **Setup:** Add players (3+), select the number of imposters, and optionally choose a category theme (or let the AI pick randomly).
3.  **Distribution:** Pass the device to each player. They tap their name to secretly reveal their role (Innocent with the secret word OR Imposter).
4.  **Game Loop:** Players ask each other subtle questions about the word.
5.  **Voting:** Once time is up or suspicion peaks, players vote on who they think the Imposter is. A reveal screen confirms the roles.

## Local Development

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run locally using `functions-framework`:
    ```bash
    functions-framework --target=imposter_game --debug
    ```
