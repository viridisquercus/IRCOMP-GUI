// Project owner: Lukáš Dubšík; implementation review pending.
import type {
  CandidateKey,
  Catalogue,
  Diagnostic,
  DraftBuffers,
  ExportPreview,
  ImportPreview,
  StudySummary,
  Validation,
  Workspace,
} from "../shared/types";

export type State = {
  workspace: Workspace | null;
  catalogue: Catalogue | null;
  studies: StudySummary[];
  view: "prepare" | "review" | "export";
  revisionId: string;
  targetId: string | null;
  candidate: CandidateKey | null;
  collectionId: string;
  buffers: DraftBuffers;
  generation: number;
  syncedGeneration: number;
  busy: boolean;
  status: string;
  error: { code: string; message: string; diagnostics: Diagnostic[] } | null;
  importPreview: ImportPreview | null;
  exportPreview: ExportPreview | null;
  validation: Validation | null;
  fields: Record<string, string>;
  exportKind: "request" | "review";
  selectedCollections: string[];
};

export const initialState: State = {
  workspace: null,
  catalogue: null,
  studies: [],
  view: "prepare",
  revisionId: "",
  targetId: null,
  candidate: null,
  collectionId: "",
  buffers: { target: null, decision: null },
  generation: 0,
  syncedGeneration: 0,
  busy: false,
  status: "",
  error: null,
  importPreview: null,
  exportPreview: null,
  validation: null,
  fields: {},
  exportKind: "request",
  selectedCollections: [],
};
export type Action =
  | { type: "patch"; value: Partial<State> }
  | { type: "field"; name: string; value: string }
  | { type: "draft"; buffers: DraftBuffers }
  | {
      type: "received";
      workspace: Workspace;
      generation: number;
      opening?: boolean;
    };

export function reducer(state: State, action: Action): State {
  if (action.type === "patch") return { ...state, ...action.value };
  if (action.type === "field")
    return {
      ...state,
      fields: { ...state.fields, [action.name]: action.value },
    };
  if (
    action.type === "draft" &&
    JSON.stringify(action.buffers) === JSON.stringify(state.buffers)
  )
    return state;
  if (action.type === "draft")
    return {
      ...state,
      buffers: action.buffers,
      generation: state.generation + 1,
      error: null,
      exportPreview: null,
      validation: null,
    };
  const workspace = action.workspace;
  const opening = action.opening ?? false;
  const sameGeneration = opening || state.generation === action.generation;
  const revisionId =
    opening ||
    !workspace.study.revisions.some(
      (item) => item.revision_id === state.revisionId,
    ) ||
    state.revisionId === state.workspace?.study.active_revision_id
      ? workspace.study.active_revision_id
      : state.revisionId;
  return {
    ...state,
    workspace,
    revisionId,
    buffers: sameGeneration ? workspace.study.draft_buffers : state.buffers,
    syncedGeneration: sameGeneration
      ? state.generation
      : state.syncedGeneration,
    targetId: opening ? null : state.targetId,
    candidate: opening ? null : state.candidate,
    collectionId: opening ? "" : state.collectionId,
    error: null,
    validation: null,
    exportPreview: null,
    importPreview: opening ? null : state.importPreview,
    fields: opening ? {} : state.fields,
  };
}
