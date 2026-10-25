"use client";

import { useCallback, useRef, useState } from "react";
import {
  LiveKitRoom,
  VideoConference,
  RoomAudioRenderer,
} from "@livekit/components-react";

const TOKEN_SERVER =
  process.env.NEXT_PUBLIC_TOKEN_SERVER || "http://localhost:8000";
const DEFAULT_ROOM = "project-mayhem-room";

// Browser speech recognition (Chrome / Edge). Optional — type works too.
function getSpeechRecognition(): any | null {
  if (typeof window === "undefined") return null;
  const W = window as any;
  const Ctor = W.SpeechRecognition || W.webkitSpeechRecognition;
  if (!Ctor) return null;
  return new Ctor();
}

export default function HomePage() {
  const [token, setToken] = useState<string | null>(null);
  const [url, setUrl] = useState<string>("");
  const [identity, setIdentity] = useState(
    "user-" + Math.random().toString(36).slice(2, 7)
  );
  const [connecting, setConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [speakText] = useState(
    "Hello from Project Mayhem. The speech pipeline is online."
  );
  const [chatMessage, setChatMessage] = useState("hello");
  const [speaking, setSpeaking] = useState(false);
  const [listening, setListening] = useState(false);
  const [speakStatus, setSpeakStatus] = useState<string | null>(null);
  const recognitionRef = useRef<any>(null);

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

  const sendChat = useCallback(async (message: string) => {
    const text = message.trim();
    if (!text) return;

    setSpeaking(true);
    setSpeakStatus(null);
    try {
      const res = await fetch(`${TOKEN_SERVER}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, room: DEFAULT_ROOM }),
      });
      const data = await res.json();
      if (!data.ok) throw new Error(data.error || "Chat failed");
      setSpeakStatus(`Agent: ${data.reply || "replied"}`);
    } catch (e: any) {
      setSpeakStatus(e.message || "Chat failed");
    } finally {
      setSpeaking(false);
    }
  }, []);

  const triggerChat = useCallback(() => {
    void sendChat(chatMessage);
  }, [chatMessage, sendChat]);

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
      setSpeakStatus("Spoken — you should hear the agent.");
    } catch (e: any) {
      setSpeakStatus(e.message || "Speak failed");
    } finally {
      setSpeaking(false);
    }
  }, [speakText]);

  const startListening = useCallback(() => {
    if (speaking || listening) return;

    const recognition = getSpeechRecognition();
    if (!recognition) {
      setSpeakStatus("Voice input not supported in this browser. Type instead.");
      return;
    }

    recognition.lang = "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setListening(true);
      setSpeakStatus("Listening… speak now.");
    };

    recognition.onerror = (event: any) => {
      setListening(false);
      setSpeakStatus(`Mic error: ${event.error}`);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.onresult = (event: any) => {
      const heard = event.results[0]?.[0]?.transcript?.trim() || "";
      setListening(false);
      if (!heard) {
        setSpeakStatus("Did not catch speech. Try again.");
        return;
      }
      setChatMessage(heard);
      setSpeakStatus(`You said: ${heard}`);
      void sendChat(heard);
    };

    recognitionRef.current = recognition;
    recognition.start();
  }, [listening, speaking, sendChat]);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    setListening(false);
  }, []);

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
            <span className="badge">Phase 1 · Week 4 · Voice + Chat</span>
            <button
              className="btn-secondary leave"
              onClick={() => {
                stopListening();
                setToken(null);
                setConnecting(false);
              }}
            >
              Leave
            </button>
          </header>
          <div className="speak-bar">
            <input
              value={chatMessage}
              onChange={(e) => setChatMessage(e.target.value)}
              placeholder="Type a message, or use Mic…"
              onKeyDown={(e) => {
                if (e.key === "Enter" && !speaking && chatMessage.trim()) {
                  triggerChat();
                }
              }}
            />
            <button
              className="btn-primary"
              onClick={triggerChat}
              disabled={speaking || listening || !chatMessage.trim()}
            >
              {speaking ? "Replying…" : "Send"}
            </button>
            <button
              className={listening ? "btn-mic active" : "btn-mic"}
              onClick={listening ? stopListening : startListening}
              disabled={speaking}
              title="Speak with the microphone"
            >
              {listening ? "Stop" : "Mic"}
            </button>
            <button
              className="btn-secondary"
              onClick={triggerSpeak}
              disabled={speaking || listening}
              title="Speak a fixed test line"
            >
              TTS test
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
          .btn-mic {
            padding: 8px 14px;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: var(--bg);
            color: var(--fg);
            cursor: pointer;
            font-size: 14px;
          }
          .btn-mic.active {
            background: #c0392b;
            color: white;
            border-color: #c0392b;
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
        <p className="phase">Phase 1 — Week 4 · Voice + Chat</p>

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
          Join, then type a message or press Mic (Chrome/Edge). The agent
          replies with speech.
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
