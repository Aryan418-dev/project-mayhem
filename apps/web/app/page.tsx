"use client";

import { useCallback, useState } from "react";
import {
  LiveKitRoom,
  VideoConference,
  RoomAudioRenderer,
} from "@livekit/components-react";

const TOKEN_SERVER =
  process.env.NEXT_PUBLIC_TOKEN_SERVER || "http://localhost:8000";
const DEFAULT_ROOM = "project-mayhem-room";

export default function HomePage() {
  const [token, setToken] = useState<string | null>(null);
  const [url, setUrl] = useState<string>("");
  const [identity, setIdentity] = useState(
    "user-" + Math.random().toString(36).slice(2, 7)
  );
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [speakText, setSpeakText] = useState(
    "Hello from Project Mayhem. The speech pipeline is online."
  );
  const [speaking, setSpeaking] = useState(false);
  const [speakStatus, setSpeakStatus] = useState<string | null>(null);

  const fetchToken = useCallback(async () => {
    setConnecting(true);
    setError(null);
    try {
      const res = await fetch(
        `${TOKEN_SERVER}/token?room=${DEFAULT_ROOM}&identity=${identity}&name=${identity}`
      );
      if (!res.ok) throw new Error(`Token server error: ${res.status}`);
      const data = await res.json();
      setToken(data.token);
      setUrl(data.url);
    } catch (e: any) {
      setError(e.message || "Failed to get token");
      setConnecting(false);
    }
  }, [identity]);

  const triggerSpeak = useCallback(async () => {
    setSpeaking(true);
    setSpeakStatus(null);
    try {
      const res = await fetch(`${TOKEN_SERVER}/speak`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: speakText, room: DEFAULT_ROOM }),
      });
      const data = await res.json();
      if (!data.ok) throw new Error(data.error || "Speak failed");
      setSpeakStatus("Spoken — you should hear the agent in the room.");
    } catch (e: any) {
      setSpeakStatus(e.message || "Speak failed");
    } finally {
      setSpeaking(false);
    }
  }, [speakText]);

  if (token && url) {
    return (
      <LiveKitRoom
        token={token}
        serverUrl={url}
        connect={true}
        video={true}
        audio={true}
        onDisconnected={() => {
          setToken(null);
          setConnecting(false);
        }}
        style={{ height: "100vh" }}
      >
        <div className="room-container">
          <header className="header">
            <h1>Project Mayhem</h1>
            <span className="badge">Phase 1 · Week 2 · Speech</span>
            <button
              className="btn-secondary leave"
              onClick={() => {
                setToken(null);
                setConnecting(false);
              }}
            >
              Leave
            </button>
          </header>
          <div className="speak-bar">
            <input
              value={speakText}
              onChange={(e) => setSpeakText(e.target.value)}
              placeholder="Text for the agent to speak…"
            />
            <button
              className="btn-primary"
              onClick={triggerSpeak}
              disabled={speaking || !speakText.trim()}
            >
              {speaking ? "Speaking…" : "Speak"}
            </button>
            {speakStatus && <span className="speak-status">{speakStatus}</span>}
          </div>
          <main className="main">
            <VideoConference />
          </main>
          <RoomAudioRenderer />
        </div>
        <style jsx>{`
          .room-container {
            height: 100vh;
            display: flex;
            flex-direction: column;
          }
          .header {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 20px;
            border-bottom: 1px solid var(--border);
          }
          .header h1 {
            font-size: 18px;
          }
          .badge {
            font-size: 12px;
            background: var(--accent);
            color: white;
            padding: 2px 8px;
            border-radius: 999px;
          }
          .leave {
            margin-left: auto;
          }
          .speak-bar {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            align-items: center;
            padding: 10px 16px;
            border-bottom: 1px solid var(--border);
            background: var(--card);
          }
          .speak-bar input {
            flex: 1;
            min-width: 180px;
            padding: 8px 12px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg);
            color: var(--fg);
            font-size: 14px;
          }
          .speak-status {
            font-size: 12px;
            color: var(--muted);
            width: 100%;
          }
          .main {
            flex: 1;
            overflow: hidden;
          }
        `}</style>
      </LiveKitRoom>
    );
  }

  return (
    <div className="landing">
      <div className="card">
        <h1>Project Mayhem</h1>
        <p className="subtitle">Real-time video interaction</p>
        <p className="phase">Phase 1 — Week 2 · Speech</p>

        <label>
          Identity
          <input
            value={identity}
            onChange={(e) => setIdentity(e.target.value)}
            placeholder="your-name"
          />
        </label>

        {error && <p className="error">{error}</p>}

        <button
          className="btn-primary"
          onClick={fetchToken}
          disabled={connecting}
        >
          {connecting ? "Connecting…" : "Join Room"}
        </button>

        <p className="hint">
          Join the room, then use the Speak bar to hear the agent via TTS.
        </p>
      </div>

      <style jsx>{`
        .landing {
          min-height: 100vh;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 24px;
        }
        .card {
          background: var(--card);
          border: 1px solid var(--border);
          border-radius: 16px;
          padding: 40px;
          max-width: 400px;
          width: 100%;
          text-align: center;
        }
        h1 {
          font-size: 28px;
          margin-bottom: 4px;
        }
        .subtitle {
          color: var(--muted);
          margin-bottom: 8px;
        }
        .phase {
          font-size: 13px;
          color: var(--accent);
          margin-bottom: 28px;
        }
        label {
          display: block;
          text-align: left;
          font-size: 13px;
          color: var(--muted);
          margin-bottom: 20px;
        }
        input {
          display: block;
          width: 100%;
          margin-top: 6px;
          padding: 10px 12px;
          border-radius: 8px;
          border: 1px solid var(--border);
          background: var(--bg);
          color: var(--fg);
          font-size: 14px;
        }
        .error {
          color: #ff6b6b;
          font-size: 13px;
          margin-bottom: 12px;
        }
        .btn-primary {
          width: 100%;
          margin-bottom: 16px;
        }
        .hint {
          font-size: 12px;
          color: var(--muted);
          line-height: 1.5;
        }
      `}</style>
    </div>
  );
}
