"use client";

import { useState } from "react";
import { Check, Pencil, X } from "lucide-react";

type Props = {
    label: string;
    value: string;
    placeholder?: string;
    onSave: (next: string) => Promise<void> | void;
};

export default function EditableField({ label, value, placeholder, onSave }: Props) {
    const [editing, setEditing] = useState(false);
    const [draft, setDraft] = useState(value);
    const [busy, setBusy] = useState(false);

    return (
        <div className="flex items-start justify-between gap-6 py-5 border-b border-white/10">
            <div className="min-w-0">
                <div className="text-sm text-white/60">{label}</div>

                {!editing ? (
                    <div className="mt-2 text-lg text-white/90 truncate">{value || "—"}</div>
                ) : (
                    <input
                        value={draft}
                        onChange={(e) => setDraft(e.target.value)}
                        placeholder={placeholder}
                        className="mt-2 w-full bg-transparent text-lg outline-none text-white/90"
                        autoFocus
                    />
                )}
            </div>

            {!editing ? (
                <button
                    onClick={() => {
                        setDraft(value);
                        setEditing(true);
                    }}
                    className="h-10 w-10 rounded-full border border-white/15 hover:bg-white/5 flex items-center justify-center"
                    aria-label={`Edit ${label}`}
                >
                    <Pencil className="h-4 w-4" />
                </button>
            ) : (
                <div className="flex gap-2">
                    <button
                        disabled={busy}
                        onClick={() => {
                            setEditing(false);
                            setDraft(value);
                        }}
                        className="h-10 w-10 rounded-full border border-white/15 hover:bg-white/5 flex items-center justify-center disabled:opacity-50"
                        aria-label="Cancel"
                    >
                        <X className="h-4 w-4" />
                    </button>

                    <button
                        disabled={busy}
                        onClick={async () => {
                            setBusy(true);
                            try {
                                await onSave(draft.trim());
                                setEditing(false);
                            } finally {
                                setBusy(false);
                            }
                        }}
                        className="h-10 w-10 rounded-full bg-white text-black hover:bg-white/90 flex items-center justify-center disabled:opacity-50"
                        aria-label="Save"
                    >
                        <Check className="h-4 w-4" />
                    </button>
                </div>
            )}
        </div>
    );
}
