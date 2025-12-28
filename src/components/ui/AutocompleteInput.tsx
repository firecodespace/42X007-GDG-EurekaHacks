"use client";

import { useEffect, useMemo, useRef, useState } from "react";

type Props = {
    label: string;
    placeholder?: string;
    value: string;
    onChange: (next: string) => void;
    options: string[];
    showUnderline?: boolean;
};

export default function AutocompleteInput({
    label,
    placeholder,
    value,
    onChange,
    options,
    showUnderline = true,
}: Props) {
    const [open, setOpen] = useState(false);
    const rootRef = useRef<HTMLDivElement | null>(null);

    const filtered = useMemo(() => {
        const q = value.trim().toLowerCase();
        if (!q) return options.slice(0, 8);
        return options.filter((o) => o.toLowerCase().includes(q)).slice(0, 8);
    }, [options, value]);

    useEffect(() => {
        const onDoc = (e: MouseEvent) => {
            if (!rootRef.current) return;
            if (!rootRef.current.contains(e.target as Node)) setOpen(false);
        };
        document.addEventListener("mousedown", onDoc);
        return () => document.removeEventListener("mousedown", onDoc);
    }, []);

    return (
        <div ref={rootRef} className="w-full">
            <label className="block text-white/90 text-lg">{label}</label>
            <input
                value={value}
                onChange={(e) => {
                    onChange(e.target.value);
                    setOpen(true);
                }}
                onFocus={() => setOpen(true)}
                placeholder={placeholder}
                className="mt-6 w-full bg-transparent text-white text-2xl outline-none"
            />
            {showUnderline && <div className="mt-4 h-px w-full bg-white/30" />}

            {open && filtered.length > 0 && (
                <div className="mt-3 w-full rounded-xl border border-white/15 bg-black/30 backdrop-blur-md overflow-hidden">
                    {filtered.map((opt) => (
                        <button
                            key={opt}
                            type="button"
                            onClick={() => {
                                onChange(opt);
                                setOpen(false);
                            }}
                            className="w-full cursor-pointer text-left px-4 py-3 text-white/90 hover:bg-white/10"
                        >
                            {opt}
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
}
