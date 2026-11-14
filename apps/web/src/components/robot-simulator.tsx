"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { LoaderCircle, Pause, Play, RotateCcw } from "lucide-react";
import type { Job } from "@/lib/types";
import { workspaceRequestHeaders } from "@/lib/local-workspace";
import "./robot-simulator.css";

type Camera = { azimuth: number; elevation: number; distance: number };
const defaultCamera: Camera = { azimuth: 135, elevation: -24, distance: 1.8 };

type Frame = { protocol: string; backend: string; model: string; q: number[]; tool_position_m: number[]; joint_limits_rad: number[][]; image_png_base64: string; width: number; height: number };

export function RobotSimulator({ visible, result, draft, evaluating, playJobId, onRunAndPlay }: { visible: boolean; result: Job | null; draft: string; evaluating: boolean; playJobId: string | null; onRunAndPlay: () => Promise<void> }) {
  const [frame, setFrame] = useState<Frame | null>(null);
  const [error, setError] = useState("");
  const [localDemoAvailable, setLocalDemoAvailable] = useState(false);
  const [busy, setBusy] = useState(false);
  const [index, setIndex] = useState(0);
  const [playing, setPlaying] = useState(false);
  const viewport = useRef<HTMLDivElement>(null);
  const desiredPose = useRef<number[] | undefined>(undefined);
  const camera = useRef<Camera>({ ...defaultCamera });
  const drag = useRef<{ id: number; x: number; y: number } | null>(null);
  const dirty = useRef(true);
  const halted = useRef(false);
  const visibleRef = useRef(visible);
  const consumedPlayJob = useRef<string | null>(null);
  visibleRef.current = visible;
  const preview = result?.status === "completed" && result.preview?.kind === "fr3-joint-trajectory-v1" ? result.preview : null;
  const trajectory = preview?.q;
  const stale = Boolean(preview && result?.code !== draft);

  // Controls only replace the desired state. The loop keeps one request in flight,
  // so fast drags never build a queue of obsolete native renders.
  const render = useCallback((q?: number[]) => {
    desiredPose.current = q; dirty.current = true; halted.current = false;
  }, []);
  const changeCamera = useCallback((next: Camera) => {
    camera.current = {
      azimuth: ((next.azimuth + 180) % 360 + 360) % 360 - 180,
      elevation: Math.max(-85, Math.min(85, next.elevation)),
      distance: Math.max(.5, Math.min(4, next.distance)),
    };
    dirty.current = true; halted.current = false;
  }, []);
  useEffect(() => {
    let active = true;
    const controller = new AbortController();
    dirty.current = true;
    async function stream() {
      while (active) {
        if (document.hidden || halted.current || (!visibleRef.current && !dirty.current)) {
          await new Promise(resolve => setTimeout(resolve, 100)); continue;
        }
        dirty.current = false;
        setBusy(true); setError(""); setLocalDemoAvailable(false);
        try {
          const response = await fetch("/api/simulator/fr3", {
            method: "POST", headers: { "Content-Type": "application/json", ...await workspaceRequestHeaders() },
            body: JSON.stringify({ q: desiredPose.current, camera: camera.current }),
            signal: AbortSignal.any([controller.signal, AbortSignal.timeout(35000)]),
          });
          const next = await response.json();
          if (active) setLocalDemoAvailable(!response.ok && next.code === "simulator_not_deployed");
          if (!response.ok) throw new Error(next.error || "Could not render this pose");
          if (next.protocol !== "joint-tonic.simulator.v1" || !Array.isArray(next.q) || next.q.length !== 7 || typeof next.image_png_base64 !== "string") throw new Error("Invalid simulator response");
          if (active) setFrame(next);
        } catch (cause) {
          if (active) { setError(cause instanceof Error ? cause.message : "Simulator connection failed"); setPlaying(false); halted.current = true; }
        } finally { if (active) setBusy(false); }
        await new Promise(resolve => setTimeout(resolve, 60));
      }
    }
    void stream();
    return () => { active = false; controller.abort(); };
  }, []);
  useEffect(() => {
    const element = viewport.current;
    if (!element) return;
    const zoom = (event: WheelEvent) => {
      event.preventDefault();
      const delta = event.deltaY * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? 300 : 1);
      changeCamera({ ...camera.current, distance: camera.current.distance * Math.exp(Math.max(-100, Math.min(100, delta)) * .002) });
    };
    element.addEventListener("wheel", zoom, { passive: false });
    return () => element.removeEventListener("wheel", zoom);
  }, [changeCamera]);
  useEffect(() => {
    setPlaying(false); setIndex(0);
    if (trajectory?.length) void render(trajectory[0]);
    else if (result) void render();
  }, [result?.id, trajectory, render]);
  useEffect(() => { if (!visible || stale || evaluating) setPlaying(false); }, [visible, stale, evaluating]);
  useEffect(() => {
    if (!playJobId || consumedPlayJob.current === playJobId) return;
    consumedPlayJob.current = playJobId;
    if (playJobId && playJobId === result?.id && trajectory && !stale && visible && !evaluating) {
      setIndex(0); render(trajectory[0]); setPlaying(true);
    }
  }, [playJobId, result?.id, trajectory, stale, visible, evaluating, render]);
  useEffect(() => {
    if (!playing || !visible || !trajectory || error) return;
    if (index >= trajectory.length - 1) { setPlaying(false); return; }
    const timer = setTimeout(() => { const next = index + 1; setIndex(next); void render(trajectory[next]); }, 150);
    return () => clearTimeout(timer);
  }, [playing, visible, index, trajectory, error, render]);

  return <div id="robot-simulation-panel" role="tabpanel" aria-labelledby="robot-simulation-tab" hidden={!visible} className="robot-simulator">
    <div className="robot-simulator-heading"><div><strong>Franka Research 3</strong><span>Live MuJoCo view · joint-space kinematics</span></div><button className="icon-button" type="button" aria-label="Reset robot to home" disabled={!frame && busy} onClick={() => { setPlaying(false); setIndex(0); void render(); }}><RotateCcw size={16} /></button></div>
    {error && <div className="error-banner" role="alert"><span>{error}</span><button className="button secondary small" onClick={() => void render(trajectory?.[index])}>Retry simulator</button></div>}
    {localDemoAvailable && <p className="robot-simulator-note"><a href="http://localhost:3000/problems/fr3-joint-interpolation">Open the local Franka demo</a> on the computer running Joint Tonic. No login is required for local practice.</p>}
    <div ref={viewport} className="robot-simulator-viewport" role="group" tabIndex={0} aria-label="Interactive MuJoCo camera" aria-describedby="robot-camera-help"
      onPointerDown={event => { if (!event.isPrimary || event.button !== 0) return; event.preventDefault(); event.currentTarget.focus(); event.currentTarget.setPointerCapture(event.pointerId); drag.current = { id: event.pointerId, x: event.clientX, y: event.clientY }; }}
      onPointerMove={event => { const previous = drag.current; if (!previous || previous.id !== event.pointerId) return; changeCamera({ ...camera.current, azimuth: camera.current.azimuth - (event.clientX - previous.x) * .5, elevation: camera.current.elevation - (event.clientY - previous.y) * .4 }); drag.current = { id: event.pointerId, x: event.clientX, y: event.clientY }; }}
      onPointerUp={event => { if (drag.current?.id === event.pointerId) { drag.current = null; if (event.currentTarget.hasPointerCapture(event.pointerId)) event.currentTarget.releasePointerCapture(event.pointerId); } }}
      onPointerCancel={() => { drag.current = null; }} onLostPointerCapture={() => { drag.current = null; }}
      onKeyDown={event => {
        const next = { ...camera.current };
        if (event.key === "ArrowLeft") next.azimuth -= 10;
        else if (event.key === "ArrowRight") next.azimuth += 10;
        else if (event.key === "ArrowUp") next.elevation += 5;
        else if (event.key === "ArrowDown") next.elevation -= 5;
        else if (event.key === "+" || event.key === "=") next.distance *= .85;
        else if (event.key === "-") next.distance /= .85;
        else if (event.key.toLowerCase() === "r") Object.assign(next, defaultCamera);
        else return;
        event.preventDefault(); changeCamera(next);
      }}>
      {frame ? <img draggable={false} src={`data:image/png;base64,${frame.image_png_base64}`} width={frame.width} height={frame.height} alt="MuJoCo rendering of the Franka Research 3 arm at the joint angles listed below" /> : <p role="status">{busy ? "Initializing the local MuJoCo model…" : "Robot view is unavailable."}</p>}
      {busy && !frame && <span className="robot-render-status" role="status"><LoaderCircle size={15} className="spin" /> {frame ? "Rendering pose…" : "Starting MuJoCo…"}</span>}
    </div>
    <div className="robot-camera-controls"><p id="robot-camera-help">Drag to orbit · scroll to zoom. Keyboard: arrows, +/−, R to reset.</p><div><button type="button" className="button secondary small" aria-label="Zoom camera in" onClick={() => changeCamera({ ...camera.current, distance: camera.current.distance * .85 })}>+</button><button type="button" className="button secondary small" aria-label="Zoom camera out" onClick={() => changeCamera({ ...camera.current, distance: camera.current.distance / .85 })}>−</button><button type="button" className="button secondary small" onClick={() => changeCamera({ ...defaultCamera })}>Reset camera</button></div></div>
    <div className="robot-playback"><button className="button secondary small" disabled={evaluating || (!playing && (!frame || Boolean(error)))} onClick={() => {
      if (playing) { setPlaying(false); return; }
      if (!trajectory || stale) { void onRunAndPlay(); return; }
      if (index >= trajectory.length - 1) { setIndex(0); render(trajectory[0]); }
      setPlaying(true);
    }}>{evaluating ? <LoaderCircle size={14} className="spin" /> : playing ? <Pause size={14} /> : <Play size={14} />}{evaluating ? "Running your code…" : playing ? "Pause" : !trajectory || stale ? "Run and play" : "Play your result"}</button>
      {trajectory && <label>Waypoint {index + 1} / {trajectory.length}<input type="range" aria-label="Trajectory waypoint" min={0} max={trajectory.length - 1} value={index} disabled={stale || evaluating} onChange={event => { const next = Number(event.target.value); setPlaying(false); setIndex(next); render(trajectory[next]); }} /></label>}
    </div>
    {trajectory ? <>
      <p className="robot-simulator-note">{stale ? "Your code has changed. Run and play will execute the current editor before replaying its output." : `Actual return value from your ${result?.mode === "submit" ? "submitted" : "Run"} code on the public inputs below.`}</p>
      <details className="robot-output"><summary>Function inputs and returned joint positions</summary><pre>{`interpolate_fr3_joints(\n  [0, 0, 0, -1.57079, 0, 1.57079, -0.7853],\n  [0.4, -0.3, 0.2, -1.8, 0.1, 1.9, -0.4],\n  41\n)\n\nReturned row ${index}:\n${JSON.stringify(trajectory[index])}`}</pre></details>
    </> : <p className="robot-simulator-note">Run and play calls your function in the isolated worker and sends its returned joint positions to MuJoCo.{result?.preview_error && ` Preview unavailable: ${result.preview_error}`}</p>}
    {frame && <><p className="robot-tool-position">Tool position in world (m): {frame.tool_position_m.map(value => value.toFixed(4)).join(", ")}</p><table className="robot-joint-table"><caption>Current arm joint angles (radians)</caption><thead><tr>{frame.q.map((_, i) => <th key={i} scope="col">J{i + 1}</th>)}</tr></thead><tbody><tr>{frame.q.map((value, i) => <td key={i}>{value.toFixed(3)}</td>)}</tr></tbody></table></>}
    <p className="robot-simulator-note">Kinematic pose replay, not a dynamics or collision-safety test. The live view follows your camera and trajectory; display timing is independent of physical execution speed.</p>
  </div>;
}
