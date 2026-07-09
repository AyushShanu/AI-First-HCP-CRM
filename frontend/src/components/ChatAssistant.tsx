import { useEffect, useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";

import type { RootState, AppDispatch } from "../store";

import {
  addUserMessage,
  sendChat,
} from "../store/chatSlice";

export default function ChatAssistant() {
  const [input, setInput] = useState("");

  const dispatch = useDispatch<AppDispatch>();

  const { messages, loading } = useSelector(
    (state: RootState) => state.chat
  );

  const endRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const send = () => {
    if (!input.trim()) return;

    dispatch(addUserMessage(input));
    dispatch(sendChat(input));

    setInput("");
  };

  return (
    <div className="card chat-card">
      <div className="card-header">
        🤖 AI Assistant

        <div className="subtitle">
          Log interaction via chat
        </div>
      </div>

      <div className="chat-messages">
        {messages.map((m, i) => (
          <div key={i} className={`bubble ${m.role}`}>
            {m.text}
          </div>
        ))}

        {loading && (
          <div className="bubble assistant">
            Thinking...
          </div>
        )}

        <div ref={endRef} />
      </div>

      <div className="chat-input">
     <textarea
  value={input}
  rows={1}
  placeholder="Describe interaction..."
  onChange={(e) => {
    setInput(e.target.value);

    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
  }}
  onKeyDown={(e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }}
/>

        <button
          className="btn-primary"
          onClick={send}
          disabled={loading}
        >
          Log
        </button>
      </div>
    </div>
  );
}