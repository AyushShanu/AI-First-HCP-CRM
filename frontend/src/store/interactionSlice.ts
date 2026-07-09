import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import { api, type InteractionForm, type InteractionResponse } from "../api";

export const submitInteraction = createAsyncThunk<
  InteractionResponse,
  InteractionForm
>("interaction/submit", async (form) => {
  return api.createInteraction(form);
});

const initialForm: InteractionForm = {
  hcp_name: "",
  interaction_type: "Meeting",
  date: new Date().toISOString().slice(0, 10),
  time: new Date().toTimeString().slice(0, 5),
  attendees: "",
  topics_discussed: "",
  materials_shared: "",
  samples_distributed: "",
  sentiment: "Neutral",
  outcomes: "",
  follow_up_actions: "",
};

interface InteractionState {
  form: InteractionForm;
  status: "idle" | "saving" | "saved" | "error";
  lastSavedId: number | null;
}

const initialState: InteractionState = {
  form: initialForm,
  status: "idle",
  lastSavedId: null,
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    setField: (
      state,
      action: PayloadAction<{
        field: keyof InteractionForm;
        value: string;
      }>
    ) => {
      state.form[action.payload.field] = action.payload.value;
    },

fillFromAI: (state, action) => {

    Object.entries(action.payload).forEach(([key, value]) => {

        if (
            value !== undefined &&
            value !== null &&
            key in state.form
        ) {
            state.form[key as keyof typeof state.form] = value as never;
        }

    });

},

    resetForm: (state) => {
      state.form = {
        ...initialForm,
        date: new Date().toISOString().slice(0, 10),
        time: new Date().toTimeString().slice(0, 5),
      };
    },
  },

  extraReducers: (builder) => {
    builder
      .addCase(submitInteraction.pending, (state) => {
        state.status = "saving";
      })
      .addCase(submitInteraction.fulfilled, (state, action) => {
        state.status = "saved";
        state.lastSavedId = action.payload.id;
      })
      .addCase(submitInteraction.rejected, (state) => {
        state.status = "error";
      });
  },
});

export const {
  setField,
  fillFromAI,
  resetForm,
} = interactionSlice.actions;

export default interactionSlice.reducer;