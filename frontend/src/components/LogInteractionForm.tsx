import type { ChangeEvent } from "react";
import { useDispatch, useSelector } from "react-redux";
import type { RootState, AppDispatch } from "../store";
import {
  setField,
  submitInteraction,
  resetForm,
} from "../store/interactionSlice";

const SENTIMENTS = ["Positive", "Neutral", "Negative"] as const;

export default function LogInteractionForm() {
  const dispatch = useDispatch<AppDispatch>();

  const { form, status, lastSavedId } = useSelector(
    (state: RootState) => state.interaction
  );

  const set =
    (field: string) =>
    (
      e: ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
    ) =>
      dispatch(
        setField({
          field: field as keyof typeof form,
          value: e.target.value,
        })
      );

  return (
    <div className="card">
      <div className="card-header">Interaction Details</div>

      <div className="card-body">
        <div className="row">
          <div className="col">
            <label>HCP Name</label>
            <input
              value={form.hcp_name}
              onChange={set("hcp_name")}
              placeholder="Search or select HCP..."
            />
          </div>

          <div className="col">
            <label>Interaction Type</label>

            <select
              value={form.interaction_type}
              onChange={set("interaction_type")}
            >
              <option>Meeting</option>
              <option>Call</option>
              <option>Email</option>
              <option>Conference</option>
            </select>
          </div>
        </div>

        <div className="row">
          <div className="col">
            <label>Date</label>

            <input
              type="date"
              value={form.date}
              onChange={set("date")}
            />
          </div>

          <div className="col">
            <label>Time</label>

            <input
              type="time"
              value={form.time}
              onChange={set("time")}
            />
          </div>
        </div>

        <label>Attendees</label>

        <input
          value={form.attendees}
          onChange={set("attendees")}
          placeholder="Enter names..."
        />

        <label>Topics Discussed</label>

        <textarea
  value={form.topics_discussed}
  onChange={(e) => {
    set("topics_discussed")(e);

    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
  }}
/>

        <label>Materials Shared</label>

        <input
          value={form.materials_shared}
          onChange={set("materials_shared")}
        />

        <label>Samples Distributed</label>

        <input
          value={form.samples_distributed}
          onChange={set("samples_distributed")}
        />

        <label>Observed/Inferred HCP Sentiment</label>

        <div className="sentiment-row">
          {SENTIMENTS.map((s) => (
            <label key={s} className="sentiment-option">
              <input
                type="radio"
                name="sentiment"
                value={s}
                checked={form.sentiment === s}
                onChange={set("sentiment")}
              />
              {s}
            </label>
          ))}
        </div>

        <label>Outcomes</label>

       <textarea
  value={form.topics_discussed}
  onChange={(e) => {
    set("topics_discussed")(e);

    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
  }}
/>

        <label>Follow-up Actions</label>

        <textarea
  value={form.topics_discussed}
  onChange={(e) => {
    set("topics_discussed")(e);

    e.target.style.height = "auto";
    e.target.style.height = `${e.target.scrollHeight}px`;
  }}
/>

        <div className="actions">
          <button
            className="btn-primary"
            onClick={() => dispatch(submitInteraction(form))}
          >
            {status === "saving"
              ? "Saving..."
              : "Log Interaction"}
          </button>

          <button
            className="btn-secondary"
            onClick={() => dispatch(resetForm())}
          >
            Clear
          </button>

          {status === "saved" && (
            <span className="saved">
              ✅ Saved (ID {lastSavedId})
            </span>
          )}
        </div>
      </div>
    </div>
  );
}