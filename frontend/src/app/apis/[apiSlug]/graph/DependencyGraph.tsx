"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import type { PointerEvent as ReactPointerEvent, WheelEvent as ReactWheelEvent } from "react";
import type { ComponentGraph } from "@/lib/api";

type Props = {
  apiSlug: string;
  graph: ComponentGraph;
};

type PositionedNode = {
  name: string;
  x: number;
  y: number;
  level: number;
};

const SVG_WIDTH = 960;
const BASE_HEIGHT = 520;
const MIN_SCALE = 0.6;
const MAX_SCALE = 2.6;
const ZOOM_STEP = 1.18;

export default function DependencyGraph({ graph, apiSlug }: Props) {
  const [focused, setFocused] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [view, setView] = useState({ x: 0, y: 0, scale: 1 });
  const [isPanning, setIsPanning] = useState(false);
  const svgRef = useRef<SVGSVGElement | null>(null);
  const panState = useRef<{
    pointerId: number | null;
    originX: number;
    originY: number;
    startX: number;
    startY: number;
  }>({ pointerId: null, originX: 0, originY: 0, startX: 0, startY: 0 });

  const layout = useMemo(() => computeLayout(graph), [graph]);
  const nodesByName = useMemo(() => {
    const lookup = new Map<string, PositionedNode>();
    layout.nodes.forEach((node) => lookup.set(node.name, node));
    return lookup;
  }, [layout.nodes]);
  const graphNodesByName = useMemo(() => {
    const lookup = new Map<string, ComponentGraph["nodes"][number]>();
    graph.nodes.forEach((node) => lookup.set(node.component_name, node));
    return lookup;
  }, [graph.nodes]);

  const normalizedQuery = search.trim().toLowerCase();

  useEffect(() => {
    setFocused(null);
    setSearch("");
    setView({ x: 0, y: 0, scale: 1 });
  }, [apiSlug]);

  const visibleNames = useMemo(() => {
    if (!normalizedQuery) {
      return new Set(layout.nodes.map((node) => node.name));
    }
    const matches = new Set<string>();
    graph.nodes.forEach((node) => {
      if (node.component_name.toLowerCase().includes(normalizedQuery)) {
        matches.add(node.component_name);
        node.references.forEach((ref) => matches.add(ref));
      }
    });
    graph.edges.forEach(({ source, target }) => {
      if (matches.has(source) || matches.has(target)) {
        matches.add(source);
        matches.add(target);
      }
    });
    if (matches.size === 0) {
      return new Set(layout.nodes.map((node) => node.name));
    }
    return matches;
  }, [graph.edges, graph.nodes, layout.nodes, normalizedQuery]);

  useEffect(() => {
    if (focused && !visibleNames.has(focused)) {
      setFocused(null);
    }
  }, [focused, visibleNames]);

  const visibleLayoutNodes = useMemo(() => layout.nodes.filter((node) => visibleNames.has(node.name)), [layout.nodes, visibleNames]);

  const visibleEdges = useMemo(
    () => graph.edges.filter((edge) => visibleNames.has(edge.source) && visibleNames.has(edge.target)),
    [graph.edges, visibleNames]
  );

  const focusedNode = focused ? graph.nodes.find((n) => n.component_name === focused) ?? null : null;

  const highlightedTargets = useMemo(() => {
    const targets = new Set<string>();
    if (focusedNode) {
      focusedNode.references.forEach((ref) => {
        if (visibleNames.has(ref)) targets.add(ref);
      });
    }
    return targets;
  }, [focusedNode, visibleNames]);

  const highlightedSources = useMemo(() => {
    const sources = new Set<string>();
    if (focusedNode) {
      graph.edges.forEach((edge) => {
        if (edge.target === focusedNode.component_name && visibleNames.has(edge.source)) {
          sources.add(edge.source);
        }
      });
    }
    return sources;
  }, [focusedNode, graph.edges, visibleNames]);

  const adjustScale = useCallback(
    (factor: number, anchor?: { x: number; y: number }) => {
      setView((prev) => {
        const nextScale = clamp(prev.scale * factor, MIN_SCALE, MAX_SCALE);
        if (nextScale === prev.scale) return prev;
        const anchorX = anchor?.x ?? SVG_WIDTH / 2;
        const anchorY = anchor?.y ?? layout.height / 2;
        const ratio = nextScale / prev.scale;
        const nextX = anchorX - ratio * (anchorX - prev.x);
        const nextY = anchorY - ratio * (anchorY - prev.y);
        return { x: nextX, y: nextY, scale: nextScale };
      });
    },
    [layout.height]
  );

  const handleWheel = useCallback(
    (event: ReactWheelEvent<SVGSVGElement>) => {
      if (!event.ctrlKey && !event.metaKey) {
        return;
      }
      event.preventDefault();
      const rect = svgRef.current?.getBoundingClientRect();
      if (!rect) return;
      const anchor = {
        x: event.clientX - rect.left,
        y: event.clientY - rect.top,
      };
      adjustScale(event.deltaY < 0 ? 1.1 : 1 / 1.1, anchor);
    },
    [adjustScale]
  );

  const endPan = useCallback(
    (event: ReactPointerEvent<SVGSVGElement>) => {
      if (panState.current.pointerId !== event.pointerId) return;
      setIsPanning(false);
      svgRef.current?.releasePointerCapture(event.pointerId);
      panState.current.pointerId = null;
    },
    []
  );

  const handlePointerDown = useCallback(
    (event: ReactPointerEvent<SVGSVGElement>) => {
      if (event.button !== 0) return;
      if (event.target !== svgRef.current && !event.altKey) return;
      event.preventDefault();
      panState.current = {
        pointerId: event.pointerId,
        originX: event.clientX,
        originY: event.clientY,
        startX: view.x,
        startY: view.y,
      };
      setIsPanning(true);
      svgRef.current?.setPointerCapture(event.pointerId);
    },
    [view.x, view.y]
  );

  const handlePointerMove = useCallback((event: ReactPointerEvent<SVGSVGElement>) => {
    if (!isPanning || panState.current.pointerId !== event.pointerId) return;
    event.preventDefault();
    const dx = event.clientX - panState.current.originX;
    const dy = event.clientY - panState.current.originY;
    setView((prev) => ({
      ...prev,
      x: panState.current.startX + dx,
      y: panState.current.startY + dy,
    }));
  }, [isPanning]);

  const handleResetView = useCallback(() => {
    setView({ x: 0, y: 0, scale: 1 });
  }, []);

  return (
    <section className="grid gap-6 lg:grid-cols-[2fr,1fr]">
      <div className="rounded border bg-white shadow">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 bg-slate-50 px-4 py-3">
          <label className="flex items-center gap-2 text-xs font-medium text-slate-600">
            <span>Filter</span>
            <input
              value={search}
              onChange={(event) => setSearch(event.target.value)}
              placeholder="Component name…"
              className="w-44 rounded border border-slate-300 bg-white px-2 py-1 text-xs font-normal text-slate-700 shadow-inner focus:border-blue-500 focus:outline-none"
              type="search"
            />
          </label>
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
            <div className="flex items-center gap-1 rounded border border-slate-300 bg-white p-1 shadow-sm">
              <button
                type="button"
                onClick={() => adjustScale(1 / ZOOM_STEP)}
                className="rounded px-2 py-1 font-semibold text-slate-600 transition hover:bg-blue-50 hover:text-blue-600"
                aria-label="Zoom out"
              >
                −
              </button>
              <button
                type="button"
                onClick={() => adjustScale(ZOOM_STEP)}
                className="rounded px-2 py-1 font-semibold text-slate-600 transition hover:bg-blue-50 hover:text-blue-600"
                aria-label="Zoom in"
              >
                +
              </button>
            </div>
            <button
              type="button"
              onClick={handleResetView}
              className="rounded border border-slate-300 bg-white px-3 py-1 font-semibold text-slate-600 shadow-sm transition hover:border-blue-500 hover:text-blue-600"
            >
              Reset view
            </button>
            <span className="hidden sm:block">
              Showing {visibleLayoutNodes.length} of {graph.nodes.length}
            </span>
          </div>
        </div>

        <div className="relative overflow-auto">
          <svg
            ref={svgRef}
            width={SVG_WIDTH}
            height={layout.height}
            viewBox={`0 0 ${SVG_WIDTH} ${layout.height}`}
            className="block w-full select-none"
            onWheel={handleWheel}
            onPointerDown={handlePointerDown}
            onPointerMove={handlePointerMove}
            onPointerUp={endPan}
            onPointerLeave={endPan}
            onPointerCancel={endPan}
            onMouseLeave={() => setFocused(null)}
            style={{ cursor: isPanning ? "grabbing" : undefined }}
            aria-label="Component dependency graph"
          >
            <defs>
              <marker
                id="arrowhead"
                viewBox="0 0 10 10"
                refX="10"
                refY="5"
                markerWidth="8"
                markerHeight="8"
                orient="auto-start-reverse"
              >
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#94a3b8" />
              </marker>
            </defs>

            <g transform={`translate(${view.x} ${view.y}) scale(${view.scale})`}>
              {visibleEdges.map((edge) => {
                const source = nodesByName.get(edge.source);
                const target = nodesByName.get(edge.target);
                if (!source || !target) return null;
                const isHighlighted =
                  focusedNode &&
                  (edge.source === focusedNode.component_name || edge.target === focusedNode.component_name);
                const stroke = isHighlighted ? "#1d4ed8" : "#cbd5f5";
                const opacity =
                  focusedNode || normalizedQuery.length > 0
                    ? isHighlighted
                      ? 0.9
                      : 0.18
                    : 0.65;
                return (
                  <line
                    key={`${edge.source}->${edge.target}`}
                    x1={source.x}
                    y1={source.y}
                    x2={target.x}
                    y2={target.y}
                    stroke={stroke}
                    strokeWidth={isHighlighted ? 2.4 : 1.2}
                    markerEnd="url(#arrowhead)"
                    opacity={opacity}
                  />
                );
              })}
              {visibleLayoutNodes.map((layoutNode) => {
                const positioned = nodesByName.get(layoutNode.name);
                const graphNode = graphNodesByName.get(layoutNode.name);
                if (!positioned || !graphNode) return null;
                const isFocused = focusedNode?.component_name === graphNode.component_name;
                const isUpstream = highlightedTargets.has(graphNode.component_name);
                const isDownstream = highlightedSources.has(graphNode.component_name);
                const isMatch =
                  normalizedQuery.length > 0 && graphNode.component_name.toLowerCase().includes(normalizedQuery);
                const baseFill = isFocused
                  ? "#1d4ed8"
                  : isMatch
                    ? "#0ea5e9"
                    : isUpstream
                      ? "#2563eb"
                      : isDownstream
                        ? "#7c3aed"
                        : "#0f172a";
                const label = graphNode.component_name;
                const showLabel = isFocused || isMatch || layout.radius > 20;
                const dimmed =
                  normalizedQuery.length > 0 && !isFocused && !isMatch && !isUpstream && !isDownstream;

                return (
                  <g
                    key={graphNode.component_name}
                    transform={`translate(${positioned.x}, ${positioned.y})`}
                    onMouseEnter={() => setFocused(graphNode.component_name)}
                    onFocus={() => setFocused(graphNode.component_name)}
                    onBlur={() => setFocused(null)}
                    tabIndex={0}
                    role="button"
                    aria-label={`View relationships for ${label}`}
                    className="outline-none"
                  >
                    <title>{label}</title>
                    <circle
                      r={layout.radius}
                      fill={baseFill}
                      className="transition-all duration-150"
                      stroke={isFocused ? "#dbeafe" : "white"}
                      strokeWidth={isFocused ? 3 : 1.5}
                      opacity={dimmed ? 0.35 : 1}
                      style={{ cursor: "pointer" }}
                    />
                    {showLabel ? (
                      <text
                        x={0}
                        y={0}
                        textAnchor="middle"
                        alignmentBaseline="central"
                        fill="#f8fafc"
                        fontSize={Math.max(11, layout.radius * (showLabel ? 0.72 : 0.6))}
                        pointerEvents="none"
                      >
                        {label.length > 16 ? `${label.slice(0, 14)}…` : label}
                      </text>
                    ) : null}
                  </g>
                );
              })}
            </g>
          </svg>
        </div>
      </div>

      <aside className="space-y-4 rounded border bg-white p-4 shadow">
        <div>
          <h2 className="text-lg font-semibold">Details</h2>
          <p className="text-sm text-gray-600">
            Hover or focus nodes to explore dependencies. Hold <span className="font-semibold">Alt</span> and drag to
            pan, pinch or use the buttons to zoom.
          </p>
        </div>

        {focusedNode ? (
          <div className="space-y-3">
            <div>
              <div className="text-sm font-medium text-gray-500">Component</div>
              <div className="font-semibold">{focusedNode.component_name}</div>
            </div>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <div>
                <div className="text-gray-500">Storage key</div>
                <div className="font-mono text-xs break-all">{focusedNode.storage_key}</div>
              </div>
              <div>
                <div className="text-gray-500">Properties</div>
                <div>{focusedNode.property_count}</div>
              </div>
              <div>
                <div className="text-gray-500">Referencing</div>
                <div>{focusedNode.references.length}</div>
              </div>
              <div>
                <div className="text-gray-500">Referenced by</div>
                <div>{focusedNode.dependent_count}</div>
              </div>
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">Depends on</div>
              {focusedNode.references.length === 0 ? (
                <p className="text-sm text-gray-600">No downstream component references.</p>
              ) : (
                <ul className="list-disc pl-4 text-sm text-blue-700">
                  {focusedNode.references.map((ref) => (
                    <li key={ref}>{ref}</li>
                  ))}
                </ul>
              )}
            </div>
            <div>
              <div className="text-sm font-medium text-gray-500">Referenced by</div>
              {graph.edges.filter((edge) => edge.target === focusedNode.component_name).length === 0 ? (
                <p className="text-sm text-gray-600">No upstream references.</p>
              ) : (
                <ul className="list-disc pl-4 text-sm text-purple-700">
                  {graph.edges
                    .filter((edge) => edge.target === focusedNode.component_name)
                    .map((edge) => edge.source)
                    .filter((value, index, arr) => arr.indexOf(value) === index)
                    .map((source) => (
                      <li key={source}>{source}</li>
                    ))}
                </ul>
              )}
            </div>
          </div>
        ) : (
          <div className="rounded border border-dashed p-4 text-sm text-gray-600">
            Hover a node to inspect dependencies, or tap on touch devices.
          </div>
        )}

        <div className="text-xs text-gray-500">
          Data sourced live from <code className="font-mono">{apiSlug}</code> ({graph.nodes.length} components, {graph.edges.length} links).
        </div>
      </aside>
    </section>
  );
}

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function computeLayout(graph: ComponentGraph): { nodes: PositionedNode[]; height: number; radius: number } {
  if (graph.nodes.length === 0) {
    return { nodes: [], height: BASE_HEIGHT, radius: 26 };
  }

  const adjacency = new Map<string, string[]>();
  const indegree = new Map<string, number>();
  graph.nodes.forEach((node) => {
    adjacency.set(node.component_name, []);
    indegree.set(node.component_name, 0);
  });

  graph.edges.forEach((edge) => {
    const list = adjacency.get(edge.source);
    if (list) list.push(edge.target);
    indegree.set(edge.target, (indegree.get(edge.target) ?? 0) + 1);
  });

  const queue: string[] = [];
  indegree.forEach((value, key) => {
    if (value === 0) queue.push(key);
  });

  const level = new Map<string, number>();
  queue.forEach((name) => level.set(name, 0));

  while (queue.length > 0) {
    const current = queue.shift()!;
    const currentLevel = level.get(current) ?? 0;
    (adjacency.get(current) ?? []).forEach((target) => {
      const proposed = currentLevel + 1;
      if ((level.get(target) ?? -1) < proposed) {
        level.set(target, proposed);
      }
      const incoming = (indegree.get(target) ?? 0) - 1;
      indegree.set(target, incoming);
      if (incoming === 0) {
        queue.push(target);
      }
    });
  }

  const fallbackLevel = Math.max(0, ...Array.from(level.values()));
  graph.nodes.forEach((node) => {
    if (!level.has(node.component_name)) {
      level.set(node.component_name, fallbackLevel);
    }
  });

  const groups = new Map<number, string[]>();
  level.forEach((lvl, name) => {
    const bucket = groups.get(lvl) ?? [];
    bucket.push(name);
    groups.set(lvl, bucket);
  });

  const maxLevel = Math.max(...groups.keys());
  const height = Math.max(BASE_HEIGHT, (maxLevel + 1) * 180);
  const nodeRadius = Math.max(16, Math.min(34, 420 / Math.max(graph.nodes.length, 8)));

  const positioned: PositionedNode[] = [];
  groups.forEach((names, lvl) => {
    const y = ((lvl + 1) * height) / (maxLevel + 2);
    const sortedNames = [...names].sort((a, b) => a.localeCompare(b));
    const spacing = SVG_WIDTH / (sortedNames.length + 1);
    sortedNames.forEach((name, idx) => {
      const x = spacing * (idx + 1);
      positioned.push({ name, x, y, level: lvl });
    });
  });

  return { nodes: positioned, height, radius: nodeRadius };
}
