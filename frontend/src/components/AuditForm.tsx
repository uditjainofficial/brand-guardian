import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { runAudit } from "../services/api";
import AuditProgress from "./AuditProgress";

export default function AuditForm() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const [step, setStep] = useState(
    "Preparing Audit..."
  );

  const navigate = useNavigate();

  useEffect(() => {
    if (!loading) return;

    const stages = [
      "Downloading Video...",
      "Transcribing Audio with Whisper...",
      "Extracting OCR from Frames...",
      "Retrieving Compliance Policies...",
      "Running Groq Compliance Audit...",
      "Generating Report...",
    ];

    let index = 0;

    setStep(stages[0]);

    const interval = setInterval(() => {
      index++;

      if (index < stages.length) {
        setStep(stages[index]);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [loading]);

  const handleAudit = async () => {
    if (!url.trim()) {
      alert("Please enter a YouTube URL");
      return;
    }

    try {
      setLoading(true);

      const result = await runAudit(url);

      navigate("/results", {
        state: result,
      });
    } catch (error) {
      console.error(error);

      alert(
        "Audit failed. Please check backend logs."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {loading && (
        <AuditProgress step={step} />
      )}

      <div className="max-w-3xl mx-auto">
        <div className="flex gap-4">

          <input
            type="text"
            placeholder="Paste YouTube URL..."
            value={url}
            onChange={(e) =>
              setUrl(e.target.value)
            }
            disabled={loading}
            className="
              flex-1
              rounded-xl
              border
              border-gray-700
              bg-gray-900
              px-4
              py-3
              text-white
              outline-none
            "
          />

          <button
            onClick={handleAudit}
            disabled={loading}
            className="
              rounded-xl
              bg-blue-500
              px-6
              py-3
              font-medium
              hover:bg-blue-600
              transition
              disabled:opacity-50
            "
          >
            {loading
              ? "Auditing..."
              : "Run Audit"}
          </button>

        </div>
      </div>
    </>
  );
}