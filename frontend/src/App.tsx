import LogInteractionForm from "./components/LogInteractionForm";
import ChatAssistant from "./components/ChatAssistant";

function App() {
  return (
    <div className="page">
      <h1>Log HCP Interaction</h1>

      <div className="layout">
        <LogInteractionForm />
        <ChatAssistant />
      </div>
    </div>
  );
}

export default App;