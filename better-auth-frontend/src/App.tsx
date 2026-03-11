import { Toaster } from "react-hot-toast";
import LoginPage from "./pages/LoginPage";
import { AuthProvider } from "./context/AuthProvider";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import ProtectedAuthRoute from "./components/ProtectedAuthRoute";
import UserDashboard from "./pages/UserDashboard";

const App = () => {
  return (
    <div className="bg-red-200 **:transition-all **:duration-600 text-black h-screen flex items-center justify-center">
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
