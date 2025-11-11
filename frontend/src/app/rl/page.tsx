"use client";

import { useCallback, useEffect, useState } from "react";
import Link from "next/link";
import {
  listApis,
  ApiSummary,
  createGoal,
  startEpisode,
  getEpisode,
  getState,
  GoalResponse,
  EpisodeResponse,
  StateResponse,
} from "@/lib/api";

const DEFAULT_GOAL_STATE = JSON.stringify(
  {
    target_components: {
      example_component: [
        {
          id: "record-id-or-key",
          status: "approved",
        },
      ],
    },
  },
  null,
  2,
);

export default function RLWorkflowPage() {
  const [apiSlug, setApiSlug] = useState("");
  const [apis, setApis] = useState<ApiSummary[]>([]);
  const [isLoadingApis, setIsLoadingApis] = useState(false);
  const [apiListError, setApiListError] = useState<string | null>(null);

  const [goalDescription, setGoalDescription] = useState("");
  const [goalStateText, setGoalStateText] = useState(DEFAULT_GOAL_STATE);
  const [goal, setGoal] = useState<GoalResponse | null>(null);
  const [goalError, setGoalError] = useState<string | null>(null);
  const [isCreatingGoal, setIsCreatingGoal] = useState(false);

  const [episode, setEpisode] = useState<EpisodeResponse | null>(null);
  const [stateDetails, setStateDetails] = useState<StateResponse | null>(null);
  const [episodeError, setEpisodeError] = useState<string | null>(null);
  const [isStartingEpisode, setIsStartingEpisode] = useState(false);
  const [isRefreshingEpisode, setIsRefreshingEpisode] = useState(false);

  const loadApis = useCallback(async () => {
    try {
      setIsLoadingApis(true);
      setApiListError(null);
      const result = await listApis();
      setApis(result);
    } catch (err) {
      setApiListError(err instanceof Error ? err.message : "Unable to load APIs.");
    } finally {
      setIsLoadingApis(false);
    }
  }, []);

  useEffect(() => {
    void loadApis();
  }, [loadApis]);

  useEffect(() => {
    setGoal(null);
    setEpisode(null);
    setStateDetails(null);
    setGoalError(null);
    setEpisodeError(null);
  }, [apiSlug]);

  const selectedApi = apis.find((api) => api.api_slug === apiSlug);

  async function handleCreateGoal(e: React.FormEvent) {
    e.preventDefault();
    setGoalError(null);
    if (!apiSlug.trim()) {
      setGoalError("Select an API or provide a slug first.");
      return;
    }

    let parsedGoal: Record<string, unknown>;
    try {
      parsedGoal = JSON.parse(goalStateText);
    } catch (err) {
      setGoalError("Goal state JSON is invalid.");
      return;
    }

    try {
      setIsCreatingGoal(true);
      const response = await createGoal({
        api_slug: apiSlug.trim(),
        goal_state: parsedGoal,
        description: goalDescription.trim() || undefined,
      });
      setGoal(response);
      setEpisode(null);
      setStateDetails(null);
    } catch (err) {
      setGoalError(err instanceof Error ? err.message : "Failed to create goal.");
    } finally {
      setIsCreatingGoal(false);
    }
  }

  async function loadState(stateId: string) {
    try {
      const state = await getState(stateId);
      setStateDetails(state);
      setEpisodeError(null);
    } catch (err) {
      setEpisodeError(err instanceof Error ? err.message : "Failed to load state snapshot.");
    }
  }

  async function handleStartEpisode() {
    if (!goal) {
      setEpisodeError("Create a goal first.");
      return;
    }

    try {
      setIsStartingEpisode(true);
      const started = await startEpisode(goal.goal_id);
      setEpisode(started);
      await loadState(started.current_state_id);
    } catch (err) {
      setEpisodeError(err instanceof Error ? err.message : "Failed to start episode.");
    } finally {
      setIsStartingEpisode(false);
    }
  }

  async function refreshEpisode() {
    if (!episode) return;
    try {
      setIsRefreshingEpisode(true);
      const latest = await getEpisode(episode.episode_id);
      setEpisode(latest);
      await loadState(latest.current_state_id);
    } catch (err) {
      setEpisodeError(err instanceof Error ? err.message : "Unable to refresh episode.");
    } finally {
      setIsRefreshingEpisode(false);
    }
  }

  return (
    <main className="mx-auto max-w-5xl p-8 space-y-8">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h1 className="text-2xl font-semibold">RL Workflow Lab</h1>
          <p className="text-sm text-gray-600">Pick an existing API → define goal → start an episode, all from one screen.</p>
        </div>
        <div className="flex gap-3 text-sm">
          <Link href="/" className="text-blue-600 hover:underline">
            Dashboard
          </Link>
          <span className="text-gray-300">|</span>
          <Link href="/upload" className="text-blue-600 hover:underline">
            Upload new API
          </Link>
        </div>
      </div>

      <section className="rounded-lg border bg-white p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-medium">Step 1 · Choose an API</h2>
          <span className="text-xs uppercase tracking-wide text-gray-500">
            {apiSlug ? "API selected" : "Select to continue"}
          </span>
        </div>
        <div className="space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Available APIs</label>
            <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
              <select
                value={selectedApi ? selectedApi.api_slug : ""}
                onChange={(e) => setApiSlug(e.target.value)}
                className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-300"
              >
                <option value="">Select from registry</option>
                {apis.map((api) => (
                  <option key={api.api_slug} value={api.api_slug}>
                    {api.api_name || api.title || api.api_slug} ({api.api_slug})
                  </option>
                ))}
              </select>
              <button
                type="button"
                onClick={() => void loadApis()}
                className="rounded border px-3 py-2 text-sm hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-60"
                disabled={isLoadingApis}
              >
                {isLoadingApis ? "Refreshing..." : "Refresh list"}
              </button>
            </div>
            {apiListError && <p className="text-sm text-red-700">{apiListError}</p>}
            {!apiListError && apis.length === 0 && !isLoadingApis && (
              <p className="text-sm text-gray-500">No APIs found. Upload an API from the dashboard first.</p>
            )}
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">Or paste a slug manually</label>
            <input
              className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-300"
              value={apiSlug}
              onChange={(e) => setApiSlug(e.target.value)}
              placeholder="e.g., petstore"
            />
          </div>
          {selectedApi && (
            <div className="rounded border bg-gray-50 p-4 text-sm">
              <p className="font-medium">{selectedApi.api_name || selectedApi.title || selectedApi.api_slug}</p>
              <dl className="mt-2 grid gap-2 sm:grid-cols-2">
                <div>
                  <dt className="text-gray-500">Slug</dt>
                  <dd className="font-mono text-xs sm:text-sm">{selectedApi.api_slug}</dd>
                </div>
                <div>
                  <dt className="text-gray-500">Version</dt>
                  <dd>{selectedApi.version || "n/a"}</dd>
                </div>
                <div className="sm:col-span-2">
                  <dt className="text-gray-500">Registered</dt>
                  <dd>{new Date(selectedApi.created_at).toLocaleString()}</dd>
                </div>
              </dl>
            </div>
          )}
        </div>
      </section>

      <section className="rounded-lg border bg-white p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-medium">Step 2 · Define a Goal</h2>
          <span className="text-xs uppercase tracking-wide text-gray-500">
            {goal ? "Goal ready" : apiSlug ? "Waiting on you" : "Needs API slug"}
          </span>
        </div>
        <form className="space-y-4" onSubmit={handleCreateGoal}>
          <div className="space-y-2">
            <label className="text-sm font-medium">Goal description</label>
            <input
              className="w-full rounded border px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-300"
              value={goalDescription}
              onChange={(e) => setGoalDescription(e.target.value)}
              placeholder="e.g., Reach state with approved example_component"
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium flex items-center justify-between">
              <span>Goal state JSON</span>
              <button
                type="button"
                className="text-xs text-purple-700 hover:underline"
                onClick={() => setGoalStateText(DEFAULT_GOAL_STATE)}
              >
                Reset template
              </button>
            </label>
            <textarea
              className="min-h-[180px] w-full rounded border px-3 py-2 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-purple-300"
              value={goalStateText}
              onChange={(e) => setGoalStateText(e.target.value)}
            />
            <p className="text-xs text-gray-500">
              The payload is passed directly to <code>/rl/goals</code>. Use{" "}
              <code>{`{"target_components": {...}}`}</code> or <code>{"{ \"target_conditions\": [...] }"}</code>.
            </p>
          </div>
          <div>
            <button
              type="submit"
              className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60 focus:outline-none focus:ring-2 focus:ring-blue-300"
              disabled={isCreatingGoal || !apiSlug.trim()}
            >
              {isCreatingGoal ? "Creating..." : "Create goal"}
            </button>
          </div>
          <div className="min-h-[20px] text-sm">
            {goal && (
              <p className="text-green-700">
                Goal <span className="font-mono">{goal.goal_id}</span> ready. Start state:{" "}
                <span className="font-mono">{goal.start_state_id}</span>
              </p>
            )}
            {goalError && <p className="text-red-700">{goalError}</p>}
          </div>
        </form>
      </section>

      <section className="rounded-lg border bg-white p-6 shadow-sm space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-medium">Step 3 · Run & Monitor an Episode</h2>
          <span className="text-xs uppercase tracking-wide text-gray-500">
            {episode ? (episode.done ? "Episode finished" : "Episode running") : "Waiting on goal"}
          </span>
        </div>
        <div className="flex flex-wrap gap-3">
          <button
            type="button"
            disabled={!goal || isStartingEpisode}
            onClick={handleStartEpisode}
            className="rounded bg-green-600 px-4 py-2 text-white hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-60 focus:outline-none focus:ring-2 focus:ring-green-300"
          >
            {isStartingEpisode ? "Starting..." : "Start new episode"}
          </button>
          <button
            type="button"
            disabled={!episode || isRefreshingEpisode}
            onClick={refreshEpisode}
            className="rounded border px-4 py-2 text-sm hover:bg-gray-50 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {isRefreshingEpisode ? "Refreshing..." : "Refresh snapshot"}
          </button>
        </div>
        {episodeError && <p className="text-sm text-red-700">{episodeError}</p>}
        {episode && (
          <div className="space-y-4">
            <div className="grid gap-3 rounded border bg-gray-50 p-4 text-sm sm:grid-cols-2">
              <div>
                <p className="text-gray-500">Episode</p>
                <p className="font-mono">{episode.episode_id}</p>
              </div>
              <div>
                <p className="text-gray-500">Current state</p>
                <p className="font-mono">{episode.current_state_id}</p>
              </div>
              <div>
                <p className="text-gray-500">Reward</p>
                <p>{episode.reward.toFixed(3)}</p>
              </div>
              <div>
                <p className="text-gray-500">Status</p>
                <p>{episode.done ? "Done" : "Active"}</p>
              </div>
            </div>
            <div>
              <p className="text-sm font-medium">Action history</p>
              {episode.action_history.length === 0 ? (
                <p className="text-sm text-gray-600">No actions recorded yet. Invoke generated routes or use the RL API.</p>
              ) : (
                <ul className="mt-2 list-inside list-decimal text-sm font-mono text-gray-700">
                  {episode.action_history.map((actionId) => (
                    <li key={actionId}>{actionId}</li>
                  ))}
                </ul>
              )}
            </div>
            {stateDetails && (
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <p className="text-sm font-medium">State snapshot</p>
                  <p className="text-xs text-gray-500">
                    Created {new Date(stateDetails.created_at).toLocaleString()}
                  </p>
                </div>
                <pre className="max-h-[360px] overflow-auto rounded bg-black p-4 text-xs text-green-200">
                  {JSON.stringify(stateDetails.modified_components, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </section>
    </main>
  );
}
