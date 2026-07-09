const BASE = "http://localhost:8000";

export interface InteractionForm {
  hcp_name: string;
  interaction_type: string;
  date: string;
  time: string;
  attendees: string;
  topics_discussed: string;
  materials_shared: string;
  samples_distributed: string;
  sentiment: string;
  outcomes: string;
  follow_up_actions: string;
}

export interface InteractionResponse {
  id: number;
  message?: string;
}

export interface ChatResponse {
    reply: string;
    interaction_id?: number;
    form?: Partial<InteractionForm>;
}

export interface HCP {
  id: number;
  name: string;
}

export const api = {
  getHcps: async (): Promise<HCP[]> => {
    const res = await fetch(`${BASE}/hcps`);
    return res.json();
  },

  createInteraction: async (
    data: InteractionForm
  ): Promise<InteractionResponse> => {
    const res = await fetch(`${BASE}/interactions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    return res.json();
  },

  chat: async (
    message: string,
    session_id: string = "ui-session"
  ): Promise<ChatResponse> => {
    const res = await fetch(`${BASE}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        session_id,
      }),
    });

    return res.json();
  },
};