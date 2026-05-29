import { describe, expect, it } from "vitest";

import { buildRealtimeAgent, buildRealtimeSession } from "../src/agent";
import { formatTransportEvent } from "../src/event-log";
import {
  REALTIME_AGENT_NAME,
  REALTIME_MODEL,
  buildRealtimeSessionConfig,
  extractClientSecret,
  isFunctionCallSafeName
} from "../src/session-config";

describe("realtime browser agent contracts", () => {
  it("uses function-call-safe names", () => {
    expect(isFunctionCallSafeName(REALTIME_AGENT_NAME)).toBe(true);
    expect(isFunctionCallSafeName("Billing specialist")).toBe(false);
  });

  it("builds realtime session config for client secret minting", () => {
    expect(buildRealtimeSessionConfig()).toEqual({
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
            voice: "marin"
          }
        },
        reasoning: {
          effort: "low"
        }
      }
    });
  });

  it("extracts both documented client secret shapes", () => {
    expect(extractClientSecret({ value: "ek_direct" })).toBe("ek_direct");
    expect(extractClientSecret({ client_secret: { value: "ek_nested" } })).toBe("ek_nested");
  });

  it("builds SDK realtime objects without connecting", () => {
    const agent = buildRealtimeAgent();
    const session = buildRealtimeSession(agent);

    expect(agent).toBeTruthy();
    expect(session).toBeTruthy();
  });

  it("formats realtime transcript events", () => {
    expect(
      formatTransportEvent({
        type: "conversation.item.input_audio_transcription.completed",
        transcript: "Can you hear me?"
      })
    ).toBe("You said: Can you hear me?");
    expect(
      formatTransportEvent({
        type: "response.output_audio_transcript.done",
        transcript: "Yes, I can hear you."
      })
    ).toBe("Assistant said: Yes, I can hear you.");
    expect(
      formatTransportEvent({
        type: "conversation.item.input_audio_transcription.completed",
        transcript: ""
      })
    ).toBeNull();
    expect(
      formatTransportEvent({
        type: "response.output_audio_transcript.delta",
        delta: "Yes"
      })
    ).toBeNull();
    expect(formatTransportEvent({ type: "history.updated" })).toBeNull();
  });
});
