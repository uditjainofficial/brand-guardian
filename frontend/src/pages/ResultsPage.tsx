import { useLocation } from "react-router-dom";
import type { AuditResponse } from "../types/audit";

export default function ResultsPage() {

  const location = useLocation();

  const result =
    location.state as AuditResponse;

  if (!result) {
    return (
      <div className="text-white p-8">
        No audit results found.
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white p-10">

      <h1 className="text-4xl font-bold mb-6">
        Audit Report
      </h1>

      <div className="mb-6">
        <span className="font-bold">
          Status:
        </span>{" "}
        {result.status}
      </div>

      <div className="mb-6">
        <span className="font-bold">
          Summary:
        </span>{" "}
        {result.final_report}
      </div>

      <div className="space-y-4">

        {result.compliance_results.map(
          (item, index) => (
            <div
              key={index}
              className="border border-zinc-800 p-4 rounded-xl"
            >
              <h3 className="font-semibold">
                {item.category}
              </h3>

              <p>
                Severity:
                {" "}
                {item.severity}
              </p>

              <p>
                {item.description}
              </p>
            </div>
          )
        )}

      </div>

    </div>
  );
}