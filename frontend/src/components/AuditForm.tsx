import { useState } from "react";

export default function AuditForm() {
  const [url, setUrl] = useState("");

  return (
    <div className="max-w-3xl mx-auto">
      <div className="flex gap-4">
        <input
          type="text"
          placeholder="Paste YouTube URL..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
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
          className="
            rounded-xl
            bg-blue-500
            px-6
            py-3
            font-medium
            hover:bg-blue-600
            transition
          "
        >
          Run Audit
        </button>
      </div>
    </div>
  );
}