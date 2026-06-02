export interface ComplianceResult {
  category: string;
  severity: string;
  description: string;
}

export interface AuditResponse {
  session_id: string;
  video_id: string;
  status: string;
  final_report: string;
  compliance_results: ComplianceResult[];
}