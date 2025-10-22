const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export type ApiSummary = {
  api_slug: string;
  api_name: string;
  title: string;
  version?: string | null;
  created_at: string;
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
  return res.json();
}

