import React from "react";
import ReactDOM from "react-dom/client";
import Router from "./Router";

const appRoot = document.getElementById('react-app-root')!;

ReactDOM.createRoot(appRoot).render(
    <React.StrictMode>
         <Router />
    </React.StrictMode>
)