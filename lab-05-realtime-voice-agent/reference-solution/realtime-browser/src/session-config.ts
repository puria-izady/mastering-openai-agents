export const REALTIME_MODEL = "gpt-realtime-2";
export const REALTIME_AGENT_NAME = "realtime_course_assistant";
export const REALTIME_VOICE = "marin";

export type TokenResponse = {
  value?: string;
  client_secret?: {
    value?: string;
  };
};

export function extractClientSecret(data: TokenResponse): string {
  const value = data.value ?? data.client_secret?.value;
  if (!value) {
    throw new Error("Token response did not include a client secret value.");
  }
  return value;
}

export function buildRealtimeSessionConfig() {
  return {
    session: {
      type: "realtime",
      model: REALTIME_MODEL,
      output_modalities: ["audio"],
      audio: {
        input: {
          transcription: {
            model: "gpt-4o-mini-transcribe"
          },
          turn_detection: {
            type: "semantic_vad",
            eagerness: "low"
          }
        },
        output: {
          voice: REALTIME_VOICE
        }
      },
      reasoning: {
        effort: "low"
      }
    }
  };
}

export function isFunctionCallSafeName(name: string): boolean {
  return /^[a-z0-9_]+$/.test(name);
}
