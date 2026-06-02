import axios from "axios";
import type { AuditResponse } from "../types/audit";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const runAudit = async (
  videoUrl: string
): Promise<AuditResponse> => {

  const response = await api.post<AuditResponse>(
    "/audit",
    {
      video_url: videoUrl,
    }
  );

  return response.data;
};

export default api;