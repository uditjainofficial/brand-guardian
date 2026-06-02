import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { runAudit } from "../services/api";

export default function AuditForm() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

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
    <div className="max-w-3xl mx-auto">
      <div className="flex gap-4">

        <input
          type="text"
          placeholder="Paste YouTube URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
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
  );
}