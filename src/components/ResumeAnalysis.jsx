export default function ResumeAnalysis({ analysis }) {
  if (!analysis) return null

  const {
    ats_score,
    improvement_suggestions,
    strengths,
    weaknesses,
    keywords_present,
    missing_keywords,
  } = analysis

  const scoreColor =
    ats_score >= 80 ? "text-green-600" : ats_score >= 60 ? "text-yellow-600" : "text-red-600"

  const scoreBgColor =
    ats_score >= 80 ? "bg-green-50" : ats_score >= 60 ? "bg-yellow-50" : "bg-red-50"

  return (
    <div className="space-y-8">
      {/* ATS Score */}
      <div className={`${scoreBgColor} border border-slate-200 rounded-lg p-8`}>
        <h3 className="text-lg font-semibold text-slate-900 mb-4">ATS Score</h3>
        <div className={`text-6xl font-bold ${scoreColor}`}>{ats_score}/100</div>
        <p className="text-slate-600 mt-2">
          {ats_score >= 80
            ? "Excellent! Your resume is well-optimized for ATS systems."
            : ats_score >= 60
              ? "Good! There are opportunities to improve your ATS score."
              : "Your resume needs improvements for better ATS compatibility."}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Strengths */}
        {strengths && strengths.length > 0 && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4 flex items-center">
              <span className="text-2xl mr-2">✓</span> Strengths
            </h3>
            <ul className="space-y-2">
              {strengths.map((strength, idx) => (
                <li key={idx} className="text-slate-700 flex items-start">
                  <span className="text-green-600 mr-2">•</span>
                  <span>{strength}</span>
                </li>
              ))}
            </ul>
          </div>
        )}

        {/* Weaknesses */}
        {weaknesses && weaknesses.length > 0 && (
          <div className="bg-orange-50 border border-orange-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4 flex items-center">
              <span className="text-2xl mr-2">!</span> Areas to Improve
            </h3>
            <ul className="space-y-2">
              {weaknesses.map((weakness, idx) => (
                <li key={idx} className="text-slate-700 flex items-start">
                  <span className="text-orange-600 mr-2">•</span>
                  <span>{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Improvement Suggestions */}
      {improvement_suggestions && improvement_suggestions.length > 0 && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-slate-900 mb-4">💡 Improvement Suggestions</h3>
          <ul className="space-y-3">
            {improvement_suggestions.map((suggestion, idx) => (
              <li key={idx} className="text-slate-700 flex items-start">
                <span className="text-blue-600 mr-3 font-medium">{idx + 1}.</span>
                <span>{suggestion}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Keywords Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {keywords_present && keywords_present.length > 0 && (
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              ✓ Keywords Present ({keywords_present.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {keywords_present.map((keyword, idx) => (
                <span
                  key={idx}
                  className="bg-green-100 text-green-800 px-3 py-1 rounded-full text-sm"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}

        {missing_keywords && missing_keywords.length > 0 && (
          <div className="bg-slate-50 border border-slate-200 rounded-lg p-6">
            <h3 className="text-lg font-semibold text-slate-900 mb-4">
              Missing Keywords ({missing_keywords.length})
            </h3>
            <div className="flex flex-wrap gap-2">
              {missing_keywords.map((keyword, idx) => (
                <span
                  key={idx}
                  className="bg-red-100 text-red-800 px-3 py-1 rounded-full text-sm"
                >
                  {keyword}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
