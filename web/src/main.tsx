/*************************************************************************
 * Name: Lukas (Viridis) Dubsik
 * Login: xdubsil00
 * Project: IRCOMP
 * School-Project: ITU-1
 *************************************************************************/
import { createRoot } from "react-dom/client";
import { WorkspaceProvider } from "./app/WorkspaceProvider";
import { App } from "./app/App";
import "./styles.css";

createRoot(document.getElementById("root")!).render(
  <WorkspaceProvider>
    <App />
  </WorkspaceProvider>,
);
