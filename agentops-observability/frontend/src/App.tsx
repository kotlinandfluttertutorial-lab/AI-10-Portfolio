/**
 * AgentOps frontend application root.
 * Routes and feature components are added in P05-15 (Dashboard) and later.
 */

function App(): JSX.Element {
  return (
    <main style={{ fontFamily: "system-ui, sans-serif", padding: "2rem" }}>
      <h1>AgentOps — AI Agent Monitoring</h1>
      <p>
        Platform is initialising. Dashboard components will appear in P05-15.
      </p>
      <p>
        API:{" "}
        <a href="/docs" target="_blank" rel="noreferrer">
          /docs
        </a>{" "}
        |{" "}
        <a href="/health" target="_blank" rel="noreferrer">
          /health
        </a>{" "}
        |{" "}
        <a href="/metrics" target="_blank" rel="noreferrer">
          /metrics
        </a>
      </p>
    </main>
  );
}

export default App;
