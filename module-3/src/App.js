import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "./pages/Login";
import { Registr } from "./pages/Registr";
import { Recept } from "./pages/Recept";
import { ReceptForm } from "./pages/ReceptForm";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="" element={<Recept />} />
        <Route path="login" element={<Login />} />
        <Route path="registr" element={<Registr />} />
        <Route path="recept/create" element={<ReceptForm />} />
        <Route path="recept/:id/:still_id" element={<ReceptForm />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
