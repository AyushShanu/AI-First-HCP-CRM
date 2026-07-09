import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type { PayloadAction } from "@reduxjs/toolkit";
import { api } from "../api";
import { fillFromAI } from "./interactionSlice";

export const sendChat = createAsyncThunk(
    "chat/send",
    async (
        message: string,
        { dispatch }
    ) => {

        const res = await api.chat(message);

        if (res.form) {
            dispatch(fillFromAI(res.form));
        }

        return res;
    }
);

interface Message {
  role: "assistant" | "user";
  text: string;
}

interface ChatState {
  messages: Message[];
  loading: boolean;
}

const initialState: ChatState = {
  messages: [
    {
      role: "assistant",
      text:
        'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.',
    },
  ],
  loading: false,
};

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    addUserMessage: (
      state,
      action: PayloadAction<string>
    ) => {
      state.messages.push({
        role: "user",
        text: action.payload,
      });
    },
  },

  extraReducers: (builder) => {
    builder
      .addCase(sendChat.pending, (state) => {
        state.loading = true;
      })
     .addCase(sendChat.fulfilled, (state, action) => {

    state.loading = false;

    state.messages.push({
        role: "assistant",
        text: action.payload.reply,
    });

})
      .addCase(sendChat.rejected, (state) => {
        state.loading = false;

        state.messages.push({
          role: "assistant",
          text: "⚠️ Error contacting AI agent.",
        });
      });
  },
});

export const { addUserMessage } = chatSlice.actions;

export default chatSlice.reducer;