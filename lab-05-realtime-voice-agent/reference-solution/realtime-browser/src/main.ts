import {
  buildRealtimeAgent,
  buildRealtimeSession,
  connectRealtimeSession
} from "./agent";
import { formatTransportEvent } from "./event-log";
import { extractClientSecret } from "./session-config";
import "./styles.css";

const connectButton = document.querySelector<HTMLButtonElement>("#connect");
const disconnectButton = document.querySelector<HTMLButtonElement>("#disconnect");
const sendTextButton = document.querySelector<HTMLButtonElement>("#sendText");
const textPrompt = document.querySelector<HTMLInputElement>("#textPrompt");
const status = document.querySelector<HTMLPreElement>("#status");

let session: ReturnType<typeof buildRealtimeSession> | null = null;

function log(message: string) {
  if (!status) return;
  status.textContent = `${new Date().toLocaleTimeString()} ${message}\n${status.textContent}`;
}

function setConnected(connected: boolean) {
  if (connectButton) connectButton.disabled = connected;
  if (disconnectButton) disconnectButton.disabled = !connected;
  if (sendTextButton) sendTextButton.disabled = !connected;
}

async function fetchClientSecret(): Promise<string> {
  const response = await fetch("/token");
  if (!response.ok) {
    throw new Error(`Token endpoint failed with ${response.status}`);
  }
  return extractClientSecret(await response.json());
}

connectButton?.addEventListener("click", async () => {
  try {
    log("Requesting microphone permission and realtime client secret.");
    const clientSecret = await fetchClientSecret();
    session = buildRealtimeSession(buildRealtimeAgent());

    const eventSource = session as unknown as {
      on?: (event: string, listener: (...args: unknown[]) => void) => void;
    };
    eventSource.on?.("error", (event) => log(`error ${JSON.stringify(event)}`));
    eventSource.on?.("agent_start", () => log("Agent started responding."));
    eventSource.on?.("audio_start", () => log("Assistant audio started."));
    eventSource.on?.("audio_stopped", () => log("Assistant audio stopped."));
    eventSource.on?.("audio_interrupted", () => log("Assistant audio interrupted."));
    eventSource.on?.("transport_event", (event) => {
      const message = formatTransportEvent(event as Parameters<typeof formatTransportEvent>[0]);
      if (message) log(message);
    });

    await connectRealtimeSession(session, clientSecret);
    setConnected(true);
    log("Connected. Speak into the browser microphone.");
  } catch (error) {
    log(error instanceof Error ? error.message : String(error));
    setConnected(false);
  }
});

disconnectButton?.addEventListener("click", () => {
  const maybeClosable = session as unknown as {
    close?: () => void;
    disconnect?: () => void;
  };
  maybeClosable?.close?.();
  maybeClosable?.disconnect?.();
  session = null;
  setConnected(false);
  log("Disconnected.");
});

sendTextButton?.addEventListener("click", () => {
  if (!session || !textPrompt) return;
  const maybeSend = session as unknown as {
    sendMessage?: (message: string) => void;
    send?: (event: unknown) => void;
  };

  if (maybeSend.sendMessage) {
    maybeSend.sendMessage(textPrompt.value);
    log(`Sent text prompt: ${textPrompt.value}`);
    return;
  }

  maybeSend.send?.({
    type: "conversation.item.create",
    item: {
      type: "message",
      role: "user",
      content: [
        {
          type: "input_text",
          text: textPrompt.value
        }
      ]
    }
  });
  maybeSend.send?.({ type: "response.create" });
  log(`Sent text event: ${textPrompt.value}`);
});
