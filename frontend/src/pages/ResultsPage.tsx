import { useLocation, useNavigate } from "react-router-dom";
import type { AuditResponse } from "../types/audit";

export default function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();

  const result = location.state as AuditResponse;

  if (!result) {
    return (
      <div className="min-h-screen bg-black text-white flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">
            No audit results found
          </h2>

          <button
            onClick={() => navigate("/")}
            className="
              rounded-xl
              bg-blue-600
              px-5
              py-3
              hover:bg-blue-700
              transition
            "
          >
            Back Home
          </button>
        </div>
      </div>
    );
  }

  const criticalCount = result.compliance_results.filter(
    (v) => v.severity === "CRITICAL"
  ).length;

  const majorCount = result.compliance_results.filter(
    (v) => v.severity === "MAJOR"
  ).length;

  const minorCount = result.compliance_results.filter(
    (v) => v.severity === "MINOR"
  ).length;

  const score = Math.max(
    0,
    100 -
      criticalCount * 30 -
      majorCount * 15 -
      minorCount * 5
  );

  const scoreColor =
    score >= 80
      ? "text-green-400"
      : score >= 60
      ? "text-yellow-400"
      : "text-red-400";

  const statusColor =
    result.status === "PASS"
      ? "bg-green-600"
      : "bg-red-600";

  const getSeverityColor = (
    severity: string
  ) => {
    switch (severity) {
      case "CRITICAL":
        return "bg-red-600";

      case "MAJOR":
        return "bg-orange-500";

      case "MINOR":
        return "bg-yellow-500";

      default:
        return "bg-gray-500";
    }
  };

  return (
    <div className="min-h-screen bg-black text-white">
      <div className="max-w-6xl mx-auto px-6 py-12">

        {/* Header */}

        <div className="flex items-center justify-between mb-10">
          <div>
            <h1 className="text-5xl font-bold">
              Audit Report
            </h1>

            <p className="text-gray-400 mt-2">
              AI Compliance Assessment
            </p>

            <p className="text-sm text-gray-500 mt-3">
              Video ID: {result.video_id}
            </p>
          </div>

          <button
            onClick={() => navigate("/")}
            className="
              rounded-xl
              border
              border-gray-700
              px-5
              py-3
              hover:bg-gray-900
              transition
            "
          >
            ← Run Another Audit
          </button>
        </div>

        {/* Score + Status */}

        <div className="grid md:grid-cols-2 gap-6 mb-8">

          <div
            className="
              rounded-2xl
              border
              border-zinc-800
              p-8
              bg-zinc-950
            "
          >
            <p className="text-gray-400 mb-2">
              Compliance Score
            </p>

            <h2
              className={`
                text-6xl
                font-bold
                ${scoreColor}
              `}
            >
              {score}
            </h2>

            <p className="text-gray-500 mt-2">
              out of 100
            </p>
          </div>

          <div
            className="
              rounded-2xl
              border
              border-zinc-800
              p-8
              bg-zinc-950
            "
          >
            <p className="text-gray-400 mb-4">
              Final Status
            </p>

            <span
              className={`
                ${statusColor}
                px-5
                py-2
                rounded-full
                font-semibold
              `}
            >
              {result.status}
            </span>
          </div>

        </div>

        {/* Severity Summary */}

        <div className="grid md:grid-cols-3 gap-6 mb-10">

          <div
            className="
              rounded-xl
              border
              border-red-700
              p-6
            "
          >
            <h3 className="text-red-400 text-sm">
              🚨 CRITICAL
            </h3>

            <p className="text-4xl font-bold mt-2">
              {criticalCount}
            </p>
          </div>

          <div
            className="
              rounded-xl
              border
              border-orange-600
              p-6
            "
          >
            <h3 className="text-orange-400 text-sm">
              ⚠ MAJOR
            </h3>

            <p className="text-4xl font-bold mt-2">
              {majorCount}
            </p>
          </div>

          <div
            className="
              rounded-xl
              border
              border-yellow-600
              p-6
            "
          >
            <h3 className="text-yellow-400 text-sm">
              ℹ MINOR
            </h3>

            <p className="text-4xl font-bold mt-2">
              {minorCount}
            </p>
          </div>

        </div>

        {/* Executive Summary */}

        <div
          className="
            rounded-2xl
            border
            border-zinc-800
            p-8
            mb-10
            bg-zinc-950
          "
        >
          <h2 className="text-2xl font-bold mb-4">
            Executive Summary
          </h2>

          <p className="text-gray-300 leading-8">
            {result.final_report}
          </p>
        </div>

        {/* Empty State */}

        {result.compliance_results.length === 0 ? (
          <div
            className="
              rounded-2xl
              border
              border-green-700
              bg-green-950/20
              p-8
              text-center
            "
          >
            <h2 className="text-3xl font-bold text-green-400 mb-3">
              🎉 No Compliance Issues Detected
            </h2>

            <p className="text-gray-300">
              This content passed all compliance checks.
            </p>
          </div>
        ) : (
          <>
            <h2 className="text-3xl font-bold mb-6">
              Detected Violations
            </h2>

            <div className="space-y-5">

              {result.compliance_results.map(
                (item, index) => (
                  <div
                    key={index}
                    className="
                      rounded-2xl
                      border
                      border-zinc-800
                      bg-zinc-950
                      p-6
                    "
                  >
                    <div className="flex items-center justify-between mb-4">

                      <h3 className="text-xl font-semibold">
                        {item.category}
                      </h3>

                      <span
                        className={`
                          ${getSeverityColor(
                            item.severity
                          )}
                          px-3
                          py-1
                          rounded-full
                          text-sm
                          font-semibold
                        `}
                      >
                        {item.severity}
                      </span>

                    </div>

                    <p className="text-gray-300 leading-8">
                      {item.description}
                    </p>
                  </div>
                )
              )}

            </div>
          </>
        )}

      </div>
    </div>
  );
}