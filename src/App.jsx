import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom"
import { useState, useEffect } from "react"
import { tokenStore } from "./lib/api"
import ResumePage from "./pages/ResumePage"
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage"

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!tokenStore.getAccess())

  useEffect(() => {
    const handleStorageChange = () => {
      setIsLoggedIn(!!tokenStore.getAccess())
    }

    window.addEventListener("storage", handleStorageChange)
    return () => window.removeEventListener("storage", handleStorageChange)
  }, [])

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<LoginPage setIsLoggedIn={setIsLoggedIn} />} />
        <Route path="/register" element={<RegisterPage setIsLoggedIn={setIsLoggedIn} />} />
        <Route
          path="/"
          element={isLoggedIn ? <ResumePage /> : <Navigate to="/login" />}
        />
      </Routes>
    </Router>
  )
}

export default App
