// Project owner: Lukáš Dubšík; implementation review pending.
import type { State } from "./state";
import type { CandidateKey, Collection } from "../shared/types";

export const keyEqual = (
  left: CandidateKey | null,
  right: CandidateKey | null,
) =>
  left?.bundle_id === right?.bundle_id &&
  left?.candidate_id === right?.candidate_id;
export const revision = (state: State) =>
  state.workspace?.study.revisions.find(
    (item) => item.revision_id === state.revisionId,
  );
export const dirty = (state: State) =>
  !!state.workspace?.dirty || state.generation !== state.syncedGeneration;
export const unapplied = (state: State) =>
  state.buffers.target !== null || state.buffers.decision !== null;
export const collections = (state: State) =>
  state.workspace?.study.collections.filter(
    (item) => item.revision_id === state.revisionId,
  ) ?? [];
export const selectedCollection = (state: State) =>
  collections(state).find(
    (item) => item.collection_id === state.collectionId,
  ) ?? collections(state)[0];
export function unresolvedCount(items: Collection[]): number {
  return items.reduce(
    (count, item) =>
      count +
      (item.memberships.length
        ? item.memberships.filter(
            (member) =>
              member.disposition === "undecided" ||
              member.disposition === "needs_clarification" ||
              !member.rationale.trim(),
          ).length
        : 1),
    0,
  );
}
export function candidates(state: State) {
  return (
    state.workspace?.study.evidence
      .filter((item) => item.bundle.context.revision_id === state.revisionId)
      .flatMap((item) =>
        item.bundle.candidates.map((candidate) => ({
          candidate,
          bundle: item.bundle,
          key: {
            bundle_id: item.bundle.bundle_id,
            candidate_id: candidate.candidate_id,
          },
        })),
      ) ?? []
  );
}

export function draftProblems(
  state: State,
  draft: import("../shared/types").TargetDraft | null,
): import("../shared/types").Diagnostic[] {
  if (!draft) return [];
  const errors: import("../shared/types").Diagnostic[] = [];
  const add = (field: string, message: string) =>
    errors.push({
      code: "INTERVAL_INVALID",
      severity: "error",
      location: `/target/${field}`,
      message,
    });
  if (!draft.label.trim()) add("label", "Enter a target label.");
  const reference = state.catalogue?.references.find(
    (item) => item.reference_id === revision(state)?.reference_id,
  );
  const contig = reference?.contigs.find(
    (item) => item.accession === draft.contig,
  );
  if (!contig) add("contig", "Choose an exact supported contig accession.");
  for (const field of ["start", "end"] as const) {
    if (
      !/^[0-9]+$/.test(draft[field]) ||
      !Number.isSafeInteger(Number(draft[field]))
    )
      add(field, `Enter a nonnegative whole number for ${field}.`);
  }
  if (
    errors.every(
      (item) =>
        !item.location?.endsWith("/start") && !item.location?.endsWith("/end"),
    ) &&
    (Number(draft.start) >= Number(draft.end) ||
      (contig && Number(draft.end) > contig.length))
  )
    add(
      "end",
      `Require 0 ≤ start < end ≤ ${contig?.length.toLocaleString() ?? "contig length"} (end-exclusive).`,
    );
  return errors;
}
