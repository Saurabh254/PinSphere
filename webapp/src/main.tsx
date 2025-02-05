import ReactDOM from "react-dom/client";
import { BrowserRouter as Router } from "react-router-dom";
import App from "./App";

const root = document.getElementById("root")!;

ReactDOM.createRoot(root).render(
  <Router>
    <App />
  </Router>
);
