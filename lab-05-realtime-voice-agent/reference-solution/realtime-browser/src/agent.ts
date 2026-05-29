import { RealtimeAgent, RealtimeSession } from "@openai/agents/realtime";

import {
  REALTIME_AGENT_NAME,
  REALTIME_MODEL,
  isFunctionCallSafeName
} from "./session-config";

export function buildRealtimeAgent(): RealtimeAgent {
  if (!isFunctionCallSafeName(REALTIME_AGENT_NAME)) {
    throw new Error("Realtime agent name must be function-call safe.");
  }

  return new RealtimeAgent({
    name: REALTIME_AGENT_NAME,
    instructions:
      "You are a concise realtime voice assistant for an OpenAI Agents SDK course lab. " +
      "Explain the difference between RealtimeAgent/RealtimeSession and Python VoicePipeline. " +
      "Keep spoken answers short. Respond only to the user's spoken or typed content. " +
      "Never claim to read minds. If the current audio turn is empty, unclear, or contains no " +
      "new request, ask the user to repeat instead of answering a previous question again."
  });
}

export function buildRealtimeSession(agent = buildRealtimeAgent()): RealtimeSession {
  return new RealtimeSession(agent, {
    model: REALTIME_MODEL,
    workflowName: "lab-05-realtime-browser-agent",
    traceMetadata: {
      course: "mastering-openai-agents",
      lab: "05",
      surface: "realtime_browser"
    },
    config: {
      outputModalities: ["audio"],
      audio: {
        input: {
          transcription: {
            model: "gpt-4o-mini-transcribe"
          },
          turnDetection: {
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
}

export async function connectRealtimeSession(
  session: RealtimeSession,
  clientSecret: string
): Promise<void> {
  await session.connect({
    apiKey: clientSecret
  });
}
