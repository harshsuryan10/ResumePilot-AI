import { useState } from "react"
import { useNavigate, Link } from "react-router-dom"
import { motion, AnimatePresence } from "framer-motion"
import { Mail, Lock, Loader2, Sparkles, AlertCircle } from "lucide-react"
import { api, tokenStore, apiError } from "../lib/api"

export default function LoginPage({ setIsLoggedIn }) {
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError("")
    setLoading(true)

    try {
      const response = await api.post("/auth/login", { email, password })
      
      // FIX: Notice we are extracting from response.data.data.tokens!
      const { access_token, refresh_token } = response.data.data.tokens
      
      tokenStore.set(access_token, refresh_token)
      setIsLoggedIn(true)
      navigate("/")
    } catch (err) {
      setError(apiError(err, "Login failed. Please check your credentials."))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center bg-slate-950 overflow-hidden font-sans">
      
      {/* Animated Background Orbs */}
      <motion.div 
        animate={{ scale: [1, 1.2, 1], opacity: [0.3, 0.5, 0.3] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        className="absolute -top-32 -left-32 w-96 h-96 bg-blue-600 rounded-full mix-blend-screen filter blur-[128px]"
      />
      <motion.div 
        animate={{ scale: [1, 1.5, 1], opacity: [0.2, 0.4, 0.2] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut", delay: 1 }}
        className="absolute -bottom-32 -right-32 w-96 h-96 bg-indigo-600 rounded-full mix-blend-screen filter blur-[128px]"
      />

      {/* Main Login Card */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, ease: "easeOut" }}
        className="w-full max-w-md p-8 m-4 bg-slate-900/60 backdrop-blur-xl border border-slate-800 rounded-2xl shadow-2xl relative z-10"
      >
        
        {/* Header */}
        <div className="text-center mb-8">
          <motion.div 
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 260, damping: 20, delay: 0.2 }}
            className="inline-flex items-center justify-center w-12 h-12 rounded-xl bg-gradient-to-br from-blue-500 to-indigo-600 mb-4 shadow-lg shadow-blue-500/30"
          >
            <Sparkles className="w-6 h-6 text-white" />
          </motion.div>
          <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">Welcome Back</h1>
          <p className="text-slate-400">Sign in to AI Resume Copilot</p>
        </div>

        {/* Error Message Animation */}
        <AnimatePresence>
          {error && (
            <motion.div 
              initial={{ opacity: 0, height: 0, y: -10 }}
              animate={{ opacity: 1, height: "auto", y: 0 }}
              exit={{ opacity: 0, height: 0, y: -10 }}
              className="mb-6 overflow-hidden"
            >
              <div className="flex items-center gap-2 bg-red-500/10 border border-red-500/50 text-red-400 px-4 py-3 rounded-lg text-sm">
                <AlertCircle className="w-5 h-5 flex-shrink-0" />
                <p>{error}</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1.5 ml-1">
              Email Address
            </label>
            <div className="relative group">
              <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-blue-500 transition-colors" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full pl-11 pr-4 py-2.5 bg-slate-950/50 border border-slate-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all placeholder:text-slate-600"
                placeholder="you@example.com"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-1.5 ml-1">
              Password
            </label>
            <div className="relative group">
              <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-blue-500 transition-colors" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full pl-11 pr-4 py-2.5 bg-slate-950/50 border border-slate-700 text-white rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all placeholder:text-slate-600"
                placeholder="••••••••"
              />
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.01 }}
            whileTap={{ scale: 0.99 }}
            type="submit"
            disabled={loading}
            className="w-full relative flex items-center justify-center gap-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-2.5 rounded-xl font-semibold shadow-lg shadow-blue-600/20 hover:shadow-blue-600/40 disabled:opacity-70 disabled:cursor-not-allowed transition-all mt-6"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Authenticating...</span>
              </>
            ) : (
              <span>Sign In</span>
            )}
          </motion.button>
        </form>

        <p className="text-center text-slate-400 mt-8 text-sm">
          Don&apos;t have an account?{" "}
          <Link to="/register" className="text-blue-400 hover:text-blue-300 hover:underline font-medium transition-colors">
            Create one now
          </Link>
        </p>
      </motion.div>
    </div>
  )
}