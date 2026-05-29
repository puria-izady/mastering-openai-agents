export const REALTIME_MODEL = "gpt-realtime-2";
export const REALTIME_VOICE = "marin";

export function buildRealtimeSessionConfig() {
  return {
    session: {
      type: "realtime",
      model: REALTIME_MODEL,
      output_modalities: ["audio"],
      audio: {
        input: {
          transcription: {
            model: "gpt-4o-mini-transcribe",
          },
          turn_detection: {
            type: "semantic_vad",
            eagerness: "low",
          },
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

export function buildClientSecretRequest(apiKey, safetyIdentifier = "lab-05-realtime-browser") {
  return {
    url: "https://api.openai.com/v1/realtime/client_secrets",
    init: {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "OpenAI-Safety-Identifier": safetyIdentifier
      },
      body: JSON.stringify(buildRealtimeSessionConfig())
    }
  };
}
