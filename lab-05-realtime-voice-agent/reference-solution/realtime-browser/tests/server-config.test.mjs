import { describe, expect, it } from "vitest";

import { buildClientSecretRequest } from "../server/session-config.mjs";

describe("token server request", () => {
  it("keeps the OpenAI API key on the trusted server", () => {
    const request = buildClientSecretRequest("sk_test", "hashed-user-id");

    expect(request.url).toBe("https://api.openai.com/v1/realtime/client_secrets");
    expect(request.init.method).toBe("POST");
    expect(request.init.headers.Authorization).toBe("Bearer sk_test");
    expect(request.init.headers["OpenAI-Safety-Identifier"]).toBe("hashed-user-id");
    expect(JSON.parse(request.init.body)).toMatchObject({
      session: {
        type: "realtime",
        model: "gpt-realtime-2",
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
          }
        }
      }
    });
  });
});
