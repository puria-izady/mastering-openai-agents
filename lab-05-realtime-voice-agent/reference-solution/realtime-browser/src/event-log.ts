export type RealtimeTransportLike = {
  type?: string;
  transcript?: string;
  delta?: string;
  error?: unknown;
};

export function formatTransportEvent(event: RealtimeTransportLike): string | null {
  switch (event.type) {
    case "conversation.item.input_audio_transcription.completed":
      return event.transcript?.trim() ? `You said: ${event.transcript}` : null;
    case "conversation.item.input_audio_transcription.failed":
      return `Input transcription failed: ${JSON.stringify(event.error ?? event)}`;
    case "response.output_audio_transcript.delta":
      return null;
    case "response.output_audio_transcript.done":
      return `Assistant said: ${event.transcript ?? ""}`;
    case "response.done":
      return "Realtime turn complete.";
    case "error":
      return `Realtime error: ${JSON.stringify(event.error ?? event)}`;
    default:
      return null;
  }
}
