import axios from "axios"

const API_BASE = import.meta.env.VITE_API_BASE_URL || "/api/v1"

const TOKEN_KEY = "arc_access_token";
const REFRESH_KEY = "arc_refresh_token";

export const tokenStore = {
  getAccess: () => localStorage.getItem(TOKEN_KEY),
  getRefresh: () => localStorage.getItem(REFRESH_KEY),
  set: (access, refresh) => {
    if (access) localStorage.setItem(TOKEN_KEY, access);
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
  },
  clear: () => {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_KEY);
  },
}

export const api = axios.create({
  baseURL: API_BASE,
})

api.interceptors.request.use((config) => {
  const token = tokenStore.getAccess()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let isRefreshing = false
let pendingQueue = []

function resolveQueue(error, token = null) {
  pendingQueue.forEach((p) => (error ? p.reject(error) : p.resolve(token)))
  pendingQueue = []
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    const status = error.response?.status

    if (status === 401 && !original._retry && tokenStore.getRefresh()) {
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          pendingQueue.push({ resolve, reject })
        }).then((token) => {
          original.headers.Authorization = `Bearer ${token}`
          return api(original)
        })
      }

      original._retry = true
      isRefreshing = true

      try {
        const { data } = await axios.post(`${API_BASE}/auth/refresh`, {
          refresh_token: tokenStore.getRefresh(),
        })
        const tokens = data.data || data;
        tokenStore.set(tokens.access_token, tokens.refresh_token)
        resolveQueue(null, tokens.access_token)
        original.headers.Authorization = `Bearer ${tokens.access_token}`
        return api(original)
      } catch (refreshError) {
        resolveQueue(refreshError, null)
        tokenStore.clear()
        window.location.href = "/login"
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    return Promise.reject(error)
  }
)

export function apiError(error, fallback = "Something went wrong.") {
  return (
    error?.response?.data?.message ||
    error?.message ||
    fallback
  )
}
