import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./pages/Home";
import ResultsPage from "./pages/ResultsPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/results"
          element={<ResultsPage />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;