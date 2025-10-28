"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import type { RouteInventoryEntry } from "@/lib/api";

type RoutePlaygroundProps = {
  apiSlug: string;
  routes: RouteInventoryEntry[];
};

type HeaderEntry = [string, string];

const BACKEND_BASE = (process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000").replace(/\/$/, "");

const METHOD_COLORS: Record<string, string> = {
  GET: "bg-emerald-100 text-emerald-700",
  POST: "bg-sky-100 text-sky-700",
  PUT: "bg-amber-100 text-amber-700",
  PATCH: "bg-purple-100 text-purple-700",
  DELETE: "bg-rose-100 text-rose-700",
  HEAD: "bg-gray-100 text-gray-700",
  OPTIONS: "bg-gray-100 text-gray-700",
};

function routeKey(route: RouteInventoryEntry): string {
  return `${route.method} ${route.path}`;
}

function MethodBadge({ method }: { method: string }) {
  const normalised = method.toUpperCase();
  const palette = METHOD_COLORS[normalised] || "bg-gray-100 text-gray-700";
  return <span className={`rounded px-2 py-0.5 text-xs font-semibold ${palette}`}>{normalised}</span>;
}

export default function RoutePlayground({ apiSlug, routes }: RoutePlaygroundProps) {
  const [selectedKey, setSelectedKey] = useState(() => (routes[0] ? routeKey(routes[0]) : ""));
  const [search, setSearch] = useState("");
  const [pathParams, setPathParams] = useState<Record<string, string>>({});
  const [queryParams, setQueryParams] = useState<Record<string, string>>({});
  const [requestBody, setRequestBody] = useState("");
  const [responseStatus, setResponseStatus] = useState<string | null>(null);
  const [responseBody, setResponseBody] = useState<string | null>(null);
  const [responseHeaders, setResponseHeaders] = useState<HeaderEntry[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [isSending, setIsSending] = useState(false);

  useEffect(() => {
    if (!routes.length) {
      setSelectedKey("");
      return;
    }
    const exists = routes.some((route) => routeKey(route) === selectedKey);
    if (!exists) {
      setSelectedKey(routeKey(routes[0]));
    }
  }, [routes, selectedKey]);

  const filteredRoutes = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return routes;
    return routes.filter((route) => {
      const summary = route.summary || "";
      const tagText = (route.tags || []).join(" ");
      return (
        route.method.toLowerCase().includes(term) ||
        route.path.toLowerCase().includes(term) ||
        summary.toLowerCase().includes(term) ||
        tagText.toLowerCase().includes(term)
      );
    });
  }, [routes, search]);

  const selectedRoute = useMemo(() => {
    const fromSelected = routes.find((route) => routeKey(route) === selectedKey);
    if (fromSelected) return fromSelected;
    return filteredRoutes[0] ?? routes[0] ?? null;
  }, [filteredRoutes, routes, selectedKey]);

  const pathParamKeys = useMemo(() => {
    if (!selectedRoute) return [];
    const explicit = selectedRoute.path_parameters || [];
    if (explicit.length > 0) return explicit;
    const matches = Array.from(selectedRoute.path.matchAll(/\{([^}]+)\}/g));
    return matches.map((match) => match[1]).filter(Boolean);
  }, [selectedRoute]);

  const queryParamKeys = useMemo(() => {
    if (!selectedRoute) return [];
    return selectedRoute.query_parameters || [];
  }, [selectedRoute]);

  useEffect(() => {
    if (!selectedRoute) return;
    setPathParams(() => {
      const next: Record<string, string> = {};
      pathParamKeys.forEach((param) => {
        next[param] = "";
      });
      return next;
    });
    setQueryParams(() => {
      const next: Record<string, string> = {};
      queryParamKeys.forEach((param) => {
        next[param] = "";
      });
      return next;
    });
    const allowsBody = !["GET", "HEAD"].includes(selectedRoute.method.toUpperCase());
    setRequestBody(allowsBody && selectedRoute.request_body_ref ? "{}" : "");
    setResponseStatus(null);
    setResponseBody(null);
    setResponseHeaders([]);
    setError(null);
  }, [selectedRoute, pathParamKeys, queryParamKeys]);

  const previewUrl = useMemo(() => {
    if (!selectedRoute) return "";
    let resolvedPath = selectedRoute.path;
    pathParamKeys.forEach((param) => {
      const value = pathParams[param];
      const replacement = value ? encodeURIComponent(value) : `{${param}}`;
      const pattern = new RegExp(`{${param}}`, "g");
      resolvedPath = resolvedPath.replace(pattern, replacement);
    });

    const base = `${BACKEND_BASE}/generated/${encodeURIComponent(apiSlug)}`;
    const normalisedPath = resolvedPath.startsWith("/") ? resolvedPath : `/${resolvedPath}`;

    const searchParams = new URLSearchParams();
    Object.entries(queryParams).forEach(([key, value]) => {
      if (value) searchParams.append(key, value);
    });
    const queryString = searchParams.toString();
    return queryString ? `${base}${normalisedPath}?${queryString}` : `${base}${normalisedPath}`;
  }, [apiSlug, pathParams, pathParamKeys, queryParams, selectedRoute]);

  const sendRequest = async () => {
    if (!selectedRoute) return;
    const method = selectedRoute.method.toUpperCase();
    for (const param of pathParamKeys) {
      if (!pathParams[param]) {
        setError(`Provide a value for path parameter "${param}".`);
        return;
      }
    }

    let resolvedPath = selectedRoute.path;
    pathParamKeys.forEach((param) => {
      const value = encodeURIComponent(pathParams[param] || "");
      const pattern = new RegExp(`{${param}}`, "g");
      resolvedPath = resolvedPath.replace(pattern, value);
    });

    const searchParams = new URLSearchParams();
    Object.entries(queryParams).forEach(([key, value]) => {
      if (value) searchParams.append(key, value);
    });

    const baseUrl = `${BACKEND_BASE}/generated/${encodeURIComponent(apiSlug)}`;
    let targetUrl = resolvedPath.startsWith("/") ? `${baseUrl}${resolvedPath}` : `${baseUrl}/${resolvedPath}`;
    const queryString = searchParams.toString();
    if (queryString) {
      targetUrl = `${targetUrl}?${queryString}`;
    }

    const init: RequestInit = {
      method,
    };

    const headers: Record<string, string> = {};
    const expectsBody = !["GET", "HEAD"].includes(method);

    if (expectsBody && requestBody.trim()) {
      try {
        JSON.parse(requestBody);
      } catch {
        setError("Request body must be valid JSON.");
        return;
      }
      init.body = requestBody;
      headers["Content-Type"] = "application/json";
    }

    if (Object.keys(headers).length > 0) {
      init.headers = headers;
    }

    setIsSending(true);
    setError(null);
    setResponseStatus(null);
    setResponseBody(null);
    setResponseHeaders([]);

    try {
      const res = await fetch(targetUrl, init);
      setResponseStatus(`${res.status} ${res.statusText || ""}`.trim());
      const headerEntries = Array.from(res.headers.entries()) as HeaderEntry[];
      setResponseHeaders(headerEntries);
      const text = await res.text();
      const contentType = res.headers.get("content-type") || "";
      if (!text) {
        setResponseBody("");
      } else if (contentType.includes("application/json")) {
        try {
          const parsed = JSON.parse(text);
          setResponseBody(JSON.stringify(parsed, null, 2));
        } catch {
          setResponseBody(text);
        }
      } else {
        setResponseBody(text);
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : "Unexpected error while calling the route.";
      setError(message);
    } finally {
      setIsSending(false);
    }
  };

  const methodAllowsBody = selectedRoute
    ? !["GET", "HEAD"].includes(selectedRoute.method.toUpperCase())
    : false;

  if (!selectedRoute) {
    return <p className="text-gray-600">No routes available.</p>;
  }

  const requestComponent = selectedRoute.request_body_ref
    ? selectedRoute.request_body_ref.split("/").pop()
    : null;
  const responseComponent = selectedRoute.response_body_ref
    ? selectedRoute.response_body_ref.split("/").pop()
    : null;

  return (
    <section className="grid gap-6 md:grid-cols-[300px_minmax(0,1fr)]">
      <aside className="space-y-4">
        <div>
          <label htmlFor="route-search" className="block text-sm font-medium text-gray-700">
            Filter routes
          </label>
          <input
            id="route-search"
            type="search"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
            className="mt-1 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30"
            placeholder="Search by path, method, or tag"
          />
        </div>
        <ul className="space-y-2 max-h-[28rem] overflow-y-auto pr-2">
          {filteredRoutes.map((route) => {
            const key = routeKey(route);
            const isSelected = key === routeKey(selectedRoute);
            return (
              <li key={key}>
                <button
                  type="button"
                  onClick={() => setSelectedKey(key)}
                  className={`w-full rounded border px-3 py-2 text-left transition ${
                    isSelected
                      ? "border-blue-500 bg-blue-50 shadow-sm"
                      : "border-gray-200 hover:border-blue-400 hover:bg-blue-50/50"
                  }`}
                >
                  <div className="flex items-center gap-2">
                    <MethodBadge method={route.method} />
                    <span className="font-mono text-xs text-gray-700">{route.path}</span>
                  </div>
                  {route.summary && <p className="mt-1 text-xs text-gray-600">{route.summary}</p>}
                </button>
              </li>
            );
          })}
          {filteredRoutes.length === 0 && (
            <li className="text-sm text-gray-600">No routes match your search.</li>
          )}
        </ul>
      </aside>
      <div className="space-y-6">
        <div className="rounded border border-gray-200 p-4 space-y-3">
          <div className="flex flex-wrap items-center gap-3">
            <MethodBadge method={selectedRoute.method} />
            <span className="font-mono text-sm text-gray-800">{selectedRoute.path}</span>
          </div>
          {selectedRoute.summary && <p className="text-sm text-gray-700">{selectedRoute.summary}</p>}
          {selectedRoute.tags && selectedRoute.tags.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {selectedRoute.tags.map((tag) => (
                <span key={tag} className="rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-700">
                  {tag}
                </span>
              ))}
            </div>
          )}
          <div className="rounded bg-gray-50 p-3 text-xs text-gray-700">
            <div className="font-semibold text-gray-800">Full URL</div>
            <code className="block break-all font-mono">{previewUrl}</code>
          </div>
          <dl className="grid gap-3 sm:grid-cols-2">
            {requestComponent && (
              <div>
                <dt className="text-xs font-semibold text-gray-600">Request body</dt>
                <dd className="text-xs text-blue-600">
                  <Link href={`/apis/${encodeURIComponent(apiSlug)}/components/${encodeURIComponent(requestComponent)}`}>
                    {requestComponent}
                  </Link>
                </dd>
              </div>
            )}
            {responseComponent && (
              <div>
                <dt className="text-xs font-semibold text-gray-600">Response body</dt>
                <dd className="text-xs text-blue-600">
                  <Link href={`/apis/${encodeURIComponent(apiSlug)}/components/${encodeURIComponent(responseComponent)}`}>
                    {responseComponent}
                  </Link>
                </dd>
              </div>
            )}
          </dl>
        </div>

        {pathParamKeys.length > 0 && (
          <div className="rounded border border-gray-200 p-4 space-y-3">
            <h2 className="text-sm font-semibold text-gray-700">Path parameters</h2>
            <div className="grid gap-3 sm:grid-cols-2">
              {pathParamKeys.map((param) => (
                <label key={param} className="text-xs font-medium text-gray-600">
                  {param}
                  <input
                    type="text"
                    value={pathParams[param] || ""}
                    onChange={(event) =>
                      setPathParams((prev) => ({
                        ...prev,
                        [param]: event.target.value,
                      }))
                    }
                    className="mt-1 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30"
                    placeholder={`Value for ${param}`}
                  />
                </label>
              ))}
            </div>
          </div>
        )}

        {queryParamKeys.length > 0 && (
          <div className="rounded border border-gray-200 p-4 space-y-3">
            <h2 className="text-sm font-semibold text-gray-700">Query parameters</h2>
            <div className="grid gap-3 sm:grid-cols-2">
              {queryParamKeys.map((param) => (
                <label key={param} className="text-xs font-medium text-gray-600">
                  {param}
                  <input
                    type="text"
                    value={queryParams[param] || ""}
                    onChange={(event) =>
                      setQueryParams((prev) => ({
                        ...prev,
                        [param]: event.target.value,
                      }))
                    }
                    className="mt-1 w-full rounded border border-gray-300 px-3 py-2 text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30"
                    placeholder={`Value for ${param}`}
                  />
                </label>
              ))}
            </div>
          </div>
        )}

        <div className="rounded border border-gray-200 p-4 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-gray-700">Request body</h2>
            <span className="text-xs text-gray-500">
              {methodAllowsBody ? "JSON payload" : "Not sent for this method"}
            </span>
          </div>
          <textarea
            value={requestBody}
            onChange={(event) => setRequestBody(event.target.value)}
            rows={8}
            disabled={!methodAllowsBody}
            className="w-full rounded border border-gray-300 px-3 py-2 font-mono text-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500/30 disabled:bg-gray-100 disabled:text-gray-500"
            placeholder='{ "example": true }'
          />
          <div className="flex items-center gap-3">
            <button
              type="button"
              onClick={sendRequest}
              disabled={isSending}
              className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:bg-blue-400"
            >
              {isSending ? "Sending…" : "Send request"}
            </button>
            {error && <span className="text-sm text-rose-600">{error}</span>}
            {responseStatus && !error && (
              <span className="text-sm text-gray-700">Status: {responseStatus}</span>
            )}
          </div>
        </div>

        <div className="rounded border border-gray-200 p-4 space-y-3">
          <h2 className="text-sm font-semibold text-gray-700">Response</h2>
          {responseHeaders.length > 0 && (
            <div className="rounded bg-gray-50 p-3">
              <h3 className="text-xs font-semibold text-gray-600">Headers</h3>
              <ul className="mt-2 space-y-1">
                {responseHeaders.map(([key, value]) => (
                  <li key={`${key}:${value}`} className="text-xs text-gray-700">
                    <span className="font-medium">{key}</span>: {value}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <pre className="max-h-80 overflow-auto rounded bg-gray-900 p-3 text-xs text-gray-100">
            {responseBody ?? "No response yet."}
          </pre>
        </div>
      </div>
    </section>
  );
}
