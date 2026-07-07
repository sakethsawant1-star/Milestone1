# 🎧 Spotify Vibe
> **An AI-Native Music Discovery MVP**

![Node.js](https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)
![Express.js](https://img.shields.io/badge/Express.js-000000?style=for-the-badge&logo=express&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-f55036?style=for-the-badge)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)

---

## 🌟 What is Spotify Vibe?

**Spotify Vibe** is a next-generation music discovery platform that allows users to type a natural language description of their current mood, activity, or moment. 

Instead of choosing from pre-defined genres or scrolling through generic "workout" playlists, the AI interprets your exact intent and returns a highly customized, curated Spotify playlist.

**Example Input:** *"focused but restless, like coding at midnight when the deadline is tomorrow"*
**Expected Output:** A perfectly curated 10-track Spotify playlist that captures that semantic context.

---

## 🚀 Key Features

* **Natural Language Intent Extraction:** Uses Groq (Llama-3.3-70b-versatile) to extract structured JSON (mood, energy, valence, genres, tempo) from your casual description.
* **Smart Audio Feature Filtering:** Dynamically maps intent to the Spotify Web API using precise audio characteristics like energy, valence, and tempo.
* **Instant Playlist Generation (Mock):** Click a button to save your exact vibe directly to your Spotify library. *(Note: Currently showing a mock of adding recommendations to playlists and favorites due to Spotify API limitations).*
* **Stateless & Secure:** No database required. Fully relies on zero-storage stateless execution with Spotify OAuth.

---

## 🏗️ System Architecture

Our solution bridges the gap between AI and the Spotify ecosystem through a seamless 3-layer architecture:

```mermaid
flowchart TD
    %% Styling
    classDef default fill:#1db954,stroke:#191414,stroke-width:2px,color:#fff,font-family:sans-serif,font-weight:bold;
    classDef layer fill:#191414,stroke:#1db954,stroke-width:2px,color:#1db954,font-family:sans-serif;
    classDef highlight fill:#f55036,stroke:#fff,stroke-width:2px,color:#fff;
    classDef spotify fill:#1db954,stroke:#fff,stroke-width:2px,color:#191414,font-weight:bold;

    subgraph Frontend ["🖥️ Frontend (Vercel)"]
        UI[User types Vibe Prompt]
    end

    subgraph Backend ["⚙️ Backend (Railway - Node.js)"]
        API[API Router /api/vibe]
        
        API -->|1. Sends Prompt| LLM[Groq AI: Llama 3]:::highlight
        LLM -->|2. Returns JSON Intent| API
        
        API -->|3. Fetches Recommendations| S_API[Spotify Web API]:::spotify
        S_API -->|4. Returns 10 Tracks| API
    end

    subgraph Output ["🎶 Result"]
        Display[Renders Song Cards & 30s Previews]
        Save[Mocks Saving to Spotify Playlist]
    end

    UI --> API
    API --> Display
    Display --> Save

    class Frontend,Backend,Output layer;
```

---

## 🛠️ Technology Stack

| Layer | Technologies Used |
| :--- | :--- |
| **Frontend UI** | HTML5, CSS3, Vanilla JavaScript, Vercel |
| **Backend API** | Node.js, Express, Railway |
| **AI Intelligence** | Groq API (llama-3.3-70b-versatile) |
| **Music Ecosystem** | Spotify Web API, Spotify OAuth 2.0 |

---

## 🔒 Security & Performance

* **Zero User Data Stored:** The architecture is fully stateless. We don't save your prompts, music tastes, or account details.
* **Environment Isolation:** API keys and Secrets are kept securely in Railway environment variables.
* **Graceful Fallbacks:** If the AI interprets an intent vaguely, it will fall back to safe, neutral musical parameters to guarantee a smooth user experience.
