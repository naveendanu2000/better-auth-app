import { Toaster } from "react-hot-toast";
import LoginPage from "./pages/LoginPage";
import { AuthProvider } from "./context/AuthProvider";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ProtectedAuthRoute from "./components/ProtectedAuthRoute";
import UserDashboard from "./pages/UserDashboard";

const App = () => {
  return (
    <div className="bg-black **:transition-all **:duration-600 text-[#3B3B3B] h-screen flex items-center justify-center">
      <div className="h-full w-full absolute bg-linear-to-br from-white/0 from-0% via-white via-60% to-white/0 to-100% opacity-40"></div>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route
            path="/user"
            element={
              <ProtectedAuthRoute>
                <AuthProvider>
                  <UserDashboard />
                </AuthProvider>
              </ProtectedAuthRoute>
            }
          />
        </Routes>
      </BrowserRouter>
      <Toaster />
    </div>
  );
};

export default App;
