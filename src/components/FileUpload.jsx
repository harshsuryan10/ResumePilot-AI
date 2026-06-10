import { useRef } from "react"

export default function FileUpload({ onFileSelect, loading, fileInputRef }) {
  const dragRef = useRef(null)
  const localInputRef = useRef(null)

  const inputRef = fileInputRef || localInputRef

  const handleDragOver = (e) => {
    e.preventDefault()
    e.stopPropagation()
    dragRef.current?.classList.add("bg-blue-50", "border-blue-400")
  }

  const handleDragLeave = (e) => {
    e.preventDefault()
    e.stopPropagation()
    dragRef.current?.classList.remove("bg-blue-50", "border-blue-400")
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    dragRef.current?.classList.remove("bg-blue-50", "border-blue-400")

    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  const handleFile = (file) => {
    if (file && (file.type === "application/pdf" || file.name.endsWith(".pdf"))) {
      onFileSelect(file)
    } else {
      alert("Please upload a PDF file")
    }
  }

  const handleInputChange = (e) => {
    const files = e.target.files
    if (files.length > 0) {
      handleFile(files[0])
    }
  }

  return (
    <div
      ref={dragRef}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
      className="max-w-2xl mx-auto border-2 border-dashed border-slate-300 rounded-lg p-12 text-center cursor-pointer transition bg-white hover:border-blue-400 hover:bg-blue-50"
      onClick={() => inputRef.current?.click()}
    >
      <div className="space-y-4">
        <div className="text-4xl">📄</div>
        <div>
          <h3 className="text-xl font-semibold text-slate-900">
            Click to upload your resume
          </h3>
          <p className="text-slate-600 mt-2">or drag and drop</p>
          <p className="text-sm text-slate-500 mt-1">PDF format only</p>
        </div>
      </div>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,application/pdf"
        onChange={handleInputChange}
        disabled={loading}
        className="hidden"
      />

      {loading && <p className="mt-4 text-blue-600 font-medium">Analyzing...</p>}
    </div>
  )
}
