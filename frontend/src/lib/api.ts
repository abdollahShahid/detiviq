const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL!;

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${path}`);
  }

  return response.json();
}

export type OpenDetentionCasesSummary = {
  open_case_count: number;
  total_open_amount: string;
  avg_open_amount: string;
};

export type TopDelayedFacility = {
  facility_id: number;
  facility_name: string;
  stop_count: number;
  avg_dwell_minutes: string;
  total_amount: string;
};

export type RevenueLossSummary = {
  total_cases: number;
  total_amount: string;
  avg_amount: string;
  closed_case_count: number;
  open_case_count: number;
};

export const getOpenDetentionCasesSummary = () =>
  getJson<OpenDetentionCasesSummary>("/analytics/open-detention-cases-summary");

export const getTopDelayedFacilities = () =>
  getJson<TopDelayedFacility[]>("/analytics/top-delayed-facilities");

export const getRevenueLossSummary = () =>
  getJson<RevenueLossSummary>("/analytics/revenue-loss-summary");
