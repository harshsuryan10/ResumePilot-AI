import { useState, useRef } from "react"
import { useNavigate } from "react-router-dom"
import { api, tokenStore, apiError } from "../lib/api"
import FileUpload from "../components/FileUpload"
import ResumeAnalysis from "../components/ResumeAnalysis"

export default function ResumePage() {
  const navigate = useNavigate()
  const [resume, setResume] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const fileInputRef = useRef(null)

  const handleFileUpload = async (file) => {
  setError("")
  setLoading(true)

  const formData = new FormData()
  formData.append("file", file)

  try {
    // Step 1: Upload Resume
    const uploadResponse = await api.post("/resumes", formData)

    const resumeId = uploadResponse.data?.data?._id

    if (!resumeId) {
      throw new Error("Resume ID not returned from upload API")
    }

    // Step 2: Analyze Resume
    const analysisResponse = await api.post(
      `/resumes/${resumeId}/analyze`
    )

    setAnalysis({
      resume: uploadResponse.data.data,
      analysis: analysisResponse.data.data,
    })

    setResume(file)
  } catch (err) {
    console.error(err)
    setError(
      apiError(err, "Failed to upload and analyze resume. Please try again.")
    )
    setAnalysis(null)
  } finally {
    setLoading(false)
  }
}

  const handleLogout = () => {
    tokenStore.clear()
    navigate("/login")
  }

  const handleNewResume = () => {
    setResume(null)
    setAnalysis(null)
    setError("")
    if (fileInputRef.current) {
      fileInputRef.current.value = ""
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      <nav className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-slate-900">AI Resume Copilot</h1>
          <button
            onClick={handleLogout}
            className="px-4 py-2 text-slate-600 hover:text-slate-900 font-medium"
          >
            Logout
          </button>
        </div>
      </nav>

      <main className="max-w-6xl mx-auto px-6 py-12">
        {!analysis ? (
          <>
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-slate-900 mb-4">
                Analyze Your Resume
              </h2>
              <p className="text-xl text-slate-600 mb-8">
                Get an ATS score and AI-powered feedback to improve your resume
              </p>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mb-8 max-w-2xl mx-auto">
                {error}
              </div>
            )}

            <FileUpload
              onFileSelect={handleFileUpload}
              loading={loading}
              fileInputRef={fileInputRef}
            />
          </>
        ) : (
          <>
            <div className="mb-8 flex justify-between items-center">
              <h2 className="text-3xl font-bold text-slate-900">Resume Analysis</h2>
              <button
                onClick={handleNewResume}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium"
              >
                Analyze Another
              </button>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-6 py-4 rounded-lg mb-8">
                {error}
              </div>
            )}

            <ResumeAnalysis analysis={analysis} />
          </>
        )}
      </main>
    </div>
  )
}
