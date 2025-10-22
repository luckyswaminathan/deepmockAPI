"use client";

import { useMemo, useState } from "react";
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

export default function DependencyGraph({ graph, apiSlug }: Props) {
  const [focused, setFocused] = useState<string | null>(null);

  const layout = useMemo(() => computeLayout(graph), [graph]);
  const nodesByName = useMemo(() => {
    const lookup = new Map<string, PositionedNode>();
    layout.nodes.forEach((node) => lookup.set(node.name, node));
    return lookup;
  }, [layout.nodes]);

  const focusedNode = focused ? graph.nodes.find((n) => n.component_name === focused) ?? null : null;
  const highlightedTargets = new Set<string>();
  const highlightedSources = new Set<string>();

  if (focusedNode) {
    focusedNode.references.forEach((ref) => highlightedTargets.add(ref));
    graph.edges.forEach((edge) => {
      if (edge.target === focusedNode.component_name) highlightedSources.add(edge.source);
    });
  }

  return (
    <section className="grid gap-6 lg:grid-cols-[2fr,1fr]">
      <div className="overflow-auto rounded border bg-white shadow">
        <svg
          width={SVG_WIDTH}
          height={layout.height}
          viewBox={`0 0 ${SVG_WIDTH} ${layout.height}`}
          className="block w-full"
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

          {graph.edges.map((edge) => {
            const source = nodesByName.get(edge.source);
            const target = nodesByName.get(edge.target);
            if (!source || !target) return null;
            const isHighlighted =
              focusedNode &&
              (edge.source === focusedNode.component_name || edge.target === focusedNode.component_name);
            return (
              <line
                key={`${edge.source}->${edge.target}`}
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                stroke={isHighlighted ? "#1d4ed8" : "#cbd5f5"}
                strokeWidth={isHighlighted ? 2.5 : 1.4}
                markerEnd="url(#arrowhead)"
                opacity={focusedNode && !isHighlighted ? 0.25 : 0.9}
              />
            );
          })}

          {graph.nodes.map((node) => {
            const positioned = nodesByName.get(node.component_name);
            if (!positioned) return null;
            const isFocused = focusedNode?.component_name === node.component_name;
            const isUpstream = highlightedTargets.has(node.component_name);
            const isDownstream = highlightedSources.has(node.component_name);
            const baseFill = isFocused ? "#1d4ed8" : isUpstream ? "#2563eb" : isDownstream ? "#7c3aed" : "#0f172a";
            const label = node.component_name;
            return (
              <g
                key={node.component_name}
                transform={`translate(${positioned.x}, ${positioned.y})`}
                onMouseEnter={() => setFocused(node.component_name)}
                onMouseLeave={() => setFocused(null)}
                onFocus={() => setFocused(node.component_name)}
                onBlur={() => setFocused(null)}
                tabIndex={0}
                role="button"
                aria-label={`View relationships for ${label}`}
              >
                <circle
                  r={layout.radius}
                  fill={baseFill}
                  className="transition-all duration-150"
                  stroke={isFocused ? "#dbeafe" : "white"}
                  strokeWidth={isFocused ? 3 : 1.5}
                />
                <text
                  x={0}
                  y={0}
                  textAnchor="middle"
                  alignmentBaseline="central"
                  fill="#f8fafc"
                  fontSize={Math.max(11, layout.radius * 0.7)}
                  pointerEvents="none"
                >
                  {label.length > 14 ? `${label.slice(0, 12)}…` : label}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      <aside className="space-y-4 rounded border bg-white p-4 shadow">
        <div>
          <h2 className="text-lg font-semibold">Details</h2>
          <p className="text-sm text-gray-600">Hover nodes to explore dependencies.</p>
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
