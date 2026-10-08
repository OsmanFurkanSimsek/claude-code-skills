# Prior session transcript (this is the conversation that just happened)

USER: I'm trying to decide between Server-Sent Events and WebSockets for streaming agent responses to our React frontend. Can you walk me through the tradeoffs?

ASSISTANT: Sure. The short version: SSE is one-directional (server → client) over plain HTTP, auto-reconnects, and works through most proxies without special handling. WebSockets are bidirectional, lower per-message overhead, but need explicit reconnection logic and sometimes special proxy/load-balancer config. For streaming LLM tokens where the client only sends the occasional request and mostly receives, SSE is usually the simpler, more robust choice.

USER: What about the connection-limit issue with SSE over HTTP/1.1? I read browsers cap concurrent SSE connections.

ASSISTANT: Right — HTTP/1.1 browsers cap at ~6 concurrent connections per domain, and a long-lived SSE stream holds one open. If a user opens many tabs it can starve other requests. Over HTTP/2 the cap is much higher (multiplexed streams, default ~100), so if you're on HTTP/2 end-to-end it's mostly a non-issue. Most Cloud Run / modern proxy setups give you HTTP/2.

USER: And reconnection — does SSE really handle that for free?

ASSISTANT: The browser EventSource API auto-reconnects and sends a Last-Event-ID header so you can resume, but only if your server emits id: fields and knows how to replay from an ID. The reconnect itself is free; resuming without gaps is something you have to design for.

USER: Got it, that's really helpful. I think we'll go SSE but I need to check with the team whether our load balancer does HTTP/2 to the origin. Let me wrap up here — session handoff please.
