const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export type ApiSummary = {
  api_slug: string;
  api_name: string;
  title: string;
  version?: string | null;
  created_at: string;
};

export type UploadResponse = {
  api_slug: string;
  api_name: string;
  version?: string | null;
  components: {
    component_name: string;
    storage_key: string;
    property_count: number;
  }[];
};

export type ComponentMeta = {
  component_name: string;
  storage_key: string;
  property_count: number;
  created_at: string;
};

export type PropertyRow = {
  id: number;
  property_name: string;
  property_type?: string | null;
  property_format?: string | null;
  is_required: boolean;
  description?: string | null;
  example?: unknown;
  reference?: string | null;
};

export type ComponentDetail = {
  component_name: string;
  storage_key?: string | null;
  component_schema: Record<string, unknown>;
  properties: PropertyRow[];
};

export type ComponentDataset = Record<string, Record<string, unknown>[]>;

export type ComponentGraphNode = {
  component_name: string;
  storage_key: string;
  created_at: string;
  property_count: number;
  references: string[];
  dependent_count: number;
};

export type ComponentGraphEdge = {
  source: string;
  target: string;
};

export type ComponentGraph = {
  nodes: ComponentGraphNode[];
  edges: ComponentGraphEdge[];
};

export type RouteInventoryEntry = {
  method: string;
  path: string;
  operation_id?: string | null;
  summary?: string | null;
  tags: string[];
  request_body_ref?: string | null;
  response_body_ref?: string | null;
  path_parameters: string[];
  query_parameters: string[];
};

export async function listApis(): Promise<ApiSummary[]> {
  const res = await fetch(`${BACKEND_URL}/apis`, { next: { revalidate: 0 } });
  if (!res.ok) throw new Error(`Failed to list APIs: ${res.status}`);
  return res.json();
}

export async function getComponentGraph(apiSlug: string): Promise<ComponentGraph> {
  const res = await fetch(`${BACKEND_URL}/apis/${encodeURIComponent(apiSlug)}/graph`, {
    next: { revalidate: 0 },
  });
  if (!res.ok) throw new Error(`Failed to load component graph: ${res.status}`);
  return res.json();
}

export async function listComponents(apiSlug: string): Promise<ComponentMeta[]> {
  const res = await fetch(`${BACKEND_URL}/apis/${encodeURIComponent(apiSlug)}/components`, {
    next: { revalidate: 0 },
  });
  if (!res.ok) throw new Error(`Failed to list components: ${res.status}`);
  return res.json();
}

export async function listRoutes(apiSlug: string): Promise<RouteInventoryEntry[]> {
  const res = await fetch(`${BACKEND_URL}/apis/${encodeURIComponent(apiSlug)}/routes`, {
    next: { revalidate: 0 },
  });
  if (!res.ok) throw new Error(`Failed to list routes: ${res.status}`);
  return res.json();
}

export async function getComponentDetail(
  apiSlug: string,
  componentName: string
): Promise<ComponentDetail> {
  const res = await fetch(
    `${BACKEND_URL}/apis/${encodeURIComponent(apiSlug)}/components/${encodeURIComponent(componentName)}`,
    { next: { revalidate: 0 } }
  );
  if (!res.ok) throw new Error(`Failed to fetch component: ${res.status}`);
  return res.json();
}

export async function uploadOpenApiSpec(formData: FormData) {
  const res = await fetch(`${BACKEND_URL}/apis/upload`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Upload failed: ${res.status} ${text}`);
  }
  return res.json() as Promise<UploadResponse>;
}

export type GoalResponse = {
  goal_id: string;
  api_slug: string;
  description?: string | null;
  start_state_id: string;
  goal_state: Record<string, unknown>;
  reward_config?: RewardConfig | null;
  created_at: string;
};

export type RewardCondition = {
  component: string;
  field: string;
  operator?: string;
  value: unknown;
  reward?: number;
};

export type RewardConfig = {
  invalid_status_penalty?: number;
  success_bonus?: number;
  progress_weight?: number;
  custom_conditions?: RewardCondition[];
};

export type CreateGoalPayload = {
  api_slug: string;
  goal_state: Record<string, unknown>;
  description?: string;
  start_state_id?: string | null;
  seed_data?: ComponentDataset;
  reward_config?: RewardConfig;
};

export async function createGoal(payload: CreateGoalPayload): Promise<GoalResponse> {
  const res = await fetch(`${BACKEND_URL}/rl/goals`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Failed to create goal: ${res.status} ${detail}`);
  }
  return res.json();
}

export type EpisodeResponse = {
  episode_id: string;
  goal_id: string;
  current_state_id: string;
  action_history: string[];
  reward: number;
  done: boolean;
  created_at: string;
  updated_at: string;
};

export async function startEpisode(goalId: string): Promise<EpisodeResponse> {
  const res = await fetch(`${BACKEND_URL}/rl/goals/${encodeURIComponent(goalId)}/episodes`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal_id: goalId }),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Failed to start episode: ${res.status} ${detail}`);
  }
  return res.json();
}

export async function getEpisode(episodeId: string): Promise<EpisodeResponse> {
  const res = await fetch(`${BACKEND_URL}/rl/episodes/${encodeURIComponent(episodeId)}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Failed to load episode: ${res.status} ${detail}`);
  }
  return res.json();
}

export type StateResponse = {
  state_id: string;
  api_slug: string;
  parent_state_id?: string | null;
  action_path: string[];
  modified_components: ComponentDataset;
  created_at: string;
};

export async function getState(stateId: string): Promise<StateResponse> {
  const res = await fetch(`${BACKEND_URL}/rl/states/${encodeURIComponent(stateId)}`, {
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Failed to load state: ${res.status} ${detail}`);
  }
  return res.json();
}
